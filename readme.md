<div align="center">

# 🌿 AeroThermal SDP
### Township Climate Resilience & Planning Dashboard

**A visual B2B workspace for township leadership, ESG teams, engineers and planners.**

*Sime Darby Property University Hackathon 2026*

![Platform](https://img.shields.io/badge/Platform-B2B_Web_Dashboard-263D2D?style=for-the-badge)
![Framework](https://img.shields.io/badge/Framework-Django-0C4B33?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Climate_Resilience-A3E635?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Hosted_Prototype-38BDF8?style=for-the-badge)

### [🚀 Open AeroThermal](https://aerothermal.onrender.com/)

[Features](#features) · [Dashboard Guide](#dashboard-guide) · [Local Setup](#local-setup) · [Render Deployment](#render-deployment) · [Troubleshooting](#troubleshooting)

**Flood preparedness · Heat exposure · Dry conditions · Resident reports**

</div>

---

## About

AeroThermal combines lake-storage information, geographic context, resident-style reports and planning tools in one dashboard.

It helps township teams review:

- Available lake capacity before an assumed storm.
- Reported drainage, vegetation and heat-related concerns.
- Report locations, attachments and operational follow-up.
- Hypothetical tree-planting layouts.
- Climate evidence and advisory responses.

**City of Elmina** is the primary reference project used by the setup instructions. Additional township views support geographic exploration.

The repository also includes a separate **EcoCool Resident Companion** demonstration.

> AeroThermal is a prototype. Demonstration inputs, illustrative previews and connected data sources have different levels of completeness. See [Current Implementation Scope](#current-implementation-scope).

## Hosted Access

Open:

**https://aerothermal.onrender.com/**

1. Sign in with an account created in the hosted database.
2. Select a project assigned to that account.
3. Open the B2B workspace.

Access requires both a valid account and project membership. Local laptop accounts do not automatically exist on the hosted website.

The application runs on Render’s free web-service tier. After inactivity, the first request may take longer while the service starts.

## Features

| Feature | Purpose |
|---|---|
| Township overview | Review headline metrics, maps and charts |
| Lake-storage indicator | See stored water as a percentage of configured capacity |
| Storm buffer | Review remaining storage volume |
| Engineering scenarios | Explore assumed inflow and storage conditions |
| Geographic map | Locate reports and reference planning features |
| Resident-report inbox | Inspect, assign and update project reports |
| Map & Tree Simulator | Explore and save hypothetical proposed-tree layouts |
| AeroThermal AI | Review climate evidence and ask contextual questions |
| Project access controls | Separate viewer and planner capabilities |

### Lake Storage and Storm Buffer

The lake card displays the percentage of configured capacity currently occupied.

For example:

| Metric | Demonstration value |
|---|---:|
| Total capacity | 100,000 m³ |
| Stored water | 65,000 m³ |
| Lake storage | 65% |
| Available buffer | 35,000 m³ |

Storage percentage is not flood probability. Available capacity alone does not establish that a site is safe during a storm.

### Engineering Scenarios

The engineering view supports:

- Applying available demonstration scenarios.
- Comparing stored volume and assumed inflow.
- Reviewing remaining capacity.
- Inspecting an illustrative candidate release volume.
- Reviewing downstream hold conditions.

Applying a scenario changes shared project state. The prototype does not operate physical gates.

### Resident Reports

The B2B inbox provides:

- Report categories and locations.
- Available image attachments.
- Status and search filters.
- Map inspection.
- Staff assignment.
- Review notes and status updates.

Current demonstration inputs are seeded app-style records. Production mobile report intake is not connected in the inspected repository snapshot.

### Map & Tree Simulator

The planning interface supports proposed-tree editing and layout persistence.

The checked-in backend engine in `simulation/engine.py` is currently a placeholder. It returns mock-mode output without calculated shade percentages.

Example shade and cooling figures in interface previews are illustrative until a validated calculation engine is integrated.

### AeroThermal AI

The advisory page combines climate assessment with local knowledge retrieval and an optional Gemini connection.

Responses support staff review. They do not replace official warnings or engineering approval.

## Dashboard Guide

After login, use your assigned project. Project IDs can differ between installations.

### 1. Overview

Use this page to understand the project before opening individual tools.

1. Review the lake-storage ring.
2. Compare stored volume and storm buffer.
3. Check active report counts.
4. Explore the map and available charts.
5. Click a report marker or card.
6. Use the information buttons for metric explanations.

Read data labels and timestamps when interpreting results.

### 2. Report Inspector

Use this feature to understand an individual issue.

1. Select a report marker or card.
2. Review its category, location, attachment and status.
3. Choose **Locate on map** to focus on the location.
4. Choose **Open work item** to review the operational record.

Some attachments are labelled demonstration illustrations.

### 3. Resident Reports

Use this page to organize follow-up.

1. Open **Resident reports**.
2. Filter or search the inbox.
3. Open a report.
4. With planner access, assign staff and update its status.
5. Add a note and save.
6. Refresh Overview to see updated counts.

A saved staff update does not establish that a mobile notification was delivered.

### 4. Engineering View

Use this page to explore storm-storage assumptions.

1. Open the engineering link or its direct route.
2. Select a scenario.
3. Click **Apply scenario**.
4. Review stored volume, assumed inflow and available buffer.
5. Inspect candidate release and hold conditions.

Coordinate scenario changes when multiple users share a project.

### 5. Map & Tree Simulator

Use this page to explore hypothetical layouts.

1. Open **Map & Tree Simulator**.
2. Explore the reference map.
3. Add or select proposed trees using the available controls.
4. Adjust their dimensions or positions.
5. Inspect the current calculation response.
6. Use the available save/load controls.

The backend currently returns placeholder results. Proposed layouts do not authorize changes to existing trees or approved plans.

### 6. AeroThermal AI

Use this page to review evidence and ask questions.

1. Review flood, heat, dry-condition and wind information.
2. Check source indicators and timestamps.
3. Identify unavailable inputs.
4. Ask a project-related question.
5. Review the response and supporting material.

Example questions:

- “What should be reviewed before considering a lake release?”
- “Which reports need attention during heavy rainfall?”
- “What information is missing from this heat assessment?”

### Page Routes

Replace `PROJECT_ID` with the assigned project’s ID.

| Page | Route |
|---|---|
| Project list | `/` |
| Login | `/accounts/login/` |
| Overview | `/projects/PROJECT_ID/resilience/` |
| Map & Tree Simulator | `/projects/PROJECT_ID/` |
| Engineering view | `/projects/PROJECT_ID/resilience/view/engineer/` |
| Resident reports | `/projects/PROJECT_ID/resilience/view/operations/` |
| AeroThermal AI | `/projects/PROJECT_ID/resilience/alerts/` |
| Administration | `/admin/` |

Append these paths to either the hosted address or `http://127.0.0.1:8000`.

## Local Setup

These instructions use Windows PowerShell inside VS Code.

### 1. Install prerequisites

Install Python 3.12, Git and VS Code.

```powershell
py -3.12 --version
git --version
```

### 2. Clone the repository

```powershell
git clone https://github.com/d1msums/ecocool.git
cd ecocool
code .
```

Run subsequent commands from the folder containing `manage.py`.

### 3. Create the environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Select `.venv\Scripts\python.exe` as the VS Code Python interpreter.

### 4. Configure local secrets

If `.env` does not already exist:

```powershell
Copy-Item .env.example .env
```

Generate a secret:

```powershell
.\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Edit `.env`:

```dotenv
DJANGO_SECRET_KEY='PASTE_YOUR_GENERATED_SECRET'
GOOGLE_MAPS_API_KEY=
```

Optional external AI configuration:

```dotenv
GEMINI_API_KEY='YOUR_PRIVATE_MODEL_KEY'
```

Do not overwrite an existing `.env` or commit real secrets.

For normal local development, leave `DATABASE_URL` unset so the project uses local SQLite.

### 5. Create tables and an account

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Choose your own credentials. Password characters are hidden while typing.

### 6. Create the reference project

```powershell
.\.venv\Scripts\python.exe manage.py shell -c "exec(open('create_elmina.py', encoding='utf-8').read())"
```

The script prints the project ID. It preserves matching existing project data and stops if conflicting site data is found.

### 7. Assign membership and seed demo data

Open Django’s shell:

```powershell
.\.venv\Scripts\python.exe manage.py shell
```

Replace `YOUR_USERNAME`, then paste:

```python
from django.contrib.auth import get_user_model
from django.core.management import call_command
from planner.models import Project, Membership

user = get_user_model().objects.get(username="YOUR_USERNAME")

project = Project.objects.get(
    name="Elmina Valley Central Park - Map Pilot"
)

Membership.objects.update_or_create(
    project=project,
    user=user,
    defaults={"role": "planner"},
)

call_command("seed_resilience", project=project.pk)
call_command("seed_app_reports", project=project.pk)

print("Project ID:", project.pk)
print("Dashboard path:", f"/projects/{project.pk}/resilience/")

exit()
```

Use `"viewer"` for read-only membership. Even an administrator needs project membership for the B2B pages.

### 8. Start the dashboard

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Stop the server with **Ctrl+C**.

Historical `install_*.py` scripts are not part of normal startup.

## Resident Companion Demo

Open a second terminal from the repository root:

```powershell
.\.venv\Scripts\python.exe -m http.server 8080 --bind 127.0.0.1 --directory b2c_resident_app
```

Visit:

```text
http://127.0.0.1:8080/
```

Django continues running separately on port `8000`.

The resident demonstration uses browser-local state and iframe messaging. It does not currently submit corresponding reports to Django.

The repository’s companion links originally point to localhost. For hosted use, configure the actual hosted companion URL and the correct B2B project URL. A localhost link points to the visitor’s own computer.

## Database Configuration

The project selects PostgreSQL when `DATABASE_URL` is set and SQLite otherwise.

In `config/settings.py`, ensure this database selection is outside any Render-only or DEBUG-only condition:

```python
database_url = os.environ.get("DATABASE_URL", "").strip()

if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
```

Required imports:

```python
import os
import dj_database_url
```

Keep one database-selection block. A later `DATABASES` assignment can override the intended connection.

## Render Deployment

The hosted prototype uses a Render Python web service and PostgreSQL.

### Service settings

| Setting | Value |
|---|---|
| Root Directory | Leave blank |
| Build Command | `bash build.sh` |
| Pre-deploy Command | Leave blank on the free plan |
| Start Command | See below |

Start command:

```bash
python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

This applies migrations against the runtime database before starting Django.

Create `build.sh` beside `manage.py`, using LF line endings:

```bash
#!/usr/bin/env bash
set -o errexit

python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
```

The start command handles migrations. If an older build script also runs migrations, completed migrations are tracked and will not be reapplied.

### Required hosting packages

Ensure `requirements.txt` includes:

- `gunicorn`
- `whitenoise`
- `dj-database-url`
- `psycopg2-binary`

Preserve the project’s other dependencies.

### Render environment variables

| Key | Purpose |
|---|---|
| `PYTHON_VERSION` | Tested Python version, currently 3.12.10 |
| `DJANGO_SECRET_KEY` | Private production secret |
| `DJANGO_DEBUG` | Set to `False` |
| `DATABASE_URL` | Internal URL of the connected Render PostgreSQL database |
| `GOOGLE_MAPS_API_KEY` | Optional restricted Maps browser key |
| `GEMINI_API_KEY` | Optional private model key |

Keep the web service and database in the same region when using the internal database URL.

### Host and HTTPS settings

The deployed domain must be allowed in `config/settings.py`.

```python
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

DEBUG = os.environ.get(
    "DJANGO_DEBUG",
    "False" if render_hostname else "True",
).lower() == "true"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "aerothermal.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://aerothermal.onrender.com",
]

if render_hostname:
    if render_hostname not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(render_hostname)

    render_origin = f"https://{render_hostname}"
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

Update existing definitions instead of adding conflicting duplicates.

### Static files

Place WhiteNoise immediately after Django’s SecurityMiddleware, retaining the remaining middleware:

```python
"django.middleware.security.SecurityMiddleware",
"whitenoise.middleware.WhiteNoiseMiddleware",
```

Configure:

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

Preserve any separately configured cloud-upload backend.

Run locally before pushing:

```powershell
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

Commit source assets under the app’s static directories. Do not commit the generated `staticfiles/` directory.

### Free-plan storage considerations

Render’s free web-service filesystem is temporary. Uploaded files are not durable across service replacement or redeployment.

PostgreSQL stores database records separately. Durable uploaded photos require an appropriate external storage service or a hosting setup with persistent storage.

Check the database plan’s expiry date and current limits before scheduling a demonstration.

## Hosted Account Setup Without Render Shell

Render’s free web service does not provide dashboard Shell access. Use your laptop to connect temporarily to the hosted PostgreSQL database.

### 1. Obtain the correct connection URL

Open the PostgreSQL database in Render:

**Info → Connections → External Database URL**

Use the database connected to the web service. Keep the URL private.

### 2. Set the temporary connection

In a new VS Code PowerShell terminal, from the project root:

```powershell
$renderDatabaseSecret = Read-Host "Paste Render External Database URL" -AsSecureString

$env:DATABASE_URL = [System.Net.NetworkCredential]::new(
    "",
    $renderDatabaseSecret
).Password

$env:PGSSLMODE = "require"

Remove-Variable renderDatabaseSecret
```

The URL is entered through a hidden prompt.

### 3. Verify the target

```powershell
.\.venv\Scripts\python.exe manage.py shell -c "from django.db import connection; print('Database backend:', connection.vendor); connection.ensure_connection(); print('Connection successful')"
```

Expected:

```text
Database backend: postgresql
Connection successful
```

If it says `sqlite`, stop and check the database configuration and environment variable.

### 4. Create hosted tables and account

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
```

If the account already exists and its password needs changing:

```powershell
.\.venv\Scripts\python.exe manage.py changepassword YOUR_USERNAME
```

### 5. Create the project and membership

While the same terminal remains connected to PostgreSQL, repeat **Local Setup steps 6 and 7**.

Those commands now create the project, membership and sample data in the hosted database.

Do not use a local photo directory when seeding hosted reports through this connection: the files would be saved on the laptop, where the hosted server cannot read them.

### 6. Disconnect the terminal

```powershell
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
Remove-Item Env:PGSSLMODE -ErrorAction SilentlyContinue
```

Close the terminal.

Visit the hosted website and log in. Database changes take effect without a redeployment.

## Maps and Optional Integrations

### Google Maps

Configure Maps JavaScript API access and permitted website referrers for the browser key.

Example referrers:

```text
http://127.0.0.1:8000/*
http://localhost:8000/*
https://aerothermal.onrender.com/*
```

Use browser Developer Tools → Console to inspect the exact error when imagery fails.

### Weather

Warning retrieval is controlled by:

```python
AEROTHERMAL_LIVE_WARNINGS = True
```

Set it to `False` for an offline demonstration.

Retrieved national bulletins require date and location review. Static example panels may remain visible without a successful live retrieval.

### AI

Configure `GEMINI_API_KEY` privately to enable the optional external-model path.

Check response source indicators and review any project context sent to the provider. The Maps key and model key serve different purposes.

## Logging and Troubleshooting

Keep production `DEBUG=False`.

To send Django request failures to Render logs, configure the following if no logging configuration exists:

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
```

If `LOGGING` already exists, merge the relevant entries.

| Symptom | Cause or next step |
|---|---|
| `DisallowedHost` | Add the deployed hostname to `ALLOWED_HOSTS` |
| Login returns 500 | Inspect the complete traceback in Render Logs |
| `relation "auth_user" does not exist` | Apply migrations to the database used by the hosted service |
| Login says credentials are wrong | Create or reset the account in the hosted database |
| “No project assigned” | Create the project and assign membership |
| Connection check says `sqlite` | `DATABASE_URL` is missing, ignored or overwritten |
| External database connection fails | Check the external URL, TLS and database IP-access rules |
| Static collection reports missing Leaflet images | Restore the version-matched images beside `leaflet.css` |
| Missing `Leaflet.GoogleMutant.js.map` | Restore the matching source map or remove its dangling source-map comment |
| Old styling appears | Confirm deployed files and hard-refresh with Ctrl+F5 |
| Map background fails | Inspect browser console and Maps key restrictions |
| Resident App link fails | Start the local companion server or configure a hosted URL |
| Shade calculations are unavailable | Current backend engine is a placeholder |

### Leaflet static assets

For Leaflet 1.9.4, the source directory should contain these images:

```text
planner/static/planner/vendor/images/layers.png
planner/static/planner/vendor/images/layers-2x.png
planner/static/planner/vendor/images/marker-icon.png
planner/static/planner/vendor/images/marker-icon-2x.png
planner/static/planner/vendor/images/marker-shadow.png
```

The referenced Leaflet source map belongs at:

```text
planner/static/planner/vendor/leaflet.js.map
```

For GoogleMutant, if the matching source map is absent, remove only this dangling debugging comment from the source JavaScript file:

```javascript
//# sourceMappingURL=Leaflet.GoogleMutant.js.map
```

Then rerun:

```powershell
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

## Updating the Application

### Pull merged changes locally

Preserve uncommitted work before updating.

```powershell
git status
git switch main
git pull --ff-only origin main
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Ensure the temporary hosted database connection has been removed before normal local development.

### Publish a reviewed change

Stage the specific files changed:

```powershell
git status
git diff
git add path/to/changed-file
git commit -m "Describe the update"
git push
```

When automatic deployments are enabled, Render deploys changes to its connected branch. Otherwise use **Manual Deploy → Deploy latest commit**.

Code changes require deployment. Hosted database records and memberships do not require a code deployment.


## Current Implementation Scope

| Component | Status |
|---|---|
| Hosted login and project membership | Configured |
| Dashboard and geographic interface | Implemented |
| Lake scenario arithmetic | Demonstration inputs |
| Report inspection and staff workflow | Implemented |
| Resident input feed | Seeded sample reports |
| Weather adapter | Available when enabled and reachable |
| Tree layout editing and persistence | Available |
| Backend shade engine | Placeholder in the inspected repository snapshot |
| Cooling preview values | Illustrative unless backed by validated calculations |
| AI assistant | Local retrieval and optional external-model connection |
| Resident companion | Separate static demonstration |
| Production mobile report intake | Not connected |
| Physical telemetry and gate control | Not connected |

Displayed insurance values, weather examples and notification confirmations need supporting data or integration before being described as operational results.

## Repository Guide

| Path | Purpose |
|---|---|
| `config/` | Django settings and root routing |
| `planner/` | Projects, memberships, tree layouts and saved scenarios |
| `resilience/` | Dashboard, reports, climate assessment and advisory features |
| `resilience/knowledge/` | Local retrieval material |
| `simulation/engine.py` | Simulation integration point |
| `contracts/` | Payload examples |
| `elmina/site.json` | Reference geometry |
| `b2c_resident_app/` | Resident companion demonstration |
| `create_elmina.py` | Project bootstrap script |
| `build.sh` | Render dependency and static-file preparation |
| `requirements.txt` | Python dependencies |
| `.env.example` | Example configuration without secrets |

---

<div align="center">

**AeroThermal SDP**

*Explore township conditions. Review evidence. Plan informed responses.*

[Open the dashboard](https://aerothermal.onrender.com/)

</div>
