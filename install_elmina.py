"""Run from the ecocool folder. Patches the known dashboard safely, once."""
from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parent
target = root / 'planner/templates/planner/dashboard.html'
marker = '<!-- ECOCOOL_ELMINA_MAP_V1 -->'
if not target.exists():
    raise SystemExit('Cannot find planner/templates/planner/dashboard.html. Put this script beside manage.py.')
text = target.read_text(encoding='utf-8')
if marker in text:
    print('Elmina script block is already installed; no change needed.')
else:
    anchors = ['id="map"', 'planner/dashboard.js', 'site|json_script', '{% load static %}', '</body>']
    missing = [anchor for anchor in anchors if anchor not in text]
    if missing:
        raise SystemExit('Dashboard differs from the visual-upgrade version. No files changed. Missing: ' + ', '.join(missing))
    if text.index('planner/dashboard.js') > text.index('</body>'):
        raise SystemExit('Unexpected script order. No files changed.')
    backup = root / 'elmina_backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True)
    (backup / 'dashboard.html').write_text(text, encoding='utf-8')
    block = '''
<!-- ECOCOOL_ELMINA_MAP_V1 -->
{% if site.basemap.provider == "google" %}
{{ ecocool_map_config|json_script:"ecocool-map-config" }}
<script src="{% static 'planner/vendor/Leaflet.GoogleMutant.js' %}"></script>
<script src="{% static 'planner/elmina-map.js' %}?v=elmina1"></script>
{% endif %}
'''
    target.write_text(text.replace('</body>', block + '</body>', 1), encoding='utf-8')
    print('Updated:', target)
    print('Original template backup:', backup / 'dashboard.html')
