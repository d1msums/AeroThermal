/* Hallmark: present existing data and form state; visual.js owns maps and actions. */
(()=>{
 'use strict';
 const node=document.getElementById('visual-data'),ring=document.getElementById('lake-gauge-fill');
 if(node&&ring){try{const data=JSON.parse(node.textContent),pct=Number(data.metrics?.capacity_pct);if(data.climate&&Number.isFinite(pct))ring.style.strokeDashoffset=String(2*Math.PI*45*(1-Math.max(0,Math.min(100,pct))/100));else ring.setAttribute('hidden','');}catch{ring.setAttribute('hidden','');}}
 document.querySelectorAll('.hm-navigation a').forEach(a=>{if(a.classList.contains('active'))a.setAttribute('aria-current','page');});
 document.querySelectorAll('[data-filter-status]').forEach(button=>{
  button.setAttribute('aria-pressed',String(button.classList.contains('active')));
  button.addEventListener('click',()=>document.querySelectorAll('[data-filter-status]').forEach(b=>b.setAttribute('aria-pressed',String(b.classList.contains('active')))));
 });
 const count=document.getElementById('inbox-count');if(count){count.setAttribute('aria-live','polite');count.setAttribute('aria-atomic','true');}
 // Keep native form validation and POST ownership; prevent a second click in flight.
 document.querySelectorAll('body.hallmark-workspace form[method="post"]').forEach(form=>{
  form.addEventListener('submit',event=>{
   if(form.getAttribute('aria-busy')==='true'){event.preventDefault();return;}
   form.setAttribute('aria-busy','true');
   for(const b of form.querySelectorAll('button:not([type="button"]),input[type="submit"]')){b.dataset.state='loading';b.setAttribute('aria-disabled','true');}
  });
 });
 window.addEventListener('pageshow',()=>{
  document.querySelectorAll('form[aria-busy=true]').forEach(f=>f.removeAttribute('aria-busy'));
  document.querySelectorAll('[data-state=loading][aria-disabled=true]').forEach(b=>{delete b.dataset.state;b.removeAttribute('aria-disabled');});
 });
 // A keyboard/touch target includes its existing location letter and background colour.
 const makeMarkerTargets=()=>document.querySelectorAll('.report-marker').forEach(m=>{m.style.minWidth='44px';m.style.minHeight='44px';m.style.marginLeft='-22px';m.style.marginTop='-22px';m.style.display='grid';m.style.placeItems='center';});
 const map=document.getElementById('visual-map');if(map){makeMarkerTargets();new MutationObserver(makeMarkerTargets).observe(map,{childList:true,subtree:true});}
})();
/* Contextual icons and attention styling; report categories and statuses keep their meaning. */
(()=>{
 'use strict';
 const NS='http://www.w3.org/2000/svg';
 const paths={
  storage:['M12 3C9 7 5 11 5 15a7 7 0 0 0 14 0c0-4-4-8-7-12Z','M8 16a4 4 0 0 0 4 3'],
  buffer:['M6 14a4 4 0 1 1 1-8 5 5 0 0 1 9 1 3.5 3.5 0 1 1 1 7','m8 17-1 3m6-3-1 3m6-3-1 3'],
  active:['M5 21V4','M5 4c4-3 8 3 14 0v10c-6 3-10-3-14 0'],
  shade:['M20 3C8 1 2 7 5 15c4 7 16 4 15-12Z','M4 21 16 8'],
  map:['m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2Z','M9 3v16m6-14v16'],
  apply:['M4 7h16M4 17h16','M8 4v6m8 4v6']
 };
 function icon(kind,cls){const svg=document.createElementNS(NS,'svg');svg.setAttribute('viewBox','0 0 24 24');svg.setAttribute('aria-hidden','true');svg.setAttribute('focusable','false');if(cls)svg.setAttribute('class',cls);for(const d of paths[kind]){const path=document.createElementNS(NS,'path');path.setAttribute('d',d);svg.append(path);}return svg;}
 let active=0;try{active=Number(JSON.parse(document.getElementById('visual-data')?.textContent||'{}').counts?.active)||0;}catch{}
 for(const kind of ['storage','buffer','active','shade']){
  const card=document.querySelector(`.kpi [data-value="${kind}"]`)?.closest('.kpi');if(!card)continue;
  card.dataset.metric=kind;const label=card.querySelector('.kpi-label');
  if(label&&!label.querySelector('.hm-metric-icon')){const badge=document.createElement('span');badge.className='hm-metric-icon';badge.setAttribute('aria-hidden','true');badge.append(icon(kind));label.prepend(badge);}
  if(kind==='active')card.classList.toggle('has-active-reports',active>0);
 }
 const form=document.getElementById('shared-scenario')?.form;
 const button=form?.querySelector('button:not([type="button"])');if(button&&!button.querySelector('svg'))button.prepend(icon('apply'));
 for(const panel of document.querySelectorAll('.map-panel,.inbox-panel')){
  const heading=panel.querySelector('.panel-heading h2');if(heading&&!heading.querySelector('svg'))heading.prepend(icon(panel.classList.contains('map-panel')?'map':'active','hm-heading-icon'));
 }
})();
