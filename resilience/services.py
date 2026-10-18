import math
from django.utils import timezone

PRESETS = {
 'normal':(65000,0), 'storm':(65000,40000),
 'heat':(65000,0), 'drought':(25000,0), 'wind':(65000,0),
}

def storage_metrics(state):
    total,stored,reserve,target = state.capacity_m3,state.stored_m3,state.reserve_m3,state.target_m3
    if total <= 0 or not 0 <= reserve <= total or not 0 <= target <= total or not 0 <= stored <= total:
        raise ValueError('Storage assumptions are inconsistent.')
    candidate = max(0,min(stored-target,stored-reserve)) if state.scenario == 'storm' else 0
    return {'capacity_pct':round(stored/total*100,1),'buffer_m3':total-stored,
            'candidate_m3':candidate,'after_buffer_m3':total-stored+candidate,
            'overflow_without_m3':max(0,stored+state.assumed_inflow_m3-total),
            'overflow_after_m3':max(0,stored-candidate+state.assumed_inflow_m3-total),
            'forecast_storage_m3':stored-candidate+state.assumed_inflow_m3,
            'release_status':'HOLD: downstream capacity and permitted release rate are unverified.'}

def within_site(project,lat,lon):
    centre = project.site_data.get('site',{})
    if 'latitude' not in centre or 'longitude' not in centre: return False
    a,b = math.radians(float(centre['latitude'])),math.radians(lat)
    dlat=b-a;dlon=math.radians(lon-float(centre['longitude']))
    hav=math.sin(dlat/2)**2+math.cos(a)*math.cos(b)*math.sin(dlon/2)**2
    return 6371000*2*math.asin(min(1,math.sqrt(max(0,hav)))) <= 2000

def event(actor,action,note=''):
    return {'at':timezone.now().isoformat(),'actor':actor.username,'action':action,'note':note}

def shade_summary(scenarios):
    rows=[]
    for scenario in scenarios:
        result=scenario.result_data or {}
        value=(result.get('proposed') or {}).get('path_shade_pct')
        rows.append({'name':scenario.name,'mode':result.get('mode','unknown'),
                     'shade':value if result.get('mode')=='simulation' and isinstance(value,(float,int)) and math.isfinite(value) else None,
                     'timestamp':(scenario.input_data or {}).get('timestamp',''),
                     'model':result.get('model_version','unknown'),'site_version':scenario.site_version})
    return rows
