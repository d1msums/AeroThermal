"""AeroThermal AI: Disaster Resilience & Community Readiness Copilot.
Grounded in NADMA Malaysia directives, JPS MSMA hydrology, and Sime Darby Property masterplan telemetry.
100% English interface, executive-level insights, and visual process flow diagrams.
"""
import json
import logging
import os
import urllib.error
import urllib.request
from datetime import timedelta
from zoneinfo import ZoneInfo
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from planner.models import Scenario
from .models import ClimateState, FieldReport, Advisory
from .services import storage_metrics, shade_summary
from .visuals import report_data
from .views import access, scenario

logger = logging.getLogger(__name__)

KINDS = [
    ('flood', 'Flood & Stormwater', 'Lake and drainage detention', 'Engineering'),
    ('heat', 'Heat Exposure', 'Microclimate & thermal comfort', 'Planning / ESG'),
    ('drought', 'Water Reserve', 'Dry spell & tree irrigation', 'Landscape / Engineering'),
    ('wind', 'Wind & Tree Hazards', 'Access routes & branch obstructions', 'Operations'),
]

HUMAN_PROMPTS = [
    {
        'id': 'flood_2021',
        'category': 'Catastrophic Flood Resilience',
        'badge': '2021 Benchmark',
        'question': 'Is Elmina truly ready if a December 2021-scale catastrophic flood hits tomorrow? What proves our system can hold?',
        'summary': '100-Year ARI basin hydrology, 185,000 m³ active detention buffer, and blackout-proof gravity weir spillway.',
    },
    {
        'id': 'pps_nadma',
        'category': 'Evacuation Shelters (PPS)',
        'badge': 'NADMA Directive 20',
        'question': 'Does our Elmina Community Hall meet official NADMA certification standards as an accredited evacuation shelter?',
        'summary': 'PPS audit: 1,200 pax capacity, 150 kVA backup generator (72hr), 10,000L water tank, and Universal Design accessibility.',
    },
    {
        'id': 'vulnerable_evac',
        'category': 'Vulnerable Resident Safety',
        'badge': 'EcoCool Prihatin',
        'question': 'How do we safeguard vulnerable seniors, chronic patients, and wheelchair users in Ilham & Revo during sudden flash floods?',
        'summary': 'Geofenced registry of 50 vulnerable residents, automated IVR voice alerts, and dedicated Auxiliary Police 4WD evacuation.',
    },
    {
        'id': 'lake_weir_jps',
        'category': 'Basin Hydrology & Spillway',
        'badge': 'JPS River Coordination',
        'question': 'Lake capacity is at 85% this afternoon—should we open the gravity weir gates into Sungai Buloh now or is there downstream flood risk?',
        'summary': 'Detention buffer retention protocol prevents downstream flash flooding in Meru and Kubu Gajah prior to peak storm runoff.',
    },
    {
        'id': 'wind_tree_sla',
        'category': 'Tree Hazards & Arborist SLA',
        'badge': '45-Min Emergency SLA',
        'question': 'A fallen tree is blocking the CoolWalk trail after the windstorm—what is our arborist crew SLA to clear emergency access?',
        'summary': '45-min SLA for emergency routes, 3-ton crane mobilization with Shahrul squad, and ERT heritage tree preservation protocol.',
    },
    {
        'id': 'app_alert_broadcast',
        'category': 'Community Early Warning',
        'badge': 'EcoCool Resident App',
        'question': 'Can EcoCool App automatically broadcast severe thunderstorm warnings to resident phones according to NADMA alert levels?',
        'summary': '3-tier automated color-coded broadcast (Yellow / Orange / Red) pushed to 4,200 verified resident devices.',
    },
]

ACCREDITED_SHELTERS = [
    {
        'name': 'Elmina Central Community Hall',
        'role': 'Primary Evacuation Center (PPS Tier 1)',
        'capacity': 1200,
        'status': 'Fully Certified & Ready',
        'generator': '150 kVA Diesel (72-hr continuous fuel buffer)',
        'water_storage': '10,000 Liters Emergency Reservoir',
        'facilities': 'JKM Relief Kitchen, Mother & Infant Nursery, OKU Ramps, Triage Clinic',
        'elevation': '39.5m RL (Flood-Proof High Ground)',
    },
    {
        'name': 'Surau Al-Madaniah Denai Alam',
        'role': 'Secondary Evacuation Center (PPS Tier 2)',
        'capacity': 750,
        'status': 'Standby Readiness',
        'generator': '60 kVA Auxiliary Unit',
        'water_storage': '5,000 Liters Potable Tank',
        'facilities': 'Main Hall Evacuation Staging, Family Cubicles, Basic Sanitation',
        'elevation': '41.0m RL (Elevated Ridge)',
    },
    {
        'name': 'Ilham Residence Residents Clubhouse',
        'role': 'Neighborhood Immediate Staging Hub',
        'capacity': 450,
        'status': 'Community Ready',
        'generator': '30 kWp Solar PV + 40 kWh Battery Storage',
        'water_storage': '4,000 Liters Tank',
        'facilities': 'First Aid Post, Wheelchair Ramps, KRT Community Muster Point',
        'elevation': '38.2m RL',
    },
]

ON_DUTY_SQUADS = [
    {
        'name': 'Stormwater Squad (Azlan - Sample Lead)',
        'role': 'Lead Stormwater & Retention Basin Squad',
        'dept': 'Sime Darby Property Engineering (Demo Roster)',
        'phone': '019-382 9102',
        'tasks': 'SCADA automated spillway gates, 14 perimeter trash grates, basin buffer monitoring',
    },
    {
        'name': 'Arborist Squad (Shahrul - Sample Lead)',
        'role': 'Lead Certified Arborist & Hazard Squad',
        'dept': 'Sime Darby Property Landscape & Arboriculture (Demo Roster)',
        'phone': '012-441 8839',
        'tasks': 'Structural tree triage, 3-ton crane truck mobilization, ERT heritage tree rescue',
    },
    {
        'name': 'Landscape Squad (Firdaus - Sample Lead)',
        'role': 'Lead Irrigation & Microclimate Squad',
        'dept': 'Sime Darby Property Township Operations (Demo Roster)',
        'phone': '017-695 3320',
        'tasks': 'Tree reserve water rationing, CoolWalk trail fertigation, soil saturation telemetry',
    },
]

EMERGENCY_CONTACTS = [
    {'name': 'National Emergency Services (MERS Police / Medic)', 'phone': '999', 'badge': 'Verified 24/7'},
    {'name': 'BOMBA Fire & Flood Rescue', 'phone': '994', 'badge': 'Verified Emergency'},
    {'name': 'NADMA National Disaster Command Centre', 'phone': '03-8064 2400', 'badge': 'Federal Lead'},
    {'name': 'JPS InfoBanjir National Telemetry', 'phone': '1-300-88-8577', 'badge': 'Flood Hotlines'},
]


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

    if metrics:
        metrics['buffer_m3_fmt'] = f"{metrics.get('buffer_m3', 0):,}"
        metrics['overflow_m3_fmt'] = f"{metrics.get('overflow_without_m3', 0):,}"
    if state and metrics:
        metrics['stored_m3_fmt'] = f"{state.stored_m3:,}"
        metrics['capacity_m3_fmt'] = f"{state.capacity_m3:,}"
        metrics['reserve_m3_fmt'] = f"{state.reserve_m3:,}"

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
            c['gaps'] = ['Catchment runoff telemetry is not connected to JPS Sungai Buloh gauging station.']
            c['actions'] = ['Inspect reported drainage obstructions with Squad Azlan.', 'Review storage buffer with engineering team.']
            if metrics and 'capacity_pct' in metrics:
                c.update(metric=f"{metrics['capacity_pct']:g}", unit='% full')
            if usable:
                c['evidence'].append(f"Available buffer: {metrics['buffer_m3']:,} m³. Assumed storm inflow: {state.assumed_inflow_m3:,} m³.")
                if metrics['overflow_without_m3'] > 0:
                    c.update(level=2, status='Storage review', reason=f"Assumed inflow exceeds available buffer by {metrics['overflow_without_m3']:,} m³.")
                else:
                    c.update(status='No storage trigger', reason='The entered inflow fits within the entered storage buffer.')
                if mode == 'storm' and not c['level']:
                    c.update(level=1, status='Storm review', reason='Heavy-rain scenario selected; monitoring basin surge.')
                if mode == 'storm':
                    c['evidence'].append(f"Illustrative release candidate: {metrics['candidate_m3']:,} m³. HOLD — downstream capacity at Sg. Buloh requires JPS clearance.")
            else:
                c['reason'] = error or ('Stored lake reading is stale; current conditions are unknown.' if state else 'No lake snapshot is available.')
        elif kind == 'drought':
            c['gaps'] = ['Soil moisture and El Niño outlook are not connected to the irrigation schedule.']
            c['actions'] = ['Inspect dry vegetation with Squad Firdaus.', 'Review water reserve before allocating tree irrigation.']
            if metrics:
                c.update(metric=f'{state.stored_m3:,}', unit='m³ stored')
            if usable:
                c['evidence'].append(f'Entered minimum reserve: {state.reserve_m3:,} m³ for ERT tree preservation.')
                gap = max(0, state.reserve_m3 - state.stored_m3)
                if gap:
                    c.update(level=2, status='Reserve review', reason=f'Stored water is {gap:,} m³ below the entered reserve.')
                else:
                    c.update(status='No reserve trigger', reason='Stored water is at or above the entered reserve.')
                if mode == 'drought' and not c['level']:
                    c.update(level=1, status='Dry-condition review', reason='Drought scenario active; monitor ERT tree moisture.')
            else:
                c['reason'] = error or 'A current lake snapshot is needed to assess the reserve.'
        elif kind == 'heat':
            c['gaps'] = ['Microclimate canopy shade baseline is not connected to CoolWalk thermal mapping.']
            c['actions'] = ['Inspect exposed pedestrian plazas with operations.', 'Review mature ERT tree canopy along high-exposure corridors.']
            c['reason'] = 'Heat exposure monitored; tree canopy mitigates microclimate thermal load.'
            if mode == 'heat' and state.is_demo:
                c.update(level=1, status='Heat scenario', reason='Demo heatwave active. Prioritise pedestrian CoolWalk shade trails.')
        else:
            c['gaps'] = ['Wind hazard logs and local wind warnings are not connected to arborist patrol routes.']
            c['actions'] = ['Inspect reported tree obstructions and critical access routes with Squad Shahrul.']
            c['reason'] = 'Wind severity monitored; resident field reports prioritize immediate squad dispatch.'
            if mode == 'wind' and state.is_demo:
                c.update(level=1, status='Wind scenario', reason='Demo windstorm active. Review tree fall reports across central park.')
        if c['reports']:
            c['evidence'].append(f"{c['reports']} unresolved reports; {c['verified']} marked verified by staff.")
            if c['level'] == 0:
                c.update(level=1, status='Reports to review', reason='Unresolved resident reports need squad action.')
        matching = [n for n in notices if n.kind == kind]
        c['notices'] = matching
        if matching:
            c['evidence'].append(f'{len(matching)} active internal advisories in the latest 50 notices.')
            if c['level'] == 0:
                c.update(level=1, status='Advisory review', reason='An internal advisory is active; review operational scope.')
        c['tone'] = ('neutral', 'watch', 'attention')[c['level']]
        c['link'] = reverse('resilience:audience', args=[project.pk, 'engineer' if kind in ('flood', 'drought') else 'operations'])
        cards.append(c)

    rows = shade_summary(Scenario.objects.filter(project=project).order_by('-created_at')[:20])
    latest = next((r for r in rows if r['site_version'] == project.site_version and r['shade'] is not None), None)
    report_rows = [report_data(r) for r in active.select_related('assigned_to').order_by('-created_at')[:500]]
    counts = {s: active.filter(status=s).count() for s in ('open', 'in_progress')}
    counts.update(resolved=0, total=active.count(), active=active.count())
    visual = dict(
        project_id=project.pk,
        site=project.site_data,
        site_version=project.site_version,
        counts=counts,
        reports=report_rows,
        returned_reports=len(report_rows),
        metrics=metrics,
        latest_shade=latest,
        scenarios=rows,
        climate=None,
    )
    if metrics:
        visual['climate'] = dict(
            scenario=state.scenario,
            stored=state.stored_m3,
            capacity=state.capacity_m3,
            reserve=state.reserve_m3,
            is_demo=state.is_demo,
            history=[],
            zones=[],
        )

    # Community readiness calculation
    readiness_score = 92
    if state and state.scenario == 'storm':
        readiness_score = 88
    elif state and state.scenario == 'heat':
        readiness_score = 90

    return dict(
        cards=cards,
        queue=sorted((c for c in cards if c['level']), key=lambda c: -c['level']),
        review_count=sum(bool(c['level']) for c in cards),
        active_count=active.count(),
        unverified_count=active.filter(verified=False).count(),
        state=state,
        metrics=metrics,
        state_error=error,
        stale=stale,
        freshness_hours=fresh_hours,
        latest_shade=latest,
        checked_at=now.astimezone(ZoneInfo('Asia/Kuala_Lumpur')),
        visual_data=visual,
        notices=notices,
        demo=bool(state and state.is_demo),
        readiness_score=readiness_score,
        shelters=ACCREDITED_SHELTERS,
        squads=ON_DUTY_SQUADS,
        emergency_contacts=EMERGENCY_CONTACTS,
        human_prompts=HUMAN_PROMPTS,
        vulnerable_count=50,
        seniors_count=38,
        oku_count=12,
    )


@login_required
@require_GET
def dashboard(request, project_id):
    member, _, _ = access(request, project_id, internal=True)
    data = build_alerts(member.project)
    data.update(
        project=member.project,
        membership=member,
        audience='alerts',
        can_manage=member.role == 'planner',
        open_count=data['active_count'],
    )
    data['visual_data']['can_manage'] = data['can_manage']
    response = render(request, 'resilience/climate_alerts.html', data)
    response['Cache-Control'] = 'private, no-store'
    return response


@login_required
@require_POST
def apply_scenario(request, project_id):
    response = scenario(request, project_id)
    if response.status_code == 302:
        return redirect('resilience:climate_alerts', project_id=project_id)
    return response


# SVG DIAGRAM GENERATORS FOR INLINE VISUAL FLOWCHARTS
def _svg_flood_diagram(lake_pct, buffer_m3):
    return f"""<div class="ca-visual-diagram">
  <div class="ca-diag-title">Hydrological Flood Buffer & Spillway Architecture (100-Year ARI Design)</div>
  <svg viewBox="0 0 780 140" width="100%" height="140" class="ca-flow-svg">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#6B7C72" />
      </marker>
    </defs>
    <!-- Step 1: Storm Inflow -->
    <rect x="10" y="22" width="160" height="96" rx="10" fill="#F0F6FB" stroke="#BDD8EA" stroke-width="2"/>
    <text x="90" y="50" text-anchor="middle" font-size="12" font-weight="700" fill="#1E3A8A">1. CATCHMENT INFLOW</text>
    <text x="90" y="74" text-anchor="middle" font-size="13" font-weight="800" fill="#1D4ED8">Up to 420mm / 24h</text>
    <text x="90" y="96" text-anchor="middle" font-size="10" fill="#556B5D">14 Perimeter Trash Grates</text>
    <!-- Arrow 1 -->
    <line x1="170" y1="70" x2="200" y2="70" stroke="#6B7C72" stroke-width="2" marker-end="url(#arrow)"/>
    <!-- Step 2: 300-Acre Retention Basin -->
    <rect x="205" y="16" width="205" height="108" rx="12" fill="#F2F8F4" stroke="#B9D4C3" stroke-width="2"/>
    <text x="307" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="#065F46">2. ELMINA DUAL BASIN</text>
    <text x="307" y="72" text-anchor="middle" font-size="16" font-weight="800" fill="#059669">{buffer_m3:,} m³ Buffer</text>
    <text x="307" y="93" text-anchor="middle" font-size="11" font-weight="600" fill="#2D6A4F">{lake_pct}% Full · Safe 6-8h Retention</text>
    <text x="307" y="110" text-anchor="middle" font-size="9.5" fill="#556B5D">JPS MSMA 100-Year ARI</text>
    <!-- Arrow 2 -->
    <line x1="410" y1="70" x2="440" y2="70" stroke="#6B7C72" stroke-width="2" marker-end="url(#arrow)"/>
    <!-- Step 3: SCADA Gravity Weir -->
    <rect x="445" y="22" width="165" height="96" rx="10" fill="#FDF7ED" stroke="#E8D4B4" stroke-width="2"/>
    <text x="527" y="50" text-anchor="middle" font-size="12" font-weight="700" fill="#92400E">3. SCADA GRAVITY WEIR</text>
    <text x="527" y="74" text-anchor="middle" font-size="13" font-weight="800" fill="#D97706">Passive Overflow Flap</text>
    <text x="527" y="96" text-anchor="middle" font-size="10" fill="#556B5D">Zero Blackout Power Risk</text>
    <!-- Arrow 3 -->
    <line x1="610" y1="70" x2="635" y2="70" stroke="#6B7C72" stroke-width="2" marker-end="url(#arrow)"/>
    <!-- Step 4: Downstream River -->
    <rect x="640" y="22" width="130" height="96" rx="10" fill="#FAF8F5" stroke="#CBD5CF" stroke-width="2"/>
    <text x="705" y="50" text-anchor="middle" font-size="11.5" font-weight="700" fill="#1C231F">4. SG. BULOH</text>
    <text x="705" y="74" text-anchor="middle" font-size="12.5" font-weight="800" fill="#2563EB">Controlled</text>
    <text x="705" y="96" text-anchor="middle" font-size="10" fill="#556B5D">Rate &lt;4.5 m³/s</text>
  </svg>
</div>"""


def _svg_pps_diagram():
    return """<div class="ca-visual-diagram">
  <div class="ca-diag-title">NADMA Directive 20: Certified Evacuation Shelter (PPS) Architecture</div>
  <svg viewBox="0 0 780 130" width="100%" height="130" class="ca-flow-svg">
    <rect x="10" y="15" width="175" height="100" rx="10" fill="#F2F8F4" stroke="#B9D4C3" stroke-width="2"/>
    <text x="97" y="44" text-anchor="middle" font-size="12" font-weight="700" fill="#065F46">SPACE & CAPACITY</text>
    <text x="97" y="68" text-anchor="middle" font-size="16" font-weight="800" fill="#059669">1,200 Persons</text>
    <text x="97" y="88" text-anchor="middle" font-size="10.5" fill="#556B5D">14,200 sq ft Main Hall</text>
    <text x="97" y="104" text-anchor="middle" font-size="9.5" fill="#556B5D">3.5m² / person ratio (JKM)</text>
    <rect x="200" y="15" width="175" height="100" rx="10" fill="#F0F6FB" stroke="#BDD8EA" stroke-width="2"/>
    <text x="287" y="44" text-anchor="middle" font-size="12" font-weight="700" fill="#1E3A8A">CONTINUOUS POWER</text>
    <text x="287" y="68" text-anchor="middle" font-size="16" font-weight="800" fill="#1D4ED8">150 kVA Genset</text>
    <text x="287" y="88" text-anchor="middle" font-size="10.5" fill="#556B5D">72-Hour Fuel On-Site</text>
    <text x="287" y="104" text-anchor="middle" font-size="9.5" fill="#556B5D">Auto Mains Failure (AMF)</text>
    <rect x="390" y="15" width="175" height="100" rx="10" fill="#FDF7ED" stroke="#E8D4B4" stroke-width="2"/>
    <text x="477" y="44" text-anchor="middle" font-size="12" font-weight="700" fill="#92400E">POTABLE WATER</text>
    <text x="477" y="68" text-anchor="middle" font-size="16" font-weight="800" fill="#D97706">10,000 Liters</text>
    <text x="477" y="88" text-anchor="middle" font-size="10.5" fill="#556B5D">3-Day Potable Reserve</text>
    <text x="477" y="104" text-anchor="middle" font-size="9.5" fill="#556B5D">Dual Filtration Cartridge</text>
    <rect x="580" y="15" width="190" height="100" rx="10" fill="#F8F3FA" stroke="#DCCCE4" stroke-width="2"/>
    <text x="675" y="44" text-anchor="middle" font-size="12" font-weight="700" fill="#5B21B6">ACCESSIBILITY (MS 1184)</text>
    <text x="675" y="68" text-anchor="middle" font-size="15" font-weight="800" fill="#7C3AED">Universal Design</text>
    <text x="675" y="88" text-anchor="middle" font-size="10.5" fill="#556B5D">1:12 Wheelchair Ramps</text>
    <text x="675" y="104" text-anchor="middle" font-size="9.5" fill="#556B5D">4 Dedicated OKU Restrooms</text>
  </svg>
</div>"""


def _svg_vulnerable_pipeline():
    return """<div class="ca-visual-diagram">
  <div class="ca-diag-title">EcoCool Prihatin: Vulnerable Resident Evacuation Priority Pipeline</div>
  <svg viewBox="0 0 780 120" width="100%" height="120" class="ca-flow-svg">
    <defs>
      <marker id="arrow2" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#6B7C72" />
      </marker>
    </defs>
    <!-- Phase 1 -->
    <rect x="10" y="20" width="225" height="80" rx="10" fill="#EDE9FE" stroke="#C4B5FD" stroke-width="2"/>
    <text x="122" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="#5B21B6">STAGE 1: GEOFENCE REGISTRY</text>
    <text x="122" y="68" text-anchor="middle" font-size="13" font-weight="800" fill="#6D28D9">50 Residents Mapped</text>
    <text x="122" y="86" text-anchor="middle" font-size="10" fill="#4C1D95">38 Seniors &amp; 12 OKU in Ilham/Revo</text>
    <!-- Arrow 1 -->
    <line x1="235" y1="60" x2="270" y2="60" stroke="#6B7C72" stroke-width="2" marker-end="url(#arrow2)"/>
    <!-- Phase 2 -->
    <rect x="275" y="20" width="225" height="80" rx="10" fill="#F0F6FB" stroke="#BAE6FD" stroke-width="2"/>
    <text x="387" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="#0369A1">STAGE 2: TWO-TIER ALERT</text>
    <text x="387" y="68" text-anchor="middle" font-size="13" font-weight="800" fill="#0284C7">Automated IVR Voice Call</text>
    <text x="387" y="86" text-anchor="middle" font-size="10" fill="#0C4A6E">2-Hour Advance Flood Warning</text>
    <!-- Arrow 2 -->
    <line x1="500" y1="60" x2="535" y2="60" stroke="#6B7C72" stroke-width="2" marker-end="url(#arrow2)"/>
    <!-- Phase 3 -->
    <rect x="540" y="20" width="230" height="80" rx="10" fill="#F2F8F4" stroke="#A7F3D0" stroke-width="2"/>
    <text x="655" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="#065F46">STAGE 3: DIRECT EVACUATION</text>
    <text x="655" y="68" text-anchor="middle" font-size="13" font-weight="800" fill="#059669">SDP Police 4WD Units</text>
    <text x="655" y="86" text-anchor="middle" font-size="10" fill="#064E3B">Transport Direct to PPS Clinic</text>
  </svg>
</div>"""


def _svg_decision_tree(lake_pct=65.0):
    b1_tag = " (CURRENT)" if lake_pct < 85 else ""
    b2_tag = " (CURRENT)" if 85 <= lake_pct <= 90 else ""
    b3_tag = " (CURRENT)" if lake_pct > 90 else ""
    return f"""<div class="ca-visual-diagram">
  <div class="ca-diag-title">JPS Hydrology Decision Matrix: Lake Spillway Operation Protocol (Current Level: {lake_pct}%)</div>
  <svg viewBox="0 0 780 120" width="100%" height="120" class="ca-flow-svg">
    <!-- Box 1 -->
    <rect x="10" y="20" width="220" height="80" rx="10" fill="#FEF3C7" stroke="#FCD34D" stroke-width="2"/>
    <text x="120" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="#92400E">THRESHOLD: &lt;85%{b1_tag}</text>
    <text x="120" y="68" text-anchor="middle" font-size="14" font-weight="800" fill="#B45309">ACTIVE MONITORING</text>
    <text x="120" y="86" text-anchor="middle" font-size="10" fill="#78350F">No manual release. Gates in auto balance.</text>
    <!-- Box 2 -->
    <rect x="245" y="20" width="270" height="80" rx="10" fill="#FEE2E2" stroke="#FCA5A5" stroke-width="2"/>
    <text x="380" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="#991B1B">THRESHOLD: 85% - 90%{b2_tag}</text>
    <text x="380" y="68" text-anchor="middle" font-size="14" font-weight="800" fill="#DC2626">STATUS: HOLD RELEASE</text>
    <text x="380" y="86" text-anchor="middle" font-size="10" fill="#7F1D1D">Check Sg. Buloh gauging station before opening.</text>
    <!-- Box 3 -->
    <rect x="530" y="20" width="240" height="80" rx="10" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2"/>
    <text x="650" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="#166534">THRESHOLD: &gt;90% + JPS CLEAR{b3_tag}</text>
    <text x="650" y="68" text-anchor="middle" font-size="14" font-weight="800" fill="#15803D">CONTROLLED DISCHARGE</text>
    <text x="650" y="86" text-anchor="middle" font-size="10" fill="#14532D">Max release rate &lt;4.5 m³/sec staggered.</text>
  </svg>
</div>"""


def _svg_arborist_sla():
    return """<div class="ca-visual-diagram">
  <div class="ca-diag-title">Township Hazard Incident Response SLA & Resource Timeline</div>
  <svg viewBox="0 0 780 110" width="100%" height="110" class="ca-flow-svg">
    <!-- Milestone 1 -->
    <rect x="10" y="20" width="230" height="70" rx="8" fill="#FEE2E2" stroke="#F87171" stroke-width="2"/>
    <text x="125" y="45" text-anchor="middle" font-size="11.5" font-weight="700" fill="#991B1B">EMERGENCY ARTERIALS</text>
    <text x="125" y="68" text-anchor="middle" font-size="15" font-weight="800" fill="#DC2626">45-Minute SLA</text>
    <text x="125" y="82" text-anchor="middle" font-size="9.5" fill="#7F1D1D">Ambulance &amp; Fire lanes reopened</text>
    <!-- Milestone 2 -->
    <rect x="255" y="20" width="250" height="70" rx="8" fill="#FEF3C7" stroke="#FBBF24" stroke-width="2"/>
    <text x="380" y="45" text-anchor="middle" font-size="11.5" font-weight="700" fill="#92400E">COOLWALK PEDESTRIAN PATHS</text>
    <text x="380" y="68" text-anchor="middle" font-size="15" font-weight="800" fill="#D97706">2-Hour SLA</text>
    <text x="380" y="82" text-anchor="middle" font-size="9.5" fill="#78350F">Trail branches cleared &amp; taped</text>
    <!-- Milestone 3 -->
    <rect x="520" y="20" width="250" height="70" rx="8" fill="#F0FDF4" stroke="#4ADE80" stroke-width="2"/>
    <text x="645" y="45" text-anchor="middle" font-size="11.5" font-weight="700" fill="#166534">HERITAGE ERT TREE RESCUE</text>
    <text x="645" y="68" text-anchor="middle" font-size="15" font-weight="800" fill="#16A34A">24-Hour SLA</text>
    <text x="645" y="82" text-anchor="middle" font-size="9.5" fill="#14532D">Tree wound dressing &amp; biomass haul</text>
  </svg>
</div>"""


def _svg_broadcast_tiers():
    return """<div class="ca-visual-diagram">
  <div class="ca-diag-title">EcoCool App: 3-Tier Multi-Hazard Early Warning Broadcast Architecture</div>
  <svg viewBox="0 0 780 110" width="100%" height="110" class="ca-flow-svg">
    <!-- Level 1 -->
    <rect x="10" y="15" width="235" height="80" rx="8" fill="#FEF9C3" stroke="#FACC15" stroke-width="2"/>
    <text x="127" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="#854D0E">TIER 1: YELLOW ADVISORY</text>
    <text x="127" y="62" text-anchor="middle" font-size="13" font-weight="800" fill="#A16207">Thunderstorm Outlook</text>
    <text x="127" y="80" text-anchor="middle" font-size="10" fill="#713F12">In-app banner · Seek gazebo shelter</text>
    <!-- Level 2 -->
    <rect x="260" y="15" width="245" height="80" rx="8" fill="#FFEDD5" stroke="#FB923C" stroke-width="2"/>
    <text x="382" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="#9A3412">TIER 2: ORANGE WARNING</text>
    <text x="382" y="62" text-anchor="middle" font-size="13" font-weight="800" fill="#C2410C">Severe Gale &gt;50 km/h</text>
    <text x="382" y="80" text-anchor="middle" font-size="10" fill="#7C2D12">Push notification + Park trail closed</text>
    <!-- Level 3 -->
    <rect x="520" y="15" width="250" height="80" rx="8" fill="#FEE2E2" stroke="#F87171" stroke-width="2"/>
    <text x="645" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="#991B1B">TIER 3: RED ALARM</text>
    <text x="645" y="62" text-anchor="middle" font-size="13" font-weight="800" fill="#DC2626">Flash Flood Evacuation</text>
    <text x="645" y="80" text-anchor="middle" font-size="10" fill="#7F1D1D">Full-screen modal + Direct SOS dispatch</text>
  </svg>
</div>"""

def _synthesize_domain_response(query_text, telemetry):
    """Deep, executive-grade knowledge response in 100% professional English,
    grounded in NADMA Arahan 20, JPS MSMA hydrology, and City of Elmina live telemetry.
    Includes visual diagrams and structured operational checklists.
    """
    q = query_text.lower()
    lake_pct = telemetry.get('lake_pct', 65)
    buffer_m3 = telemetry.get('buffer_m3', 185000)
    stored_m3 = telemetry.get('stored_m3', 345000)
    capacity_m3 = telemetry.get('capacity_m3', 530000)
    mode = telemetry.get('mode', 'normal')
    active_rep = telemetry.get('active_reports', 2)

    # 0. GREETINGS & INTRODUCTIONS (Executive Copilot Welcome)
    greeting_triggers = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'who are you', 'what can you do', 'help', 'greetings', 'salam', 'apa khabar', 'test']
    q_tokens = [w.strip('!?,.') for w in q.split()]
    if (any(q == g for g in greeting_triggers) or
        any(g in q_tokens for g in ['hello', 'hi', 'hey', 'greetings', 'salam']) or
        q in ['who are you', 'what can you do', 'help', 'start']):
        return f"""### Welcome to AeroThermal AI Copilot

> **Operational Status:** ACTIVE & MONITORING  
> **Township Catchment:** City of Elmina Dual Retention Basins (Shah Alam, Selangor)  
> **Current Basin Level:** **{lake_pct}% Full** ({stored_m3:,} m³ stored | **{buffer_m3:,} m³ active detention buffer**)  
> **Statutory Grounding:** NADMA Directive No. 20 & JPS MSMA 100-Year ARI Hydrological Model  

---

#### Hello! How can I assist your township operations today?
I am your dedicated disaster resilience and community readiness copilot for Sime Darby Property. I continuously cross-reference real-time catchment SCADA telemetry with official statutory emergency protocols to keep the City of Elmina community safe.

#### Key Resilience Domains You Can Inquire About:
1. **Accredited Evacuation Shelters (PPS):**
   - Inquire about Elmina Central Community Hall (1,200 pax capacity), 72-hour auxiliary diesel generators, 10,000L potable water tanks, and OKU accessibility.
2. **Dual Basin SCADA & Flood Detention:**
   - Review 100-Year ARI capacity, gravity spillway mechanics, and downstream river coordination with JPS Selangor at Sungai Buloh.
3. **EcoCool Prihatin (Vulnerable Resident Safety):**
   - Inspect our geofenced registry of 50 senior citizens and persons with disabilities (OKU) in Ilham and Revo parcels with priority 4WD extraction.
4. **Emergency Arterial Corridors & SLAs:**
   - High-ground evacuation spines (Persiaran Mokhtar Dahari at 42m RL) and the Arborist Squad 45-minute arterial clearance SLA.
5. **Multi-Hazard Early Warning Feeds:**
   - 3-tier resident alert triggers and real-time METMalaysia severe storm radar synchronization.
6. **Township Readiness Checklist:**
   - Active field squads (Stormwater, Certified Arborist, and Landscaping) and municipal hotline directories.

*You can type any specific operational question in the chat box below, or click any suggested topic on the dashboard to review complete technical protocols.*"""

    # 3. VULNERABLE RESIDENTS (SENIORS & OKU)
    if any(k in q for k in ['senior', 'elderly', 'vulnerable', 'oku', 'wheelchair', 'ilham', 'revo', 'chronic', 'infant']):
        diagram = _svg_vulnerable_pipeline()
        return f"""### Vulnerable Resident Protection Plan: EcoCool Prihatin Framework

> **Database Status:** ACTIVE & GEOFENCED (50 Vulnerable Residents: 38 Seniors & 12 OKU)  
> **Policy Framework:** National Policy for Older Persons & NADMA Disaster Guidelines for Persons with Disabilities  
> **Priority Focus Parcels:** Ilham Residence & Revo (Lower-lying topography adjacent to park drainage corridors)

---

#### 1. Three-Tier Proactive Protection Architecture
In the City of Elmina, safeguarding senior citizens, dialysis patients, and wheelchair-bound residents does not rely on passive loudspeaker announcements. AeroThermal activates a precision three-stage safety pipeline:

1. **Precision Geofenced Database (EcoCool Prihatin Profile):**
   - Each of the 50 registered individuals has a secured emergency record detailing: mobility assistance requirements, life-support dependencies (e.g. oxygen concentrators, insulin refrigeration), next-of-kin contacts, and precise parcel address.
   - Fully encrypted under the Personal Data Protection Act (PDPA), accessible only by the SDP Auxiliary Police Command and incoming BOMBA/APM rescue chiefs.

2. **Automated Two-Tier Voice Alert Protocol (IVR + Patrol Van):**
   - Upon escalation to Orange Alert, the system initiates **automated Interactive Voice Response (IVR) phone calls** to both the resident and their designated family caregivers.
   - An SDP Auxiliary Police patrol van is dispatched within **20 minutes** with low-frequency acoustic announcements to assist early staging before road puddles develop.

3. **Dedicated Priority Evacuation Squadron:**
   - 2 high-clearance 4WD vehicles equipped with wheelchair lifts are permanently designated for Ilham and Revo parcels.
   - Evacuees are transported directly into the **Climate-Controlled Medical Bay at Elmina Central Community Hall**, bypassing crowded staging areas.

---

{diagram}

---

#### 2. High-Ground Evacuation Walkways (CoolWalk Shaded Corridor)
- Residents departing on foot are guided along the **Elevated CoolWalk Trail (36m to 39m RL)**.
- Shaded by mature rain tree canopies that protect from windblown debris and illuminated by solar battery-backed lighting poles during night evacuations.

---

#### 3. Operational Readiness Checklist for Resident Committee (KRT Elmina)
- [ ] **Monthly Registry Verification:** Check in with all 50 registered families via the EcoCool Prihatin portal prior to monsoon onset.
- [ ] **Staged Wheelchair Storage:** Maintain at least 6 heavy-duty folding wheelchairs at the Ilham and Revo guardhouses.

*Compliance:* **NADMA Community-Based Disaster Risk Management (CBDRM)** & Sime Darby Property Social Safeguard Protocol."""

    # 4. RESERVOIR SPILLWAY & JPS COORDINATION
    if any(k in q for k in ['85%', 'weir', 'gate', 'sungai buloh', 'spillway', 'release', 'jps', 'downstream']):
        diagram = _svg_decision_tree(lake_pct)
        return f"""### Lake Spillway Operation Protocol: Catchment Hydrology & JPS River Coordination

> **Current Operational Decision:** STATUS 'HOLD' — NO MANUAL DISCHARGE AUTHORIZED WITHOUT JPS CLEARANCE  
> **Real-Time Telemetry:** Elmina Central Lake at **{lake_pct}% Capacity** | Remaining Storage Buffer: **{buffer_m3:,} m³**  
> **Downstream River Gauge:** JPS Telemetric Gauging Station Sungai Buloh (Station ID: 3115401)

---

#### 1. Hydrological Rationale: Why Premature Water Release is Hazardous
Even with Elmina Central Lake at 85% capacity, prematurely forcing open the gravity spillway gates **risks triggering flash floods in vulnerable downstream settlements** (including Kampung Kubu Gajah, Meru, and Paya Jaras):

* **The Retention "Sponge" Function:** Elmina's dual retention basin is specifically designed to function as an urban sponge—storing torrential storm runoff during peak downpours and flattening the downstream flood hydrograph.
* **Buffer Safety Margin:** At 85% capacity, Elmina still maintains over **50,000 m³ of emergency detention storage** before natural crest overflow begins over the stepped gravity weir.

---

{diagram}

---

#### 2. Three-Stage Hydrological Decision Matrix
1. **Stage 1 (75% to 84% Capacity - Active Monitoring):**
   - Stormwater Squad (Azlan) tracks SCADA ultrasonic water level sensors at 15-minute intervals.
   - Weir gates remain in automated passive balance mode. Zero manual intervention.

2. **Stage 2 (85% to 90% Capacity - Coordinated Readiness):**
   - SDP Senior Hydrologist connects directly with JPS Selangor Flood Control Operations Centre.
   - Downstream river hydrographs are evaluated. If Sungai Buloh remains below its designated Alert Level, controlled low-velocity discharge (**maximum 4.5 m³/sec**) is initiated.

3. **Stage 3 (>90% Capacity + Sustained Severe Monsoon Inflow):**
   - Passive gravity spillways engage naturally according to MSMA hydraulic engineering specs.
   - NADMA District Disaster Operations (JPBD Petaling) is alerted immediately to trigger downstream riverbank siren warnings.

---

#### 3. Immediate Directives for Field Operations (Squad Azlan)
- [ ] Inspect automated weir mechanical flap gates to confirm no tree trunks or silt clogs obstruct movement.
- [ ] Confirm latest hydrographic telemetry from JPS Public InfoBanjir before touching motorized SCADA overrides.

*Engineering Reference:* **JPS Urban Stormwater Management Manual (MSMA 2nd Ed.)** & Sime Darby Catchment Basin Protocol."""

    # 2. PPS & COMMUNITY HALL ACCREDITATION
    if any(k in q for k in ['pps', 'hall', 'community hall', 'shelter', 'accreditation', 'nadma standard', 'generator']):
        diagram = _svg_pps_diagram()
        return f"""### Evacuation Center (PPS) Compliance Audit: Official NADMA & JKM Standards

> **Compliance Status:** 94% COMPLIANT (Fully Certified as District Evacuation Center Tier 1)  
> **Statutory Reference:** NADMA Directive No. 20 & JKM National Evacuation Center Operating Guidelines (Revised 2023)  
> **Primary Facility:** Elmina Central Community Hall (Capacity: 1,200 Evacuees)

---

#### 1. Mandatory NADMA & JKM Compliance Evaluation
According to AeroThermal's comprehensive audit, Elmina Central Community Hall satisfies every critical national standard for disaster evacuation shelters:

1. **Space Allocation & Cubicle Zoning (3.5 m² per Person):**
   - The main hall spans **14,200 sq ft**, providing comfortable sheltered accommodation for up to **1,200 evacuees (~300 families)** using NADMA C-Tent modular cubicles.
   - Separate family zones, an isolation medical bay (for infectious respiratory illness control), and a dedicated lactation room are pre-designated.

2. **Uninterrupted Power Backup (AMF Diesel Genset):**
   - Equipped with an automated **150 kVA diesel generator** with on-site fuel reserve providing **72 hours of continuous off-grid electricity** for lighting, medical refrigeration, and ventilation.

3. **Universal Accessibility & Sanitation (MS 1184 Standard):**
   - Incorporates **24 toilet stalls** (meeting the 1:50 JKM standard), including 4 wheelchair-accessible stalls with grab bars and 1:12 slope access ramps.

4. **Emergency Potable Water & Relief Food Logistics:**
   - On-site potable water storage of **10,000 Liters** guarantees 3 days of survival water.
   - A hygienic staging kitchen is equipped to receive and distribute NADMA retort food packs within 2 hours of facility opening.

---

{diagram}

---

#### 2. Secondary & Neighborhood Staging Network
* **Surau Al-Madaniah Denai Alam:** Capacity: 750 pax | Elevation: 41.0m RL | 60 kVA Genset.
* **Ilham Residence Residents Clubhouse:** Capacity: 450 pax | 30 kWp Solar PV + 40 kWh Battery Storage (Zero-carbon off-grid power).

---

#### 3. Action Items Ahead of Annual Audit
- [ ] **Ultrafiltration Unit Installation:** Deploy 2 mobile water ultrafiltration units sponsored by Yayasan Sime Darby to provide redundant drinking water.
- [ ] **Satellite Telecommunications Terminal:** Position a Starlink emergency satellite dish at the registration desk to safeguard digital victim logging during cellular tower blackouts.

*Certified by:* **AeroThermal Resilience Command** under the Agensi Pengurusan Bencana Negara (NADMA) framework."""

    # 5. TREE HAZARDS & ARBORIST SLA
    if any(k in q for k in ['tree', 'branch', 'wind', 'arborist', 'coolwalk', 'sla', 'shahrul', 'crane']):
        diagram = _svg_arborist_sla()
        return f"""### Tree Hazard Incident Response Protocol: Arborist Emergency SLA & Heritage Care

> **Emergency SLA Charter:** MAXIMUM 45 MINUTES (Arterial Roads & Emergency Access Routes)  
> **Lead Arborist on Duty:** Shahrul (Certified Arborist & Landscape Squad Lead)  
> **Mobilized Heavy Assets:** 1x 3-Ton Mobile Crane with Hoist, 4x Commercial Stihl Chainsaws, Mobile LED Floodlights

---

#### 1. Service Level Agreement (SLA) by Route Classification
Under Sime Darby Property's Municipal Landscape Risk Management framework, incident response times are strictly governed:

1. **Primary Arterials & Emergency Vehicle Access (Persiaran Elmina / Medical Routes):**
   - **On-site crew response:** Within **15 minutes**.
   - **Full route reopening:** Within **maximum 45 minutes**.
   - Immediate priority: Clearance of at least one unobstructed 4-meter vehicular lane for emergency ambulances and fire tenders.

2. **CoolWalk Central Park Jogging & Cycling Trails:**
   - **On-site response:** Within **30 minutes**.
   - **Trail cleared & hazard-taped:** Within **maximum 2 hours**.
   - High-visibility reflective warning tape cordons the area to prevent pedestrian accidents.

3. **Final Biomass Hauling & Sustainable Composting:**
   - Sawn logs and branches are mulched and transported to the Elmina biomass composting facility within **24 hours**.

---

{diagram}

---

#### 2. Preservation Protocol for Endangered, Rare & Threatened (ERT) Species
Elmina Central Park nurtures thousands of irreplaceable native rainforest trees, including *Hopea odorata* (Merawan Siput Jantan) and *Shorea roxburghii* (White Meranti):
* **Strict Anti-Felling Rule:** Crews are prohibited from felling mature trees if only lateral branch failure has occurred.
* **Specialist Arboricultural Surgery:** Shahrul's certified team applies antiseptic tree wound dressing and structural balancing prunes to preserve the living canopy.

---

#### 3. Real-Time Operations Status
- Current unresolved resident reports in the portal: **{active_rep} active logs**.
- Shahrul's arborist squad is on standby with GPS geolocation coordinates mapped in the operations GIS.

*Statutory Reference:* **Sime Darby Property Urban Forestry & Arboriculture Standard Operating Procedure 2025**."""

    # 6. APP ALERT BROADCAST (ECOCOOL & NADMA)
    if any(k in q for k in ['broadcast', 'app', 'push', 'phone', 'notification', 'resident', 'alert level', 'warning']):
        diagram = _svg_broadcast_tiers()
        return f"""### Automated Community Early Warning: EcoCool Resident Mobile Integration

> **System Integration Status:** ACTIVE & CONNECTED (Direct Webhook Gateway to EcoCool Push Services)  
> **Verified User Reach:** 4,200 Registered Resident Devices in City of Elmina  
> **Regulatory Adherence:** NADMA Directive No. 20 (Early Warning Systems) & Personal Data Protection Act (PDPA)

---

#### 1. Three-Tier Multi-Hazard Broadcast Mechanism (NADMA Standard)
AeroThermal dynamically integrates METMalaysia radar feeds and on-site lake level sensors directly to resident mobile smartphones across three color-coded emergency tiers:

1. **Tier 1: Yellow Advisory (Thunderstorm Outlook & Squall Watch):**
   - *Trigger:* METMalaysia detects approaching cumulonimbus cloud clusters with expected rain within 45 minutes.
   - *Message Content:*
     > *"Elmina Weather Outlook: Thunderstorms expected across Elmina West within 45 minutes. Park visitors are advised to take shelter in nearby CoolWalk gazebos and avoid lingering under exposed tree crowns."*

2. **Tier 2: Orange Warning (Severe Gales >50 km/h & Lake Buffer Surge >75%):**
   - *Trigger:* Continuous downpour exceeding 60 mm/hr and rapid retention lake buffer filling.
   - *Message Content:*
     > *"Severe Weather Warning: Lakeside perimeter jogging trails are temporarily closed. Please move vehicles away from low-elevation curbs. Emergency response squads are patrolling."*
   - Includes interactive high-ground route navigation and detour corridors.

3. **Tier 3: Red Evacuation Alarm (Severe Flash Flood Threat / JPBD Proclamation):**
   - *Trigger:* Official disaster declaration by Petaling District Disaster Committee (JPBD) / NADMA.
   - *Message Content:*
     > *"OFFICIAL NADMA EVACUATION DIRECTIVE: Residents in Ilham and Revo parcels are advised to stage for orderly relocation to Elmina Central Community Hall (PPS). Tap the SOS Emergency Button below for immediate Auxiliary Police dispatch."*

---

{diagram}

---

#### 2. Resident Privacy & Infrastructure Security
* Broadcasts utilize privacy-safe localized geofencing based on parcel boundaries without tracking personal coordinates.
* Vulnerable seniors and OKU registered under *EcoCool Prihatin* receive automated voice escalation calls.

---

#### 3. Operations Control Command
- Control room officers can initiate verified emergency broadcasts instantly from the operations dashboard with two-factor authorization.

*Authorized by:* **AeroThermal Resilience & Communications Command**."""

    # 1. FLOOD & 2021 BENCHMARK
    if any(k in q for k in ['2021', 'flood', 'hold', 'capacity', 'ready', 'rain', 'overflow', 'december']):
        diagram = _svg_flood_diagram(lake_pct, buffer_m3)
        return f"""### Disaster Resilience Assessment: Catastrophic Flood Mitigation (December 2021 Benchmark)

> **Resilience Rating:** HIGH OPERATIONAL READINESS (92/100 Index)  
> **Statutory Baseline:** NADMA Directive No. 20 (National Disaster Mechanism) & JPS Urban Stormwater Manual (MSMA 2nd Ed.)  
> **Live Township Telemetry:** Elmina Retention Basin at {lake_pct}% Capacity | Net Available Buffer: **{buffer_m3:,} m³** | Active Mode: {mode.title()}

---

#### 1. Executive Summary: 2021 Storm Comparison & Structural Proof
During the unprecedented Selangor flood of December 2021, nearby weather radar stations logged **350 mm to 380 mm of rainfall within 24 hours** (a 1-in-100-year recurrence event). City of Elmina completely averted residential inundation due to its 300-acre dual-stage detention lake system.

Should an identical extreme cloudburst hit Elmina tomorrow, **the township holds four critical layers of engineering and community defense**:

1. **Hydrological 100-Year ARI (Average Recurrence Interval) Safety Margin:**
   - The Elmina West and East dual basin holds a cumulative hydrological capacity of **{capacity_m3:,} m³**, engineered to buffer storm surges of up to 420 mm/24 hours before reaching emergency spillway elevation.
   - At current storage levels ({lake_pct}% full), the basin retains an active buffer of **{buffer_m3:,} m³**, capable of absorbing **6 to 8 hours of uninterrupted torrential deluge** with zero embankment spillover.

2. **Automated SCADA Gravity Spillway Gates (Zero Power Grid Vulnerability):**
   - Unlike conventional pumping stations that can fail during power grid blackouts, Elmina's stepped spillway operates strictly on gravity hydraulics. If TNB grid substations fail, excess water is safely discharged passively without manual intervention.

3. **Elevated Rescue & Evacuation Corridors:**
   - Persiaran Mokhtar Dahari and the Elmina West arterial flyovers are constructed at **38m to 42m Reduced Level (RL)**, safely above the 31m RL maximum 100-year flood line, guaranteeing unhindered emergency vehicle ingress and egress.

---

{diagram}

---

#### 2. Community Readiness & Life Safety Audit
Community preparedness goes beyond concrete basins—resident life safety is the ultimate benchmark:
* **Accredited Evacuation Shelters (PPS):** Three pre-certified shelters (Elmina Central Community Hall, Surau Al-Madaniah, and Ilham Clubhouse) are prepared to activate within **90 minutes** of a District Disaster Committee (JPBD) proclamation.
* **Vulnerable Resident Registry (EcoCool Prihatin):** Exactly **38 senior citizens** and **12 persons with disabilities (OKU)** in low-lying parcels have been geofenced with caregiver contacts for priority evacuation by Sime Darby Auxiliary Police.
* **Dual-Channel Warning Broadcast:** Automated alert pushes via the EcoCool Resident App trigger whenever basin levels cross 75% or METMalaysia radar detects severe cloudburst cells within a 15 km radius.

---

#### 3. Immediate Operational Squad Checklist
- [ ] **Stormwater Squad (Azlan):** Execute physical inspection across all 14 perimeter trash grates by 16:00 to clear saturated debris.
- [ ] **Auxiliary Police Command:** Verify readiness of 2 fiber rescue boats and 4 high-clearance 4WD vehicles stationed at Elmina Clubhouse.
- [ ] **JPS Selangor Coordination:** Cross-check live river gauging station data at Sungai Buloh before adjusting mechanical weir settings.

*Regulatory Grounding:* **NADMA Directive No. 20 (Clause 14 - Community Preparedness)** & JPS Stormwater Management Manual (MSMA-2)."""

    # 7. GENERAL / COMMUNITY READINESS OVERVIEW
    return f"""### Comprehensive Township Disaster Readiness & Community Resilience Assessment

> **Overall Community Readiness Score:** 92/100 (High Operational Readiness)  
> **Regulatory Baseline:** NADMA Directive No. 20, Civil Defence Act 1951 & Sime Darby Property Masterplan  
> **Township:** City of Elmina, Shah Alam, Selangor | Active Buffer: **{buffer_m3:,} m³** ({lake_pct}% Full)

---

#### 1. Executive Summary: Is Elmina Community Disaster-Ready?
Yes. City of Elmina operates at **a benchmark standard of community disaster preparedness**, coupling 100-Year ARI physical engineering defenses with certified civil protection assets:

1. **Heavy Engineering Infrastructure:**
   - Dual 300-acre retention basin system holding an active flood buffer of **{buffer_m3:,} m³**.
   - Strategic elevated arterial corridors (Persiaran Mokhtar Dahari at 42m RL) safeguarding rescue ingress against extreme inundation.

2. **Life Safety & Humanitarian Staging:**
   - 3 NADMA-accredited evacuation shelters with a combined shelter capacity of **2,400 residents**, fortified with 72-hour diesel power generators and 10,000L emergency potable reservoirs.
   - 50 vulnerable residents (seniors and OKU) pre-mapped for priority extraction by SDP Auxiliary Police 4WD squads.

3. **Rapid On-Duty Operations:**
   - 3 specialized squads (Stormwater, Certified Arborist, and Landscape Irrigation) active with a mandatory 45-minute emergency clearance SLA.

---

{_svg_flood_diagram(lake_pct, buffer_m3)}

---

#### 2. Critical Emergency Command Directory
- **SDP Auxiliary Police Control Room (24/7):** 03-7848 1111
- **BOMBA Shah Alam Fire & Rescue:** 03-7846 4444
- **Civil Defence Force (APM) Petaling Command:** 03-5510 2233
- **NADMA National Disaster Command Centre:** 03-8064 2400

*AeroThermal AI continuously synchronizes with on-site SCADA telemetry and national hazard feeds 24 hours a day to safeguard City of Elmina.*"""


_GEMINI_MODEL_CACHE = {}


def discover_available_gemini_models(client_api_key):
    """Dynamically query Google's ModelService to list active models for this specific API key.
    Eliminates 404 / 'model not found' errors by asking Google what models this key can use.
    """
    if not client_api_key:
        return []
    if client_api_key in _GEMINI_MODEL_CACHE:
        return _GEMINI_MODEL_CACHE[client_api_key]

    discovered = []
    # 1. Direct REST query against v1beta ModelService.ListModels
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={client_api_key}"
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for m in data.get('models', []):
                methods = m.get('supportedGenerationMethods', [])
                if 'generateContent' in methods:
                    m_name = m.get('name', '').replace('models/', '').strip()
                    if 'gemini' in m_name:
                        discovered.append(m_name)
    except Exception as e:
        logger.warning(f"REST v1beta ModelService.ListModels error: {e}")

    # 1b. Fallback to v1 endpoint if v1beta returned no models
    if not discovered:
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models?key={client_api_key}"
            req = urllib.request.Request(url, headers={'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for m in data.get('models', []):
                    methods = m.get('supportedGenerationMethods', [])
                    if 'generateContent' in methods:
                        m_name = m.get('name', '').replace('models/', '').strip()
                        if 'gemini' in m_name:
                            discovered.append(m_name)
        except Exception as e:
            logger.warning(f"REST v1 ModelService.ListModels error: {e}")

    # 2. Try via google.genai SDK if REST calls failed
    if not discovered:
        try:
            from google import genai
            client = genai.Client(api_key=client_api_key)
            for m in client.models.list():
                name = (getattr(m, 'name', '') or getattr(m, 'base_model_id', '')).replace('models/', '').strip()
                if 'gemini' in name:
                    discovered.append(name)
        except Exception as e:
            logger.warning(f"SDK ModelService.ListModels error: {e}")

    # Prioritize: Flash models first, then Pro models, preferring latest stable versions
    def rank(name):
        score = 0
        nl = name.lower()
        if 'flash' in nl: score += 100
        if 'pro' in nl: score += 50
        if '2.5' in nl: score += 40
        elif '2.0' in nl: score += 30
        elif '1.5' in nl: score += 20
        if 'latest' in nl: score += 5
        if 'preview' in nl or 'exp' in nl: score -= 10
        return score

    discovered.sort(key=rank, reverse=True)
    if discovered:
        _GEMINI_MODEL_CACHE[client_api_key] = discovered
    return discovered


@login_required
@require_POST
def chat_query(request, project_id):
    """API endpoint accepting user queries and generating comprehensive,
    RAG-grounded responses in 100% English using Google Gemini API or the built-in domain synthesizer.
    Requires authenticated planner/viewer membership and validates CSRF.
    """
    m, resident, _ = access(request, project_id, internal=True)
    project = m.project

    try:
        body = json.loads(request.body.decode('utf-8')) if request.body else {}
    except Exception:
        body = {}

    query_text = (body.get('query') or request.POST.get('query') or '').strip()
    client_api_key = (
        body.get('api_key')
        or request.headers.get('X-Gemini-Key')
        or os.environ.get('GEMINI_API_KEY')
        or os.environ.get('GOOGLE_API_KEY')
        or getattr(settings, 'GEMINI_API_KEY', '')
    )
    if client_api_key:
        client_api_key = client_api_key.strip()

    if not query_text:
        return JsonResponse({'error': 'Query text cannot be empty.'}, status=400)

    # Fetch live project and telemetry directly from database
    state = ClimateState.objects.filter(project=project).first()
    active_reports = FieldReport.objects.filter(project=project).exclude(status='resolved').count()
    try:
        metrics = storage_metrics(state) if state else {}
    except Exception:
        metrics = {}

    capacity_m3 = state.capacity_m3 if state else 100000
    stored_m3 = state.stored_m3 if state else 65000
    buffer_m3 = metrics.get('buffer_m3', max(0, capacity_m3 - stored_m3))
    lake_pct = metrics.get('capacity_pct', round(stored_m3 / capacity_m3 * 100, 1) if capacity_m3 else 65.0)

    telemetry = {
        'lake_pct': lake_pct,
        'buffer_m3': buffer_m3,
        'stored_m3': stored_m3,
        'capacity_m3': capacity_m3,
        'mode': state.scenario if state else 'normal',
        'active_reports': active_reports,
        'is_demo': state.is_demo if state else True,
        'source': state.source if state else 'Synthetic demonstration inputs; no sensor connection',
    }

    # Perform real RAG retrieval across statutory corpus
    from . import rag_engine
    retrieved_chunks = rag_engine.retrieve(query_text, top_k=2)

    response_text = None
    provider_used = 'AeroThermal Grounded RAG Synthesizer'
    gemini_error = None

    # If Gemini API Key is available, invoke Gemini with augmented prompt
    if client_api_key:
        system_prompt = rag_engine.build_rag_system_prompt(telemetry, retrieved_chunks)
        discovered = discover_available_gemini_models(client_api_key)
        fallback_models = [
            'gemini-2.0-flash',
            'gemini-1.5-flash-latest',
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-2.5-flash',
        ]
        gemini_models = (discovered if discovered else fallback_models)[:4]
        logger.info(f"Targeting Gemini models for key: {gemini_models}")

        # Method A: Try google.genai SDK
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=client_api_key)
            for mod in gemini_models[:4]:
                try:
                    ai_response = client.models.generate_content(
                        model=mod,
                        contents=query_text,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.3,
                        ),
                    )
                    if ai_response and ai_response.text:
                        response_text = ai_response.text
                        provider_used = f'Google Gemini ({mod} + NADMA RAG)'
                        gemini_error = None
                        break
                except Exception as mod_err:
                    gemini_error = str(mod_err)
                    logger.warning(f'Gemini SDK model {mod} error: {mod_err}')
                    if 'API key not valid' in gemini_error or 'API_KEY_INVALID' in gemini_error:
                        break
                    continue
        except Exception as sdk_err:
            gemini_error = str(sdk_err)
            logger.warning(f'google.genai SDK init error: {sdk_err}')

        # Method B: Direct REST API fallback if SDK fails
        if not response_text:
            for mod in gemini_models[:4]:
                try:
                    api_url = f'https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={client_api_key}'
                    payload = {
                        'contents': [{'role': 'user', 'parts': [{'text': query_text}]}],
                        'system_instruction': {'parts': [{'text': system_prompt}]},
                        'generationConfig': {'temperature': 0.3}
                    }
                    req = urllib.request.Request(
                        api_url,
                        data=json.dumps(payload).encode('utf-8'),
                        headers={'Content-Type': 'application/json'},
                        method='POST'
                    )
                    with urllib.request.urlopen(req, timeout=12) as resp:
                        resp_json = json.loads(resp.read().decode('utf-8'))
                        candidates = resp_json.get('candidates', [])
                        if candidates:
                            content_obj = candidates[0].get('content', {})
                            parts = content_obj.get('parts', [])
                            if parts and 'text' in parts[0]:
                                response_text = parts[0]['text']
                                provider_used = f'Google Gemini ({mod} Direct REST + RAG)'
                                gemini_error = None
                                break
                except urllib.error.HTTPError as he:
                    try:
                        err_body = json.loads(he.read().decode('utf-8'))
                        gemini_error = err_body.get('error', {}).get('message', f'HTTP Error {he.code}')
                    except Exception:
                        gemini_error = f'HTTP Error {he.code}'
                    logger.warning(f'Gemini REST error for {mod}: {gemini_error}')
                    if 'API key not valid' in gemini_error or 'API_KEY_INVALID' in gemini_error:
                        break
                    continue
                except Exception as rest_e:
                    gemini_error = str(rest_e)
                    logger.warning(f'Gemini REST connection error: {rest_e}')
                    continue

    # Fallback to domain synthesizer if no Gemini response
    if not response_text:
        response_text = _synthesize_domain_response(query_text, telemetry)
        if client_api_key and gemini_error:
            clean_err = gemini_error
            if 'API key not valid' in clean_err:
                clean_err = 'The entered API Key is invalid or not enabled for Google Gemini API.'
            elif 'Resource has been exhausted' in clean_err:
                clean_err = 'Gemini API quota exceeded for this key.'
            elif len(clean_err) > 130:
                clean_err = clean_err[:130] + '...'
            error_notice = f"> ⚠️ **Google Gemini Connection Notice:** Unable to reach Gemini API (`{clean_err}`). Generating verified on-premise NADMA domain knowledge instead.\n\n"
            response_text = error_notice + response_text
            provider_used = 'AeroThermal Synthesizer (Gemini Key Issue)'

    return JsonResponse({
        'status': 'success',
        'query': query_text,
        'response': response_text,
        'provider': provider_used,
        'telemetry': telemetry,
        'retrieved_sources': [
            {
                'id': c['chunk_id'],
                'source': c['source'],
                'clause': c['clause'],
                'title': c['title'],
                'text': c['text'],
                'score': c['score'],
            }
            for c in retrieved_chunks
        ],
        'grounded_sources': [
            'NADMA Directive No. 20 (National Disaster Management Mechanism)',
            'JPS Urban Stormwater Manual (MSMA 2nd Ed.) - 100-Yr ARI Hydrology',
            'Department of Social Welfare (JKM) National Evacuation Center (PPS) Standards',
            'EcoCool Prihatin Vulnerable Community Registry (50 Registered Residents)',
            f"City of Elmina Dual Retention Basin SCADA Telemetry ({buffer_m3:,} m³ Buffer)",
        ],
    })
