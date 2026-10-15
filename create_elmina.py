"""Run with manage.py shell, after copying elmina/site.json beside manage.py."""
import json
from pathlib import Path
from django.conf import settings
from django.db import transaction
from planner.models import Project, Membership

name = 'Elmina Valley Central Park - Map Pilot'
version = 'elmina-osm-v1'
data = json.loads((Path(settings.BASE_DIR) / 'elmina/site.json').read_text(encoding='utf-8'))
assert data['basemap']['provider'] == 'google'
assert data['path']['type'] == 'LineString'
assert 2 <= len(data['path']['coordinates']) <= 500
assert data['existing_trees'] == [] and data['baseline_inventory_available'] is False
assert all(101 < x < 102 and 3 < y < 4 for x, y in data['path']['coordinates'])
with transaction.atomic():
    matches = Project.objects.filter(name=name)
    if matches.count() > 1:
        raise ValueError('Multiple Elmina projects found. Resolve duplicates in admin before continuing.')
    project, created = Project.objects.get_or_create(name=name, defaults={'site_version':version, 'site_data':data})
    if not created and (project.site_version != version or project.site_data != data):
        raise ValueError('An Elmina project already has different data. It was not overwritten.')
    source = Project.objects.filter(name='EcoCool Lakeside Concept Park').first()
    if source is None:
        source = Project.objects.filter(name='EcoCool Demonstration Park').first()
    if source:
        for membership in Membership.objects.filter(project=source):
            Membership.objects.get_or_create(project=project, user=membership.user, defaults={'role':membership.role})
print(('Created' if created else 'Already exists') + ': ' + project.name)
print('Project ID:', project.pk)
print('Memberships:', Membership.objects.filter(project=project).count())
print('Open the project from the homepage. If missing, assign your account to this project in Django admin.')
