"""Run with manage.py shell. Creates a new illustrative site; preserves old sites."""
import math
from django.db import transaction
from planner.models import Project, Membership

LON, LAT = 101.5, 3.1
def xy(x, y):
    return [LON + x / (111320 * math.cos(math.radians(LAT))), LAT + y / 110574]

def ring(points):
    values = [xy(x, y) for x, y in points]
    return values + [values[0]]

def oval(cx, cy, rx, ry, n=72, organic=False):
    points = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1 + (0.13*math.sin(3*a) + 0.05*math.cos(5*a) if organic else 0)
        points.append((cx + rx*math.cos(a)*r, cy + ry*math.sin(a)*r))
    return points

def polygon(points):
    return {'type': 'Polygon', 'coordinates': [ring(points)]}

def feature(kind, geometry, **props):
    return {'type': 'Feature', 'properties': {'kind': kind, **props}, 'geometry': geometry}

boundary = polygon(oval(0, 0, 176, 114, organic=True))
lake = polygon(oval(-48, 20, 63, 42, organic=True))
pavilion = polygon([(92,-43),(118,-43),(118,-24),(92,-24)])
playground = polygon(oval(82,52,24,17))
planting = {'type':'Polygon','coordinates': [
    boundary['coordinates'][0],
    list(reversed(lake['coordinates'][0])),
    list(reversed(pavilion['coordinates'][0])),
    list(reversed(playground['coordinates'][0])),
]}

path_points = oval(-42, 15, 82, 61, n=100, organic=True)
route = {'type':'LineString','coordinates':ring(path_points)}
spur = {'type':'LineString','coordinates':[xy(x,y) for x,y in [(24,-42),(48,-42),(66,-33),(86,-33),(105,-33)]]}
features = [
    feature('land', boundary),
    feature('meadow',polygon(oval(66,6,51,31,organic=True))),
    feature('grove',polygon(oval(-36,-79,74,20,organic=True))),
    feature('grove',polygon(oval(10,87,70,15,organic=True))),
    feature('lake', lake),
    feature('path',route),
    feature('walkway',spur),
    feature('playground',playground),
    feature('building',pavilion),
]

# All trees are synthetic assumptions. They are genuine model inputs, not extra decorative trees.
from shapely.geometry import Point, shape
permitted = shape(planting)
existing = []
positions = [(-140,22),(-135,-2),(-132,-28),(-112,-56),(-91,-70),(-65,-79),(-41,-78),(-18,-74),
             (5,-82),(30,-77),(64,-69),(86,-64),(119,-62),(137,-34),(145,-8),(145,25),
             (119,74),(91,84),(61,89),(35,90),(7,91),(-22,90),(-49,88),(-78,86),
             (-108,69),(-132,48),(-87,-31),(-67,-40),(-43,-43),(27,50),(36,29),(40,4)]
for i,(x,y) in enumerate(positions):
    if permitted.covers(Point(xy(x,y))):
        existing.append({'id':f'existing-{i+1}','status':'existing','coordinates':xy(x,y),
                         'canopy_radius_m':5.0+(i%4)*0.8,'canopy_height_m':7.0+(i%3)})

seats = [{'id':f'seat-{i+1}','coordinates':xy(x,y)} for i,(x,y) in enumerate([(-82,-30),(-26,-40),(28,5),(-110,48),(19,60)])]
labels = [
    {'text':'LAKESIDE WATER GARDEN','coordinates':xy(-48,23),'kind':'water'},
    {'text':'OPEN LAWN','coordinates':xy(75,3),'kind':'land'},
    {'text':'PLAY GARDEN','coordinates':xy(82,52),'kind':'land'},
    {'text':'PAVILION','coordinates':xy(105,-33),'kind':'building'},
    {'text':'SOUTH GROVE','coordinates':xy(-30,-99),'kind':'land'},
]
data = {
    'site':{'latitude':LAT,'longitude':LON},
    'default_timestamp':'2026-10-15T15:00:00+08:00',
    'path':route,'seats':seats,'existing_trees':existing,
    'planting_area':planting,'lake':lake,
    'display_geojson':{'type':'FeatureCollection','features':features},
    'labels':labels,
    'source_note':'Illustrative concept park. Synthetic geometry and assumed tree dimensions; not an Elmina survey.',
    'example_proposed_trees':[
        {'id':f'proposed-example-{i+1}','status':'proposed','coordinates':xy(x,y),
         'canopy_radius_m':5.0,'canopy_height_m':7.0}
        for i,(x,y) in enumerate([(35,-10),(39,-27),(10,-49),(-17,-55)])
    ],
}

if not permitted.is_valid:
    raise ValueError('Concept planting geometry is invalid.')
for tree in data['example_proposed_trees']:
    if not permitted.covers(Point(tree['coordinates'])):
        raise ValueError('An example tree is outside the permitted area.')

with transaction.atomic():
    project, created = Project.objects.get_or_create(
        name='EcoCool Lakeside Concept Park',
        defaults={'site_version':'concept-v2','site_data':data},
    )
    source = Project.objects.filter(name='EcoCool Demonstration Park').first()
    count = 0
    if source:
        for member in Membership.objects.filter(project=source):
            _, added = Membership.objects.get_or_create(
                project=project,user=member.user,defaults={'role':member.role})
            count += int(added)
print(f"{'Created' if created else 'Found existing'} project {project.id}: {project.name}")
print(f'Copied {count} new memberships from the demonstration project.')
if not Membership.objects.filter(project=project).exists():
    print('Add your user to this project in Django admin > Memberships.')
