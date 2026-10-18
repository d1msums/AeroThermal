# AeroThermal Visual B2B Update

Sofea/Jia own this B2B website. The other teammates own the B2C mobile app. This update receives dummy app reports; it does not build resident-facing website screens.

## What changed

- Overview: four KPIs, report map, short inbox cards, storage trend, report-status donut and saved shade bars.
- Map & planning: shared scenario, map layers, report inspector and graphical storm-storage balance.
- Resident reports: B2B inbox with category/status/search filters synchronized with pins, plus assignment, review and activity history.
- Tree simulator: existing placement/editing, neon rings, simulation and save/history logic retained; lake planning is in Map & planning. Long model/source notes are collapsed.
- The old Resident demo navigation and web submission flow are retired. No website rewards are issued. Legacy points remain in existing records.
- Long explanations move to Data notes. Sample data labels remain visible.

## Install

Stop Django and back up the project/database outside the project folder. Save your current work on a branch such as sofea-visual-b2b. Extract this ZIP separately, then copy resilience/ into your project root beside manage.py, replacing older app files. Copy install_visual_b2b.py, requirements-resilience.txt, README_AEROTHERMAL.md and docs/ there too. Keep planner/, simulation/, .env and your database.

If the prior resilience app was already installed, keep its settings and URL include. This update has no additional model/schema changes. Run from the folder containing manage.py:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-resilience.txt
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_resilience --project 3
.\.venv\Scripts\python.exe manage.py seed_app_reports --project 3
.\.venv\Scripts\python.exe install_visual_b2b.py
.\.venv\Scripts\python.exe manage.py test resilience
.\.venv\Scripts\python.exe manage.py runserver
```

Replace 3 with the actual project ID if different. Migrate applies existing add-on migrations if needed; do not generate new migrations just for this update.

Open http://127.0.0.1:8000/projects/3/resilience/ and Ctrl+F5. Start the B2B presentation here, rather than the old tree-designer URL. The designer remains /projects/3/ and links to the workspace.

The installer backs up the designer template under visual_backups/, inserts the new navigation and presentation assets, and preserves existing IDs. Repeating it reports already installed. Failed anchor checks stop before mutation.

Keep APP_DIRS=True, django.contrib.staticfiles, and the existing Google map context processor. The logo uses the existing planner/static/planner/images/sdp-logo.png. Google imagery needs your own configured key and internet; vector fallback remains available.

## First install only

If you never installed the stakeholder app, add these entries to the existing lists in settings.py:

```python
# INSTALLED_APPS
"resilience.apps.ResilienceConfig",

# MIDDLEWARE, immediately after AuthenticationMiddleware
"resilience.middleware.ResidentBoundaryMiddleware",
```

Use private photo storage. Add this only if no MEDIA_ROOT exists:

```python
MEDIA_ROOT = BASE_DIR / "private_media"
```

Do not expose private_media via a public media/static route. Existing public upload storage needs a private configuration for report photos before using this feature.

In root urls.py, import include, and add this before catch-all routes:

```python
from django.urls import path, include
# Inside existing urlpatterns:
path("", include("resilience.urls")),
```

Keep existing admin/accounts/planner URLs. The map URL name is expected to be dashboard. If different, update that name in the new templates. The included initial migration depends on planner/0001_initial from the earlier project; review the dependency if your migration history differs.

## Dummy incoming reports

seed_app_reports creates four examples once:

| Reference | Type | Initial status |
| --- | --- | --- |
| APP-DEMO-101 | Blocked drain | New |
| APP-DEMO-102 | Fallen branch | In progress |
| APP-DEMO-103 | Dry vegetation | New |
| APP-DEMO-104 | Heat exposure | Resolved |

Three active cases appear initially; All shows four. Existing reports can increase counts. The seed uses an inactive fixture account with no login. It preserves existing reports and work status; repeated runs do not duplicate cases. Positions are sample points from the project's route, not actual resident GPS evidence.

Default attachments are labelled SVG illustrations, not photographs. Actual stored report photos use the same thumbnail/inspector layout.

## Add your own sample photos

Put appropriate photos you own in a folder, named:

```text
blocked-drain.jpg
fallen-branch.jpg
dry-vegetation.jpg
heat-exposure.jpg
```

Then run:

```powershell
.\.venv\Scripts\python.exe manage.py seed_app_reports --project 3 --photo-dir "C:\Users\sofea\demo-report-photos"
```

Only missing fixture photos are attached; existing images are preserved. They are validated/resized/re-encoded, stripping EXIF. Maximum input is 5 MB and 20 megapixels. Photos are private to authenticated project access.

The app must supply report coordinates separately. The web does not infer GPS from an image.

## Demonstrate

1. Overview: show storage, buffer, active reports and latest calculated shade.
2. Click a report card or matching pin. The inspector shows attachment, location, status and assignment.
3. Locate on map zooms to the point. Open work item opens the review form.
4. As a planner, assign to yourself, set In progress, add a note and save. Later resolve/verify. Refresh Overview to show updated counts and donut.
5. In Resident reports, filter by status/category and search locations. Pins and list update together.
6. Map & planning: apply Heavy rain. Review candidate release and graphical volume balance; no gate command is available.
7. Tree simulator: run/save using the existing engine; return to Overview for real saved shade bars.

If no shade run exists, the chart correctly shows an empty state. No fake calculated shade results are seeded. Latest KPI uses the current site version. Saved chart bars retain their individual timestamps/site versions; compare equal times/versions for A/B claims.

## Permissions and app boundary

Internal viewers can read the three B2B views. Planners can update scenarios, work items and internal notices. Resident-only memberships cannot enter this website; do not use resident_demo for B2B presentation. Old resident form URLs no longer accept submissions.

The mobile team owns resident screens, upload/GPS capture, comfort/navigation and rewards. This ZIP supplies a dummy incoming feed, not a production app API, push connection or reward service. See docs/RESIDENT_APP_HANDOFF.md.

## Data notes

Lake scenarios, history and hotspot examples are demonstration inputs. History is a fixed reference sequence, not live telemetry. Sample hotspot circles are off by default and do not affect shade calculations. No calibrated cooling, flood-safety probability, energy or avoided-loss figure is invented.

Optional official warnings remain available on Map & planning when AEROTHERMAL_LIVE_WARNINGS=True is configured. Location relevance needs review; these records are not an Elmina-specific 12-hour radar forecast and do not trigger a release.

## Git and Jia

Ignore .env, .venv, databases, private_media/, stakeholder_backups/ and visual_backups/ (and your actual private MEDIA_ROOT if different). Stage resilience/, install_visual_b2b.py, requirements-resilience.txt, docs/ and the changed dashboard template. Include first-install settings/URL changes by actual path, review the staged diff and push the agreed branch.

Jia installs dependencies, runs migrate and seeds her local project. Git does not transfer local reports/photos/users/scenarios. Do not overwrite her engine code.

## Verification

The updated backend suite passed 16 tests in a separate Django 5.2.18 fixture: boundaries, retired web submission, fixture idempotence, image privacy, scenario arithmetic, concurrent report versions, CSV escaping, no B2C reward awards and weather failures. Browser checks passed all three B2B pages, filters, pin/list inspection, attachment display, location focus, work-item updates, Data notes and mobile width. The existing designer also passed example loading, tree selection, dimension editing and neon selection checks. Its 31 original template IDs were preserved, and the installer was tested twice for idempotence. The Windows folder and live repository were not edited or certified. The unchanged scientific engine is not revalidated by visual tests.
