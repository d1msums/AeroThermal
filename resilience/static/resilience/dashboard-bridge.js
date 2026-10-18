/* Replaces only the old climate-widgets.js, after seeding shared project state. */
(()=>{
 const root=document.getElementById('at-climate'),app=document.getElementById('app');if(!root||!app)return;
 const base=`/projects/${app.dataset.projectId}/resilience/`,el=id=>document.getElementById(id),set=(id,v)=>{if(el(id))el(id).textContent=v;},vol=n=>`${Number(n).toLocaleString('en-MY')} m³`;
 const sel=el('at-scenario');if(!sel)return;
 if(!sel.querySelector('[value=wind]')){const op=document.createElement('option');op.value='wind';op.textContent='Windstorm / fallen trees';sel.append(op);}
 let editable=false;
 async function refresh(){
  const r=await fetch(base+'snapshot/',{credentials:'same-origin'});if(!r.ok)throw Error();const d=await r.json();
  editable=d.can_manage;sel.disabled=!editable;sel.value=d.scenario;
  set('at-capacity',`${d.capacity_pct}% Capacity`);el('at-storage').value=d.capacity_pct;
  set('at-condition',d.scenario.toUpperCase()+' · SHARED DEMO');set('at-buffer',vol(d.buffer_m3));set('at-stored',vol(d.stored_m3));
  set('at-water-note',`${d.source}. Saved ${new Date(d.updated_at).toLocaleString()}`);
  el('at-alert').dataset.tone=d.scenario;
  set('at-alert-state','Shared demonstration scenario · not an official forecast');
  set('at-alert-title',d.scenario==='storm'?'Storm preparation review':d.scenario==='drought'?'Conserve the water reserve':d.scenario==='wind'?'Review fallen-tree reports':d.scenario==='heat'?'Review heat exposure and shade':'No storm selected in demo');
  set('at-alert-message',d.scenario==='storm'?`Candidate pre-release: ${vol(d.candidate_m3)}. ${d.release_status}`:d.scenario==='drought'?'No pre-release proposed. Review dry vegetation reports and water reserve.':'Open the audience views for reports, notices and engineering review.');
  set('at-release',d.scenario==='storm'?`Hypothetical buffer after release: ${vol(d.after_buffer_m3)}. No gate command sent.`:'');
  set('at-flood','N/A');set('at-cooling','N/A');el('at-gauge').style.setProperty('--at-score','0%');
  root.querySelector('.at-heading-row p').textContent='SHARED DEMO DATA · No live lake sensor or calibrated thermal model';
  root.querySelector('.at-card:last-child > small').textContent='Flood safety score and cooling reduction require validated models. Saved geometric shade results remain available below.';
 }
 sel.addEventListener('change',async()=>{if(!editable)return;sel.disabled=true;try{const r=await fetch(base+'scenario/',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/x-www-form-urlencoded','Accept':'application/json','X-CSRFToken':document.querySelector('[name=csrfmiddlewaretoken]').value},body:new URLSearchParams({scenario:sel.value})});if(!r.ok)throw Error();await refresh();}catch{set('at-alert-message','Scenario could not be saved. Reload and check your permissions.');}finally{sel.disabled=!editable;}});
 refresh().catch(()=>{sel.disabled=true;set('at-alert-message','Shared project state unavailable. Run seed_resilience and check project membership.');});
})();
