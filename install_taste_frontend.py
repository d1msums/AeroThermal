"""Apply presentation-only Taste changes to the AeroThermal Visual B2B v2 pack."""
from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parent
MARKER = '<!-- AEROTHERMAL_TASTE_V1 -->'
ASSETS = ROOT / 'resilience/static/resilience'
BASE = ROOT / 'resilience/templates/resilience/base.html'
KPIS = ROOT / 'resilience/templates/resilience/kpis.html'
DESIGNER = ROOT / 'planner/templates/planner/dashboard.html'


def prepare():
    if not (ROOT / 'manage.py').is_file():
        raise SystemExit('Place this script beside manage.py, then run it again.')
    for name in ('taste.css', 'taste.js', 'favicon.svg'):
        if not (ASSETS / name).is_file():
            raise SystemExit(f'Missing {ASSETS / name}. Copy the patch resilience folder first.')
    for path in (BASE, KPIS):
        if not path.is_file():
            raise SystemExit(f'Missing {path}. Install the AeroThermal Visual B2B Update first.')
    base, kpis = BASE.read_text(encoding='utf-8'), KPIS.read_text(encoding='utf-8')
    if MARKER in base:
        print('Taste frontend is already installed. Updated static assets will apply after Ctrl+F5.')
        return {}
    for anchor in ('</head>', '<body>', '<main>', "resilience/visual.js", 'id="data-notes"'):
        if anchor not in base:
            raise SystemExit(f'Unrecognised base template (missing {anchor}). No templates were changed.')
    value = '<div class="kpi-value"><strong data-value="storage">—</strong><span class="unit">%</span></div>'
    if value not in kpis:
        raise SystemExit('Lake KPI differs from Visual B2B v2. No templates were changed.')
    head = MARKER + '''
<meta name="description" content="AeroThermal township planning workspace: lake storage, shade scenarios and resident reports.">
<link rel="icon" type="image/svg+xml" href="{% static 'resilience/favicon.svg' %}">
<link rel="stylesheet" href="{% static 'resilience/taste.css' %}?v=1">
'''
    base = base.replace('</head>', head + '</head>', 1)
    base = base.replace('<body>', '<body class="taste-workspace"><a class="skip-link" href="#workspace-content">Skip to workspace</a>', 1)
    base = base.replace('<main>', '<main id="workspace-content" tabindex="-1">', 1)
    base = base.replace('</body>', '<script src="{% static \'resilience/taste.js\' %}?v=1"></script></body>', 1)
    gauge = '''<div class="lake-gauge"><svg viewBox="0 0 104 104" aria-hidden="true" focusable="false"><circle class="lake-gauge-track" cx="52" cy="52" r="45"/><circle id="lake-gauge-fill" cx="52" cy="52" r="45"/></svg>''' + value + '</div>'
    kpis = kpis.replace(value, gauge, 1)
    changes = {BASE: base, KPIS: kpis}
    if DESIGNER.is_file():
        designer = DESIGNER.read_text(encoding='utf-8')
        if 'designer-visual.js' in designer and MARKER not in designer:
            if '</head>' not in designer:
                raise SystemExit('Tree simulator head not found. No templates were changed.')
            designer = designer.replace('</head>', head + '</head>', 1)
            changes[DESIGNER] = designer
        elif 'designer-visual.js' not in designer:
            print('Tree simulator skipped: run install_visual_b2b.py first to enable its presentation bridge.')
    return changes


def main():
    changes = prepare()
    if not changes:
        return
    backup = ROOT / 'taste_backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    # Validate everything before creating backups or modifying any templates.
    for path in changes:
        target = backup / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for path, content in changes.items():
        path.write_text(content, encoding='utf-8')
        print('Updated:', path.relative_to(ROOT))
    print('Template backups:', backup)
    print('No model, migration, database, API or permissions were changed.')


if __name__ == '__main__':
    main()
