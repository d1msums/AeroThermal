"""Explainable prototype triage, not a disaster forecast or a gate controller."""
from datetime import timedelta
from zoneinfo import ZoneInfo
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from planner.models import Scenario
from .models import ClimateState, FieldReport, Advisory
from .services import storage_metrics, shade_summary
from .visuals import report_data
from .views import access, scenario

KINDS = [('flood', 'Flood & stormwater', 'Lake and drainage', 'Engineering'),
         ('heat', 'Heat exposure', 'Heatwaves and heat islands', 'Planning / ESG'),
         ('drought', 'Water reserve', 'Dry conditions and vegetation', 'Landscape / Engineering'),
         ('wind', 'Wind & tree hazards', 'Access routes and fallen branches', 'Operations')]


def build_alerts(project, now=None):
    now = now or timezone.now()
    state = ClimateState.objects.filter(project=project).first()
    metrics, error = {}, ''
    if state:
        try:
            metrics = storage_metrics(state)
        except (ValueError, TypeError, ZeroDivisionError):
            error = 'Lake inputs are inconsistent. Correct capacity, storage, reserve and target.'
    fresh_hours = getattr(settings, 'AEROTHERMAL_ALERT_STALE_HOURS', 2)
    stale = bool(state and state.updated_at < now - timedelta(hours=fresh_hours))
    usable = bool(metrics) and (state.is_demo or not stale)
    active = FieldReport.objects.filter(project=project).exclude(status='resolved')
    grouped = {r['kind']: r['n'] for r in active.values('kind').annotate(n=Count('id'))}
    verified = {r['kind']: r['n'] for r in active.filter(verified=True).values('kind').annotate(n=Count('id'))}
    notices = list(Advisory.objects.filter(project=project, active=True, expires_at__gt=now).order_by('-created_at')[:50])
    cards = []
    for kind, title, sub, owner in KINDS:
        c = dict(kind=kind, title=title, subtitle=sub, owner=owner, level=0, status='Data needed',
                 metric='—', unit='', reports=grouped.get(kind, 0), verified=verified.get(kind, 0),
                 evidence=[], actions=[], gaps=[], demo=bool(state and state.is_demo))
        mode = state.scenario if state else ''
        if kind == 'flood':
            c['gaps'] = ['Rainfall forecast, catchment runoff and downstream capacity are not connected.']
            c['actions'] = ['Inspect reported drainage obstructions.', 'Review storage and downstream conditions with the engineer.']
            if metrics:
                c.update(metric=f"{metrics['capacity_pct']:g}", unit='% full')
            if usable:
                c['evidence'].append(f"Available buffer: {metrics['buffer_m3']:,} m³. Assumed inflow: {state.assumed_inflow_m3:,} m³.")
                if metrics['overflow_without_m3'] > 0:
                    c.update(level=2, status='Storage review', reason=f"Assumed inflow exceeds available buffer by {metrics['overflow_without_m3']:,} m³.")
                else:
                    c.update(status='No storage trigger', reason='The entered inflow fits within the entered storage buffer.')
                if mode == 'storm' and not c['level']:
                    c.update(level=1, status='Storm review', reason='Heavy-rain scenario selected; it is not a local weather forecast.')
                if mode == 'storm':
                    c['evidence'].append(f"Illustrative release candidate: {metrics['candidate_m3']:,} m³. HOLD — downstream capacity and permitted release rate are unverified.")
            else:
                c['reason'] = error or ('Stored lake reading is stale; current conditions are unknown.' if state else 'No lake snapshot is available.')
        elif kind == 'drought':
            c['gaps'] = ['Soil moisture, rainfall deficit and El Niño outlook are not connected.']
            c['actions'] = ['Inspect dry vegetation and check irrigation needs.', 'Review the entered water reserve before allocating water.']
            if metrics:
                c.update(metric=f'{state.stored_m3:,}', unit='m³ stored')
            if usable:
                c['evidence'].append(f'Entered minimum reserve: {state.reserve_m3:,} m³.')
                gap = max(0, state.reserve_m3 - state.stored_m3)
                if gap:
                    c.update(level=2, status='Reserve review', reason=f'Stored water is {gap:,} m³ below the entered reserve.')
                else:
                    c.update(status='No reserve trigger', reason='Stored water is at or above the entered reserve; drought status is unassessed.')
                if mode == 'drought' and not c['level']:
                    c.update(level=1, status='Dry-condition review', reason='Drought scenario selected; verify local conditions.')
            else:
                c['reason'] = error or 'A current, valid lake snapshot is needed to assess the reserve.'
        elif kind == 'heat':
            c['gaps'] = ['Air temperature, humidity and a validated heat-island baseline are not connected.']
            c['actions'] = ['Inspect reported exposure locations.', 'Review planting rationale and saved shade evidence in Landscape review.']
            c['reason'] = 'Heat severity is unassessed; shade coverage is not an air-temperature reading.'
            if mode == 'heat' and state.is_demo:
                c.update(level=1, status='Heat scenario', reason='Demo heatwave selected. Prioritise exposure locations for review.')
        else:
            c['gaps'] = ['Wind observations and a local wind forecast are not connected.']
            c['actions'] = ['Inspect reported tree obstructions and affected access routes.']
            c['reason'] = 'Wind severity is unassessed; resident reports indicate inspection needs.'
            if mode == 'wind' and state.is_demo:
                c.update(level=1, status='Wind scenario', reason='Demo windstorm selected. Review tree and access-route reports.')
        if c['reports']:
            c['evidence'].append(f"{c['reports']} unresolved reports; {c['verified']} marked verified by staff. Reports do not confirm a disaster.")
            if c['level'] == 0:
                c.update(level=1, status='Reports to review', reason='Unresolved resident input needs team review.')
        matching = [n for n in notices if n.kind == kind]
        c['notices'] = matching
        if matching:
            c['evidence'].append(f'{len(matching)} active internal advisories in the latest 50 notices.')
            if c['level'] == 0:
                c.update(level=1, status='Advisory review', reason='An internal advisory is active; review its scope and expiry.')
        c['tone'] = ('neutral', 'watch', 'attention')[c['level']]
        c['link'] = reverse('resilience:audience', args=[project.pk, 'engineer' if kind in ('flood','drought') else 'operations'])
        cards.append(c)
    rows = shade_summary(Scenario.objects.filter(project=project).order_by('-created_at')[:20])
    latest = next((r for r in rows if r['site_version'] == project.site_version and r['shade'] is not None), None)
    report_rows = [report_data(r) for r in active.select_related('assigned_to').order_by('-created_at')[:500]]
    counts = {s: active.filter(status=s).count() for s in ('open','in_progress')}
    counts.update(resolved=0, total=active.count(), active=active.count())
    visual = dict(project_id=project.pk, site=project.site_data, site_version=project.site_version,
                  counts=counts, reports=report_rows, returned_reports=len(report_rows), metrics=metrics,
                  latest_shade=latest, scenarios=rows, climate=None)
    if metrics:
        visual['climate'] = dict(scenario=state.scenario, stored=state.stored_m3, capacity=state.capacity_m3,
                                reserve=state.reserve_m3, is_demo=state.is_demo, history=[], zones=[])
    return dict(cards=cards, queue=sorted((c for c in cards if c['level']), key=lambda c:-c['level']),
                review_count=sum(bool(c['level']) for c in cards), active_count=active.count(),
                unverified_count=active.filter(verified=False).count(), state=state, metrics=metrics,
                state_error=error, stale=stale, freshness_hours=fresh_hours, latest_shade=latest,
                checked_at=now.astimezone(ZoneInfo('Asia/Kuala_Lumpur')), visual_data=visual,
                notices=notices, demo=bool(state and state.is_demo))


@login_required
@require_GET
def dashboard(request, project_id):
    member, _, _ = access(request, project_id, internal=True)
    data = build_alerts(member.project)
    data.update(project=member.project, membership=member, audience='alerts',
                can_manage=member.role=='planner', open_count=data['active_count'])
    data['visual_data']['can_manage'] = data['can_manage']
    response = render(request, 'resilience/climate_alerts.html', data)
    response['Cache-Control'] = 'private, no-store'
    return response


@login_required
@require_POST
def apply_scenario(request, project_id):
    # Delegate validation, membership checks and transaction to the existing handler.
    response = scenario(request, project_id)
    if response.status_code == 302:
        return redirect('resilience:climate_alerts', project_id=project_id)
    return response
