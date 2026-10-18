import math
from django.urls import reverse
from django.utils import timezone
from planner.models import Scenario
from .models import FieldReport,ClimateState,Advisory
from .services import storage_metrics,shade_summary

COLORS={'flood':'#438bb7','wind':'#b87b41','drought':'#989450','heat':'#ca705b'}
TITLES={'flood':'Blocked drain','wind':'Fallen branch','drought':'Dry vegetation','heat':'Heat exposure'}

def report_data(report):
    first=report.events[0] if report.events else {}
    sample=first.get('sample') is True
    return {'id':report.pk,'title':first.get('title') or TITLES.get(report.kind,'Resident report'),
            'kind':report.kind,'kind_label':report.get_kind_display(),'color':COLORS.get(report.kind,'#42745b'),
            'description':report.description,'lat':report.latitude,'lon':report.longitude,
            'status':report.status,'status_label':report.get_status_display(),
            'location':first.get('location_label') or ('Location attached' if report.latitude is not None else 'Location not provided'),
            'source':'Sample app input' if sample else 'Stored resident report',
            'sample':sample,'reference':first.get('external_id') or f'R-{report.pk:04d}',
            'reported_at':report.created_at.isoformat(),'assigned_to':report.assigned_to.username if report.assigned_to else 'Unassigned',
            'verified':report.verified,'version':report.version,
            'photo_url':reverse('resilience:photo',args=[report.project_id,report.pk]) if report.photo else None,
            'illustration':report.kind if report.kind in COLORS else 'flood',
            'detail_url':reverse('resilience:report',args=[report.project_id,report.pk]),
            'triage_url':reverse('resilience:triage',args=[report.project_id,report.pk]),
            'events':report.events[-8:]}

def page_data(project,user,can_manage):
    state=ClimateState.objects.filter(project=project).first()
    metrics=storage_metrics(state) if state else {}
    qs=FieldReport.objects.filter(project=project).select_related('assigned_to').order_by('-created_at')
    reports=[report_data(r) for r in qs[:500]]
    counts={status:qs.filter(status=status).count() for status in ['open','in_progress','resolved']}
    counts['total']=qs.count();counts['active']=counts['open']+counts['in_progress']
    rows=shade_summary(Scenario.objects.filter(project=project).order_by('-created_at')[:20])
    current=[r for r in rows if r['site_version']==project.site_version and r['shade'] is not None]
    latest=current[0] if current else None
    notices=[{'title':n.title,'message':n.message,'expires_at':n.expires_at.isoformat(),'id':n.pk,'kind':n.kind} for n in Advisory.objects.filter(project=project,active=True,expires_at__gt=timezone.now()).order_by('-created_at')[:10]]
    return {'project_id':project.pk,'site_version':project.site_version,'site':project.site_data,
            'can_manage':can_manage,'counts':counts,'reports':reports,'returned_reports':len(reports),
            'metrics':metrics,'latest_shade':latest,'scenarios':rows,'notices':notices,
            'climate':{'scenario':state.scenario,'stored':state.stored_m3,'capacity':state.capacity_m3,
                       'reserve':state.reserve_m3,'target':state.target_m3,'inflow':state.assumed_inflow_m3,
                       'source':state.source,'is_demo':state.is_demo,'updated_at':state.updated_at.isoformat(),
                       'history':state.history,'zones':state.zones} if state else None}
