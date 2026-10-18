/* Presentation enhancements only. Existing visual.js owns the data and actions. */
(()=>{
 'use strict';
 const node=document.getElementById('visual-data'),ring=document.getElementById('lake-gauge-fill');
 if(node&&ring){try{const data=JSON.parse(node.textContent),pct=Number(data.metrics?.capacity_pct);if(data.climate&&Number.isFinite(pct)){ring.style.strokeDashoffset=String(2*Math.PI*45*(1-Math.max(0,Math.min(100,pct))/100));}else{ring.setAttribute('hidden','');}}catch{ring.setAttribute('hidden','');}}
 document.querySelectorAll('.rail-nav a').forEach(a=>{if(a.classList.contains('active'))a.setAttribute('aria-current','page');});
 // Keep status selection available to screen readers as the inbox is filtered.
 document.querySelectorAll('[data-filter-status]').forEach(button=>{
  button.setAttribute('aria-pressed',String(button.classList.contains('active')));
  button.addEventListener('click',()=>document.querySelectorAll('[data-filter-status]').forEach(b=>b.setAttribute('aria-pressed',String(b.classList.contains('active')))));
 });
 const count=document.getElementById('inbox-count');if(count){count.setAttribute('aria-live','polite');count.setAttribute('aria-atomic','true');}
})();
