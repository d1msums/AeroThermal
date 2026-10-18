"""Patch the current designer safely. Does not change models, views or site data."""
from pathlib import Path
from datetime import datetime
import re
root=Path(__file__).resolve().parent
path=root/'planner/templates/planner/dashboard.html'
s=path.read_text(encoding='utf-8')
marker='<!-- AEROTHERMAL_VISUAL_B2B_V2 -->'
if marker in s:
    print('Visual B2B patch already installed. No template changes.')
    raise SystemExit(0)
for anchor in ['</head>','</body>','planner/dashboard.js','{% load static %}']:
    if anchor not in s:raise SystemExit('Unexpected dashboard template. No changes: missing '+anchor)
backup=root/'visual_backups'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
backup.mkdir(parents=True)
(backup/'dashboard.html').write_text(s,encoding='utf-8')
s=s.replace("{% static 'planner/climate-widgets.js' %}","{% static 'resilience/dashboard-bridge.js' %}")
s=re.sub(r'<nav class="dashboard-nav".*?</nav>','',s,count=1,flags=re.S)
s=s.replace('</head>','<link rel="stylesheet" href="{% static \'resilience/designer-visual.css\' %}?v=2">\n</head>',1)
links="{% static 'resilience/dashboard-links.js' %}"
if links not in s:s=s.replace('</body>','<script src="'+links+'?v=2"></script>\n</body>',1)
s=s.replace('</body>',marker+'\n<script src="{% static \'resilience/designer-visual.js\' %}?v=2"></script>\n</body>',1)
s=s.replace("resilience/dashboard-links.js' %}?v=1","resilience/dashboard-links.js' %}?v=2")
path.write_text(s,encoding='utf-8')
print('Installed visual B2B navigation and tree-designer polish.')
print('Backup:',backup/'dashboard.html')
