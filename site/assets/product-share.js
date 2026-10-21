(function(root){'use strict';
function payload(offer){
 if(!offer||typeof offer.id!=='string'||!offer.id||offer.id.length>200||typeof offer.title!=='string')return null;
 const url=new URL('https://offerte4zampe.it/prodotto');url.searchParams.set('id',offer.id);
 return {title:offer.title+' | Offerte a 4 Zampe',text:'Confronta questo prodotto nei negozi. Prezzi e disponibilità sono rilevamenti da verificare.',url:url.href};
}
async function share(data,nav){try{await nav.share(data);return 'opened'}catch(e){return e?.name==='AbortError'?'cancelled':'unavailable'}}
async function copy(data,nav){try{if(!nav.clipboard?.writeText)return false;await nav.clipboard.writeText(data.url);return true}catch{return false}}
function mount(container,offer,nav=navigator){
 const data=payload(offer);container.replaceChildren();container.hidden=!data;if(!data)return;
 const make=(tag,text)=>{const n=document.createElement(tag);n.textContent=text;return n};
 const status=make('p','Il link apre questa scheda con i dati aggiornati disponibili; non salva i prezzi o le tue impostazioni.');status.className='micro';status.setAttribute('role','status');
 if(typeof nav.share==='function'){const b=make('button','Condividi il prodotto');b.type='button';b.className='btn secondary';b.onclick=async()=>{b.disabled=true;const result=await share(data,nav);status.textContent=result==='opened'?'Strumento di condivisione aperto.':result==='cancelled'?'Condivisione annullata.':'Condivisione non disponibile: puoi copiare il link.';b.disabled=false};container.append(b)}
 const b=make('button','Copia link del prodotto');b.type='button';b.className='btn secondary';
 const label=make('label','Link della scheda prodotto');label.htmlFor='product-share-url';
 const input=make('input','');input.id='product-share-url';input.type='url';input.readOnly=true;input.value=data.url;input.style.width='100%';input.style.boxSizing='border-box';
 b.onclick=async()=>{b.disabled=true;const ok=await copy(data,nav);status.textContent=ok?'Link copiato.':'Copia non disponibile: seleziona il link nel campo e copialo manualmente.';if(!ok){input.focus();input.select()}b.disabled=false};
 container.append(b,label,input,status);
}
const api={payload,share,copy,mount};if(typeof module!=='undefined')module.exports=api;else root.O4ZShare=api;
})(typeof window!=='undefined'?window:this);
