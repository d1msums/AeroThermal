<div align="center">

# 🌿 AeroThermal SDP
### Township Climate Resilience & Planning Dashboard

**An interactive B2B web prototype for township leadership, ESG teams, engineers and planners.**

*Sime Darby Property University Hackathon 2026*

![Platform](https://img.shields.io/badge/Platform-B2B_Web_Dashboard-263D2D?style=for-the-badge)
![Framework](https://img.shields.io/badge/Framework-Django-0C4B33?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Climate_Resilience-A3E635?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Prototype-38BDF8?style=for-the-badge)

**Flood preparedness · Heat exposure · Dry conditions · Community reports**

[Explore Features](#-key-features) · [Run Locally](#-installation--local-setup) · [Dashboard Walkthrough](#-dashboard-walkthrough) · [Demo Guide](#-five-minute-demonstration)

</div>

---

## 🌍 About AeroThermal

AeroThermal brings township climate information, geographic context and operational follow-up into one visual workspace.

The prototype helps users explore questions such as:

- How much water is currently stored in the reference lake?
- How much capacity remains available for incoming rainfall?
- Where are residents reporting blocked drains, fallen branches or heat exposure?
- Which reports require staff attention?
- How can proposed tree layouts be explored within a planning workflow?
- What information should be reviewed before responding to a climate-related concern?

The B2B dashboard focuses on township management. A separate **EcoCool Resident Companion** demonstration presents the resident-facing experience.

**City of Elmina** is the primary reference project used by the setup instructions. Additional township views are included in the interface for exploration.

> This is a demonstration prototype. Data sources and implementation status are explained in [Prototype Data & Current Scope](#-prototype-data--current-scope).

---

## ✨ Key Features

### 💧 Lake Storage & Storm Buffer

A visual summary of the configured lake capacity and stored water volume.

- Circular lake-storage indicator.
- Stored volume and total capacity.
- Available storm-buffer volume.
- Demonstration storage-history chart.
- Scenario-based review of assumed rainfall inflow.

**Example interpretation**

For a configured capacity of **100,000 m³** and stored volume of **65,000 m³**:

| Metric | Value |
|---|---:|
| Lake storage | 65% |
| Stored water | 65,000 m³ |
| Available capacity | 35,000 m³ |

The storage percentage describes how full the lake is. It is not a flood probability.

### 🌧️ Stormwater Scenario Review

The engineering view supports reviewing how different demonstration conditions affect lake storage.

- Apply available climate scenarios.
- Compare stored volume, assumed inflow and remaining capacity.
- Review an illustrative candidate release volume.
- Inspect downstream review and hold conditions.

Scenario changes update the shared project state. Candidate release figures support discussion; the prototype does not operate physical gates.

### 🗺️ Geographic Overview

Maps place reports and planning information in a geographic context.

- City of Elmina reference geometry.
- Google satellite background when configured.
- Vector reference fallback.
- Resident-report markers.
- Report inspection and location focus.
- Township reference-view selection.

Changing a township reference view does not automatically switch the authenticated database project.

### 🌳 Map & Tree Simulator

An interactive workspace for exploring proposed tree layouts.

- View the reference site.
- Add and select proposed trees using the available controls.
- Adjust tree dimensions.
- Remove proposed trees from a hypothetical layout.
- Save and reload layouts.
- Inspect the simulation response.

**Current calculation status:** the checked-in `simulation/engine.py` is a placeholder. It returns mock-mode output without calculated shade percentages. Example shade and cooling values shown in interface previews should be treated as illustrative until the calculation engine is connected and validated.

Proposed layouts do not authorize changes to existing trees or approved township plans.

### 📍 Resident Reports

An operational inbox showing how resident information can support township follow-up.

- Report locations and available attachments.
- Category and status filters.
- Search and map inspection.
- Staff assignment.
- Status updates and review notes.
- Project-specific access.
- Updated report counts after changes are saved.

The current B2B demonstration uses seeded app-style reports. The separate resident demo does not yet submit reports through a production Django intake API.

### 🤖 AeroThermal AI

A climate-assessment and advisory interface.

- Review flood, heat, dry-condition and wind-related evidence.
- Inspect available source information.
- Ask project-related questions.
- Retrieve material from the local knowledge corpus.
- Optionally use a configured Gemini connection.

Responses support human review. They are not official warnings, engineering approvals or emergency instructions.

### 🔐 Project Access Controls

Access is based on authenticated accounts and project memberships.

| Access type | Purpose |
|---|---|
| Viewer | Read permitted project information |
| Planner | Read information and perform supported planning/report updates |
| Administrator | Manage accounts, projects and memberships through Django admin |

A superuser still needs the appropriate project membership to open the B2B workspace.

---

## 🔄 How the Prototype Works

The demonstration follows this workflow:

1. **Load project information**  
   The reference geometry, climate snapshot and sample reports are stored in the local Django database.

2. **Review the overview**  
   The dashboard presents storage, buffer, report counts and geographic context.

3. **Inspect an issue**  
   A report marker or inbox item opens its location, attachment and status.

4. **Explore a scenario**  
   A planner changes a demonstration climate scenario or proposed tree layout.

5. **Record follow-up**  
   Authorized users assign reports, update their status and add review notes.

6. **Review the updated dashboard**  
   Refresh the overview to see the current stored project information.

The resident-facing demonstration runs separately and illustrates the companion experience.

---

## 🧰 Technology

| Layer | Technology |
|---|---|
| Backend | Python and Django |
| Frontend | Django templates, HTML, CSS and JavaScript |
| Local database | SQLite |
| Mapping | Leaflet |
| Optional satellite imagery | Google Maps JavaScript API |
| Optional external AI | Gemini |
| Resident demonstration | Static HTML, CSS and JavaScript |
| Configuration | Environment variables and python-dotenv |

The repository is named `ecocool`; the dashboard product name is **AeroThermal**.

---

## 🚀 Installation & Local Setup

These instructions use **Windows PowerShell**, including the terminal inside VS Code.

Run project commands from the folder containing `manage.py`.

### 1. Install prerequisites

Install:

- Python 3.12
- Git
- Visual Studio Code

Confirm that Python and Git are available:

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

If the repository is private, authenticate with a GitHub account that has access.

If you already have a clone, use the update instructions later in this guide.

### 3. Create a virtual environment

```powershell
py -3.12 -m venv .venv
```

In VS Code, open **Python: Select Interpreter** and select:

```text
.venv\Scripts\python.exe
```

The commands below use this interpreter directly, so activating the environment is optional.

### 4. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use the committed `requirements.txt`.

If a dependency cannot be installed, inspect the exact error and check its compatibility with the selected Python version.

### 5. Configure the environment

If `.env` does not already exist, copy the example:

```powershell
Copy-Item .env.example .env
```

Do not overwrite an existing `.env` containing your configuration.

Generate a Django secret:

```powershell
.\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Open `.env` and configure:

```dotenv
DJANGO_SECRET_KEY='PASTE_YOUR_GENERATED_SECRET_HERE'
GOOGLE_MAPS_API_KEY=
```

The Django secret is required before running management commands.

The Maps key can remain empty during initial setup. Satellite imagery requires a valid configured key.

Keep `.env` out of Git.

### 6. Create database tables

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

This applies the existing database migrations.

You do not need to run `makemigrations` simply to start a cloned project.

### 7. Create an administrator account

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Choose a username, email and password.

The password will not appear as you type.

### 8. Create the Elmina reference project

```powershell
.\.venv\Scripts\python.exe manage.py shell -c "exec(open('create_elmina.py', encoding='utf-8').read())"
```

The script reads:

```text
elmina/site.json
```

It prints the created or existing project ID.

**Keep this ID.** Your project may be `1`, even if another installation uses a different ID.

### 9. Assign project membership

Open the Django shell:

```powershell
.\.venv\Scripts\python.exe manage.py shell
```

Paste the following, replacing `YOUR_USERNAME` with the account you created:

```python
from django.contrib.auth import get_user_model
from planner.models import Project, Membership

user = get_user_model().objects.get(username="YOUR_USERNAME")

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

exit()
```

Use `"viewer"` instead of `"planner"` for read-only project access.

### 10. Load demonstration data

Replace `1` with the project ID printed during setup:

```powershell
.\.venv\Scripts\python.exe manage.py seed_resilience --project 1
.\.venv\Scripts\python.exe manage.py seed_app_reports --project 1
```

These commands create the demonstration climate snapshot and sample resident reports.

Running them again preserves existing fixture records and their workflow state.

### 11. Check and start Django

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Log in and choose your assigned project.

Keep the terminal open while using the dashboard. Stop the server with **Ctrl+C**.

> Historical `install_*.py` scripts are not part of normal startup. The merged repository already contains the installed interface.

---

## 🧭 Dashboard Walkthrough

The example URLs below use project ID `1`. Replace it with your actual ID.

| Page | Local URL |
|---|---|
| Project list | `http://127.0.0.1:8000/` |
| Overview | `http://127.0.0.1:8000/projects/1/resilience/` |
| Map & Tree Simulator | `http://127.0.0.1:8000/projects/1/` |
| Engineering view | `http://127.0.0.1:8000/projects/1/resilience/view/engineer/` |
| Resident reports | `http://127.0.0.1:8000/projects/1/resilience/view/operations/` |
| AeroThermal AI | `http://127.0.0.1:8000/projects/1/resilience/alerts/` |
| Administration | `http://127.0.0.1:8000/admin/` |

### 1. Overview — Understand the Project

**Use this page when:** you want a quick picture of the project before opening individual reports or planning tools.

1. Open the project’s Overview.
2. Read the lake-storage percentage.
3. Compare the stored volume with the available storm buffer.
4. Review the active report count.
5. Explore the map and available charts.
6. Click a report card or marker to inspect its details.
7. Use the information buttons for short explanations of individual metrics.

Check the data labels and timestamps while interpreting the page.

### 2. Report Inspector — Understand an Issue

**Use this feature when:** you want to see what was reported and where it happened.

1. Select a report marker or inbox card.
2. Review the report category, location and status.
3. Inspect its attachment, where available.
4. Click **Locate on map** to focus on its position.
5. Click **Open work item** to review the operational record.

An attachment may be a labelled demonstration illustration rather than a resident photograph.

### 3. Resident Reports — Track Follow-up

**Use this page when:** staff need to organize and review reported issues.

1. Open **Resident reports**.
2. Use the available status/category filters.
3. Search for a location or report.
4. Select a report and open its work item.
5. With planner access, assign staff and update its status.
6. Add a review note and save.
7. Return to Overview and refresh to see the updated report counts.

Viewer accounts can inspect permitted information but cannot perform planner-only updates.

### 4. Engineering View — Explore Storm Storage

**Use this page when:** you want to discuss how a demonstration scenario changes the lake-volume balance.

1. Open the engineering view from its link or direct URL.
2. Select an available scenario.
3. Click **Apply scenario**.
4. Review stored volume, assumed inflow and remaining buffer.
5. Inspect the candidate release and any review/hold conditions.
6. Compare the resulting values with the previous scenario.

Scenario selection changes shared project data. Coordinate when several people are using the same hosted project.

A release recommendation is a scenario output; no physical water-control action takes place.

### 5. Map & Tree Simulator — Explore a Layout

**Use this page when:** you want to demonstrate proposed planting and layout management.

1. Open **Map & Tree Simulator**.
2. Explore the reference map.
3. Use the available controls to add or select proposed trees.
4. Adjust dimensions and inspect their positions.
5. Use the calculation button to inspect the current simulation response.
6. Save and reload a layout using the available controls.

In the current repository snapshot, the backend calculation is a placeholder. Static shade/cooling previews should be described as examples.

Layout changes represent planning proposals and do not modify an approved township plan.

### 6. AeroThermal AI — Review Climate Evidence

**Use this page when:** you want to inspect climate concerns and ask contextual questions.

1. Open **AeroThermal AI**.
2. Review the available flood, heat, dry-condition and wind information.
3. Check timestamps and source indicators.
4. Identify missing or unavailable inputs.
5. Enter a project-related question.
6. Read the response and supporting material.

Example questions:

- “What should be reviewed before considering a lake release?”
- “Which reports need follow-up during heavy rainfall?”
- “What information is missing from this heat assessment?”
- “How should dry vegetation reports be prioritized?”

The response source depends on the available local retrieval and external-model configuration.

---

## 📱 EcoCool Resident Companion

The repository includes a separate resident-facing static demonstration.

To run it, open a **second terminal** from the repository root:

```powershell
.\.venv\Scripts\python.exe -m http.server 8080 --bind 127.0.0.1 --directory b2c_resident_app
```

Open:

```text
http://127.0.0.1:8080/
```

Keep the Django server running separately on port `8000`.

| Service | Local address |
|---|---|
| AeroThermal B2B dashboard | `http://127.0.0.1:8000/` |
| EcoCool resident demonstration | `http://127.0.0.1:8080/` |

The dashboard’s **Resident App ↗** button opens the local resident demonstration.

The resident demo’s return link currently uses B2B project ID `1`. Update the link in `b2c_resident_app/index.html` if your local project uses another ID.

**Integration status:** browser-local state and iframe messages support the resident demonstration. They do not currently create corresponding Django report records. B2B sample reports are loaded using `seed_app_reports`.

---

## ⚙️ Optional Configuration

### Google Satellite Imagery

Add your Maps browser key to `.env`:

```dotenv
GOOGLE_MAPS_API_KEY='YOUR_MAPS_BROWSER_KEY'
```

Configure the key for the Maps JavaScript API and the intended websites.

Local referrer examples:

```text
http://127.0.0.1:8000/*
http://localhost:8000/*
```

Restart Django after changing configuration.

If imagery does not load, open **F12 → Console** and inspect the exact Google Maps error.

### Weather Retrieval

The uploaded configuration enables warning retrieval with:

```python
AEROTHERMAL_LIVE_WARNINGS = True
```

For an offline demonstration, change the existing setting to:

```python
AEROTHERMAL_LIVE_WARNINGS = False
```

Retrieved records require geographic and date review. An unavailable or empty feed does not establish that conditions are safe.

### Optional Gemini Connection

Add a private model key to `.env`:

```dotenv
GEMINI_API_KEY='YOUR_PRIVATE_MODEL_KEY'
```

Restart Django.

The Maps browser key and Gemini model key serve different purposes. Keep model credentials private and review the response source when testing the assistant.

### Sample Report Photos

Prepare appropriate images you own using these filenames:

```text
blocked-drain.jpg
fallen-branch.jpg
dry-vegetation.jpg
heat-exposure.jpg
```

Attach them to the sample reports:

```powershell
.\.venv\Scripts\python.exe manage.py seed_app_reports --project 1 --photo-dir "C:\path\to\demo-photos"
```

Replace the project ID and folder path.

Report location is stored separately from the image. The prototype does not infer report coordinates from photo EXIF.

---

## 🎬 Five-Minute Demonstration

| Time | Page / action | What to explain |
|---|---|---|
| 0:00–0:40 | Overview | Introduce the township workspace and key metrics |
| 0:40–1:20 | Lake storage and buffer | Explain stored water and available storm capacity |
| 1:20–2:10 | Report marker → work item | Show location-linked evidence and staff follow-up |
| 2:10–3:00 | Engineering scenario | Compare demonstration storage conditions |
| 3:00–3:45 | Map & Tree Simulator | Demonstrate hypothetical layout editing and its current calculation status |
| 3:45–4:35 | AeroThermal AI | Review evidence and ask a contextual question |
| 4:35–5:00 | Access roles and companion app | Explain authorized access and the separate resident experience |

---

## 🔄 Opening & Updating the Project

### Start an existing local installation

```powershell
cd C:\path\to\ecocool
.\.venv\Scripts\python.exe manage.py runserver
```

There is no need to recreate the database or account each time.

### Get the latest merged changes

Stop the server and check your working tree:

```powershell
git status
```

Preserve any uncommitted work before continuing.

Then:

```powershell
git switch main
git pull --ff-only origin main
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

If Git reports conflicts or divergent branches, resolve them before proceeding.

Use **Ctrl+F5** in the browser after interface updates.

Git transfers code. Local accounts, saved database records and private uploaded photos remain specific to each installation.

---

## 🧩 Troubleshooting

| Issue | What to check |
|---|---|
| `KeyError: DJANGO_SECRET_KEY` | Create `.env` beside `manage.py` and configure the secret |
| `ModuleNotFoundError` | Use the project’s virtual environment and install `requirements.txt` |
| `TemplateDoesNotExist` | Confirm the required template exists in the correct app directory |
| “No project assigned” | Create a membership for the logged-in account |
| Project page returns 404 | Check the project ID and account membership |
| Old styling still appears | Confirm the updated files are present and press Ctrl+F5 |
| Google satellite map fails | Inspect the browser console, API configuration and referrer restrictions |
| Shade results are unavailable | The current backend simulation engine is a placeholder |
| Resident App button fails | Start the separate server on port 8080 |
| Resident demo report does not appear in B2B | A production intake connection is not implemented |
| Viewer cannot update a report | Editing requires planner access |
| Report photos are missing on another laptop | Uploaded media is not transferred through Git |
| Weather retrieval fails | Check connectivity and the live-warning setting |

---

## 📊 Prototype Data & Current Scope

| Component | Current status |
|---|---|
| Project login and membership | Implemented |
| B2B navigation and visual dashboard | Implemented |
| Lake-storage scenario arithmetic | Implemented using demonstration inputs |
| Report inspection and staff workflow | Implemented |
| Sample resident-report feed | Seeded demonstration records |
| Official weather adapter | Available when enabled and reachable |
| Tree layout editing and persistence | Available |
| Backend shade calculation | Placeholder in the inspected repository snapshot |
| Cooling preview figures | Illustrative unless supported by validated calculations |
| AI assistant | Local retrieval with optional external-model connection |
| Resident companion | Separate static demonstration |
| Production mobile report intake | Not implemented |
| Physical sensor telemetry / gate control | Not connected |

Displayed weather examples, tree-insurance claims and notification/dispatch confirmations should be interpreted according to their actual data source and implementation.

---

## 📂 Repository Guide

| Path | Purpose |
|---|---|
| `config/` | Django settings and root routes |
| `planner/` | Projects, memberships, tree layouts and saved scenarios |
| `resilience/` | Dashboard, reports, climate scenarios and advisory features |
| `resilience/knowledge/` | Local retrieval material |
| `simulation/engine.py` | Simulation integration point |
| `contracts/` | Payload and interface examples |
| `elmina/site.json` | Reference site geometry |
| `b2c_resident_app/` | Resident companion demonstration |
| `create_elmina.py` | Reference-project setup script |
| `docs/` | Additional integration and deployment documentation |
| `requirements.txt` | Python dependencies |
| `.env.example` | Example environment-variable configuration |

---

<div align="center">

**AeroThermal SDP**

*Explore township conditions. Review evidence. Plan informed responses.*

</div>
