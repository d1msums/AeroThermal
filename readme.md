# EcoCool

Django prototype for comparing tree placement and projected shade
around an illustrative lakeside walking route.

## Environment

- Python 3.12
- Install dependencies from requirements.txt.
- Copy .env.example to .env and generate your own Django secret key.
- Run migrations.
- Load demo_projects.json.
- Create a local administrator account.
- Add a planner membership for that account in Django admin.
- Start the Django development server.

## Data and model scope

The supplied park geometry is illustrative.
The current scope is geometric canopy shade.
Temperature reduction, lake cooling and flood prediction are not
implemented.

## Local files excluded from Git

Virtual environment, database, secrets, logs and backup files.