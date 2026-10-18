"""Run beside manage.py after merging the resilience folder. No migrations."""
import argparse
from datetime import datetime
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if not (ROOT/'manage.py').exists():raise SystemExit('Put this installer beside manage.py before running it.')
    files={name:ROOT/name for name in ['resilience/urls.py','resilience/templates/resilience/base.html','resilience/templates/resilience/hallmark_header.html']}
    required=['resilience/climate_alerts.py','resilience/climate_alert_urls.py','resilience/templates/resilience/climate_alerts.html','resilience/static/resilience/climate-alerts.css','resilience/static/resilience/climate-alerts.js']
    for name in required:
        if not (ROOT/name).exists():raise SystemExit('Missing '+name+'. Merge the supplied resilience folder first.')
    changes={}
    url=files['resilience/urls.py'];text=url.read_text(encoding='utf-8')
    if 'from .climate_alert_urls import urlpatterns as climate_alert_patterns' not in text:
        if 'urlpatterns' not in text:raise SystemExit('Unexpected resilience/urls.py. No changes written.')
        changes[url]=text+'\n# AeroThermal Climate Alerts add-on\nfrom .climate_alert_urls import urlpatterns as climate_alert_patterns\nurlpatterns += climate_alert_patterns\n'
    base=files['resilience/templates/resilience/base.html'];text=base.read_text(encoding='utf-8')
    if 'resilience/climate-alerts.css' not in text:
        if '</head>' not in text:raise SystemExit('Cannot find </head> in base.html. No changes written.')
        text=text.replace('</head>',"<link rel=\"stylesheet\" href=\"{% static 'resilience/climate-alerts.css' %}?v=1\">\n</head>",1)
    header=files['resilience/templates/resilience/hallmark_header.html']
    target=header if 'hallmark_header.html' in text else base
    navtext=target.read_text(encoding='utf-8') if target!=base else text
    if 'resilience:climate_alerts' not in navtext:
        nav='<a class="ca-nav-link {% if audience == \'alerts\' %}active{% endif %}" {% if audience == \'alerts\' %}aria-current="page"{% endif %} href="{% url \'resilience:climate_alerts\' project.id %}"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 3 2 21h20L12 3ZM12 9v5m0 3v1"/></svg>Climate alerts</a>\n'
        anchor='<a href="{% url \'dashboard\' project.id %}"'
        if anchor in navtext:navtext=navtext.replace(anchor,nav+anchor,1)
        elif '</nav>' in navtext:navtext=navtext.replace('</nav>',nav+'</nav>',1)
        else:raise SystemExit('Cannot find workspace navigation. No changes written.')
        if target==base:text=navtext
        else:changes[target]=navtext
    if text!=base.read_text(encoding='utf-8'):changes[base]=text
    if not changes:print('Climate Alerts already installed. Open your project and select Climate alerts.');return
    for path in changes:print(('Would update: ' if args.check else 'Updating: ')+str(path.relative_to(ROOT)))
    if args.check:return
    backup=ROOT/'climate_alert_backups'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    for path,content in changes.items():
        dest=backup/path.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
        path.write_text(content,encoding='utf-8')
    print('Installed. Backups: '+str(backup));print('Restart Django, refresh the browser, then select Climate alerts.')

if __name__=='__main__':main()
