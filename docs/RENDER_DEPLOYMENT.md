# Render deployment guide — AeroThermal

This is a **preparation guide**, not a claim the uploaded repository is deployment-ready. The lake-gauge update does not implement these settings changes. Review and commit deployment changes separately.

## 1. Check the app locally first

Follow [readme.md](../readme.md), run Django checks/tests, and resolve errors. Confirm the actual simulation and resident-integration status before presenting.

Use a Render Python web service plus PostgreSQL. For the Shell/private-file workflow below, use a paid web service and an appropriate database plan after checking costs. Free web services have no dashboard Shell or persistent disk; free PostgreSQL expires after 30 days.

## 2. Add hosting dependencies

In PowerShell beside manage.py:

```powershell
.\.venv\Scripts\python.exe -m pip install gunicorn whitenoise dj-database-url psycopg2-binary
.\.venv\Scripts\python.exe -m pip freeze | Out-File -Encoding utf8 requirements.txt
```

Review requirements for Windows-only packages or file:///C:/ paths. Do not remove normal project dependencies. Keep using runserver locally; Gunicorn runs on Linux.

## 3. Edit config/settings.py carefully

Do not replace the entire file or remove existing apps/access middleware. Keep the current environment-based SECRET_KEY.

At the top, add:

```python
import dj_database_url
```

os and Path are already imported in this snapshot.

Replace DEBUG and ALLOWED_HOSTS with:

```python
IS_RENDER = bool(os.environ.get("RENDER"))
DEBUG = os.environ.get(
    "DJANGO_DEBUG", "False" if IS_RENDER else "True"
).lower() == "true"
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = []
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_hostname}")
if IS_RENDER:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

Add custom domains explicitly if used. Never use DEBUG=True to debug the public site; inspect logs.

After the existing DATABASES definition, add:

```python
database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url, conn_max_age=600, conn_health_checks=True
        )
    }
elif IS_RENDER:
    raise RuntimeError("DATABASE_URL is required on Render")
```

In MIDDLEWARE, insert the following immediately after SecurityMiddleware, retaining every other entry:

```python
"whitenoise.middleware.WhiteNoiseMiddleware",
```

Replace STATIC_URL and add:

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

If the team has since added a cloud-upload backend, preserve its default storage configuration.

Replace the existing MEDIA_ROOT assignment:

```python
MEDIA_ROOT = Path(
    os.environ.get("MEDIA_ROOT", str(BASE_DIR / "private_media"))
)
```

Keep authenticated report-photo serving. Do not create a public route exposing private_media. WhiteNoise serves design assets, not private uploaded photos.

## 4. Create build.sh

Create beside manage.py and save using LF, not CRLF, in VS Code:

```bash
#!/usr/bin/env bash
set -o errexit
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
```

Test locally:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
.\.venv\Scripts\python.exe manage.py test planner resilience
```

Commit the intended settings/build/requirements changes on a deployment branch, review, then merge.

## 5. Create PostgreSQL and the web service

In Render, choose New → Postgres. Select a region and plan, then privately copy its Internal Database URL.

Create New → Web Service, connect the GitHub repo and use the same region:

| Setting | Value |
|---|---|
| Repository | d1msums/ecocool |
| Branch | Agreed deployment branch, normally main |
| Runtime | Python |
| Root directory | Blank when manage.py is at repository root |
| Build command | bash build.sh |
| Pre-deploy command | python manage.py migrate --noinput |
| Start command | gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120 |

Set environment variables:

| Key | Value |
|---|---|
| PYTHON_VERSION | Team-tested Python version, e.g. existing 3.12.10 |
| DJANGO_SECRET_KEY | New production secret; not your public example value |
| DJANGO_DEBUG | False |
| DATABASE_URL | PostgreSQL Internal Database URL |
| GOOGLE_MAPS_API_KEY | Restricted browser key if satellite maps are used |
| GEMINI_API_KEY | Private server key only if intentionally enabling external AI |
| MEDIA_ROOT | /var/data/private_media when using the disk below |

Generate a secret using the local get_random_secret_key command in the README. Paste directly into Render, not GitHub/chat.

For local-file report photos, attach a disk at **/var/data**. Only files under that mount persist. The disk is available at runtime, not build/pre-deploy, so do not seed photo uploads in build.sh.

If using cloud object storage instead, configure that backend and skip the local-media disk. Do not leave uploads on the ephemeral service filesystem.

## 6. Initialize hosted data after a successful deployment

In the web service's Render Shell:

```bash
python manage.py createsuperuser
python manage.py shell -c "exec(open('create_elmina.py', encoding='utf-8').read())"
```

Use the printed project ID, replacing 1:

```bash
python manage.py seed_resilience --project 1
python manage.py seed_app_reports --project 1
```

Assign memberships through /admin/ or the main README's shell example. Do not recreate users/seed reset data automatically on every deploy.

Local SQLite accounts, records and photos do not transfer automatically to hosted PostgreSQL. If preserving real data is needed, plan and test a separate backed-up migration rather than committing SQLite.

## 7. Fix links and Maps restrictions

- Add https://YOUR-SERVICE.onrender.com/* to the Maps key's allowed referrers.
- The B2B Resident App link in resilience/templates/resilience/hallmark_header.html points to localhost:8080. Replace it with a separately hosted HTTPS resident-demo URL, or hide it until available.
- The B2C return link in b2c_resident_app/index.html points to localhost:8000/projects/1/resilience/. Update to the real hosted project URL.
- Hosting the static B2C files does not implement a report intake API or synchronization.
- A visitor's localhost always means that visitor's computer, not your server.

## 8. Acceptance checklist

In Render Shell:

```bash
python manage.py check --deploy
```

Review warnings, then test:

- HTTPS, authentication, project membership and viewer restrictions.
- CSS/JS/icons, Maps and fallback geometry.
- Private photo access, including rejection for unauthorized accounts.
- Database and uploaded-file persistence after redeploy.
- Scenario updates, report review, AI failure paths and placeholder behavior.
- Removal or clear labelling of hard-coded "live", cooling, insurance, dispatch and push-delivery claims.

Use fake/sample resident data for the hackathon. External AI answers require human review; do not send sensitive resident content without an appropriate data-handling decision.

## 9. Future updates

Pull GitHub changes locally, install dependencies, migrate and test. Push reviewed changes to the connected deployment branch. With Render automatic deploys enabled, the new code is built and deployed.

Git synchronizes code. Local and hosted databases remain separate.

## Official references

Reviewed 22 October 2026; check current plans before purchasing.

- https://render.com/docs/deploy-django
- https://render.com/docs/deploys
- https://render.com/docs/free
- https://render.com/docs/disks
- https://render.com/docs/python-version
- https://whitenoise.readthedocs.io/en/stable/django.html

