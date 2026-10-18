import io,json,tempfile
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from django.test import TestCase,Client,override_settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta
from planner.models import Project,Membership,Scenario
from .models import ClimateState,FieldReport,StakeholderAccess,Advisory
from .services import storage_metrics
from .weather import fetch_warnings

class WorkflowTests(TestCase):
    def setUp(self):
        self.planner=User.objects.create_user('planner',password='TestOnly_12345')
        self.viewer=User.objects.create_user('viewer',password='TestOnly_12345')
        self.resident=User.objects.create_user('resident',password='TestOnly_12345')
        self.other=User.objects.create_user('other',password='TestOnly_12345')
        self.project=Project.objects.create(name='Test pilot',site_version='elmina-osm-v1',site_data={'site':{'latitude':3.179,'longitude':101.515},'baseline_inventory_available':False,'path':{'type':'LineString','coordinates':[[101.5149,3.1791],[101.5151,3.1792],[101.5152,3.1793]]},'display_geojson':{'type':'FeatureCollection','features':[]}})
        self.state=ClimateState.objects.create(project=self.project)
        for user,role in [(self.planner,'planner'),(self.viewer,'viewer'),(self.resident,'viewer')]:
            m=Membership.objects.create(project=self.project,user=user,role=role)
            if user==self.resident: StakeholderAccess.objects.create(membership=m,resident_only=True)
        self.base=f'/projects/{self.project.pk}/resilience/'
        self.client.force_login(self.planner)
    def report(self,**kw):
        return FieldReport.objects.create(project=self.project,reporter=self.resident,kind='wind',description='Fallen branch',**kw)
    def test_viewer_reads_but_cannot_write(self):
        self.client.force_login(self.viewer)
        self.assertEqual(self.client.get(self.base+'view/operations/').status_code,200)
        self.assertEqual(self.client.post(self.base+'scenario/',{'scenario':'storm'}).status_code,403)
        self.assertEqual(self.client.post(self.base+'notices/new/',{}).status_code,403)
        self.assertEqual(self.client.post(self.base+f'reports/{self.report().pk}/triage/',{}).status_code,403)
    def test_nonmember_cannot_access(self):
        self.client.force_login(self.other)
        for suffix in ['view/leadership/','map-data/','snapshot/','export/','weather/']:
            self.assertEqual(self.client.get(self.base+suffix).status_code,404)
    def test_csrf_required(self):
        c=Client(enforce_csrf_checks=True);c.force_login(self.planner)
        self.assertEqual(c.post(self.base+'scenario/',{'scenario':'storm'}).status_code,403)
    def test_storage_and_drought(self):
        self.client.post(self.base+'scenario/',{'scenario':'storm'})
        self.state.refresh_from_db();m=storage_metrics(self.state)
        self.assertEqual((m['buffer_m3'],m['candidate_m3'],m['after_buffer_m3']),(35000,10000,45000))
        self.assertEqual((m['overflow_without_m3'],m['overflow_after_m3']),(5000,0))
        self.assertFalse(self.state.downstream_verified)
        self.client.post(self.base+'scenario/',{'scenario':'drought'})
        self.state.refresh_from_db();self.assertEqual(storage_metrics(self.state)['candidate_m3'],0)
    def test_cross_project_report_denied(self):
        p=Project.objects.create(name='Other',site_version='v1',site_data={})
        r=FieldReport.objects.create(project=p,reporter=self.other,kind='heat',description='Other project')
        self.assertEqual(self.client.get(self.base+f'reports/{r.pk}/').status_code,404)
        self.assertEqual(self.client.post(self.base+f'reports/{r.pk}/triage/',{'status':'resolved','note':'x','version':1}).status_code,404)
    def test_csv_uses_calculated_values_and_escapes_formulas(self):
        Scenario.objects.create(project=self.project,name='=1+1',site_version='v1',input_data={'timestamp':'2026-10-15T15:00:00+08:00'},result_data={'mode':'simulation','proposed':{'path_shade_pct':5.3},'model_version':'test'},created_by=self.planner)
        r=self.client.get(self.base+'export/');self.assertEqual(r.status_code,200)
        self.assertIn("'=1+1",r.content.decode());self.assertIn('Not surveyed',r.content.decode());self.assertIn('5.3',r.content.decode())
    def test_weather_disabled(self):
        with override_settings(AEROTHERMAL_LIVE_WARNINGS=False):self.assertEqual(fetch_warnings()['status'],'disabled')
    def test_weather_failure_is_not_all_clear(self):
        from django.core.cache import cache
        cache.clear()
        with override_settings(AEROTHERMAL_LIVE_WARNINGS=True),patch('resilience.weather.urlopen',side_effect=OSError):
            self.assertEqual(fetch_warnings()['status'],'unavailable')

    def test_three_visual_b2b_pages(self):
        for page in ['engineer','operations','leadership']:
            r=self.client.get(self.base+'view/'+page+'/')
            self.assertEqual(r.status_code,200)
            self.assertContains(r,'visual-data')
            self.assertNotContains(r,'Resident demo')
        self.assertEqual(self.client.get(self.base+'view/resident/').status_code,410)

    def test_resident_accounts_cannot_enter_b2b(self):
        self.client.force_login(self.resident)
        for url in [self.base,self.base+'view/operations/',self.base+'visual-data/',f'/projects/{self.project.pk}/']:
            self.assertEqual(self.client.get(url).status_code,403)

    def test_web_submission_removed(self):
        before=FieldReport.objects.count()
        r=self.client.post(self.base+'reports/new/',{'kind':'wind','description':'Should not be accepted'})
        self.assertEqual(r.status_code,410)
        self.assertEqual(FieldReport.objects.count(),before)

    def test_dummy_app_inputs_are_idempotent(self):
        from django.core.management import call_command
        call_command('seed_app_reports',project=self.project.pk,verbosity=0)
        self.assertEqual(FieldReport.objects.count(),4)
        call_command('seed_app_reports',project=self.project.pk,verbosity=0)
        self.assertEqual(FieldReport.objects.count(),4)
        for report in FieldReport.objects.all():
            self.assertTrue(report.events[0]['sample'])
            self.assertFalse(report.reporter.is_active)
        data=self.client.get(self.base+'visual-data/').json()
        self.assertEqual(data['counts'],{'open':2,'in_progress':1,'resolved':1,'total':4,'active':3})
        self.assertEqual(len(data['reports']),4)
        self.assertTrue(all(r['sample'] for r in data['reports']))

    def test_workflow_does_not_issue_app_rewards(self):
        report=self.report()
        data={'status':'resolved','verified':'on','assign_to_me':'on','note':'Inspected and cleared','version':1}
        self.assertEqual(self.client.post(self.base+f'reports/{report.pk}/triage/',data).status_code,302)
        report.refresh_from_db()
        self.assertEqual(report.status,'resolved');self.assertEqual(report.demo_points,0)
        self.assertEqual(self.client.post(self.base+f'reports/{report.pk}/triage/',data).status_code,409)
        self.assertEqual(report.assigned_to,self.planner)

    def test_visual_data_scoped_and_nonmembers_denied(self):
        other_project=Project.objects.create(name='Other project',site_version='v1',site_data={})
        FieldReport.objects.create(project=other_project,reporter=self.other,kind='heat',description='Private other project')
        self.assertNotContains(self.client.get(self.base+'visual-data/'),'Private other project')
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(self.base+'visual-data/').status_code,404)

    def test_photo_from_sample_fixture_is_private(self):
        from django.core.management import call_command
        with tempfile.TemporaryDirectory() as folder,override_settings(MEDIA_ROOT=folder):
            image=io.BytesIO();Image.new('RGB',(20,20)).save(image,format='JPEG')
            Path(folder,'blocked-drain.jpg').write_bytes(image.getvalue())
            call_command('seed_app_reports',project=self.project.pk,photo_dir=folder,verbosity=0)
            report=FieldReport.objects.get(kind='flood')
            self.assertTrue(report.photo)
            response=self.client.get(self.base+f'reports/{report.pk}/photo/')
            self.assertEqual(response.status_code,200);response.close()
            self.client.force_login(self.other)
            self.assertEqual(self.client.get(self.base+f'reports/{report.pk}/photo/').status_code,404)

    def test_notices_are_internal_and_expire(self):
        self.client.post(self.base+'notices/new/',{'kind':'wind','title':'Notice for app handoff','message':'Path inspection pending.','hours':12})
        notice=Advisory.objects.get()
        self.assertContains(self.client.get(self.base+'view/operations/'),'Notice for app handoff')
        notice.expires_at=timezone.now()-timedelta(seconds=1);notice.save()
        self.assertNotContains(self.client.get(self.base+'view/operations/'),'Notice for app handoff')
