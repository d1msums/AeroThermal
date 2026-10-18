"""Run beside manage.py after adding the app and its URL include."""
from pathlib import Path
from datetime import datetime
root=Path(__file__).resolve().parent
p=root/'planner/templates/planner/dashboard.html'
s=p.read_text(encoding='utf-8')
marker='<!-- AEROTHERMAL_STAKEHOLDERS_V1 -->'
if marker in s:
    print('Already installed. No template changes.')
else:
    for anchor in ['</head>','</body>','planner/dashboard.js','{% load static %}']:
        if anchor not in s: raise SystemExit('Unexpected dashboard template. No change: missing '+anchor)
    target="{% static 'planner/climate-widgets.js' %}"
    if target not in s: raise SystemExit('Cannot find climate-widgets.js reference. Review the template; no change made.')
    backup=root/'stakeholder_backups'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True)
    (backup/'dashboard.html').write_text(s,encoding='utf-8')
    s=s.replace(target,"{% static 'resilience/dashboard-bridge.js' %}",1)
    s=s.replace('</head>', '<style>.stakeholder-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}.stakeholder-tabs a{padding:9px 12px;border:1px solid #587b50;border-radius:8px;background:#153b2a;color:#d8f0cb;text-decoration:none;font-size:12px}</style>\n</head>',1)
    s=s.replace('</body>',marker+'\n<script src="{% static \'resilience/dashboard-links.js\' %}?v=1"></script>\n</body>',1)
    p.write_text(s,encoding='utf-8')
    print('Dashboard navigation and shared climate data bridge installed.')
    print('Backup:',backup/'dashboard.html')
