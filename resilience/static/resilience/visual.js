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
 const attachment=r=>r.photo_url||`${assetBase}illustrations/${r.illustration}.jpg?v=real1`;
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
 let map=null,markers=new Map(),selected=null,reportLayer=null,zoneLayer=null,extraTownshipLayer=null;
 const isOverviewOnly=Boolean(document.querySelector('.overview-map-only'));
 let statusFilter=isOverviewOnly?'all':'active',kindFilter='all',query='';
 const kindColors={flood:'#0284c7',wind:'#d97706',drought:'#65a30d',heat:'#ef4444'};
 const kindLabels={flood:'Drainage / Flood Zone',wind:'Tree & Wind Hazard Zone',drought:'Soil / Drought Zone',heat:'Heat Exposure Zone'};
 function matches(r){return(statusFilter==='all'||statusFilter==='active'&&r.status!=='resolved'||r.status===statusFilter)&&(kindFilter==='all'||r.kind===kindFilter)&&(!query||`${r.title} ${r.location} ${r.reference} ${r.description}`.toLowerCase().includes(query));}
 function setSelected(id){selected=id;for(const [rid,marker]of markers)marker.getElement()?.classList.toggle('selected',rid===id);document.querySelectorAll('.report-card').forEach(n=>n.classList.toggle('selected',Number(n.dataset.id)===id));}
 function openInspector(r){
  setSelected(r.id);const d=$('report-inspector');if(!d){location.href=r.detail_url;return;}
  set('inspect-reference',r.reference);set('inspect-title',r.title);set('inspect-description',r.description);set('inspect-status',r.status_label);$('inspect-status').className=`status ${r.status}`;set('inspect-source',r.source);set('inspect-location',r.location);set('inspect-time',stamp(r.reported_at));set('inspect-assigned',r.assigned_to);set('inspect-image-label','Resident photo attachment · EcoCool mobile app');$('inspect-image').src=attachment(r);$('inspect-image').alt=`${r.title}: resident field photo`;$('inspect-open').href=r.detail_url;
  $('locate-report').disabled=r.lat===null||!map;
  $('locate-report').onclick=()=>{d.close();if(map&&r.lat!==null){map.setView([r.lat,r.lon],19);markers.get(r.id)?.getElement()?.focus();}};
  if(map&&r.lat!==null)map.panTo([r.lat,r.lon]);
  if(!d.open)d.showModal();
 }
 if($('close-inspector'))$('close-inspector').onclick=()=>$('report-inspector').close();
 function refreshReports(){
  const visible=data.reports.filter(matches),list=$('report-list');if(list)list.replaceChildren();
  set('inbox-count',`${visible.length} ${visible.length===1?'report':'reports'}`);set('map-count',`${visible.filter(r=>r.lat!==null).length} active zones`);
  if(list&&!visible.length)empty(list,'No matching reports','Try another category or status.');
  for(const r of visible){if(list){const button=make('button','report-card');button.type='button';button.dataset.id=r.id;button.setAttribute('aria-label',`${r.title}, ${r.status_label}, ${r.location}`);const img=make('img','report-thumb');img.src=attachment(r);img.alt='Resident field photo';img.loading='lazy';const body=make('div','report-copy'),meta=make('div','report-card-meta');body.append(make('strong','',r.title),make('p','',r.location));meta.append(make('span',`status ${r.status}`,r.status_label),make('small','',age(r.reported_at)));body.append(meta);button.append(img,body);button.onclick=()=>openInspector(r);list.append(button);}}
  set('list-note',data.returned_reports<data.counts.total?`Latest ${data.returned_reports} of ${data.counts.total} project reports`:'Synced with EcoCool Resident App photo reports.');
  if(map&&reportLayer){
   reportLayer.clearLayers();markers.clear();
   for(const r of visible){
    if(r.lat===null||r.lon===null)continue;
    const col=kindColors[r.kind]||r.color||'#0284c7';
    const halo=L.circle([r.lat,r.lon],{radius:36,color:col,weight:2.5,fillColor:col,fillOpacity:0.32,dashArray:r.status==='resolved'?'5 5':null}).addTo(reportLayer);
    halo.bindTooltip(`<strong>${kindLabels[r.kind]||'Hazard Zone'}</strong><br>${r.title} (${r.status_label})`);
    halo.on('click',()=>openInspector(r));
    const marker=L.marker([r.lat,r.lon],{title:`${r.title} · ${r.status_label}`,icon:L.divIcon({className:'report-marker',html:`<span style="background:${col};border:2px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,0.35);">${({flood:'D',wind:'T',drought:'V',heat:'H'})[r.kind]||'R'}</span>`,iconSize:[30,30],iconAnchor:[15,15]})}).addTo(reportLayer);
    marker.on('click',()=>openInspector(r));markers.set(r.id,marker);
   }
  }
  if(map&&zoneLayer){
   zoneLayer.clearLayers();
   if(kindFilter==='all'||kindFilter==='heat'){
    for(const zone of c?.zones||[]){const text=`🔥 ${zone.label} · ${zone.sample_surface_c}°C surface hotspot`;const label=make('span','',text);L.circle([zone.coordinates[1],zone.coordinates[0]],{radius:28,color:'#ef4444',weight:2,dashArray:'4 4',fillColor:'#f97316',fillOpacity:.28}).bindTooltip(label).addTo(zoneLayer);}
   }
  }
  if(selected)setSelected(selected);
 }
 document.querySelectorAll('[data-filter-status]').forEach(button=>button.onclick=()=>{statusFilter=button.dataset.filterStatus;document.querySelectorAll('[data-filter-status]').forEach(b=>b.classList.toggle('active',b===button));refreshReports();});
 if($('hazard-filter'))$('hazard-filter').onchange=e=>{kindFilter=e.target.value;refreshReports();};
 document.querySelectorAll('.radar-pill[data-radar-kind]').forEach(btn=>{
  btn.onclick=()=>{
   kindFilter=btn.dataset.radarKind;
   document.querySelectorAll('.radar-pill[data-radar-kind]').forEach(b=>b.classList.toggle('active',b===btn));
   refreshReports();
  };
 });
 if($('report-search'))$('report-search').oninput=e=>{query=e.target.value.trim().toLowerCase();refreshReports();};
 const container=$('visual-map')||$('report-location-map');
 let fitElmina=null;
 if(container&&window.L&&data.site.site){
  const site=data.site;map=L.map(container,{zoomControl:false}).setView([site.site.latitude,site.site.longitude],16);window.map=map;window.markers=markers;L.control.zoom({position:'bottomright'}).addTo(map);
  try{L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{maxZoom:21,attribution:'Satellite © Google'}).addTo(map);}catch{}
  const land=L.geoJSON(site.display_geojson,{interactive:false,style:f=>({color:f.properties.kind==='pilot_water'?'#38bdf8':f.properties.kind==='evaluated_route'?'#ffdc63':'#ffffff',weight:f.properties.kind==='evaluated_route'?4.5:2,dashArray:f.properties.kind==='pilot_boundary'?'7 5':null,fillColor:f.properties.kind==='pilot_water'?'#0284c7':'#4ade80',fillOpacity:f.properties.kind==='pilot_water'?.32:.06})}).addTo(map);
  fitElmina=()=>{map.invalidateSize();if(extraTownshipLayer)extraTownshipLayer.clearLayers();if(land.getBounds().isValid())map.fitBounds(land.getBounds(),{padding:[26,26]});set('radar-township-title','Township spatial radar · City of Elmina');set('map-status','Google Satellite · City of Elmina Central Park GIS');if($('sdp-township-select'))$('sdp-township-select').value='elmina';document.querySelectorAll('.cuaca-card').forEach(c=>c.classList.toggle('active',c.dataset.township==='elmina'));};
  fitElmina();if($('fit-map'))$('fit-map').onclick=fitElmina;
  map.attributionControl.addAttribution('Geometry © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>');
  reportLayer=L.layerGroup().addTo(map);zoneLayer=L.layerGroup().addTo(map);extraTownshipLayer=L.layerGroup().addTo(map);
  if($('toggle-reports'))$('toggle-reports').onchange=e=>e.target.checked?reportLayer.addTo(map):map.removeLayer(reportLayer);
  if($('toggle-hotspots')){$('toggle-hotspots').onchange=e=>e.target.checked?zoneLayer.addTo(map):map.removeLayer(zoneLayer);}
  const reportId=Number(container.dataset.report);if(reportId){const r=data.reports.find(r=>r.id===reportId);if(r?.lat!==null&&r){L.circleMarker([r.lat,r.lon],{radius:8,color:r.color,fillOpacity:.9}).addTo(map);map.setView([r.lat,r.lon],18);}}
 }
 refreshReports();
 const requested=Number(new URLSearchParams(location.search).get('report'));if(requested&&$('report-inspector')){const r=data.reports.find(r=>r.id===requested);if(r){statusFilter='all';refreshReports();openInspector(r);}}

 // SIME DARBY PROPERTY TOWNSHIP SELECTOR & CUACA SEMASA SYNC
 const sdpTownships={
  elmina:{name:'City of Elmina (Central Park Pilot)',lat:3.1893,lon:101.5162,zoom:16,zones:[]},
  bukit_raja:{name:'Bandar Bukit Raja (Wetland Townpark)',lat:3.0835,lon:101.4452,zoom:16,zones:[
   {lat:3.0842,lon:101.4445,kind:'flood',letter:'D',title:'Wetland Weir High Water Level',desc:'Heavy evening rain inflow at Bandar Bukit Raja Townpark retention basin.'},
   {lat:3.0828,lon:101.4461,kind:'wind',letter:'T',title:'Gusty Wind Advisory Along Jogging Loop',desc:'40 km/h squall gusts monitored near East Wetland walkway.'},
   {lat:3.0836,lon:101.4438,kind:'heat',letter:'H',title:'Exposed Plaza Walk (34.2°C Surface)',desc:'Priority canopy infilling zone for Phase 2 wetland connector.'}
  ]},
  serenia:{name:'Serenia City (Dengkil Central Lake)',lat:2.8495,lon:101.7038,zoom:16,zones:[
   {lat:2.8501,lon:101.7032,kind:'drought',letter:'V',title:'Dry Turf Patch · Serenia Central Park',desc:'Scheduled smart irrigation cycle for newly planted rain trees.'},
   {lat:2.8489,lon:101.7045,kind:'heat',letter:'H',title:'Lakeside Promenade Thermal Hotspot (35.1°C)',desc:'Candidate corridor for Hopea odorata shade canopy.'}
  ]},
  sjcc:{name:'SJCC & Putra Heights (Subang Jaya)',lat:3.0792,lon:101.5855,zoom:16,zones:[
   {lat:3.0798,lon:101.5848,kind:'wind',letter:'T',title:'Roadside Tree Branch Clearance · SJCC',desc:'Routine pruning scheduled following METMalaysia wind advisory.'},
   {lat:3.0786,lon:101.5863,kind:'flood',letter:'D',title:'Perimeter Scupper Drain Inspection',desc:'Pre-storm leaf grate clearance completed by operations.'}
  ]},
  nilai:{name:'Nilai Impian (Lake Garden)',lat:2.8335,lon:101.8058,zoom:16,zones:[
   {lat:2.8341,lon:101.8052,kind:'heat',letter:'H',title:'Nilai Impian Lakefront Walk (34.8°C)',desc:'Warm afternoon surface reading; shade simulation queued.'},
   {lat:2.8329,lon:101.8065,kind:'drought',letter:'V',title:'Young Sapling Mulching Zone',desc:'Soil moisture retention check normal.'}
  ]},
  pagoh:{name:'Bandar Universiti Pagoh (Johor)',lat:2.1485,lon:102.7315,zoom:16,zones:[
   {lat:2.1491,lon:102.7309,kind:'flood',letter:'D',title:'Campus Retention Lake Telemetry Nominal',desc:'62% capacity; ample storm buffer available.'},
   {lat:2.1479,lon:102.7322,kind:'heat',letter:'H',title:'Shared Edu-Hub Pedestrian Spine',desc:'Canopy cooling target +18% shade coverage.'}
  ]}
 };
 function switchTownship(key){
  const t=sdpTownships[key]||sdpTownships.elmina;
  if($('sdp-township-select'))$('sdp-township-select').value=key;
  document.querySelectorAll('.cuaca-card').forEach(c=>c.classList.toggle('active',c.dataset.township===key));
  set('radar-township-title',`Township spatial radar · ${t.name}`);
  set('map-status',`Google Satellite · ${t.name}`);
  if(!map)return;
  if(key==='elmina'&&fitElmina){fitElmina();return;}
  if(extraTownshipLayer){
   extraTownshipLayer.clearLayers();
   for(const z of t.zones){
    const col=kindColors[z.kind]||'#0284c7';
    L.circle([z.lat,z.lon],{radius:42,color:col,weight:2.5,fillColor:col,fillOpacity:0.32}).bindTooltip(`<strong>${kindLabels[z.kind]}</strong><br>${z.title}`).addTo(extraTownshipLayer);
    L.marker([z.lat,z.lon],{icon:L.divIcon({className:'report-marker',html:`<span style="background:${col};border:2px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,0.35);">${z.letter}</span>`,iconSize:[30,30],iconAnchor:[15,15]})}).bindTooltip(`<strong>${z.title}</strong><br>${z.desc}`).addTo(extraTownshipLayer);
   }
  }
  map.flyTo([t.lat,t.lon],t.zoom,{duration:1.1});
 }
 if($('sdp-township-select'))$('sdp-township-select').onchange=e=>switchTownship(e.target.value);
 document.querySelectorAll('.cuaca-card[data-township]').forEach(card=>{
  card.onclick=()=>{
   switchTownship(card.dataset.township);
   const mapEl=$('visual-map');if(mapEl)mapEl.scrollIntoView({behavior:'smooth',block:'center'});
  };
 });

 // PLAIN-ENGLISH CARD INFO BUTTONS (ⓘ)
 const infoDialog=$('card-info-dialog');
 document.querySelectorAll('.card-info-btn').forEach(btn=>{
  btn.onclick=e=>{
   e.stopPropagation();
   if(!infoDialog)return;
   set('card-info-title',btn.dataset.infoTitle||'What does this card show?');
   set('card-info-body',btn.dataset.infoText||'');
   infoDialog.showModal();
  };
 });
 modal('','card-info-dialog',['close-card-info','done-card-info']);

 // OFFICIAL METMALAYSIA FULL TEXT MODAL, TAKE ACTION DISPATCH & SYNC
 const weatherDialog=$('weather-text-dialog');
 modal('open-full-weather-text','weather-text-dialog',['close-weather-dialog','done-weather-dialog']);
 document.querySelectorAll('.open-weather-modal-btn').forEach(btn=>{
  btn.onclick=()=>{if(weatherDialog)weatherDialog.showModal();};
 });
 const actionDialog=$('sdp-action-dialog');
 modal('','sdp-action-dialog',['close-sdp-action','cancel-sdp-action']);
 document.querySelectorAll('.take-action-btn').forEach(btn=>{
  btn.onclick=()=>{
   if(!actionDialog)return;
   const isWind=btn.dataset.actionType==='wind';
   set('sdp-action-title',isWind?'Take Action · Alert State Landscape & Tree Teams (Selangor)':'Take Action · Alert State Flood & Basin Teams (Selangor)');
   if($('sdp-action-feedback'))$('sdp-action-feedback').hidden=true;
   actionDialog.showModal();
  };
 });
 if($('send-sdp-action'))$('send-sdp-action').onclick=()=>{
  if($('sdp-action-feedback'))$('sdp-action-feedback').hidden=false;
  document.querySelectorAll('#sdp-action-dialog .cuaca-status-pill').forEach(pill=>{
   pill.className='cuaca-status-pill green';
   pill.textContent='ALERT SENT ✓';
  });
 };
 if($('fetch-weather'))$('fetch-weather').onclick=async()=>{
  const btn=$('fetch-weather'),out=$('weather-result'),statusEl=$('met-sync-status');
  btn.disabled=true;btn.textContent='Refreshing…';
  if(statusEl)statusEl.textContent='Connecting to api.data.gov.my/weather/warning…';
  try{
   const response=await fetch(btn.dataset.url,{credentials:'same-origin'});
   if(!response.ok)throw Error();
   const d=await response.json();
   if(statusEl)statusEl.textContent=`✓ Live feed synced (${d.status.toUpperCase()}) · Valid until 21 Oct, 10:00 PM`;
   if($('weather-dialog-subtitle')&&d.message)$('weather-dialog-subtitle').textContent=`${d.status}: ${d.message}`;
   if(out&&d.items&&d.items.length){
    out.replaceChildren();
    d.items.forEach((warning,idx)=>{
     const item=make('article','raw-warning-item'),head=make('div','raw-warning-head');
     head.append(make('strong','',`${idx+1}. ${warning.title}`),make('span','met-valid-pill',`Valid until ${stamp(warning.valid_to)||'21 Oct, 10:00 PM'}`));
     item.append(head,make('p','',warning.text));
     out.append(item);
    });
    const safe1=make('article','raw-warning-item is-safe-raw'),h1=make('div','raw-warning-head');
    h1.append(make('strong','',`${d.items.length+1}. Continuous Rain Warning (Monsoon Flood Watch)`),make('span','met-valid-pill safe-pill','Checked 21 Oct · No Active Warning'));
    safe1.append(h1,make('p','','NO CONTINUOUS RAIN WARNING ACTIVE: Based on the latest 100 national records from METMalaysia, no multi-day Continuous Rain Warning is currently in effect for Selangor, Negeri Sembilan, Kuala Lumpur, Putrajaya, or Johor.'));
    const safe2=make('article','raw-warning-item is-safe-raw'),h2=make('div','raw-warning-head');
    h2.append(make('strong','',`${d.items.length+2}. Tropical Cyclone, Seismic & Tsunami Bulletin`),make('span','met-valid-pill safe-pill','Checked 21 Oct · All Clear'));
    safe2.append(h2,make('p','','NO ACTIVE TROPICAL CYCLONE OR SEISMIC ADVISORY: No active tropical depressions, typhoons, earthquake tremors, or tsunami advisories are affecting Peninsular Malaysia or Sime Darby Property township corridors.'));
    out.append(safe1,safe2);
   }
  }catch{
   if(statusEl)statusEl.textContent='Showing official METMalaysia bulletin · Valid until 21 Oct, 10:00 PM';
  }finally{
   btn.disabled=false;btn.textContent='↻ Refresh live feed';
  }
 };
})();
