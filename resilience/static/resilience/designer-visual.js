(()=>{
 const app=document.getElementById('app');if(!app)return;
 const heading=document.querySelector('.page-heading h1');if(heading)heading.textContent='Tree simulator';
 const nav=document.querySelector('.stakeholder-tabs');if(nav){const current=document.createElement('a');current.className='current';current.textContent='Tree simulator';current.href='#map';nav.append(current);}
 const method=document.querySelector('.method');if(method){const details=document.createElement('details');details.className='model-details';const summary=document.createElement('summary');summary.textContent='Model assumptions';method.before(details);details.append(summary,method);}
 const footer=document.querySelector('main>footer');if(footer){const details=document.createElement('details');details.className='source-details';const summary=document.createElement('summary');summary.textContent='Data sources';const p=document.createElement('p');p.textContent=footer.textContent;details.append(summary,p);footer.replaceChildren(details);}
 // Preserve full model notes in a disclosure; keep actionable errors fully visible.
 if(typeof message==='function'){
  const target=document.getElementById('message'),details=document.createElement('details');details.className='model-details';const summary=document.createElement('summary'),body=document.createElement('p');summary.textContent='Calculation notes';details.append(summary,body);target.after(details);
  const originalMessage=message;
  message=function(text,error=false){const full=String(text);const first=full.match(/^.*?[.!?](?:\s|$)/)?.[0]?.trim()||full;const short=first.length<180?first:full.slice(0,160)+'…';originalMessage(error?full:short,error);body.textContent=full;details.hidden=error||full===short;};
  message(target.textContent,target.classList.contains('error'));
 }
})();
