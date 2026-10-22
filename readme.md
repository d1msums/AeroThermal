# AeroThermal
## Township climate-resilience dashboard — full team guide

A Django B2B prototype for the Sime Darby Property hackathon, with a City of Elmina reference site. The repository/folder remains named `ecocool`; the product is AeroThermal.

**Guide updated: 22 October 2026, based on the uploaded repository snapshot.**

> **Implementation status:** The current `simulation/engine.py` is a placeholder: it returns `mode="mock"`, empty shadows and no calculated shade percentages. Some frontend panels show illustrative shade, cooling, weather and insurance figures. Do not present those as validated measurements. The resident app is a separate static demonstration, not a connected production reporting API.

## Contents

- [Features and limits](#features-and-limits)
- [First-time laptop setup](#first-time-laptop-setup)
- [Optional integrations](#optional-integrations)
- [Page-by-page walkthrough](#page-by-page-walkthrough)
- [Team Git workflow](#team-git-workflow)
- [Troubleshooting](#troubleshooting)
- [Hosting](#hosting)
- [Project structure](#project-structure)

## Features and limits

| Area | Available in this snapshot | Limit |
|---|---|---|
| Overview | Lake-storage ring, storm buffer, report counts, map and charts | Seeded lake/history data; not live telemetry |
| Map & Tree Simulator | Layout editing and save/load workflow | Real backend simulation not connected in this snapshot |
| Engineering view | Shared climate scenarios and storage-volume review | Candidate release is illustrative, not a gate command |
| Resident reports | Project-scoped inbox, map/photo inspection, assignment and status | App-style sample inputs, not production mobile intake |
| AeroThermal AI | Climate assessment, local knowledge retrieval and optional Gemini chat | Advisory prototype, not official emergency guidance |
| Resident App | Static HTML experience in `b2c_resident_app/` | Browser-local demo state and iframe messaging, not shared Django records |
| Security | Login, project membership, planner/viewer checks and private photo views | Production hardening and integration review still required |

The map township selector changes reference views; it is not proof that another township's authenticated database project has been loaded.

The checked-in weather setting is **AEROTHERMAL_LIVE_WARNINGS = True**. The adapter attempts to fetch national warning records, but static weather cards may also appear. Review the timestamp, location and actual fetch result before calling anything live.

Tree layouts are hypothetical proposals. They do not authorize tree removal, planting, development or modification of an approved township plan. Displayed insurance/policy claims require independent supporting evidence.

### This update

The Lake storage circle is centred and enlarged to up to **164 px on desktop / 132 px on smaller screens**, with a larger percentage and centred caption. SVG geometry, percentage calculations and existing behavior are unchanged. A CSS version change refreshes the cached stylesheet.

## First-time laptop setup

These instructions use **Windows PowerShell inside VS Code**. Every teammate has a separate local database. Sofea does not need to keep her laptop running for Jia to run her own copy.

### 1. Install prerequisites

Install Git, Python 3.12 and VS Code, then check:

```powershell
git --version
py -3.12 --version
```

### 2. Clone the project

```powershell
git clone https://github.com/d1msums/ecocool.git
cd ecocool
code .
```

For a private repo, use an authorized collaborator account. If already cloned, use the Git update instructions below instead. All following commands run beside `manage.py`.

### 3. Create a virtual environment and install dependencies

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

In VS Code, use **Python: Select Interpreter** and choose `.venv\Scripts\python.exe`. Activation is optional because commands explicitly use this interpreter.

Use `requirements.txt`, not the historical requirements backup. There is no required `requirements-sim-lock.txt`. If a pinned version cannot be installed, share the exact error with the team rather than silently guessing replacements.

### 4. Create .env BEFORE running Django

The settings require `DJANGO_SECRET_KEY`. If `.env` does not already exist:

```powershell
Copy-Item .env.example .env
```

Do not overwrite an existing environment file. Generate a secret:

```powershell
.\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Edit `.env` in VS Code:

```dotenv
DJANGO_SECRET_KEY='PASTE_YOUR_GENERATED_SECRET'
GOOGLE_MAPS_API_KEY=
```

Use quotes around the secret. Keep this file private. The existing settings already load it with python-dotenv. An empty Maps key is fine for initial setup; satellite imagery will be unavailable.

### 5. Create the database and your account

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Choose your own account name, such as `jia`. Password characters do not appear while typing; this is normal. Do not run `makemigrations` merely to start the cloned app.

### 6. Create the Elmina project

```powershell
.\.venv\Scripts\python.exe manage.py shell -c "exec(open('create_elmina.py', encoding='utf-8').read())"
```

The script reads `elmina/site.json` and prints your project ID. A fresh database may use 1, whereas Sofea's earlier database used 3. Use your own ID throughout.

The script stops if an existing matching project contains conflicting site data; investigate rather than deleting it.

### 7. Assign your project membership

Even a superuser needs a membership for the B2B pages.

```powershell
.\.venv\Scripts\python.exe manage.py shell
```

Paste the following, replacing `jia` with your username:

```python
from django.contrib.auth import get_user_model
from planner.models import Project, Membership

user = get_user_model().objects.get(username="jia")
project = Project.objects.get(name="Elmina Valley Central Park - Map Pilot")
membership, created = Membership.objects.update_or_create(
    project=project,
    user=user,
    defaults={"role": "planner"},
)
print("Project ID:", project.pk)
print("Role:", membership.role)
exit()
```

Use `viewer` for read-only membership. For judges/teammates on a shared server, create ordinary users via admin and assign project roles; do not make everyone a superuser.

### 8. Load demonstration data

Replace 1 with your printed project ID:

```powershell
.\.venv\Scripts\python.exe manage.py seed_resilience --project 1
.\.venv\Scripts\python.exe manage.py seed_app_reports --project 1
```

These create demo climate state and sample app-style reports. Existing fixture records and work status are preserved on reruns; these commands are not a reset.

To attach approved sample photos you own:

```powershell
.\.venv\Scripts\python.exe manage.py seed_app_reports --project 1 --photo-dir "C:\path\to\demo-photos"
```

Expected names: `blocked-drain.jpg`, `fallen-branch.jpg`, `dry-vegetation.jpg`, `heat-exposure.jpg`. Without photos, labelled illustrations may appear. GPS/location is a separate field, not inferred from photo EXIF.

### 9. Check and start Django

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Open **http://127.0.0.1:8000/**, log in and select your project. Keep the terminal running; stop with **Ctrl+C**.

Do not rerun historical `install_*.py` scripts during normal startup: the merged repository already contains installed UI changes.

### 10. Start again another day

```powershell
cd C:\path\to\ecocool
.\.venv\Scripts\python.exe manage.py runserver
```

Do not recreate users, projects or the environment each time.

## Optional integrations

### Google Maps

Put your restricted browser key in `.env` under `GOOGLE_MAPS_API_KEY` and restart Django. Configure Maps JavaScript API access, billing and allowed referrers:

```text
http://127.0.0.1:8000/*
http://localhost:8000/*
```

A browser key is visible in browser requests, so API and website restrictions remain necessary. Check **F12 → Console** for the actual error if satellite imagery fails. A rejected key does not necessarily mean its quota is exhausted. The vector reference remains available.

### Weather

The current settings enable official warning retrieval. For an offline demo, change the existing setting to:

```python
AEROTHERMAL_LIVE_WARNINGS = False
```

An empty, stale, disabled or failed feed is not an all-clear. National records require date/location review before being applied to Elmina. Static example cards may remain visible without a successful live fetch.

### Gemini / advisory chat

Optionally add a private server-side key to `.env`:

```dotenv
GEMINI_API_KEY='YOUR_PRIVATE_MODEL_KEY'
```

Restart Django. The handler also supports GOOGLE_API_KEY, optional Google SDK usage and a REST fallback. Without a working model connection, inspect the local response/fallback indicators rather than claiming Gemini answered.

This is a different key from the Maps browser key. Review what context is sent to the external provider, avoid real resident personal data in demo inputs, and configure usage limits. Generated advice and the local knowledge corpus require verification.

### Resident-app demonstration

In a **second terminal**, from the repo root:

```powershell
.\.venv\Scripts\python.exe -m http.server 8080 --bind 127.0.0.1 --directory b2c_resident_app
```

Open **http://127.0.0.1:8080/** or click **Resident App ↗**. Keep Django running separately on port 8000.

The app's return link currently points to B2B project 1. Edit that link in `b2c_resident_app/index.html` if your project ID differs.

Browser-local demo state and iframe messages do not submit reports to Django. The backend web-report creation endpoint is retired. Use seeded reports for this demonstration; see [the future app handoff](docs/RESIDENT_APP_HANDOFF.md).

## Page-by-page walkthrough

All paths below are appended to `http://127.0.0.1:8000`; replace project 1 as needed.

| Current page | Path | Intended use |
|---|---|---|
| Project list | `/` | Select an assigned project |
| Overview | `/projects/1/resilience/` | Leadership/ESG summary |
| Map & Tree Simulator | `/projects/1/` | Hypothetical layout planning |
| Engineering view | `/projects/1/resilience/view/engineer/` | Storage/scenario review; direct route remains available |
| Resident reports | `/projects/1/resilience/view/operations/` | Staff inbox and follow-up |
| AeroThermal AI | `/projects/1/resilience/alerts/` | Climate assessment and advisory chat |
| Administration | `/admin/` | Authorized account/membership management |

### Overview

1. Start here and read Demo/Calculated/source labels.
2. Read the lake ring: 65% means 65% of configured storage is occupied, not a 65% flood probability.
3. Compare the available storm buffer. It is volume arithmetic, not proof the site is flood-safe.
4. Click a report pin/card to inspect its attachment, location and status.
5. Use **Locate on map** or **Open work item**.
6. Review charts and saved evidence; missing calculations must not be replaced with claimed measured results.
7. The township selector explores map references, not independent authenticated project datasets.

### Map & Tree Simulator

1. Open the combined tab, explore the reference geometry and proposed-tree controls.
2. Adjust a hypothetical layout and use the calculate action.
3. This backend snapshot returns a placeholder response. Any static preview shade/cooling figures are illustrative.
4. Use available save/load controls for layout workflow, not as evidence of a validated scientific result.
5. Jia's integration point is `simulation.engine.simulate(payload)`; preserve schema, units, provenance and missing-data behavior.

### Engineering view

1. Open its direct route or the overview engineering link.
2. As a planner, select a scenario and click **Apply scenario**.
3. Review stored volume, assumed inflow, available buffer and candidate release.
4. Read downstream/hold conditions. No physical gate is controlled.
5. Coordinate with teammates: this changes shared project state, not a private per-user preview.

### Resident reports

1. Filter/search the inbox using the available category/status/location controls.
2. Select a card/pin and inspect photo, coordinates and source.
3. Open the work item.
4. As a planner, assign staff, update status, add a note and save.
5. Refresh Overview to demonstrate updated counts.
6. Viewers can read but cannot perform planner-only changes.

Use only sample cases during presentations. A staff status change does not prove a mobile push notification was delivered.

### AeroThermal AI

1. Review flood, heat, dry-condition and wind evidence.
2. Check timestamps, source labels, missing inputs and unavailable states.
3. Ask a project-related question and inspect its answer/evidence.
4. Explain that staff must review suggested actions. The prototype does not issue official emergency orders.
5. Do not infer an El Niño declaration from one dry reading or a temperature reduction from shade coverage alone.

### Five-minute demonstration

| Time | Show | Explain |
|---|---|---|
| 0:00–0:40 | Overview and lake circle | Visual township condition summary |
| 0:40–1:30 | Report pin → inspector | Location-linked resident-style evidence |
| 1:30–2:15 | Work item/status change | Project-scoped operational follow-up |
| 2:15–3:05 | Engineering scenario | Illustrative storage balance, not automatic discharge |
| 3:05–3:50 | Tree layout | Planning workflow; disclose placeholder calculation |
| 3:50–4:35 | Climate/AI page | Advisory evidence, not autonomous safety decisions |
| 4:35–5:00 | Viewer account / wrap-up | Access boundaries and remaining integration work |

## Team Git workflow

### Pull your friend's merged updates

Stop Django and inspect:

```powershell
git status
git branch --show-current
git remote -v
```

Commit intended safe changes or temporarily preserve uncommitted files:

```powershell
git stash push -u -m "Before pulling team update"
```

Ignored databases/.env are not in the stash; back up important local data outside the repo.

```powershell
git switch main
git pull --ff-only origin main
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

If needed, restore with `git stash apply` and resolve overlaps carefully. On divergent branches, stop and coordinate; do not force-push, hard-reset or discard teammate work.

### Submit this UI/documentation update

```powershell
git switch -c sofea/lake-gauge-readme
git status
git diff
git add readme.md README_AEROTHERMAL.md docs/RENDER_DEPLOYMENT.md resilience/static/resilience/hallmark/ui.css resilience/templates/resilience/base.html resilience/templates/resilience/kpis.html
git diff --cached
git commit -m "Enlarge lake gauge and refresh AeroThermal guide"
git push -u origin sofea/lake-gauge-readme
```

Use an unused branch name, open a pull request to main and ask the team to review. Never commit .env, private uploads, SQLite databases or .venv.

Git shares code, not local users, photos, database records or saved scenarios.

### Checks before merging

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test planner resilience
```

Also manually test authentication, nonmember denial, viewer restrictions, scenario changes, private photo access, map fallback, AI error states and responsive layout. The existence of these commands is not a claim that the entire merged project is validated.

## Troubleshooting

| Symptom | Action |
|---|---|
| KeyError DJANGO_SECRET_KEY | Create .env beside manage.py and set a private secret |
| Module not found | Use the project's .venv Python and install committed requirements |
| Pinned package not available | Review exact version/Python compatibility with the team |
| TemplateDoesNotExist | Check the full app/template path; retain APP_DIRS=True |
| No project assigned / 404 | Assign membership and use the actual project ID |
| Old small circle remains | Copy all three UI files, restart and Ctrl+F5; check CSS version |
| Map key rejected | Inspect console, API permissions, billing and allowed referrers |
| Simulation not connected / missing shade | Current engine is a placeholder; Jia must connect real calculations |
| Resident App link fails | Start its separate localhost:8080 server |
| Mobile report does not reach B2B | No production intake API exists; seed demonstration records |
| 403 on an edit | Check planner role, session and CSRF; do not disable protection |
| Photos missing on another laptop | Private uploads are not in Git; seed approved local images |
| Weather unavailable | Check settings/network; failure is not an all-clear |
| landscape_urls missing after revert | Check for mixed versions; do not reinstall obsolete landscape updates |

## Hosting

Read [the complete Render preparation/deployment guide](docs/RENDER_DEPLOYMENT.md).

This snapshot is **not ready to deploy unchanged**: DEBUG is enabled, ALLOWED_HOSTS is empty, storage is SQLite-only, production static/media configuration is absent and app links use localhost. This UI update does not silently alter deployment settings.

Before public presentation, review hard-coded example weather, cooling, insurance, "Live App", dispatch and notification claims. UI labels/toasts alone do not establish real integrations.

## Project structure

| Path | Purpose |
|---|---|
| config/ | Settings and root routing |
| planner/ | Projects, memberships, tree UI, scenario persistence and audit |
| simulation/engine.py | Jia's engine integration point, currently placeholder |
| contracts/ | Payload examples/contracts |
| resilience/ | B2B metrics, reports, scenarios, climate assessment and AI |
| resilience/knowledge/ | Retrieval corpus; independently verify sources |
| b2c_resident_app/ | Resident-team static demo |
| elmina/site.json | Reference geometry |
| create_elmina.py | Non-overwriting project bootstrap |
| docs/ | Integration and deployment guides |
| requirements.txt | Main dependency pins |
| .env.example | Environment names, no real secrets |
| install_*.py | Historical upgrade scripts, not normal startup |

Sofea: B2B UI/GIS presentation, security integration and documentation.
Jia/Jiah: calculation implementation and validated outputs.
Resident-app teammates: resident UI/capture and future authenticated report integration.

Agree on payload schema, units, source timestamps, missing-data handling and access boundaries before merging. Keep illustrative and calculated outputs distinct.

