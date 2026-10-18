(()=>{
 'use strict';
 const node=document.getElementById('visual-data');if(!node)return;
 const data=JSON.parse(node.textContent);if(!data||typeof data!=='object'||!data.counts)return;
 const $=id=>document.getElementById(id),num=n=>Number(n).toLocaleString('en-MY',{maximumFractionDigits:1}),vol=n=>`${num(n)} m³`;
 const make=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
 const set=(id,text)=>{if($(id))$(id).textContent=text;};
 const value=(name,text)=>document.querySelectorAll(`[data-value="${name}"]`).forEach(el=>el.textContent=text);
 const stamp=s=>{const d=new Date(s);return Number.isNaN(d.getTime())?'—':d.toLocaleString('en-MY',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit',timeZone:'Asia/Kuala_Lumpur'});};
 const age=s=>{const mins=Math.max(0,Math.floor((Date.now()-new Date(s).getTime())/60000));return mins<60?`${mins}m ago`:mins<1440?`${Math.floor(mins/60)}h ago`:`${Math.floor(mins/1440)}d ago`;};
 const assetBase=new URL('.',document.currentScript.src).href;
 const attachment=r=>r.photo_url||`${assetBase}illustrations/${r.illustration}.svg`;
 function modal(openId,dialogId,closeIds){const d=$(dialogId);if(!d)return;if($(openId))$(openId).onclick=()=>d.showModal();for(const id of closeIds)if($(id))$(id).onclick=()=>d.close();}
 modal('open-notes','data-notes',['close-notes','done-notes']);modal('open-notice','notice-dialog',['close-notice']);
 if($('shared-scenario')&&data.climate)$('shared-scenario').value=data.climate.scenario;
 const c=data.climate,m=data.metrics,counts=data.counts;
 value('storage',c?num(m.capacity_pct):'—');value('buffer',c?num(m.buffer_m3):'—');value('active',counts.active);value('total',counts.total);
 value('shade',data.latest_shade?num(data.latest_shade.shade):'—');set('shade-unit',data.latest_shade?'%':'');
 if(c){if($('lake-progress'))$('lake-progress').value=m.capacity_pct;if($('buffer-fill'))$('buffer-fill').style.width=`${100-m.capacity_pct}%`;set('storage-caption',`${vol(c.stored)} of ${vol(c.capacity)}`);}
 set('report-caption',`${counts.open} new · ${counts.in_progress} in progress`);
 if(data.latest_shade)set('shade-caption',`${data.latest_shade.name} · ${stamp(data.latest_shade.timestamp)}`);
 for(const [id,key]of [['count-active','active'],['count-open','open'],['count-progress','in_progress'],['count-resolved','resolved'],['count-all','total']])set(id,counts[key]);
 const colors={open:'#d8b589',in_progress:'#9dbbc0',resolved:'#b7ce9c'};
 if($('status-donut')){
  let start=0,stops=[];for(const s of ['open','in_progress','resolved']){const end=start+(counts.total?counts[s]/counts.total*100:0);stops.push(`${colors[s]} ${start}% ${end}%`);start=end;}
  $('status-donut').style.background=counts.total?`conic-gradient(${stops.join(',')})`:'#edf1e8';
  for(const [s,label]of [['open','New'],['in_progress','In progress'],['resolved','Resolved']]){const row=make('div','donut-legend-row'),dot=make('i','dot');dot.style.background=colors[s];row.append(dot,make('span','',label),make('b','',counts[s]));$('status-legend').append(row);}
 }
 const svgNS='http://www.w3.org/2000/svg';
 function svg(tag,attrs,text){const n=document.createElementNS(svgNS,tag);for(const [k,v]of Object.entries(attrs||{}))n.setAttribute(k,String(v));if(text!==undefined)n.textContent=text;return n;}
 function empty(target,title,description){const n=make('div','empty-state');n.append(make('strong','',title),make('p','',description));target.append(n);}
 if($('storage-chart')){
  const points=(c?.history||[]).filter(p=>Number.isFinite(p.storage_pct)&&p.storage_pct>=0&&p.storage_pct<=100);
  if(points.length<2)empty($('storage-chart'),'No reference series','Add a storage history to draw this chart.');
  else{const chart=svg('svg',{viewBox:'0 0 500 180',role:'img','aria-label':'Synthetic reference storage percentage over six demo points'}),left=35,right=480,top=15,bottom=140;
   for(const y of [0,50,100]){const yy=bottom-y/100*(bottom-top);chart.append(svg('line',{x1:left,y1:yy,x2:right,y2:yy,stroke:'#edf1e7','stroke-width':1}),svg('text',{x:4,y:yy+4,class:'chart-label'},`${y}%`));}
   const xy=points.map((p,i)=>[left+i/(points.length-1)*(right-left),bottom-p.storage_pct/100*(bottom-top)]),line=xy.map((p,i)=>`${i?'L':'M'}${p[0]},${p[1]}`).join(' ');
   chart.append(svg('path',{d:`${line} L${right},${bottom} L${left},${bottom} Z`,fill:'#eef5e7',stroke:'none'}),svg('path',{d:line,stroke:'#91b777','stroke-width':2,fill:'none'}));
   xy.forEach((p,i)=>{const dot=svg('circle',{cx:p[0],cy:p[1],r:3,fill:'#8bb06f',stroke:'white','stroke-width':1});dot.append(svg('title',{},`${points[i].label}: ${points[i].storage_pct}% (demo)`));chart.append(dot);if(i===0||i===points.length-1)chart.append(svg('text',{x:p[0],y:168,'text-anchor':i?'end':'start',class:'chart-label'},points[i].label));});$('storage-chart').append(chart);}
 }
 if($('shade-chart')){
  const rows=data.scenarios.filter(r=>r.shade!==null).slice(0,4);
  if(!rows.length)empty($('shade-chart'),'No calculated run yet','Review saved shade evidence in Landscape review.');
  for(const row of rows){const box=make('div','shade-run'),head=make('div','shade-run-label'),name=make('span','',row.name);name.title=row.name;head.append(name,make('b','',`${num(row.shade)}%`));const track=make('div','shade-run-track'),bar=make('span');bar.style.width=`${Math.max(0,Math.min(100,row.shade))}%`;track.append(bar);box.append(head,track,make('small','',`${stamp(row.timestamp)} · ${row.site_version}`));$('shade-chart').append(box);}
 }
 if($('storage-balance')&&c){
  for(const [label,stored,inflow]of [['Current storage',c.stored,0],['After candidate release',c.stored-m.candidate_m3,0],['After assumed storm inflow',c.stored-m.candidate_m3,c.inflow]]){
   const row=make('div','balance-row'),head=make('div','balance-label'),track=make('div','balance-track'),a=make('span','balance-stored'),b=make('span','balance-inflow');head.append(make('span','',label),make('b','',vol(stored+inflow)));a.style.width=`${Math.min(100,stored/c.capacity*100)}%`;b.style.width=`${Math.min(100-stored/c.capacity*100,inflow/c.capacity*100)}%`;track.append(a,b);row.append(head,track);$('storage-balance').append(row);
  }set('candidate-release',vol(m.candidate_m3));
 }
 let map=null,markers=new Map(),selected=null,reportLayer=null,zoneLayer=null;
 let statusFilter='active',kindFilter='all',query='';
 function matches(r){return(statusFilter==='all'||statusFilter==='active'&&r.status!=='resolved'||r.status===statusFilter)&&(kindFilter==='all'||r.kind===kindFilter)&&(!query||`${r.title} ${r.location} ${r.reference} ${r.description}`.toLowerCase().includes(query));}
 function setSelected(id){selected=id;for(const [rid,marker]of markers)marker.getElement()?.classList.toggle('selected',rid===id);document.querySelectorAll('.report-card').forEach(n=>n.classList.toggle('selected',Number(n.dataset.id)===id));}
 function openInspector(r){
  setSelected(r.id);const d=$('report-inspector');if(!d){location.href=r.detail_url;return;}
  set('inspect-reference',r.reference);set('inspect-title',r.title);set('inspect-description',r.description);set('inspect-status',r.status_label);$('inspect-status').className=`status ${r.status}`;set('inspect-source',r.source);set('inspect-location',r.location);set('inspect-time',stamp(r.reported_at));set('inspect-assigned',r.assigned_to);set('inspect-image-label',r.photo_url?'Report attachment':'Sample illustration · no photo attached');$('inspect-image').src=attachment(r);$('inspect-image').alt=r.photo_url?'Stored report attachment':`${r.title}: sample illustration`;$('inspect-open').href=r.detail_url;
  $('locate-report').disabled=r.lat===null||!map;
  $('locate-report').onclick=()=>{d.close();if(map&&r.lat!==null){map.setView([r.lat,r.lon],19);markers.get(r.id)?.getElement()?.focus();}};
  if(map&&r.lat!==null)map.panTo([r.lat,r.lon]);
  if(!d.open)d.showModal();
 }
 if($('close-inspector'))$('close-inspector').onclick=()=>$('report-inspector').close();
 function refreshReports(){
  const visible=data.reports.filter(matches),list=$('report-list');if(list)list.replaceChildren();
  set('inbox-count',`${visible.length} ${visible.length===1?'report':'reports'}`);set('map-count',`${visible.filter(r=>r.lat!==null).length} locations`);
  if(list&&!visible.length)empty(list,'No matching reports','Try another category or status.');
  for(const r of visible){if(list){const button=make('button','report-card');button.type='button';button.dataset.id=r.id;button.setAttribute('aria-label',`${r.title}, ${r.status_label}, ${r.location}`);const img=make('img','report-thumb');img.src=attachment(r);img.alt=r.photo_url?'Report attachment':'Sample illustration';img.loading='lazy';const body=make('div','report-copy'),meta=make('div','report-card-meta');body.append(make('strong','',r.title),make('p','',r.location));meta.append(make('span',`status ${r.status}`,r.status_label),make('small','',age(r.reported_at)));body.append(meta);button.append(img,body);button.onclick=()=>openInspector(r);list.append(button);}}
  set('list-note',data.returned_reports<data.counts.total?`Latest ${data.returned_reports} of ${data.counts.total} project reports`:'Sample inputs are labelled in the report inspector.');
  if(map&&reportLayer){reportLayer.clearLayers();markers.clear();for(const r of visible){if(r.lat===null||r.lon===null)continue;const marker=L.marker([r.lat,r.lon],{title:`${r.title} · ${r.status_label}`,icon:L.divIcon({className:'report-marker',html:`<span style="background:${r.color}">${({flood:'D',wind:'T',drought:'V',heat:'H'})[r.kind]||'R'}</span>`,iconSize:[28,28],iconAnchor:[14,14]})}).addTo(reportLayer);marker.on('click',()=>openInspector(r));markers.set(r.id,marker);}}
  if(selected)setSelected(selected);
 }
 document.querySelectorAll('[data-filter-status]').forEach(button=>button.onclick=()=>{statusFilter=button.dataset.filterStatus;document.querySelectorAll('[data-filter-status]').forEach(b=>b.classList.toggle('active',b===button));refreshReports();});
 if($('hazard-filter'))$('hazard-filter').onchange=e=>{kindFilter=e.target.value;refreshReports();};
 if($('report-search'))$('report-search').oninput=e=>{query=e.target.value.trim().toLowerCase();refreshReports();};
 const container=$('visual-map')||$('report-location-map');
 if(container&&window.L&&data.site.site){
  const site=data.site;map=L.map(container,{zoomControl:false}).setView([site.site.latitude,site.site.longitude],16);L.control.zoom({position:'bottomright'}).addTo(map);
  const land=L.geoJSON(site.display_geojson,{interactive:false,style:f=>({color:f.properties.kind==='pilot_water'?'#74b8c2':f.properties.kind==='evaluated_route'?'#f0cc70':'#b4c5aa',weight:f.properties.kind==='evaluated_route'?4:1.5,fillColor:f.properties.kind==='pilot_water'?'#aad1d1':'#e3e9d7',fillOpacity:f.properties.kind==='pilot_water'?.25:.04})}).addTo(map);
  const fit=()=>{map.invalidateSize();if(land.getBounds().isValid())map.fitBounds(land.getBounds(),{padding:[26,26]});};fit();if($('fit-map'))$('fit-map').onclick=fit;
  map.attributionControl.addAttribution('Geometry © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>');
  set('map-status','Vector reference');reportLayer=L.layerGroup().addTo(map);zoneLayer=L.layerGroup();
  for(const zone of c?.zones||[]){const text=`${zone.label} · ${zone.sample_surface_c}°C sample surface value`;const label=make('span','',text);L.circle([zone.coordinates[1],zone.coordinates[0]],{radius:28,color:'#ca705b',weight:1,fillColor:'#d5926a',fillOpacity:.25}).bindTooltip(label).addTo(zoneLayer);}
  if($('toggle-reports'))$('toggle-reports').onchange=e=>e.target.checked?reportLayer.addTo(map):map.removeLayer(reportLayer);
  if($('toggle-hotspots'))$('toggle-hotspots').onchange=e=>e.target.checked?zoneLayer.addTo(map):map.removeLayer(zoneLayer);
  let cfg={};try{cfg=JSON.parse($('ecocool-map-config')?.textContent||'{}')||{};}catch{}
  if(cfg.google_maps_api_key){let layer=null,failed=false;window.gm_authFailure=()=>{failed=true;if(layer)map.removeLayer(layer);set('map-status','Satellite unavailable · vector reference');};window.aerothermalVisualMapReady=()=>{if(failed)return;layer=L.gridLayer.googleMutant({type:'satellite',maxZoom:21}).on('load',()=>{if(!failed)set('map-status','Google satellite · OSM reference');}).addTo(map);};const script=document.createElement('script');script.src='https://maps.googleapis.com/maps/api/js?'+new URLSearchParams({key:cfg.google_maps_api_key,callback:'aerothermalVisualMapReady',loading:'async',v:'weekly'});script.async=true;script.onerror=()=>set('map-status','Satellite unavailable · vector reference');document.head.append(script);}
  const reportId=Number(container.dataset.report);if(reportId){const r=data.reports.find(r=>r.id===reportId);if(r?.lat!==null&&r){L.circleMarker([r.lat,r.lon],{radius:8,color:r.color,fillOpacity:.9}).addTo(map);map.setView([r.lat,r.lon],18);}}
 }
 refreshReports();
 const requested=Number(new URLSearchParams(location.search).get('report'));if(requested&&$('report-inspector')){const r=data.reports.find(r=>r.id===requested);if(r){statusFilter='all';refreshReports();openInspector(r);}}
 if($('fetch-weather'))$('fetch-weather').onclick=async()=>{const btn=$('fetch-weather'),out=$('weather-result');btn.disabled=true;out.textContent='Checking official warning feed…';try{const response=await fetch(btn.dataset.url,{credentials:'same-origin'});if(!response.ok)throw Error();const d=await response.json();out.replaceChildren(make('p','',`${d.status}: ${d.message}`));for(const warning of d.items||[]){const item=make('article');item.append(make('strong','',warning.title),make('p','',warning.text),make('small','',`Valid until ${stamp(warning.valid_to)}`));out.append(item);}}catch{out.textContent='Feed unavailable. Check official warnings directly.';}finally{btn.disabled=false;}};
})();
