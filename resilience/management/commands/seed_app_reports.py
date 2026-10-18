"""Fixture-only mobile input; does not expose a resident web form or app API."""
from pathlib import Path
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand,CommandError
from django.db import transaction
from django.utils import timezone
from planner.models import Project
from resilience.models import FieldReport
from resilience.forms import ReportForm
from resilience.services import within_site

CASES=[
 ('drain','flood','Blocked drain','Leaves and litter are obstructing a lakeside drain.','East lake path · sample','open',0.15,24,'blocked-drain.jpg'),
 ('branch','wind','Fallen branch','A branch is obstructing part of the walking path.','Lakeside loop · sample','in_progress',0.40,65,'fallen-branch.jpg'),
 ('dry','drought','Dry vegetation','Dry planting soil and stressed young vegetation were reported.','South planting edge · sample','open',0.65,110,'dry-vegetation.jpg'),
 ('heat','heat','Heat exposure','A resident reported an exposed resting area with little shade.','West path seating · sample','resolved',0.85,180,'heat-exposure.jpg'),
]
class Command(BaseCommand):
    help='Create four explicitly labelled dummy mobile-app reports; preserve existing reports.'
    def add_arguments(self,parser):
        parser.add_argument('--project',type=int,required=True)
        parser.add_argument('--photo-dir',default=None)
    def handle(self,*args,**options):
        try:project=Project.objects.get(pk=options['project'])
        except Project.DoesNotExist:raise CommandError('Project not found.')
        coords=project.site_data.get('path',{}).get('coordinates',[])
        if len(coords)<2:raise CommandError('Project needs a GeoJSON path before sample locations can be seeded.')
        user,_=get_user_model().objects.get_or_create(username=f'app_fixture_project_{project.pk}',defaults={'is_active':False})
        if user.is_active:raise CommandError('Fixture account name is already in active use. No reports created.')
        if user.has_usable_password():user.set_unusable_password();user.save(update_fields=['password'])
        existing={e.get('sample_key'):r for r in FieldReport.objects.filter(project=project,reporter=user) for e in (r.events[:1] if r.events else [])}
        created=0
        with transaction.atomic():
            for i,(key,kind,title,desc,location,status,fraction,minutes,filename) in enumerate(CASES):
                row=existing.get(key)
                if row is None:
                    lon,lat=coords[min(len(coords)-1,int(len(coords)*fraction))]
                    if not within_site(project,lat,lon):raise CommandError('Sample route point lies outside the supported project extent.')
                    stamp=timezone.now()-timedelta(minutes=minutes)
                    events=[{'at':stamp.isoformat(),'actor':'Sample mobile app','action':'received','note':'Dummy input for the B2B prototype.',
                             'sample':True,'sample_key':key,'source':'resident_app_fixture','external_id':f'APP-DEMO-{i+101}',
                             'title':title,'location_label':location}]
                    if status!='open':events.append({'at':(stamp+timedelta(minutes=10)).isoformat(),'actor':'Sample workflow','action':status,'note':'Seeded example status; not real field work.'})
                    row=FieldReport.objects.create(project=project,reporter=user,kind=kind,description=desc,latitude=lat,longitude=lon,status=status,verified=status=='resolved',events=events)
                    FieldReport.objects.filter(pk=row.pk).update(created_at=stamp)
                    created+=1
                if options['photo_dir'] and not row.photo:
                    path=Path(options['photo_dir'])/filename
                    if not path.exists():self.stdout.write(f'No image for {key}; illustration retained.');continue
                    form=ReportForm(data={'kind':kind,'description':desc},files={'photo':SimpleUploadedFile(filename,path.read_bytes())})
                    if not form.is_valid():raise CommandError(f'Invalid sample photo {filename}: {form.errors.as_text()}')
                    row.photo=form.cleaned_data['photo'];row.save(update_fields=['photo'])
        self.stdout.write(self.style.SUCCESS(f'Created {created} dummy app reports; existing reports preserved. Locations and illustrations are samples, not field evidence.'))
