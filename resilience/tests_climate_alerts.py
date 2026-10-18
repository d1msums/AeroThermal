from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone
from planner.models import Project, Membership
from .models import ClimateState, FieldReport, StakeholderAccess, Advisory
from .climate_alerts import build_alerts

class ClimateAlertTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('planner',password='test-pass')
        self.viewer=User.objects.create_user('viewer',password='test-pass')
        self.project=Project.objects.create(name='Pilot',site_version='v1',site_data={})
        Membership.objects.create(project=self.project,user=self.user,role='planner')
        Membership.objects.create(project=self.project,user=self.viewer,role='viewer')
        self.state=ClimateState.objects.create(project=self.project)
        self.url=f'/projects/{self.project.pk}/resilience/alerts/'
        self.client.force_login(self.user)
    def card(self,kind):return next(c for c in build_alerts(self.project)['cards'] if c['kind']==kind)
    def test_storm_calculation_and_hold(self):
        self.client.post(self.url+'scenario/',{'scenario':'storm'})
        flood=self.card('flood');self.assertEqual(flood['level'],2)
        self.assertIn('5,000',flood['reason']);self.assertTrue(any('HOLD' in e for e in flood['evidence']))
        self.assertEqual(build_alerts(self.project)['metrics']['candidate_m3'],10000)
    def test_reserve_and_no_elnino_inference(self):
        self.client.post(self.url+'scenario/',{'scenario':'drought'})
        drought=self.card('drought');self.assertEqual(drought['level'],2);self.assertIn('5,000',drought['reason'])
        self.assertIn('El Niño outlook are not connected',drought['gaps'][0])
    def test_reports_resolve_and_other_projects_are_excluded(self):
        r=FieldReport.objects.create(project=self.project,reporter=self.user,kind='heat',description='Exposure')
        other=Project.objects.create(name='Private',site_version='v1',site_data={})
        FieldReport.objects.create(project=other,reporter=self.user,kind='flood',description='OTHER_PRIVATE')
        self.assertEqual(self.card('heat')['level'],1);self.assertEqual(self.card('flood')['reports'],0)
        r.status='resolved';r.save();self.assertEqual(self.card('heat')['level'],0)
        self.assertNotContains(self.client.get(self.url),'OTHER_PRIVATE')
    def test_missing_heat_does_not_claim_safe(self):
        heat=self.card('heat');self.assertEqual(heat['status'],'Data needed');self.assertEqual(heat['metric'],'—')
    def test_stale_real_reading_cannot_trigger_current_storage_assessment(self):
        self.state.scenario='storm';self.state.assumed_inflow_m3=40000;self.state.is_demo=False;self.state.save()
        ClimateState.objects.filter(pk=self.state.pk).update(updated_at=timezone.now()-timedelta(hours=3))
        self.assertEqual(self.card('flood')['level'],0);self.assertIn('stale',self.card('flood')['reason'])
    def test_invalid_lake_inputs_and_missing_state_do_not_crash(self):
        self.state.capacity_m3=0;self.state.save();self.assertEqual(self.client.get(self.url).status_code,200)
        self.assertEqual(self.card('flood')['status'],'Data needed')
        self.state.delete();self.assertEqual(self.client.get(self.url).status_code,200)
    def test_advisory_expiry_and_escaping(self):
        n=Advisory.objects.create(project=self.project,kind='heat',title='<script>unsafe()</script>',message='Review',created_by=self.user,expires_at=timezone.now()+timedelta(hours=1))
        self.assertEqual(self.card('heat')['level'],1)
        self.assertNotContains(self.client.get(self.url),'<script>unsafe()</script>')
        n.expires_at=timezone.now()-timedelta(seconds=1);n.save();self.assertEqual(self.card('heat')['level'],0)
    def test_viewer_read_and_no_scenario_write(self):
        self.client.force_login(self.viewer);self.assertEqual(self.client.get(self.url).status_code,200)
        self.assertEqual(self.client.post(self.url+'scenario/',{'scenario':'storm'}).status_code,403)
    def test_login_membership_and_resident_boundary(self):
        self.client.logout();self.assertEqual(self.client.get(self.url).status_code,302)
        outsider=User.objects.create_user('outsider');self.client.force_login(outsider)
        self.assertEqual(self.client.get(self.url).status_code,404)
        m=Membership.objects.get(user=self.viewer,project=self.project);StakeholderAccess.objects.create(membership=m,resident_only=True)
        self.client.force_login(self.viewer);self.assertIn(self.client.get(self.url).status_code,[403,404])
    def test_csrf_and_scenario_return(self):
        client=Client(enforce_csrf_checks=True);client.force_login(self.user)
        self.assertEqual(client.post(self.url+'scenario/',{'scenario':'storm'}).status_code,403)
        self.assertRedirects(self.client.post(self.url+'scenario/',{'scenario':'heat'}),self.url)
        self.assertEqual(self.client.post(self.url+'scenario/',{'scenario':'invalid'}).status_code,400)
    def test_counts_cover_reports_outside_map_limit(self):
        FieldReport.objects.bulk_create([FieldReport(project=self.project,reporter=self.user,kind='flood',description='Report') for _ in range(501)])
        data=build_alerts(self.project);self.assertEqual(data['active_count'],501)
        self.assertEqual(data['cards'][0]['reports'],501);self.assertEqual(len(data['visual_data']['reports']),500)
