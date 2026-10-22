import math
from django.urls import reverse
from django.utils import timezone
from planner.models import Scenario
from .models import FieldReport,ClimateState,Advisory
from .services import storage_metrics,shade_summary

COLORS={'flood':'#438bb7','wind':'#b87b41','drought':'#989450','heat':'#ca705b'}
TITLES={'flood':'Blocked drain','wind':'Fallen branch','drought':'Dry vegetation','heat':'Heat exposure'}

CREW_DATA = {
    'flood': {
        'unit': 'Rapid Response Team #01',
        'lead': 'En. Azlan',
        'lead_photo': 'lead_azlan.jpg',
        'contact': 'Radio Ch 1 · Hotline #5201',
        'dispatched_time': '5:22 PM',
        'elapsed_mins': 28,
        'sla_limit': 45,
        'sla_status': 'on_track',
        'sla_label': 'ON TRACK (28m elapsed · 45m target)',
        'location_detail': 'East Lake Storm Culvert #04 (Near Central Pavilion)',
        'coords_str': '3.1794°N, 101.5158°E',
        'resident_name': 'Ahmad Danial',
        'resident_phone': '+60 12-882 1940',
        'action_summary': 'Unclog storm drain grate, clear wet leaves, and inspect culvert outflow velocity.',
        'timeline': [
            {'time': '5:15 PM', 'step': 'Report Received', 'detail': 'Resident submitted photo via EcoCool Resident App', 'status': 'done'},
            {'time': '5:22 PM', 'step': 'Crew Dispatched', 'detail': 'Assigned to Rapid Response Team #01', 'status': 'done'},
            {'time': '5:35 PM', 'step': 'Arrived On-Site', 'detail': 'Maintenance van checked in at Sector 4 East Gate', 'status': 'done'},
            {'time': '5:45 PM', 'step': 'Work in Progress', 'detail': 'Clearing wet leaves and litter obstructing drain grate', 'status': 'current'},
            {'time': 'Pending', 'step': 'Verified & Closed', 'detail': 'Inspect clear water flow & award +50 GreenPoints', 'status': 'pending'}
        ]
    },
    'wind': {
        'unit': 'Rapid Response Team #02',
        'lead': 'En. Shahrul',
        'lead_photo': 'lead_shahrul.jpg',
        'contact': 'Radio Ch 2 · Hotline #5202',
        'dispatched_time': '4:30 PM',
        'elapsed_mins': 54,
        'sla_limit': 45,
        'sla_status': 'delayed',
        'sla_label': 'DELAYED (54m elapsed · Overdue by 9m)',
        'location_detail': 'Northwest Lakeside Jogging Loop (Near Forest Bridge)',
        'coords_str': '3.1791°N, 101.5149°E',
        'resident_name': 'Nur Sofea',
        'resident_phone': '+60 19-342 8119',
        'action_summary': 'Segment fallen 4-metre rain-tree branch with chainsaws and sweep wood shavings off cycling lane.',
        'timeline': [
            {'time': '4:15 PM', 'step': 'Report Received', 'detail': 'Resident flagged fallen branch blocking jogging path', 'status': 'done'},
            {'time': '4:30 PM', 'step': 'Crew Dispatched', 'detail': 'Assigned to Rapid Response Team #02', 'status': 'done'},
            {'time': '4:52 PM', 'step': 'Arrived On-Site', 'detail': 'Delayed by 12 mins due to fallen tree branch blocking access road', 'status': 'done_delayed'},
            {'time': '5:10 PM', 'step': 'Chainsaw Work', 'detail': 'Branch segmented into logs; sweeping remaining foliage', 'status': 'current'},
            {'time': 'Pending', 'step': 'Path Reopened', 'detail': 'Safety clearance inspection & award +50 GreenPoints', 'status': 'pending'}
        ]
    },
    'drought': {
        'unit': 'Rapid Response Team #03',
        'lead': 'En. Firdaus',
        'lead_photo': 'lead_firdaus.jpg',
        'contact': 'Radio Ch 3 · Hotline #5203',
        'dispatched_time': '5:40 PM',
        'elapsed_mins': 16,
        'sla_limit': 60,
        'sla_status': 'on_track',
        'sla_label': 'ON TRACK (16m elapsed · 60m target)',
        'location_detail': 'South Planting Embankment (Near Lake Retention Inlet)',
        'coords_str': '3.1796°N, 101.5164°E',
        'resident_name': 'Kavitha Rajan',
        'resident_phone': '+60 17-219 4082',
        'action_summary': 'Hook up mobile water bowser, rehydrate dry soil around sapling roots, and add coconut husk mulch.',
        'timeline': [
            {'time': '5:30 PM', 'step': 'Report Received', 'detail': 'Resident noted wilting young sapling in dry soil bed', 'status': 'done'},
            {'time': '5:40 PM', 'step': 'Crew Dispatched', 'detail': 'Assigned to Rapid Response Team #03', 'status': 'done'},
            {'time': '5:52 PM', 'step': 'Water Bowser Active', 'detail': 'Deep root hydration underway (150L target)', 'status': 'current'},
            {'time': 'Pending', 'step': 'Mulching', 'detail': 'Add moisture-retention ring & award +50 GreenPoints', 'status': 'pending'}
        ]
    },
    'heat': {
        'unit': 'Rapid Response Team #01',
        'lead': 'En. Azlan',
        'lead_photo': 'lead_azlan.jpg',
        'contact': 'Radio Ch 1 · Hotline #5201',
        'dispatched_time': '3:15 PM',
        'elapsed_mins': 28,
        'sla_limit': 60,
        'sla_status': 'resolved',
        'sla_label': 'RESOLVED (Completed in 28 mins)',
        'location_detail': 'West Promenade Seating Node (Bench #09)',
        'coords_str': '3.1789°N, 101.5176°E',
        'resident_name': 'Jason Tan',
        'resident_phone': '+60 16-550 7391',
        'action_summary': 'Inspected unshaded park bench (38.8°C surface heat); marked for Phase 2 Hopea odorata planting corridor.',
        'timeline': [
            {'time': '2:50 PM', 'step': 'Report Received', 'detail': 'Resident flagged unshaded metal/wood park bench', 'status': 'done'},
            {'time': '3:15 PM', 'step': 'Crew Dispatched', 'detail': 'Assigned to Rapid Response Team #01', 'status': 'done'},
            {'time': '3:32 PM', 'step': 'On-Site Thermal Check', 'detail': 'Measured 38.8°C; confirmed viable root space for shade tree', 'status': 'done'},
            {'time': '3:43 PM', 'step': 'Tree Corridor Logged', 'detail': 'Queued in Tree Simulator model as Proposed Tree #T-08', 'status': 'done'},
            {'time': '3:45 PM', 'step': 'Resolved & Rewarded', 'detail': '+50 GreenPoints credited to resident account', 'status': 'done'}
        ]
    }
}

def report_data(report):
    first=report.events[0] if report.events else {}
    sample=first.get('sample') is True
    crew = dict(CREW_DATA.get(report.kind, CREW_DATA['flood']))
    if report.status == 'resolved':
        crew['sla_status'] = 'resolved'
        crew['sla_label'] = 'RESOLVED · Verified & Closed'
        crew['timeline'] = [
            {'time': '2:50 PM', 'step': 'Report Received', 'detail': 'Resident submitted photo via EcoCool Mobile App', 'status': 'done'},
            {'time': '3:15 PM', 'step': 'Crew Dispatched', 'detail': 'Assigned to Rapid Response Team #01', 'status': 'done'},
            {'time': '3:35 PM', 'step': 'On-Site Work', 'detail': 'Field remediation and safety check completed', 'status': 'done'},
            {'time': '3:45 PM', 'step': 'Verified & Closed', 'detail': 'Photo proof verified & +50 GreenPoints credited', 'status': 'done'}
        ]
    elif report.status == 'open':
        crew['sla_status'] = 'pending_dispatch'
        crew['sla_label'] = 'WAITING FOR DISPATCH'
    return {'id':report.pk,'title':first.get('title') or TITLES.get(report.kind,'Resident report'),
            'kind':report.kind,'kind_label':report.get_kind_display(),'color':COLORS.get(report.kind,'#42745b'),
            'description':report.description,'lat':report.latitude,'lon':report.longitude,
            'status':report.status,'status_label':report.get_status_display(),
            'location':first.get('location_label') or ('Location attached' if report.latitude is not None else 'Location not provided'),
            'source':'Sample app input' if sample else 'Stored resident report',
            'sample':sample,'reference':first.get('external_id') or f'R-{report.pk:04d}',
            'reported_at':report.created_at.isoformat(),'assigned_to':report.assigned_to.username if report.assigned_to else 'Unassigned',
            'verified':report.verified,'version':report.version,
            'points_reward': 50,
            'crew': crew,
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
    sla_delayed=sum(1 for r in reports if r['crew']['sla_status'] == 'delayed')
    sla_on_track=sum(1 for r in reports if r['crew']['sla_status'] == 'on_track')
    rows=shade_summary(Scenario.objects.filter(project=project).order_by('-created_at')[:20])
    current=[r for r in rows if r['site_version']==project.site_version and r['shade'] is not None]
    latest=current[0] if current else None
    notices=[{'title':n.title,'message':n.message,'expires_at':n.expires_at.isoformat(),'id':n.pk,'kind':n.kind} for n in Advisory.objects.filter(project=project,active=True,expires_at__gt=timezone.now()).order_by('-created_at')[:10]]
    
    active_squads = [
        {
            'name': 'Rapid Response Team #01',
            'lead': 'En. Azlan',
            'photo': 'lead_azlan.jpg',
            'assignment': 'Active on #APP-DEMO-101 (East Lake)',
            'time_label': '28m · On-Time',
            'status': 'on_track',
            'delayed': False,
        },
        {
            'name': 'Rapid Response Team #02',
            'lead': 'En. Shahrul',
            'photo': 'lead_shahrul.jpg',
            'assignment': 'Active on #APP-DEMO-102 (Northwest Loop)',
            'time_label': '54m · Overdue',
            'status': 'delayed',
            'delayed': True,
        },
        {
            'name': 'Rapid Response Team #03',
            'lead': 'En. Firdaus',
            'photo': 'lead_firdaus.jpg',
            'assignment': 'Active on #APP-DEMO-103 (South Embankment)',
            'time_label': '16m · On-Time',
            'status': 'on_track',
            'delayed': False,
        }
    ]

    return {'project_id':project.pk,'site_version':project.site_version,'site':project.site_data,
            'can_manage':can_manage,'counts':counts,'reports':reports,'returned_reports':len(reports),
            'metrics':metrics,'latest_shade':latest,'scenarios':rows,'notices':notices,
            'active_squads': active_squads, 'sla_delayed': sla_delayed, 'sla_on_track': sla_on_track,
            'climate':{'scenario':state.scenario,'stored':state.stored_m3,'capacity':state.capacity_m3,
                       'reserve':state.reserve_m3,'target':state.target_m3,'inflow':state.assumed_inflow_m3,
                       'source':state.source,'is_demo':state.is_demo,'updated_at':state.updated_at.isoformat(),
                       'history':state.history,'zones':state.zones} if state else None}
