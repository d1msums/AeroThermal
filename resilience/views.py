import csv,json
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.http import Http404,HttpResponse,JsonResponse,FileResponse,HttpResponseForbidden
from django.shortcuts import get_object_or_404,redirect,render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST,require_GET
from planner.models import Membership,Scenario
from .models import StakeholderAccess,ClimateState,FieldReport,Advisory
from .forms import ReportForm,AdvisoryForm,TriageForm
from .services import PRESETS,storage_metrics,within_site,event,shade_summary
from .weather import fetch_warnings


def access(request,project_id,internal=False,write=False):
    m=get_object_or_404(Membership.objects.select_related('project'),user=request.user,project_id=project_id)
    resident=StakeholderAccess.objects.filter(membership=m,resident_only=True).exists()
    if internal and resident: raise Http404
    if write and (m.role!='planner' or resident): return m,resident,False
    return m,resident,True


def ctx(request,m,resident):
    project=m.project
    state=ClimateState.objects.filter(project=project).first()
    scenarios=Scenario.objects.filter(project=project).order_by('-created_at')[:20]
    reports=FieldReport.objects.filter(project=project)
    if resident: reports=reports.filter(reporter=request.user)
    return {'project':project,'site':project.site_data,'membership':m,'resident_only':resident,
            'can_manage':m.role=='planner' and not resident,
            'state':state,'metrics':storage_metrics(state) if state else None,
            'scenario_rows':shade_summary(scenarios),'scenario_count':Scenario.objects.filter(project=project).count(),
            'open_count':reports.exclude(status='resolved').count(),
            'resolved_count':reports.filter(status='resolved').count(),
            'reports':reports.select_related('reporter','assigned_to').order_by('-created_at')[:100],
            'advisories':Advisory.objects.filter(project=project,active=True,expires_at__gt=timezone.now()).order_by('-created_at')[:20]}

@login_required
@require_GET
def audience(request,project_id,audience):
    if audience == 'resident': return HttpResponse('Resident reporting is provided by the mobile app. This web workspace is B2B only.',status=410)
    if audience not in ['engineer','operations','leadership']: raise Http404
    m,resident,_=access(request,project_id,internal=audience!='resident')
    context=ctx(request,m,resident)
    context['audience']=audience
    from .visuals import page_data
    context['visual_data']=page_data(m.project,request.user,context['can_manage'])
    context['advisory_form']=AdvisoryForm()
    return render(request,f'resilience/{audience}.html',context)

@login_required
@require_GET
def hub(request,project_id):
    m,resident,_=access(request,project_id)
    if resident: return HttpResponseForbidden('This workspace is for B2B project teams. Resident access belongs to the mobile app.')
    return redirect('resilience:audience',project_id=project_id,audience='leadership')

@login_required
@require_POST
def scenario(request,project_id):
    m,resident,allowed=access(request,project_id,internal=True,write=True)
    if not allowed: return HttpResponseForbidden('Planner membership required.')
    mode=request.POST.get('scenario')
    if mode not in PRESETS: return HttpResponse('Invalid scenario',status=400)
    with transaction.atomic():
        state=get_object_or_404(ClimateState.objects.select_for_update(),project=m.project)
        stored,inflow=PRESETS[mode]
        state.scenario=mode;state.stored_m3=stored;state.assumed_inflow_m3=inflow
        state.downstream_verified=False;state.is_demo=True;state.updated_by=request.user
        state.save()
    if request.headers.get('Accept') == 'application/json': return JsonResponse({'saved':True})
    return redirect('resilience:audience',project_id=project_id,audience='engineer')

@login_required
@require_POST
def report_create(request,project_id):
    return HttpResponse('Web report submission is disabled. Reports enter from the resident mobile app.',status=410)

@login_required
@require_GET
def report_detail(request,project_id,report_id):
    m,resident,_=access(request,project_id,internal=True)
    report=get_object_or_404(FieldReport,project=m.project,pk=report_id)
    if resident and report.reporter_id!=request.user.pk: raise Http404
    context=ctx(request,m,resident);context['report']=report
    from .visuals import page_data, report_data
    context['visual_data']=page_data(m.project,request.user,context['can_manage'])
    context['selected_report']=report_data(report)
    if not any(r['id']==report.pk for r in context['visual_data']['reports']):
        context['visual_data']['reports'].append(context['selected_report'])
    context['audience']='operations'
    context['triage_form']=TriageForm(initial={'status':report.status,'verified':report.verified,'version':report.version})
    return render(request,'resilience/report.html',context)

@login_required
@require_POST
def triage(request,project_id,report_id):
    m,_,allowed=access(request,project_id,internal=True,write=True)
    if not allowed: return HttpResponseForbidden('Planner membership required.')
    form=TriageForm(request.POST)
    if not form.is_valid(): return render(request,'resilience/form_error.html',{'project':m.project,'form':form},status=400)
    with transaction.atomic():
        report=get_object_or_404(FieldReport.objects.select_for_update(),pk=report_id,project=m.project)
        d=form.cleaned_data
        if report.version!=d['version']: return HttpResponse('Report changed. Reload before updating.',status=409)
        report.status=d['status'];report.verified=d['verified']
        if d['assign_to_me']: report.assigned_to=request.user
        # B2C rewards belong to the mobile-app workflow; no points are issued here.
        report.events.append(event(request.user,report.status,d['note']))
        report.version+=1;report.save()
    return redirect('resilience:report',project_id=project_id,report_id=report_id)

@login_required
@require_POST
def publish(request,project_id):
    m,_,allowed=access(request,project_id,internal=True,write=True)
    if not allowed: return HttpResponseForbidden('Planner membership required.')
    form=AdvisoryForm(request.POST)
    if form.is_valid():
        item=form.save(commit=False);item.project=m.project;item.created_by=request.user
        item.expires_at=timezone.now()+timedelta(hours=form.cleaned_data['hours'])
        item.is_demo=True;item.save()
        return redirect('resilience:audience',project_id=project_id,audience='operations')
    return render(request,'resilience/form_error.html',{'project':m.project,'form':form},status=400)

@login_required
@require_POST
def withdraw(request,project_id,advisory_id):
    m,_,allowed=access(request,project_id,internal=True,write=True)
    if not allowed: return HttpResponseForbidden('Planner membership required.')
    item=get_object_or_404(Advisory,pk=advisory_id,project=m.project)
    item.active=False;item.save(update_fields=['active'])
    return redirect('resilience:audience',project_id=project_id,audience='operations')

@login_required
@require_GET
def photo(request,project_id,report_id):
    m,resident,_=access(request,project_id,internal=True)
    report=get_object_or_404(FieldReport,pk=report_id,project=m.project)
    if resident and report.reporter_id!=request.user.pk or not report.photo: raise Http404
    response=FileResponse(report.photo.open('rb'),content_type='image/jpeg')
    response['Cache-Control']='private, no-store'
    response['X-Content-Type-Options']='nosniff'
    return response

@login_required
@require_GET
def map_data(request,project_id):
    m,_,_=access(request,project_id,internal=True)
    state=ClimateState.objects.filter(project=m.project).first()
    features=[]
    if state:
        for zone in state.zones:
            features.append({'type':'Feature','geometry':{'type':'Point','coordinates':zone['coordinates']},
                             'properties':{'kind':'illustrative_hotspot','label':zone['label'],'sample_surface_c':zone['sample_surface_c']}})
    for report in FieldReport.objects.filter(project=m.project).exclude(status='resolved').exclude(latitude=None).order_by('-created_at')[:100]:
        features.append({'type':'Feature','geometry':{'type':'Point','coordinates':[report.longitude,report.latitude]},
                         'properties':{'kind':report.kind,'label':report.description,'report_id':report.pk,'unverified':not report.verified}})
    return JsonResponse({'type':'FeatureCollection','features':features})

@login_required
@require_GET
def weather(request,project_id):
    access(request,project_id,internal=True)
    return JsonResponse(fetch_warnings())

@login_required
@require_GET
def export(request,project_id):
    m,_,_=access(request,project_id,internal=True)
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="aerothermal-project-summary.csv"'
    writer=csv.writer(response)
    writer.writerow(['scenario','site_version','model','timestamp','mode','proposed_route_shade_pct','existing_shade'])
    def safe(value):
        text=str(value)
        return "'"+text if text.lstrip().startswith(('=','+','-','@')) else text
    unknown=m.project.site_data.get('baseline_inventory_available') is False
    for row in shade_summary(Scenario.objects.filter(project=m.project).order_by('-created_at')[:1000]):
        writer.writerow([safe(row[k]) for k in ['name','site_version','model','timestamp','mode']]+[row['shade'] if row['shade'] is not None else '', 'Not surveyed' if unknown else 'See saved result'])
    return response

@login_required
@require_GET
def snapshot(request,project_id):
    m,resident,_=access(request,project_id,internal=True)
    state=get_object_or_404(ClimateState,project=m.project)
    return JsonResponse({'scenario':state.scenario,'stored_m3':state.stored_m3,
                         'capacity_m3':state.capacity_m3,'reserve_m3':state.reserve_m3,
                         'is_demo':state.is_demo,'source':state.source,
                         'updated_at':state.updated_at.isoformat(),
                         'can_manage':m.role=='planner' and not resident,
                         **storage_metrics(state)})

@login_required
@require_GET
def visual_data(request,project_id):
    m,resident,_=access(request,project_id,internal=True)
    from .visuals import page_data
    return JsonResponse(page_data(m.project,request.user,m.role=='planner' and not resident))
