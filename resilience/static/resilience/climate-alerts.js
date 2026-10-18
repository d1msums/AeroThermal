(()=>{'use strict';
 document.querySelectorAll('.ca-hazard').forEach(link=>link.addEventListener('click',()=>{
   const target=document.querySelector(link.getAttribute('href'));if(target)target.open=true;
 }));
 const btn=document.getElementById('ca-fetch-weather'),out=document.getElementById('ca-weather-result');
 const make=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;n.textContent=text;return n;};
 const stamp=s=>{const d=new Date(s);return Number.isNaN(d.getTime())?'Unknown':d.toLocaleString('en-MY',{timeZone:'Asia/Kuala_Lumpur'})+' MYT';};
 if(btn)btn.addEventListener('click',async()=>{
  btn.disabled=true;out.setAttribute('aria-busy','true');out.textContent='Checking national warning feed…';
  const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),12000);
  try{
   const response=await fetch(btn.dataset.url,{credentials:'same-origin',signal:controller.signal,headers:{Accept:'application/json'}});
   if(!response.ok)throw Error('Feed unavailable');const data=await response.json();
   out.replaceChildren(make('span','ca-chip',({disabled:'Feed disabled',unavailable:'Feed unavailable',retrieved:'National feed checked'})[data.status]||'Feed status unknown'));
   out.append(make('p','',data.message||'Local relevance requires review.'));
   if(data.retrieved_at)out.append(make('small','',`Retrieved ${stamp(data.retrieved_at)}`));
   const items=Array.isArray(data.items)?data.items:[];
   if(data.status==='retrieved'&&!items.length)out.append(make('p','','No matching current bulletin was returned. This is not an all-clear for Elmina.'));
   for(const item of items){const box=document.createElement('details');box.className='ca-weather-item';box.append(make('summary','',item.title||'Weather bulletin'),make('p','',item.text||''),make('p','',item.instruction||''),make('small','',`Valid until ${stamp(item.valid_to)} · Check affected locations in the bulletin`));out.append(box);}
  }catch{out.replaceChildren(make('span','ca-chip','Feed unavailable'),make('p','','Current official warning status is unknown. Check METMalaysia directly.'));}
  finally{clearTimeout(timeout);btn.disabled=false;out.removeAttribute('aria-busy');}
 });
})();
