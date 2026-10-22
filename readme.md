<div align="center">

# 🌿 AeroThermal SDP - Township Climate Resilience Dashboard

### *Interactive B2B Web Prototype for Leadership, ESG, Engineering & Operations*

**Sime Darby Property University Hackathon 2026**  
*Planet · Climate Resilience · Township of Tomorrow*

<a href="https://aerothermal.onrender.com/">
  <img src="https://img.shields.io/badge/🚀_LAUNCH_DASHBOARD-OPEN_IN_BROWSER-B5FF43?style=for-the-badge&labelColor=252D27" alt="Launch AeroThermal dashboard">
</a>
<a href="https://aerothermal.onrender.com/">
  <img src="https://img.shields.io/badge/REFERENCE_TOWNSHIP-CITY_OF_ELMINA-506653?style=for-the-badge&labelColor=252D27" alt="Reference township: City of Elmina">
</a>

<br/>

<a href="https://nurewnn.github.io/aerothermal-resident-app/">
  <img src="https://img.shields.io/badge/📱_RESIDENT_COMPANION-OPEN_B2C_APP-32BFF5?style=for-the-badge&labelColor=252D27" alt="Open resident application">
</a>
<a href="https://github.com/d1msums/ecocool">
  <img src="https://img.shields.io/badge/💻_B2B_DASHBOARD-DJANGO_REPOSITORY-506653?style=for-the-badge&labelColor=252D27" alt="Dashboard repository">
</a>

<br/><br/>

**Flooding & Stormwater** · **Heatwaves & Shade Planning** · **Drought & Water Reserves** · **Resident Reports**

</div>

---

## 🌍 About AeroThermal

**AeroThermal** brings township climate information, planning tools, and resident-report workflows into one visual workspace.

The prototype helps project teams review lake storage, explore hypothetical tree layouts, locate reported hazards, and prepare responses to changing conditions.

Its main reference site is **City of Elmina**, with additional township reference selections where configured.

| Intended user | What the dashboard helps them review |
|---|---|
| **Leadership & ESG** | Overall conditions, outstanding issues, and supporting evidence. |
| **Engineers & planners** | Storage assumptions, mapped concerns, and proposed tree layouts. |
| **Operations teams** | Resident reports, work-item status, and park advisories. |

> **Prototype scope**  
> The application includes sample reports, illustrative climate scenarios, and demonstration outputs. Live connections and validated results must be distinguished from these examples.

The repository retains its original name, `ecocool`. The dashboard product is branded **AeroThermal**.

---

## 🔐 Panel Access

### Launch the dashboard

**[https://aerothermal.onrender.com/](https://aerothermal.onrender.com/)**

| Login field | Details |
|---|---|
| **Username** | `aerothermal_admin` |
| **Password** | `admin12345` |
| **Intended project role** | Planner |

### How to enter

1. Open the dashboard link.
2. Enter the username and password above.
3. Click **Sign In to AeroThermal**.
4. With direct-project navigation enabled, an account with one assigned project opens its Overview automatically.
5. If a project selector appears, choose the Elmina project.

**Direct login:**  
https://aerothermal.onrender.com/accounts/login/?next=/

If the browser opens an existing session, use a fresh private or Incognito window.

> This is a shared prototype account. Planner actions can change records visible to other reviewers. Despite its username, this account should have **Staff** and **Superuser** status disabled.

---

## 🧭 Explore the Dashboard

| Page | What you can do |
|---|---|
| **Overview** | Review key indicators, weather displays, charts, and the township map. |
| **Map & Tree Simulator** | Explore proposed tree layouts, adjust inputs, and inspect scenario displays. |
| **Resident reports** | Inspect incidents, locate issues, and update report status. |
| **AeroThermal AI** | Explore climate-response topics through the assistant interface. |
| **Resident App ↗** | Open the separate resident-facing application in a new tab. |

**Engineering view** is available through the Overview for additional storage and map review.

Small **ⓘ information buttons** explain individual cards and controls.

---

## 📊 01 — Township Overview

The Overview brings the main project indicators together.

### Key indicators

| Indicator | What it represents |
|---|---|
| **Lake storage** | Stored water as a percentage of configured capacity. |
| **Storm buffer** | Remaining storage volume based on the entered values. |
| **Active resident reports** | Reports that have not been resolved. |
| **Latest proposed-tree shade** | Eligible saved shade evidence, when available. |

### Example lake-storage calculation

```text
Configured capacity     100,000 m³
Stored water             65,000 m³
Lake storage                    65%
Available storm buffer   35,000 m³
```

These are demonstration values, not surveyed lake measurements.

### Weather and warning displays

1. Review the township weather cards.
2. Select a township card to inspect its associated map context where supported.
3. Click **Read full warning text** for the available detail.
4. Use **Refresh live feed** to request the configured weather source.
5. Check the affected area, validity period, and returned status.

Some weather cards contain preset conditions and dates. Refreshing a source does not establish that every card has received new data.

### Trends and spatial context

The lower Overview includes:

- Retention-lake storage history.
- Reports grouped by status.
- Saved canopy-shade runs.
- Township geometry and report markers.
- Hazard filters and map-layer controls.

Use **Reset Elmina view** to return to the reference location.

Select **Engineering view** for storage review or **Full report inbox** for incident handling.

> Coloured zones and heat markers provide illustrative spatial context. They are not validated flood boundaries or measured heat-island extents.

---

## 🌳 02 — Map & Tree Simulator

Explore how proposed planting layouts could be reviewed within the township map.

### Step 1 — Select the time

Set the date and time, or use:

**9 AM · 12 PM · 3 PM · 5 PM**

Keep the time consistent when comparing proposals.

### Step 2 — Choose a tree

Select a tree type and review its size inputs.

The interface includes example categories such as:

- Rain Tree.
- Merawan.
- Meranti.
- Keruing.

Species descriptions, insurance amounts, and certification wording are prototype assumptions. They do not establish actual insurance coverage or planting approval.

### Step 3 — Place a proposal

1. Click **+ Add tree on map**.
2. Click a permitted planting location.
3. Turn placement mode off before ordinary map navigation.

The placement logic checks the configured planting and exclusion geometry.

### Step 4 — Edit the layout

| Control | Function |
|---|---|
| **Tree marker / list entry** | Select a proposed tree. |
| **Update size** | Apply revised size inputs. |
| **Delete selected** | Remove one proposal from the working layout. |
| **Clear all** | Clear the working proposed layout after confirmation. |
| **Reset 5 sample trees** | Load the configured example layout. |
| **Reset view** | Return the map to the reference site. |

The number of example trees follows the configured site data and may differ from the button label.

### Step 5 — Save or load

To save:

1. Enter a descriptive scenario name.
2. Click **Save**.
3. Check the feedback message.

To reopen a layout:

1. Choose it from the saved-layout selector.
2. Click **Load**.
3. Review its inputs before calculating again.

### Step 6 — Review the output

Click **Calculate Shade & Cooling** and read the result message.

Where valid shadow geometry exists, compare:

- **Before new trees**
- **With new trees**

> **Calculation status**  
> The reviewed repository snapshot contains a placeholder engine returning `mode: mock`, without calculated shade percentages or shadow geometry. Some visible shade and cooling values are front-end examples, rather than validated predictions.

Changes to tree positions, dimensions, or time require a fresh calculation.

A saved proposal is not approval to plant or remove a real tree.

---

## 🌧️ 03 — Lake & Weather Action Center

Find this section below the tree-simulator results.

| Example condition | Review focus |
|---|---|
| **Heavy Storm** | Available storage, assumed inflow, and drainage issues. |
| **Normal Day** | Baseline conditions. |
| **Heatwave** | Exposed paths, shaded alternatives, and heat reports. |
| **Dry Spell** | Water reserves and stressed vegetation. |
| **Strong Wind** | Fallen branches and access obstructions. |

### How to use it

1. Select a condition.
2. Read the weather and site-condition panel.
3. Review the lake percentage and empty storage.
4. Read the suggested response steps.
5. Open **Take Action & Notify Crew**, where available, to inspect the proposed action.

Switching conditions demonstrates a scenario. It does not obtain a new sensor measurement.

> **Physical-control boundary**  
> The prototype does not operate a lake gate. A release suggestion or confirmation dialog does not establish downstream safety, engineering approval, or delivery of a crew notification.

---

## 🗺️ 04 — Engineering View

Open:

**Overview → Engineering view**

### Shared project scenario

Choose a condition and click **Apply scenario** with Planner access.

Available presets include normal, storm, heat, drought, and wind conditions.

Applying a scenario updates the stored project climate snapshot.

### Storage review

Inspect:

- Current storage.
- Storage after a candidate release.
- Storage after assumed storm inflow.
- Candidate pre-discharge volume.
- **MSMA & hydraulic assumptions**.

A candidate release volume is based on entered assumptions. It is not an approved discharge instruction.

### Map controls

- Toggle **App report markers**.
- Toggle **Surface thermal hotspots**.
- Click **Fit site** to reset the view.
- Select a supported report marker.
- Use **Locate on map** or **Open work item**.

The stored project snapshot and the simulator’s front-end examples may differ. Review each view’s source and values separately.

---

## 📍 05 — Resident Reports

The report workspace illustrates how project teams review resident-reported issues.

### Report categories

**Drainage / Flood · Tree / Wind · Dry Vegetation · Heat Exposure**

### Filter the queue

Use:

- **Waiting Dispatch**
- **In Progress**
- **Active Field**
- **Resolved**
- **All Reports**

The category filter and search box narrow the list.

**Refresh live feed** reloads the page.

### Inspect an incident

1. Click **Inspect Incident**.
2. Review its description, location, status, and attachment.
3. Inspect the available crew and timeline information.
4. Select **Locate on Map** to centre on the issue.
5. Use **Fit Park** to reset the view.

Some photos, crew assignments, contact fields, timelines, and verification captions are demonstration fixtures.

### Update a work item

From a supported report inspector, select **Open work item**.

With Planner access:

1. Choose a status.
2. Mark the report reviewed/verified only after review.
3. Optionally select **Assign to me**.
4. Add a clear note.
5. Click **Save update**.
6. Review the Activity history.

The queue also provides **Mark Resolved** for supported records.

If another user changes a report first, reload and review its latest version before saving.

> Saving a status updates the database record. It does not independently verify completed physical work, live crew dispatch, or reward delivery.

---

## 📢 06 — Park Advisories

Prepare notices using templates or the custom advisory form.

### Create an advisory

1. Scroll to the advisory section in **Resident reports**.
2. Select **Preview Advisory** or **+ New Custom Broadcast**.
3. Choose a category.
4. Enter the title and message.
5. Select the validity period.
6. Review the preview.
7. Submit the notice or select **Cancel**.

A useful notice identifies:

- The affected place.
- The issue.
- What residents should do.
- An alternative route or next update.

### Manage a notice

Review its active status and expiry.

Use **Withdraw Notice** when it should stop being displayed.

> The backend stores prototype advisories. The button label “Publish to Resident Phones” does not establish push delivery to the separate resident application.

---

## ✨ 07 — AeroThermal AI

The assistant workspace provides suggested climate-response topics and a message composer.

### Ask a question

1. Open **AeroThermal AI**.
2. Select a topic or type a question.
3. Press **Enter** or click the send button.
4. Use **Shift + Enter** for a new line.
5. Review the response against the available project evidence.

Use **New Inquiry** to begin a fresh conversation.

The **METMalaysia Weather Radar** link returns to the Overview weather area.

### Optional model configuration

The **Gemini API Key** dialog supports saving and clearing a supplied key.

The reviewed implementation stores this key in browser `localStorage`, which persists until cleared. API configuration should be managed separately from shared panel access.

> Built-in responses include sample claims about infrastructure, readiness, and response arrangements. These are not certified facts or official instructions.

---

## 📱 08 — Resident Companion

**[Open the AeroThermal Resident App](https://nurewnn.github.io/aerothermal-resident-app/)**

Select **Resident App ↗** in the dashboard header to open the separate application in a new tab.

| Experience | Intended audience |
|---|---|
| **B2B dashboard** | Leadership, ESG, engineering, planning, and operations teams. |
| **B2C resident app** | Residents using the community-facing experience. |

### Integration boundary

The navigation link connects the experiences for browsing. It does not automatically connect their databases.

End-to-end integration requires:

- Authenticated report submission.
- Project and location mapping.
- Attachment storage.
- Report-status synchronization.
- Advisory delivery.
- Reward synchronization.

Seeded dashboard reports illustrate the intended review workflow.

---

## 🛡️ Access & Permissions

| Role | Intended access |
|---|---|
| **Viewer** | Review permitted project information. |
| **Planner** | Review information and perform permitted project updates. |
| **Django administrator** | Manage accounts and memberships through the admin site. |

A project membership determines which project a user can access.

Planner membership is separate from Django Staff or Superuser status.

### Shared panel account configuration

```text
Active               Yes
Project membership   Planner
Staff status         No
Superuser status     No
```

Account and membership management:

**https://aerothermal.onrender.com/admin/**

---

## ⚙️ Implementation Status

| Area | Current scope |
|---|---|
| **Authentication** | Django login and project-scoped membership checks. |
| **Project entry** | Direct navigation for one assigned project when enabled. |
| **Dashboard** | Visual indicators, charts, maps, and navigation. |
| **Tree planning** | Proposed-tree placement, editing, and saved layouts. |
| **Simulation engine** | Placeholder in the reviewed snapshot. |
| **Climate scenarios** | Stored snapshots and front-end examples. |
| **Resident reports** | Sample records with database-backed status updates. |
| **Advisories** | Database-backed prototype notices. |
| **Resident App** | Separate application linked in a new tab. |
| **Weather** | Configured adapter alongside preset interface content. |
| **AI** | Assistant interface, built-in responses, and optional external model. |
| **Lake actuation** | No connected physical gate control. |

---

## 🧰 Technology

<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="Leaflet">

</div>

<br/>

| Layer | Technology |
|---|---|
| Backend | Python and Django |
| Frontend | Django templates, HTML, CSS, and JavaScript |
| Mapping | Leaflet, Google Maps integration, and reference geometry |
| Local database | SQLite when `DATABASE_URL` is unset |
| Hosted database | PostgreSQL |
| Application server | Gunicorn |
| Static assets | Django staticfiles and WhiteNoise |
| Dashboard hosting | Render |
| Resident-app hosting | GitHub Pages |

---

## 💻 Run Locally

<details>
<summary><strong>Expand the Windows / VS Code setup guide</strong></summary>

### 1. Clone the repository

```powershell
git clone https://github.com/d1msums/ecocool.git
cd ecocool
```

Open the folder in VS Code.

### 2. Create a virtual environment

Use Python 3.12:

```powershell
py -3.12 -m venv .venv
```

The following commands call the virtual environment directly, so activation is optional.

### 3. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use the dependency files supplied in the repository. A separate `requirements-sim-lock.txt` is not required unless included in a later update.

### 4. Configure the environment

Create `.env` beside `manage.py`.

Generate a local secret:

```powershell
.\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add it to `.env`:

```dotenv
DJANGO_SECRET_KEY=replace_with_your_generated_local_secret
DJANGO_DEBUG=True
GOOGLE_MAPS_API_KEY=
```

Do not commit `.env`.

For an isolated local database, leave `DATABASE_URL` unset in both `.env` and the terminal environment.

Django settings must allow `localhost` and `127.0.0.1`.

If satellite maps are required, configure a Google Maps key that permits the local website. Otherwise, use reference/vector geometry where supported.

### 5. Create the database tables

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

Run migrations through `manage.py`, not `admin.py`.

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

This loads the reference geometry from `elmina/site.json`.

If an existing project contains different data, inspect it before making changes.

### 8. Add membership and sample data

Open the Django shell:

```powershell
.\.venv\Scripts\python.exe manage.py shell
```

Replace `YOUR_LOCAL_USERNAME` and run:

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

print("Ready:", project.name)
print("Project ID:", project.pk)
```

Exit:

```python
exit()
```

### 9. Start the application

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Open:

**http://127.0.0.1:8000/**

Sign in using your local account.

Stop the server with **Ctrl + C**.

</details>

---

## 🔄 Update Your Local Copy

<details>
<summary><strong>Expand the GitHub update instructions</strong></summary>

### 1. Check for local changes

```powershell
git status
```

Preserve unfinished work before pulling.

### 2. Pull the latest main branch

```powershell
git switch main
git pull --ff-only origin main
```

If Git reports a conflict or diverged history, resolve it before continuing.

### 3. Update dependencies and schema

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
```

### 4. Restart Django

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Refresh the browser. Use **Ctrl + F5** if old styles remain visible.

</details>

---

## ☁️ Deployment

<details>
<summary><strong>Expand the Render deployment notes</strong></summary>

### Service configuration

| Setting | Value |
|---|---|
| Runtime | Python |
| Root directory | Repository root containing `manage.py` |
| Build command | `bash build.sh` |
| Application | `config.wsgi:application` |

The project’s free-service startup approach runs migrations before Gunicorn:

```bash
python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

The build script should install dependencies and collect static assets.

Production dependencies must include the configured PostgreSQL adapter, Gunicorn, database-URL parser, and WhiteNoise.

### Environment

Configure:

- `DJANGO_SECRET_KEY`
- `DATABASE_URL`
- Production debug setting
- `GOOGLE_MAPS_API_KEY`, if satellite maps are enabled

Environment-variable names and parsing must match `config/settings.py`.

Keep production `DEBUG` disabled.

Ensure the host and origin are permitted:

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

### Database selection

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

Local and hosted accounts belong to their respective databases.

Creating a local user does not create that user on the deployed service.

### Render Free considerations

- The service can pause when idle.
- The first request after inactivity may take longer.
- Local filesystem changes are temporary.
- Store relational data in PostgreSQL.
- Uploaded photos need durable external storage to survive restarts.
- Free web services do not provide dashboard Shell access.
- Check the expiry date of a free Render PostgreSQL database.

Once a hosted administrator exists, use Django admin to manage users and memberships.

### Publish an update

Review changes:

```powershell
git status
git diff
```

Stage the intended files, then commit and push. For a README-only update:

```powershell
git add README.md
git commit -m "Update AeroThermal README"
git push origin main
```

If the repository uses `readme.md`, use that exact filename.

Render deploys automatically when enabled. Otherwise, select:

**Manual Deploy → Deploy latest commit**

### Official references

- [Deploy Django on Render](https://render.com/docs/deploy-django)
- [Render Free service limitations](https://render.com/docs/free)

</details>

---

## 🛠️ Troubleshooting

<details>
<summary><strong>Expand common issues and fixes</strong></summary>

| Problem | What to check |
|---|---|
| **Login page does not appear** | An existing session may be active. Use a fresh private window or the direct login URL. |
| **Password rejected** | Confirm that the credentials belong to the local or hosted database being used. |
| **No project assigned** | Add a Membership linking the account to the existing project. |
| **Project selector still appears** | Multiple memberships can retain the selector. For one project, confirm the redirect update is deployed. |
| **Cannot edit or save** | Check Planner membership for that project. |
| **`auth_user` table missing** | Run migrations against the database used by the deployed service. |
| **`DisallowedHost`** | Add the deployed hostname to `ALLOWED_HOSTS`. |
| **CSRF verification failed** | Check the HTTPS origin, CSRF settings, and current session. |
| **`TemplateDoesNotExist`** | Confirm the template path and installed app configuration. |
| **Google rejects the map key** | Check API access, website restrictions, quota/billing status, and the console error. |
| **Map background unavailable** | Use reference/vector geometry where supported. |
| **Missing file during `collectstatic`** | Restore the exact image or source-map file referenced by CSS or JavaScript. |
| **Shade result is empty or mock** | The reviewed engine is a placeholder; valid calculations require an integrated engine. |
| **Styles look unchanged** | Check deployment completion and hard-refresh the browser. |
| **Report changed before saving** | Reload the work item and review its latest version. |
| **Resident App has different data** | The navigation link does not establish database synchronization. |
| **Feed or AI request fails** | Inspect the error and configuration. Missing information remains unavailable. |

</details>

---

## 📌 Understanding the Results

| Label or output | How to interpret it |
|---|---|
| **Demo value** | An example used to illustrate interface behaviour. |
| **Stored record** | A database entry, not independent verification. |
| **Reference map** | Spatial context for reviewing the project. |
| **Weather warning** | Information requiring source, location, and validity checks. |
| **Shade / cooling output** | Requires a connected and validated calculation model. |
| **Tree proposal** | A hypothetical layout subject to site review and approvals. |
| **Release suggestion** | An assumption-based proposal, not a physical command. |
| **AI response** | Decision-support text requiring evidence review. |

---

<div align="center">

### 🌿 AeroThermal

**Township information, planning, and response in one visual workspace.**

[Open Dashboard](https://aerothermal.onrender.com/) · [Open Resident App](https://nurewnn.github.io/aerothermal-resident-app/)

</div>
