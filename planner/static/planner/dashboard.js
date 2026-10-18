/* EcoCool concept UI v2. Compatible with the ecocool.v1 simulation response. */
const app=document.getElementById('app');
const site=JSON.parse(document.getElementById('site-data').textContent);
const savedLayouts=JSON.parse(document.getElementById('saved-data').textContent);
const canEdit=app.dataset.canEdit==='true';
const $=id=>document.getElementById(id);
const clone=value=>JSON.parse(JSON.stringify(value));
let proposedTrees=[], selectedId=null, addMode=false, busy=false, lastResult=null;
const map=L.map('map',{zoomSnap:.25,zoomDelta:.5,minZoom:16,maxZoom:21,zoomControl:false}).setView([site.site.latitude,site.site.longitude],18);
L.control.zoom({position:'bottomright'}).addTo(map);
L.control.scale({imperial:false,position:'bottomleft'}).addTo(map);
map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
map.attributionControl.addAttribution('EcoCool illustrative geometry');
map.createPane('shadows');map.getPane('shadows').style.zIndex=430;map.getPane('shadows').style.pointerEvents='none';
map.createPane('canopy');map.getPane('canopy').style.zIndex=450;
map.createPane('labels');map.getPane('labels').style.zIndex=460;map.getPane('labels').style.pointerEvents='none';
const geoStyle=f=>{
  const styles={
    land:{color:'#b6c7a1',weight:1.5,fillColor:'#e3eacb',fillOpacity:1},
    planting_area:{color:'#b6c7a1',weight:1,fillColor:'#e3eacb',fillOpacity:.5},
    meadow:{color:'#d0dfb7',weight:1,fillColor:'#d6e3b8',fillOpacity:.8},
    grove:{color:'#d0dcb9',weight:1,fillColor:'#ccdcb2',fillOpacity:.7},
    lake:{color:'#9abdb4',weight:5,fillColor:'#a6d0ca',fillOpacity:1},
    path:{color:'#b7a584',weight:9,lineCap:'round',lineJoin:'round'},
    walkway:{color:'#c4b391',weight:8,lineCap:'round',lineJoin:'round'},
    playground:{color:'#d5ba8b',weight:2,fillColor:'#e7d7b1',fillOpacity:1},
    building:{color:'#97866a',weight:2,fillColor:'#c5b08a',fillOpacity:1}
  };return {...(styles[f.properties.kind]||{color:'#bac6ab',weight:1}),interactive:false};
};
const landscape=L.geoJSON(site.display_geojson,{style:geoStyle,interactive:false}).addTo(map);
for(const f of site.display_geojson.features){
  if(['path','walkway'].includes(f.properties.kind)){
    L.geoJSON(f,{style:{color:'#f3ebd8',weight:f.properties.kind==='path'?5:4,interactive:false},interactive:false}).addTo(map);
  }
}
const bounds=landscape.getBounds();
function fit(){if(bounds.isValid())map.fitBounds(bounds,{padding:[30,30]});}
fit();if(bounds.isValid())map.setMaxBounds(bounds.pad(.8));
$('fit').onclick=fit;
const shadowLayer=L.geoJSON(null,{pane:'shadows',interactive:false,style:{color:'#80709e',weight:1,fillColor:'#8c7cad',fillOpacity:.4,interactive:false}}).addTo(map);
const treeLayer=L.layerGroup().addTo(map),seatLayer=L.layerGroup().addTo(map);
for(const label of site.labels||[]){
  const el=document.createElement('span');el.textContent=label.text;
  L.marker([label.coordinates[1],label.coordinates[0]],{interactive:false,pane:'labels',icon:L.divIcon({className:`park-label ${label.kind}`,html:el,iconSize:[180,20],iconAnchor:[90,10]})}).addTo(map);
}
for(const seat of site.seats){
  L.marker([seat.coordinates[1],seat.coordinates[0]],{interactive:false,icon:L.divIcon({className:'seat-icon',html:'<span></span>',iconSize:[13,6],iconAnchor:[6,3]})}).addTo(seatLayer);
}
function localTime(timestamp){const d=new Date(new Date(timestamp).getTime()+8*3600000);return d.toISOString().slice(0,16);}
$('timestamp').value=localTime(site.default_timestamp);
function message(text,error=false){$('message').textContent=text;$('message').classList.toggle('error',error);}
function treeIcon(tree,isProposed,selected){
  const lat=tree.coordinates[1];
  const mpp=156543.03392*Math.cos(lat*Math.PI/180)/Math.pow(2,map.getZoom());
  const size=Math.max(3,2*tree.canopy_radius_m/mpp);
  const colors=isProposed?['#b8c781','#7f9253','#d8e4aa']:['#90ad7a','#66875c','#b5ca91'];
  const html=`<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M12 18 C20 7 29 10 34 7 C46 7 48 16 55 23 C62 34 53 46 47 52 C36 61 21 55 14 49 C4 41 3 27 12 18Z" fill="${colors[0]}" stroke="${colors[1]}" stroke-width="1.7"/><path d="M17 20 C24 12 32 14 38 13 C46 17 49 24 48 31 C39 32 37 26 29 28 C21 32 13 29 17 20Z" fill="${colors[2]}" opacity=".65"/><path d="M14 38 Q30 51 49 37 Q47 55 30 54 Q18 53 14 38" fill="${colors[1]}" opacity=".22"/><circle cx="32" cy="33" r="2" fill="${colors[1]}"/>${isProposed?'<circle cx="32" cy="32" r="29" fill="none" stroke="#a67e33" stroke-width="1.4" stroke-dasharray="3 3"/>':''}</svg>`;
  return L.divIcon({
  html,
  className: `tree-icon${isProposed ? ' proposed-tree' : ''}${selected ? ' selected' : ''}`,
  iconSize: [size, size],
  iconAnchor: [size / 2, size / 2]
});
}
function renderTrees(){
  treeLayer.clearLayers();
  for(const tree of [...site.existing_trees,...proposedTrees]){
    const proposal=tree.status==='proposed';
    const marker=L.marker([tree.coordinates[1],tree.coordinates[0]],{pane:'canopy',icon:treeIcon(tree,proposal,tree.id===selectedId),draggable:proposal&&canEdit&&!busy,bubblingMouseEvents:false,keyboard:true,title:proposal?'Proposed tree':'Existing tree'}).addTo(treeLayer);
    const tooltip=document.createElement('span');tooltip.textContent=`${proposal?'Proposed':'Existing'} · canopy radius ${tree.canopy_radius_m} m`;
    marker.bindTooltip(tooltip,{direction:'top'});
    if(proposal){
      marker.on('click',e=>{L.DomEvent.stopPropagation(e.originalEvent);if(busy)return;selectedId=tree.id;$('radius').value=tree.canopy_radius_m;$('height').value=tree.canopy_height_m;renderTrees();renderList();});
      marker.on('dragend',()=>{const p=marker.getLatLng();if(!canPlant([p.lng,p.lat])){marker.setLatLng([tree.coordinates[1],tree.coordinates[0]]);message('Place the tree on planting land, outside water and activity areas.',true);return;}tree.coordinates=[p.lng,p.lat];selectedId=tree.id;invalidate();renderList();});
    }
  }
}
map.on('zoomend',renderTrees);
function renderList(){
  $('tree-count').textContent=proposedTrees.length;$('tree-list').replaceChildren();
  if(!proposedTrees.length){const p=document.createElement('div');p.className='empty';p.textContent='Your proposed trees will appear here.';$('tree-list').append(p);}
  proposedTrees.forEach((tree,i)=>{const button=document.createElement('button');button.type='button';button.className=`tree-row${tree.id===selectedId?' selected':''}`;button.disabled=busy;
    const name=document.createElement('span');name.textContent=`Tree ${String(i+1).padStart(2,'0')}`;
    const dims=document.createElement('small');dims.textContent=`R ${tree.canopy_radius_m} m / H ${tree.canopy_height_m} m`;button.append(name,dims);
    button.onclick=()=>{selectedId=tree.id;$('radius').value=tree.canopy_radius_m;$('height').value=tree.canopy_height_m;renderTrees();renderList();};$('tree-list').append(button);});
}
function clearMetrics(){for(const id of ['baseline-value','proposed-value','delta-value'])$(id).textContent='—';$('seat-value').textContent='Shaded seats: —';$('baseline-bar').style.width='0%';$('proposed-bar').style.width='0%';}
function invalidate(){lastResult=null;shadowLayer.clearLayers();clearMetrics();$('result-badge').textContent='Needs a run';message('Design updated. Run comparison to evaluate this layout.');}
function insideRing(p,ring){let inside=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){const a=ring[i],b=ring[j];if((a[1]>p[1])!==(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside;}
function insidePolygon(p,rings){return insideRing(p,rings[0])&&!rings.slice(1).some(r=>insideRing(p,r));}
function contains(p,g){if(g.type==='Polygon')return insidePolygon(p,g.coordinates);if(g.type==='MultiPolygon')return g.coordinates.some(r=>insidePolygon(p,r));return false;}
function canPlant(p){return contains(p,site.planting_area)&&!contains(p,site.lake);}
function dimensions(){const radius=Number($('radius').value),height=Number($('height').value);if(!Number.isFinite(radius)||!Number.isFinite(height)||radius<.5||radius>15||height<1||height>30){message('Use canopy radius 0.5–15 m and model height 1–30 m.',true);return null;}return {radius,height};}
function setAddMode(value){addMode=value;app.classList.toggle('adding',value);if($('add-mode')){$('add-mode').classList.toggle('active',value);$('add-mode').textContent=value?'Finish placing trees':'+ Place a tree';}}
map.on('click',e=>{if(!canEdit||!addMode||busy)return;if(proposedTrees.length>=100){message('Maximum 100 proposed trees.',true);return;}const d=dimensions();if(!d)return;const coordinates=[e.latlng.lng,e.latlng.lat];if(!canPlant(coordinates)){message('Choose planting land, outside the lake, pavilion and play garden.',true);return;}
  const tree={id:`proposed-${crypto.randomUUID()}`,status:'proposed',coordinates,canopy_radius_m:d.radius,canopy_height_m:d.height};proposedTrees.push(tree);selectedId=tree.id;renderTrees();renderList();invalidate();});
function showShadows(){shadowLayer.clearLayers();if(lastResult?.mode==='simulation')shadowLayer.addData(lastResult[$('shadow-mode').value].shadows);}
$('shadow-mode').onchange=showShadows;
$('timestamp').onchange=invalidate;
document.querySelectorAll('[data-hour]').forEach(button=>button.onclick=()=>{if(busy)return;const date=$('timestamp').value.slice(0,10);if(date){$('timestamp').value=`${date}T${button.dataset.hour}:00`;invalidate();}});
if(canEdit){
  $('add-mode').onclick=()=>{setAddMode(!addMode);message(addMode?'Click planting land to add trees. Select a proposed tree to edit it.':'Placement paused. Run your comparison when ready.');};
  $('apply').onclick=()=>{const tree=proposedTrees.find(t=>t.id===selectedId);if(!tree){message('Select a proposed tree first.',true);return;}const d=dimensions();if(!d)return;tree.canopy_radius_m=d.radius;tree.canopy_height_m=d.height;renderTrees();renderList();invalidate();};
  $('remove').onclick=()=>{if(!selectedId){message('Select a proposed tree first.',true);return;}proposedTrees=proposedTrees.filter(t=>t.id!==selectedId);selectedId=null;renderTrees();renderList();invalidate();};
  $('reset').onclick=()=>{if(proposedTrees.length&&!window.confirm('Remove the proposed trees in this unsaved layout?'))return;proposedTrees=[];selectedId=null;renderTrees();renderList();invalidate();};
  $('example').onclick=()=>{if(!site.example_proposed_trees){message('No example layout is configured for this site.');return;}if(proposedTrees.length&&!window.confirm('Replace the unsaved layout with the example?'))return;proposedTrees=clone(site.example_proposed_trees);selectedId=null;setAddMode(false);renderTrees();renderList();invalidate();message('Example layout loaded. Its shade benefit has not yet been calculated.');};
}
function setBusy(value){busy=value;document.querySelectorAll('aside input,aside select,aside button').forEach(el=>el.disabled=value);renderTrees();renderList();}
function present(result){lastResult=result;clearMetrics();showShadows();$('result-badge').textContent=result.mode==='simulation'?'Calculated':result.mode==='mock'?'Engine pending':'Unavailable';
  if(result.mode!=='simulation'){message((result.warnings||[]).join(' ')||'Calculation unavailable.');return;}
  const pct=v=>Number.isFinite(v)?`${v.toFixed(1)}%`:'Not available';
  $('baseline-value').textContent=pct(result.baseline.path_shade_pct);$('proposed-value').textContent=pct(result.proposed.path_shade_pct);
  $('delta-value').textContent=Number.isFinite(result.delta_pp)?`${result.delta_pp>=0?'+':''}${result.delta_pp.toFixed(1)} pp`:'—';
  $('seat-value').textContent=`Shaded seats: ${result.baseline.shaded_seats??'—'} → ${result.proposed.shaded_seats??'—'}`;
  for(const side of ['baseline','proposed']){const v=result[side].path_shade_pct;$(side+'-bar').style.width=`${Number.isFinite(v)?Math.max(0,Math.min(100,v)):0}%`;}
  message(`Comparison complete. ${(result.warnings||[]).join(' ')}`);
}
async function send(action){
  if(!canEdit||busy)return;if(!$('timestamp').value){message('Choose a date and time.',true);return;}
  const name=$('scenario-name').value.trim();if(action==='save'&&!name){message('Give this scenario a name.',true);return;}
  const payload={action,name,timestamp:`${$('timestamp').value}+08:00`,proposed_trees:clone(proposedTrees)};
  setBusy(true);setAddMode(false);message(action==='save'?'Saving scenario…':'Calculating projected shade…');
  try{const response=await fetch(app.dataset.actionUrl,{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json','X-CSRFToken':document.querySelector('[name=csrfmiddlewaretoken]').value},body:JSON.stringify(payload)});
    if(!(response.headers.get('content-type')||'').includes('application/json'))throw new Error('Refresh the page and check your login session.');
    const data=await response.json();if(!response.ok)throw new Error(data.error||`Request failed (${response.status}).`);present(data.result);
    if(action==='save'){sessionStorage.setItem(`ecocool-saved-${app.dataset.projectId}`,JSON.stringify({id:data.scenario_id,mode:data.result.mode}));window.location.reload();}
  }catch(error){message(error.message,true);}finally{setBusy(false);}
}
if(canEdit){$('run').onclick=()=>send('simulate');$('save').onclick=()=>send('save');}
function loadSaved(id,fromSave=false){
  const saved=savedLayouts.find(s=>s.id===id);if(!saved){message('Choose a saved layout.',true);return;}
  if(saved.site_version!==app.dataset.siteVersion){message('This layout uses another site version. Review its data before reuse.',true);return;}
  proposedTrees=clone(saved.input.trees.filter(t=>t.status==='proposed'));$('timestamp').value=localTime(saved.input.timestamp);if($('scenario-name'))$('scenario-name').value=saved.name;
  selectedId=null;setAddMode(false);renderTrees();renderList();invalidate();
  message(fromSave?'Scenario saved. Layout restored; run again to display calculated results.':canEdit?'Saved layout loaded. Run comparison to recalculate.':'Saved layout loaded with view-only access.');
}
$('load').onclick=()=>loadSaved(Number($('saved-select').value));
renderTrees();renderList();
const storageKey=`ecocool-saved-${app.dataset.projectId}`;
const previous=sessionStorage.getItem(storageKey);
if(previous){sessionStorage.removeItem(storageKey);try{const saved=JSON.parse(previous);$('saved-select').value=saved.id;loadSaved(saved.id,true);if(saved.mode==='mock')message('Draft saved with the simulation placeholder. No calculated shade results yet.');}catch{}}
window.addEventListener('resize',()=>map.invalidateSize());
