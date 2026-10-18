# AeroThermal

AeroThermal is a B2B climate-resilience web prototype developed for the Sime Darby Property Hackathon.

It helps township leadership, ESG teams, engineers and planners review lake storage, climate-related concerns, resident reports and proposed tree-shade scenarios.

The prototype uses an Elmina reference site. Climate scenarios and sample resident reports are clearly labelled as demonstration data.

## Main features

### Township overview
- Lake storage and available storm buffer.
- Active resident-report counts.
- Saved proposed-tree shade results.
- Maps and charts for reviewing project conditions.

### Map & planning
- Geographic reference map with resident-report locations.
- Shared climate scenarios.
- Lake storage and storm-buffer calculations.
- Illustrative pre-discharge volume for engineering review.

### Climate alerts
- Flood and stormwater review.
- Heat-exposure concerns.
- Water-reserve and dry-condition review.
- Wind and fallen-tree reports.
- Expandable evidence and suggested team responses.
- Official weather-feed availability and bulletin review.

### Resident reports
- Sample inputs representing reports received from the separate resident mobile app.
- Report locations and available attachments.
- Staff verification, assignment and status updates.
- Project-specific report access.

### Tree simulator
- Explore hypothetical proposed-tree layouts.
- Calculate geometric shade along the reference route.
- Save and compare scenarios.

Tree-simulator changes represent hypothetical proposals. They do not modify an approved township plan or authorise tree removal, relocation or planting.

### Access controls
- Login required for project access.
- Project membership controls access to data.
- Planner and viewer permissions.
- CSRF protection for supported write operations.
- Restricted access to stored report photos.

## B2B and B2C scope

This repository contains the B2B website.

The resident-facing B2C mobile app is developed separately. The website currently uses labelled dummy reports to demonstrate how incoming resident information would appear to township teams.

A production mobile-app integration is not included.

## Technology

- Python and Django
- Django templates, HTML, CSS and JavaScript
- SQLite for local development
- Leaflet for interactive maps
- Google Maps satellite imagery when configured
- Python simulation dependencies listed in requirements.txt

The project folder may still be named `ecocool`; the product name is AeroThermal.

---

## Run the project on your own laptop

These instructions use Windows PowerShell, including the terminal inside VS Code.

Each teammate runs their own Django server and local database. Sofea does not need to keep her laptop running for another teammate to use their own copy.

### 1. Install the prerequisites

Install:

- Git
- Python 3.12
- VS Code

Confirm Git and Python are available:

```powershell
git --version
py -3.12 --version
```

### 2. Clone the repository

Open PowerShell in the folder where you want to keep the project:

```powershell
git clone https://github.com/d1msums/ecocool.git
cd ecocool
```

If the repository is private, sign in with a GitHub account that has collaborator access.

Open the folder in VS Code:

```powershell
code .
```

Alternatively, use **VS Code → File → Open Folder** and select `ecocool`.

### 3. Create your virtual environment

Run this from the folder containing `manage.py`:

```powershell
py -3.12 -m venv .venv
```

The following commands use the virtual environment's Python directly, so activating it is optional.

### 4. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If a requirements file is missing, check that you cloned the latest branch and ask Sofea to commit the file. Avoid guessing dependency versions.

### 5. Create your local database

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

This applies the existing migrations to your local database.

Do not run `makemigrations` just to start the project.

### 6. Create your own account

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Choose your own username, email and password.

For example, Jia can use `jia` as her local username.

The password will not appear while typing in the terminal. This is normal.

Do not commit passwords or share your local database through GitHub.

### 7. Create the Elmina reference project

Run:

```powershell
.\.venv\Scripts\python.exe manage.py shell -c "exec(open('create_elmina.py', encoding='utf-8').read())"
```

The command prints the project's ID.

**Your project ID may differ from Sofea's.** A fresh database may assign ID `1`, even if Sofea uses ID `3`.

The reference project uses the geometry in:

```text
elmina/site.json
```

### 8. Assign your account to the project

A superuser account still needs project membership for the B2B dashboard.

Open the Django shell:

```powershell
.\.venv\Scripts\python.exe manage.py shell
```

Enter the following code. Replace `"jia"` with the username you created:

```python
from django.contrib.auth import get_user_model
from planner.models import Project, Membership

User = get_user_model()
user = User.objects.get(username="jia")
project = Project.objects.get(
    name="Elmina Valley Central Park - Map Pilot"
)

membership, created = Membership.objects.update_or_create(
    project=project,
    user=user,
    defaults={"role": "planner"},
)

print("Project ID:", project.pk)
print("Membership role:", membership.role)
```

Use `"viewer"` instead of `"planner"` when creating a read-only project membership.

Exit the shell:

```python
exit()
```

### 9. Load demonstration climate data and reports

Replace `1` below with the project ID printed during setup:

```powershell
.\.venv\Scripts\python.exe manage.py seed_resilience --project 1
.\.venv\Scripts\python.exe manage.py seed_app_reports --project 1
```

These commands create:
- A demonstration lake/climate snapshot.
- Labelled example resident-app reports.

Existing example records are preserved when the seed commands are run again.

### 10. Check the project

```powershell
.\.venv\Scripts\python.exe manage.py check
```

Resolve any reported errors before starting the server.

### 11. Start Django

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Keep the terminal open while using the website.

Open:

```text
http://127.0.0.1:8000/
```

Log in with the account you created and select your project.

For a project with ID `1`, direct links are:

| Page | Local URL |
|---|---|
| Overview | http://127.0.0.1:8000/projects/1/resilience/ |
| Map & planning | http://127.0.0.1:8000/projects/1/resilience/view/engineer/ |
| Resident reports | http://127.0.0.1:8000/projects/1/resilience/view/operations/ |
| Climate alerts | http://127.0.0.1:8000/projects/1/resilience/alerts/ |
| Tree simulator | http://127.0.0.1:8000/projects/1/ |

Replace `1` with your actual project ID.

To stop the server, press:

```text
Ctrl+C
```

## Optional: Google satellite map

The reference geometry can be displayed without Google satellite imagery.

For satellite imagery, obtain a Google Maps API key with:
- Maps JavaScript API enabled.
- Appropriate billing configuration.
- Website restrictions permitting your local development addresses.

Local website entries:

```text
http://127.0.0.1:8000/*
http://localhost:8000/*
```

The project reads the Django setting `GOOGLE_MAPS_API_KEY`.

For an environment-variable setup, ensure `config/settings.py` contains:

```python
import os

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")
```

If the setting already exists, update that assignment rather than adding a duplicate.

In the same PowerShell terminal used to start Django:

```powershell
$env:GOOGLE_MAPS_API_KEY = "YOUR_OWN_API_KEY"
.\.venv\Scripts\python.exe manage.py runserver
```

This environment variable applies to the current terminal session.

Do not commit the actual key. A browser map key is visible to browser requests, so website and API restrictions are still necessary.

If satellite imagery fails:
1. Open browser Developer Tools with F12.
2. Select Console.
3. Refresh the page.
4. Inspect the exact Google Maps error.

An unavailable satellite map does not necessarily mean the key's quota has been exhausted.

## Weather-feed behaviour

The climate scenario selector uses demonstration inputs.

Official weather retrieval is controlled separately by the existing setting:

```python
AEROTHERMAL_LIVE_WARNINGS = False
```

If deliberately enabled, the adapter requires internet access and retrieves national warning records.

Returned bulletins require location review before being treated as relevant to Elmina. An empty, disabled or unavailable feed is not an all-clear.

---

## Opening the project again later

After completing the first-time setup, you normally only need:

```powershell
cd C:\path\to\ecocool
.\.venv\Scripts\python.exe manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

You do not need to recreate your virtual environment, account or demo data each time.

## Getting the latest team updates

Stop the server first.

Check for your own uncommitted work:

```powershell
git status
```

Commit your work before pulling updates, or coordinate with the team if you are unsure how to preserve it.

When your working tree is ready:

```powershell
git pull --ff-only
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

If Git reports diverging branches, stop and resolve that with the team. Do not force-push or discard another teammate's work.

The repository should already contain the installed frontend and page changes. Do not rerun historical upgrade installers during normal setup unless the team specifically instructs you to.

## Suggested demonstration

1. Open the township overview.
2. Review lake storage, storm buffer and resident reports.
3. Open Climate alerts.
4. Select the Heavy rain demonstration scenario.
5. Explain the assumed inflow and available-buffer shortfall.
6. Open a resident report and inspect its location and status.
7. Select Drought to demonstrate the water-reserve concern.
8. Open Tree simulator to compare hypothetical shade proposals.

Scenario changes are shared across pages within the same local project.

## Important prototype boundaries

- Climate snapshots and sample reports are demonstration data.
- The Elmina geometry is a reference pilot, not the complete approved township plan.
- Existing tree inventory is incomplete or unavailable in the reference dataset.
- Tree placement is hypothetical and subject to professional assessment and applicable approvals.
- Shade results describe geometric route coverage, not a verified air-temperature reduction.
- Storage calculations are simplified volume balances, not calibrated flood forecasts.
- A pre-discharge candidate requires engineering review; the prototype does not control a gate.
- Heatwave, soil-moisture and El Niño monitoring are not established by selecting a demo scenario.
- Internal advisories do not constitute official government warnings.
- Production mobile-app intake and push notifications are not included.

## Troubleshooting

### “No project assigned”

Create a Membership linking your user to the correct project, as described in step 8.

### Project page returns 404

Check your local project ID and membership. Do not assume your database uses project ID `3`.

### The browser cannot connect

Make sure `manage.py runserver` is running and the terminal remains open.

If port 8000 is occupied:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 8001
```

Then open:

```text
http://127.0.0.1:8001/
```

Google Maps website restrictions may also need to allow that port.

### Old colours or labels remain visible

Save the edited files and press Ctrl+Shift+R.

If necessary, open Developer Tools → Network → Disable cache, then refresh while Developer Tools remains open.

### Tree simulator still redirects to Landscape review

The Landscape Review rollback is incomplete. Check that the restored navigation links use the `dashboard` URL and that the retired-editor middleware hook has been removed.

Do not run `install_landscape_review.py` if you want to keep the Tree simulator.

### “No module named resilience.landscape_urls”

The URL configuration still imports the retired Landscape Review add-on. Remove its import and appended URL-pattern lines if using the restored Tree simulator version.

### Climate cards show missing data

Confirm that `seed_resilience` was run for the correct project.

Some measurements intentionally remain unavailable because no real sensor or validated data source is connected.
