<div align="center">

# AeroThermal

### Township Climate Resilience Dashboard

A visual B2B workspace for reviewing climate conditions, exploring tree-planting proposals, and managing resident-reported issues.

**Flooding · Heatwaves · Drought · Tree & Wind Hazards**

[Open Dashboard](https://aerothermal.onrender.com/) · [Open Resident App](https://nurewnn.github.io/aerothermal-resident-app/) · [Repository](https://github.com/d1msums/ecocool)

</div>

---

## About AeroThermal

AeroThermal is a climate-resilience prototype developed for the Sime Darby Property hackathon.

The dashboard brings lake-storage information, weather displays, township maps, proposed tree layouts, and resident reports into one workspace.

Its intended users include:

- **Leadership and ESG teams:** review overall conditions and supporting evidence.
- **Engineers and planners:** inspect storage assumptions and explore proposed planting layouts.
- **Operations teams:** review reported incidents, update their status, and prepare advisories.

The main reference site is **City of Elmina**. Other township selections provide additional reference views where configured.

The repository retains the original `ecocool` name, while the product interface uses **AeroThermal**.

> **Prototype status:** The application includes sample reports, illustrative climate scenarios, and demonstration outputs. Live services, validated simulation results, and end-to-end resident-app integration should be distinguished from these examples.

---

## Contents

- [Panel Access](#panel-access)
- [Dashboard Navigation](#dashboard-navigation)
- [Overview](#overview)
- [Map & Tree Simulator](#map--tree-simulator)
- [Lake & Weather Action Center](#lake--weather-action-center)
- [Engineering View](#engineering-view)
- [Resident Reports](#resident-reports)
- [Advisories](#advisories)
- [AeroThermal AI](#aerothermal-ai)
- [Resident App](#resident-app)
- [Access Roles](#access-roles)
- [Implementation Status](#implementation-status)
- [Technology](#technology)
- [Run Locally](#run-locally)
- [Update Your Local Copy](#update-your-local-copy)
- [Deployment Notes](#deployment-notes)
- [Troubleshooting](#troubleshooting)

---

## Panel Access

### Open the deployed dashboard

**https://aerothermal.onrender.com/**

Use the shared prototype account:

| Field | Value |
|---|---|
| Username | `aerothermal_admin` |
| Password | `admin12345` |
| Intended project role | Planner |

The account is intended for prototype review. Despite its username, it should not have Django Staff or Superuser privileges.

### Sign in

1. Open the dashboard.
2. Enter the credentials above.
3. Select **Sign In to AeroThermal**.
4. With direct-project navigation enabled, an account with one assigned project opens its Overview automatically.
5. If multiple projects appear, select the Elmina project.

If the browser opens an existing account automatically, use a fresh private or Incognito session.

Direct login:

**https://aerothermal.onrender.com/accounts/login/?next=/**

### Shared account behaviour

Planner access allows changes to shared prototype records, including saved layouts, climate scenarios, report statuses, and advisories.

Changes made through this account may be visible to other reviewers. Use the sample records when exploring editing features.

---

## Dashboard Navigation

| Navigation item | Purpose |
|---|---|
| **Overview** | Review key indicators, weather displays, trends, and the township map. |
| **Map & Tree Simulator** | Explore hypothetical tree layouts and climate-response scenarios. |
| **Resident reports** | Inspect reported issues, locations, and workflow status. |
| **AeroThermal AI** | Explore climate-response topics through the assistant interface. |
| **Resident App ↗** | Open the separate resident-facing application in a new tab. |

The account area at the top right identifies the signed-in user and project role.

Small **i** buttons explain individual cards and controls.

---

## Overview

The Overview is the starting point for reviewing the project.

### Key indicators

| Indicator | Meaning |
|---|---|
| **Lake storage** | Stored water as a percentage of the configured lake capacity. |
| **Storm buffer** | Remaining storage volume based on the entered capacity and stored water. |
| **Active resident reports** | Reports that have not been resolved. |
| **Latest proposed-tree shade** | Eligible saved shade evidence, when available. |

Example storage calculation:

```text
Configured capacity: 100,000 m³
Stored water:         65,000 m³

Lake storage:         65%
Remaining buffer:     35,000 m³
```

These are demonstration values, not surveyed lake measurements.

### Weather displays

1. Review the township weather cards.
2. Select a township card to inspect its associated map context where supported.
3. Select **Read full warning text** to inspect the available warning detail.
4. Use **Refresh live feed** to request the configured weather source.
5. Check the response, affected area, and timestamp.

Some weather cards contain preset conditions and dates. A feed refresh does not establish that every displayed card has received new data.

### Trends and map

The lower Overview includes:

- Retention-lake storage history.
- Report counts grouped by status.
- Saved canopy-shade runs.
- Township geometry and resident-report markers.
- Hazard category filters.
- Report and surface-heat layer controls.

Use **Reset Elmina view** to return to the reference location.

Select **Engineering view** for storage review or **Full report inbox** for incident handling.

> Coloured zones and heat markers provide illustrative spatial context. They are not validated flood boundaries or measured heat-island extents.

---

## Map & Tree Simulator

This page supports exploration of hypothetical planting layouts.

### 1. Select the time

Set the date and time, or use:

- **9 AM**
- **12 PM**
- **3 PM**
- **5 PM**

Keep the time consistent when comparing proposals.

### 2. Choose a tree

Select a tree type and review its size inputs.

The interface includes example tree categories such as Rain Tree, Merawan, Meranti, and Keruing.

Species descriptions, insurance amounts, and certification wording are prototype assumptions. They do not establish actual coverage or planting approval.

### 3. Place a proposal

1. Click **+ Add tree on map**.
2. Click a permitted planting location.
3. Turn placement mode off before ordinary map navigation.

The placement logic checks the configured planting and exclusion geometry.

### 4. Edit the layout

| Control | Action |
|---|---|
| Tree marker or list entry | Select a proposed tree. |
| **Update size** | Apply revised size inputs to the selected proposal. |
| **Delete selected** | Remove one proposed tree from the working layout. |
| **Clear all** | Clear the working proposed layout after confirmation. |
| **Reset 5 sample trees** | Load the configured example layout. |
| **Reset view** | Return the map to the reference site. |

The number of trees loaded by the example button follows the site data and may differ from its label.

### 5. Save or load

1. Enter a descriptive scenario name.
2. Click **Save**.
3. Check the feedback message.

To revisit a saved layout:

1. Choose it from the saved-layout selector.
2. Click **Load**.
3. Review its inputs before calculating again.

### 6. Review the result

Click **Calculate Shade & Cooling** and read the result message.

Where valid shadow geometry exists, use:

- **Before new trees**
- **With new trees**

> **Calculation status:** The reviewed repository snapshot contains a placeholder simulation engine returning `mode: mock`, without calculated shade percentages or shadow geometry. Some visible before/after and cooling values are front-end examples. They should not be treated as validated environmental predictions.

Changing a layout does not approve planting or removal of real trees. Site suitability and the relevant approvals remain separate requirements.

---

## Lake & Weather Action Center

Find this section below the tree-simulator results.

Available example conditions include:

| Condition | Review focus |
|---|---|
| **Heavy Storm** | Storage space, assumed inflow, and drainage issues. |
| **Normal Day** | Baseline conditions. |
| **Heatwave** | Exposed paths, shaded alternatives, and heat reports. |
| **Dry Spell** | Water reserves and stressed vegetation. |
| **Strong Wind** | Fallen branches and access obstructions. |

### How to use it

1. Select a condition.
2. Read the weather and site-condition panel.
3. Review the lake percentage and remaining storage.
4. Read the suggested response steps.
5. Open **Take Action & Notify Crew** where available to inspect the proposed action.

Switching conditions demonstrates a scenario. It does not obtain a new sensor measurement.

> The prototype does not operate a lake gate. A release suggestion or confirmation dialog does not establish downstream safety, engineering approval, or delivery of a crew notification.

---

## Engineering View

Open:

**Overview → Engineering view**

This workspace is separate from the main tree-simulator page.

### Shared project scenario

Choose a condition and click **Apply scenario** with Planner access.

The available presets include normal, storm, heat, drought, and wind conditions.

Applying a scenario updates the stored project climate snapshot.

### Storage review

Inspect:

- Current storage.
- Storage after a candidate release.
- Storage after assumed storm inflow.
- Candidate pre-discharge volume.
- **MSMA & hydraulic assumptions**.

A candidate volume is an output of the entered assumptions. It is not an approved discharge instruction.

### Map controls

- Toggle **App report markers**.
- Toggle **Surface thermal hotspots**.
- Click **Fit site** to reset the view.
- Select a supported report marker.
- Use **Locate on map** or **Open work item**.

The shared project snapshot and the simulator’s front-end weather examples may differ. Review each view’s source and values separately.

---

## Resident Reports

The report workspace illustrates how project teams can review issues received from residents.

Sample categories include:

- Drainage and flooding.
- Tree and wind hazards.
- Dry vegetation.
- Heat exposure.

### Filter the queue

Use:

- **Waiting Dispatch**
- **In Progress**
- **Active Field**
- **Resolved**
- **All Reports**

Use the category filter and search box to narrow the list.

**Refresh live feed** reloads the page.

### Inspect an incident

1. Click **Inspect Incident**.
2. Review the description, location, status, and attachment.
3. Inspect the available crew and timeline information.
4. Select **Locate on Map** to centre on the issue.
5. Use **Fit Park** to reset the map.

Some photos, crew assignments, contact fields, timelines, and verification captions are demonstration fixtures.

### Update a work item

From a supported report inspector, select **Open work item**.

With Planner access:

1. Choose the status.
2. Set the reviewed/verified field only after reviewing the report.
3. Optionally select **Assign to me**.
4. Add a clear note.
5. Click **Save update**.
6. Review the Activity history.

The queue also includes **Mark Resolved** for supported records.

If another user changes the report first, reload it and review the latest version before saving again.

> Saving a status updates the database record. It does not verify completed physical work. Demonstration crew, escalation, and reward displays do not establish live dispatch or points delivery.

---

## Advisories

The Resident reports page includes notice templates and a custom advisory form.

### Create a notice

1. Scroll to the advisory section.
2. Select **Preview Advisory** on a template or **+ New Custom Broadcast**.
3. Choose a category.
4. Enter the title and message.
5. Select the validity period.
6. Review the preview.
7. Submit the notice or select **Cancel**.

A useful notice identifies:

- The affected location.
- The issue.
- What residents should do.
- An alternative route or next update.

### Manage notices

Review the active notices list and expiry.

Select **Withdraw Notice** when a notice should stop being displayed.

> The backend stores prototype advisories. The label “Publish to Resident Phones” does not establish push delivery to the separate resident application.

---

## AeroThermal AI

The AI workspace provides suggested climate-response topics and a message composer.

### Use the assistant

1. Open **AeroThermal AI**.
2. Select a suggested topic or type a question.
3. Press **Enter** or select the send button.
4. Use **Shift + Enter** for a new line.
5. Review the answer against the available project evidence.

Use **New Inquiry** to begin a fresh conversation.

The **METMalaysia Weather Radar** link returns to the Overview weather area.

### Optional external model

The **Gemini API Key** dialog supports saving and clearing a supplied key.

In the reviewed implementation, the browser stores that key in `localStorage`. This storage persists until cleared. API configuration should be managed separately from the shared panel login.

Built-in responses include sample claims about infrastructure, readiness, and response arrangements. These should not be treated as certified facts or official instructions.

---

## Resident App

The resident-facing application is available at:

**https://nurewnn.github.io/aerothermal-resident-app/**

Select **Resident App ↗** in the dashboard header to open it in a new tab.

### B2B and B2C roles

| Interface | Intended audience |
|---|---|
| **AeroThermal dashboard** | Leadership, ESG, engineering, planning, and operations teams. |
| **Resident App** | Residents using the community-facing experience. |

### Integration status

The navigation link connects the two experiences for browsing.

It does not automatically connect their databases.

End-to-end integration requires separate implementation of:

- Authenticated report submission.
- Project and location mapping.
- Attachment storage.
- Report-status synchronization.
- Advisory delivery.
- Reward synchronization.

The dashboard’s seeded resident reports illustrate the intended review workflow.

---

## Access Roles

| Role | Intended access |
|---|---|
| **Viewer** | Review permitted project pages and information. |
| **Planner** | Review information and perform permitted project updates. |
| **Django administrator** | Manage accounts and project memberships through the admin site. |

Project membership determines which project a user can access.

A Planner membership is different from Django Staff or Superuser status.

The shared panel account should have:

```text
Active: Yes
Project membership: Planner
Staff status: No
Superuser status: No
```

The project administrator can manage accounts and memberships at:

**https://aerothermal.onrender.com/admin/**

---

## Implementation Status

| Area | Current scope |
|---|---|
| Authentication | Django login and project-scoped membership checks. |
| Project entry | Direct navigation for one assigned project when the redirect update is deployed. |
| Dashboard | Visual indicators, charts, maps, and navigation. |
| Tree planning | Proposed-tree placement, editing, and saved-layout workflow. |
| Calculation engine | Placeholder in the reviewed snapshot; validation and integration remain necessary. |
| Climate scenarios | Stored project snapshots and front-end scenario examples. |
| Resident reports | Sample records and database-backed status updates. |
| Advisories | Database-backed prototype notices. |
| Resident App | Separate hosted application linked in a new tab. |
| Weather | Configured source adapter alongside preset interface content. |
| AI | Assistant interface, built-in responses, and optional external-model configuration. |
| Physical actuation | No connected lake-gate control. |

---

## Technology

| Layer | Technology |
|---|---|
| Backend | Python and Django |
| Frontend | Django templates, HTML, CSS, and JavaScript |
| Mapping | Leaflet, Google Maps integration, and reference geometry |
| Local database | SQLite when `DATABASE_URL` is unset |
| Hosted database | PostgreSQL configured through `DATABASE_URL` |
| Application server | Gunicorn |
| Static assets | Django staticfiles and WhiteNoise in the deployment configuration |
| Dashboard hosting | Render |
| Resident-app hosting | GitHub Pages |

---

## Run Locally

These instructions use Windows PowerShell.

### 1. Clone the repository

```powershell
git clone https://github.com/d1msums/ecocool.git
cd ecocool
```

Open this folder in VS Code.

### 2. Create a virtual environment

Use Python 3.12:

```powershell
py -3.12 -m venv .venv
```

The commands below call the virtual environment directly, so activation is optional.

### 3. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use the dependency files included in the repository. A separate `requirements-sim-lock.txt` is not required unless it is actually supplied by a later update.

### 4. Configure local settings

Create a `.env` file beside `manage.py`.

Generate a local secret:

```powershell
.\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add the generated value:

```dotenv
DJANGO_SECRET_KEY=replace_with_your_generated_local_secret
DJANGO_DEBUG=True
GOOGLE_MAPS_API_KEY=
```

Do not commit `.env`.

For an isolated local database, leave `DATABASE_URL` unset in both `.env` and the terminal environment.

The settings must allow `localhost` and `127.0.0.1` for local access.

If satellite maps are required, configure a Google Maps key that permits the local website. Otherwise, use reference/vector geometry where available.

### 5. Create database tables

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

Migrations run through `manage.py`, not `admin.py`.

### 6. Create a local administrator

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Choose your own local credentials.

The hosted panel account does not automatically exist in a new local database.

### 7. Create the Elmina reference project

```powershell
.\.venv\Scripts\python.exe manage.py shell -c "exec(open('create_elmina.py', encoding='utf-8').read())"
```

The script loads the configured reference geometry from `elmina/site.json`.

If it reports that an existing project has different data, inspect that project before changing anything. Do not delete it merely to bypass the check.

### 8. Assign membership and seed sample data

Open the Django shell:

```powershell
.\.venv\Scripts\python.exe manage.py shell
```

Paste the following, replacing `YOUR_LOCAL_USERNAME`:

```python
from django.contrib.auth import get_user_model
from django.core.management import call_command
from planner.models import Project, Membership

user = get_user_model().objects.get(
    username="YOUR_LOCAL_USERNAME"
)

project = Project.objects.get(
    name="Elmina Valley Central Park - Map Pilot"
)

Membership.objects.update_or_create(
    user=user,
    project=project,
    defaults={"role": "planner"},
)

call_command("seed_resilience", project=project.pk)
call_command("seed_app_reports", project=project.pk)

print("Ready:", project.name, "| Project ID:", project.pk)
```

Exit:

```python
exit()
```

These commands create sample climate and report records for the selected project.

### 9. Check and start Django

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Open:

**http://127.0.0.1:8000/**

Sign in with the local account created above.

Stop the server with **Ctrl + C**.

---

## Update Your Local Copy

After changes are merged on GitHub:

### 1. Check your working files

```powershell
git status
```

Commit or otherwise preserve unfinished local work before pulling.

### 2. Pull the latest main branch

```powershell
git switch main
git pull --ff-only origin main
```

If Git reports a conflict or diverged history, resolve it before continuing. Avoid force-resetting files containing work you need.

### 3. Update dependencies and database schema

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
```

### 4. Restart the server

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Refresh the browser. Use **Ctrl + F5** if old styles or scripts remain visible.

---

## Deployment Notes

The dashboard is hosted on Render with PostgreSQL.

### Service configuration

| Setting | Project configuration |
|---|---|
| Runtime | Python |
| Root directory | Repository root, containing `manage.py` |
| Build command | `bash build.sh` |
| Application | `config.wsgi:application` |

The project’s free-service startup approach runs migrations before Gunicorn:

```bash
python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

The build script should install dependencies and collect static assets. Production dependencies must include the configured PostgreSQL adapter, Gunicorn, database-URL parser, and WhiteNoise.

### Environment and settings

Configure:

- `DJANGO_SECRET_KEY`
- `DATABASE_URL`
- Production debug setting
- `GOOGLE_MAPS_API_KEY`, if satellite maps are enabled

Ensure Django settings include:

```python
ALLOWED_HOSTS = [
    "aerothermal.onrender.com",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://aerothermal.onrender.com",
]
```

Keep production `DEBUG` disabled. Environment variable names and parsing must match `config/settings.py`.

### Database selection

The project selects PostgreSQL when `DATABASE_URL` is set and SQLite otherwise:

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

Local and hosted accounts belong to their respective databases. Creating a user locally does not create it on the hosted service.

### Render Free considerations

- The service can pause when idle, so the first request may take longer.
- Local filesystem changes are temporary.
- Store relational data in PostgreSQL.
- Uploaded photos require durable external storage if they must survive restarts.
- Free web services do not provide dashboard Shell access.
- Free Render PostgreSQL databases have an expiry period; check the database’s current expiry date.

Use the hosted Django admin for account and membership management once an administrator exists.

### Publish an update

Review the changes before committing:

```powershell
git status
git diff
```

Stage only the intended files, then commit and push:

```powershell
git add README.md
git commit -m "Update AeroThermal documentation"
git push origin main
```

If the repository uses `readme.md`, use that exact filename instead.

Render deploys the pushed commit when automatic deployment is enabled. Otherwise, use **Manual Deploy → Deploy latest commit**.

Official references:

- [Deploy Django on Render](https://render.com/docs/deploy-django)
- [Render Free service limitations](https://render.com/docs/free)

---

## Troubleshooting

| Problem | What to check |
|---|---|
| Login does not appear | The browser may already have a session. Use a fresh private window or the direct login URL. |
| Login rejects the password | Confirm whether you are using the local or hosted database account. |
| No project assigned | Add a Membership linking the user to the existing project. |
| Project selector still appears | Multiple memberships can retain the selector. For one project, confirm the redirect update was deployed. |
| Cannot edit or save | Check that the account has Planner membership for that project. |
| `relation "auth_user" does not exist` | Run migrations against the database used by the deployed service. |
| `DisallowedHost` | Add the deployed hostname to `ALLOWED_HOSTS`. |
| CSRF verification failed | Check the HTTPS origin, CSRF settings, and current session. |
| `TemplateDoesNotExist` | Confirm the template exists at the expected path and the corresponding app is installed. |
| Google rejects the map key | Check API access, website restrictions, quota/billing status, and the browser console error. |
| Map background is unavailable | Use reference/vector geometry where supported. |
| `collectstatic` reports a missing file | Restore the exact image or source-map file referenced by the CSS or JavaScript. |
| Shade output is empty or marked mock | The reviewed engine is a placeholder. A connected calculation engine is required for valid results. |
| Styles look unchanged | Check deployment completion and perform a hard refresh. |
| A report changed before saving | Reload the work item and review the latest version. |
| Resident App shows different data | The navigation link does not establish database synchronization. |
| Feed or AI request fails | Review the returned error and configuration. Missing information should remain marked unavailable. |

---

## Data and Interpretation

Read each result alongside its source, timestamp, and scope.

- **Demo values** illustrate interface behaviour.
- **Stored records** represent database entries, not independent verification.
- **Reference maps** provide spatial context.
- **Weather warnings** require location and validity checks.
- **Shade and cooling outputs** require a connected, validated model.
- **Tree proposals** remain subject to site review and approvals.
- **Release suggestions** are not physical control commands.
- **AI responses** require evidence review.

AeroThermal demonstrates how these workflows can be brought together for township climate-resilience planning and operations.
