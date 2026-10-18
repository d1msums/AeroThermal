"""Install Hallmark presentation into AeroThermal Visual B2B v2, with or without Taste."""
from pathlib import Path
from datetime import datetime
import argparse,re,shutil
ROOT=Path(__file__).resolve().parent
MARKER='<!-- AEROTHERMAL_HALLMARK_V1 -->'
STATIC=ROOT/'resilience/static/resilience/hallmark'
BASE=ROOT/'resilience/templates/resilience/base.html'
KPIS=ROOT/'resilience/templates/resilience/kpis.html'
DESIGNER=ROOT/'planner/templates/planner/dashboard.html'
VALUE='<div class="kpi-value"><strong data-value="storage">—</strong><span class="unit">%</span></div>'
TASTE_GAUGE='<div class="lake-gauge"><svg viewBox="0 0 104 104" aria-hidden="true" focusable="false"><circle class="lake-gauge-track" cx="52" cy="52" r="45"/><circle id="lake-gauge-fill" cx="52" cy="52" r="45"/></svg>'+VALUE+'</div>'
HEAD=MARKER+'''\n<link rel="stylesheet" href="{% static 'resilience/hallmark/ui.css' %}?v=2">\n'''
SCRIPT='''<script src="{% static 'resilience/hallmark/ui.js' %}?v=2"></script>'''


def no_taste(text):
    # Remove only the two earlier generated presentation links. Keep their files for rollback.
    text=re.sub(r'<link\b[^>]*href="\{% static \'resilience/taste.css\' %\}[^\"]*"[^>]*>', '', text)
    text=re.sub(r'<script\b[^>]*src="\{% static \'resilience/taste.js\' %\}[^\"]*"[^>]*>\s*</script>', '', text)
    return text.replace('<!-- AEROTHERMAL_TASTE_V1 -->','')


def prepare():
    if not (ROOT/'manage.py').is_file():
        raise SystemExit('Put install_hallmark_frontend.py beside manage.py, then run it again.')
    needed=[STATIC/'ui.css',STATIC/'ui.js',STATIC/'tokens.css',STATIC/'fonts/geist-latin.woff2',STATIC/'fonts/space-grotesk-latin.woff2',BASE.with_name('hallmark_header.html'),BASE.with_name('hallmark_gauge.html'),BASE,KPIS]
    for path in needed:
        if not path.is_file():
            raise SystemExit(f'Missing {path.relative_to(ROOT)}. Merge this patch into the Visual B2B project first. No templates changed.')
    base,kpis=BASE.read_text(encoding='utf-8'),KPIS.read_text(encoding='utf-8')
    if MARKER in base:
        if "resilience/hallmark_header.html" not in base or "resilience/hallmark_gauge.html" not in kpis:
            raise SystemExit('Partial Hallmark installation detected. Restore base.html and kpis.html from the same hallmark backup before retrying.')
        changes={}
        for path in (BASE,DESIGNER):
            if not path.is_file():continue
            old=path.read_text(encoding='utf-8')
            updated=old
            for asset in ('ui.css','ui.js'):
                updated=updated.replace("resilience/hallmark/"+asset+"' %}?v=1","resilience/hallmark/"+asset+"' %}?v=2")
            if updated!=old:changes[path]=updated
        if not changes:print('Hallmark refinement 2 already installed. Press Ctrl+F5 for refreshed assets.')
        return changes
    for anchor in ('</head>','</body>',"resilience/visual.js",'id="data-notes"','<aside class="rail">','<main'):
        if anchor not in base:
            raise SystemExit(f'Unexpected base template (missing {anchor}). No templates changed; compare your edits with Visual B2B v2 first.')
    if base.count('<aside class="rail">')!=1:
        raise SystemExit('More than one sidebar found. No templates changed.')
    # The known shell has no nested aside; refuse an ambiguous custom shell.
    start=base.index('<aside class="rail">');end=base.find('</aside>',start)
    if end<0 or '<aside' in base[start+len('<aside class="rail">'):end]:
        raise SystemExit('Sidebar structure differs. No templates changed.')
    base=no_taste(base)
    start=base.index('<aside class="rail">');end=base.index('</aside>',start)+len('</aside>')
    base=base[:start]+"{% include 'resilience/hallmark_header.html' %}"+base[end:]
    match=re.search(r'<body(?: class="([^"]*)")?>',base)
    if not match:
        raise SystemExit('Body tag differs. No templates changed.')
    classes=[c for c in (match.group(1) or '').split() if c!='taste-workspace']
    classes.append('hallmark-workspace')
    base=base[:match.start()]+'<body class="'+' '.join(dict.fromkeys(classes))+'">'+base[match.end():]
    if 'href="#workspace-content"' not in base:
        base=base.replace('<body class="hallmark-workspace">','<body class="hallmark-workspace"><a class="skip-link" href="#workspace-content">Skip to workspace</a>',1)
    if 'id="workspace-content"' not in base:
        base=base.replace('<main>','<main id="workspace-content" tabindex="-1">',1)
    if 'id="workspace-content"' not in base:
        raise SystemExit('Cannot identify the workspace main element. No templates changed.')
    base=base.replace('</head>',HEAD+'</head>',1).replace('</body>',SCRIPT+'</body>',1)
    if 'name="description"' not in base:
        base=base.replace('</head>','<meta name="description" content="AeroThermal township workspace for lake storage, shade planning and incoming resident reports."></head>',1)
    if TASTE_GAUGE in kpis:
        kpis=kpis.replace(TASTE_GAUGE,VALUE,1)
    elif 'id="lake-gauge-fill"' in kpis:
        raise SystemExit('Lake gauge differs from the known Taste patch. No templates changed.')
    if kpis.count(VALUE)!=1:
        raise SystemExit('Lake KPI differs from Visual B2B v2. No templates changed.')
    kpis=kpis.replace(VALUE,"{% include 'resilience/hallmark_gauge.html' %}",1)
    changes={BASE:base,KPIS:kpis}
    if DESIGNER.is_file():
        designer=DESIGNER.read_text(encoding='utf-8')
        if 'designer-visual.js' in designer:
            if '</head>' not in designer:
                raise SystemExit('Tree simulator head not found. No templates changed.')
            if MARKER not in designer:
                changes[DESIGNER]=no_taste(designer).replace('</head>',HEAD+'</head>',1)
        else:
            print('Tree simulator style skipped: its Visual B2B bridge is not installed.')
    return changes


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Validate and list edits without writing templates')
    args=parser.parse_args();changes=prepare()
    if not changes:return
    for path in changes:print('Will update:',path.relative_to(ROOT))
    if args.check:
        print('Compatibility check passed. No templates changed.');return
    backup=ROOT/'hallmark_backups'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    for path in changes:
        dest=backup/path.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
    written=[]
    try:
        for path,value in changes.items():
            path.write_text(value,encoding='utf-8');written.append(path)
    except OSError:
        for path in written:shutil.copy2(backup/path.relative_to(ROOT),path)
        raise
    print('Hallmark installed. Template backups:',backup)
    print('No models, migrations, database, map handlers or permissions changed.')
    print('Restart Django and press Ctrl+F5 in the browser.')

if __name__=='__main__':main()
