from django.core.management.base import BaseCommand,CommandError
from planner.models import Project
from resilience.models import ClimateState

class Command(BaseCommand):
    help='Create synthetic climate data for one existing project without changing existing records.'
    def add_arguments(self,parser): parser.add_argument('--project',required=True,type=int)
    def handle(self,*args,**options):
        try: project=Project.objects.get(pk=options['project'])
        except Project.DoesNotExist: raise CommandError('Project not found.')
        coords=project.site_data.get('path',{}).get('coordinates',[])
        zones=[]
        for i,fraction in enumerate([0.2,0.5,0.8]):
            if coords:
                zones.append({'coordinates':coords[min(len(coords)-1,int(len(coords)*fraction))],
                              'label':f'Illustrative hotspot {i+1} - not satellite LST',
                              'sample_surface_c':[38,36,39][i]})
        state,created=ClimateState.objects.get_or_create(project=project,defaults={
            'history':[{'label':f'Demo T-{5-i}','storage_pct':v} for i,v in enumerate([60,61,63,64,64,65])],
            'zones':zones})
        self.stdout.write(('Created' if created else 'Preserved existing')+f' demo state for project {project.pk}. No reports, notices, users or awards were fabricated.')
