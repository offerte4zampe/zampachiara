/* Manual ration only: arithmetic estimate, never a feeding recommendation. */
(function(root){
'use strict';
function estimate(offer,grams,now=Date.now()){
 const stamp=Date.parse(offer.checked_at),price=Number(offer.price),kg=Number(offer.weight_kg),g=Number(grams);
 if(!offer.available||!Number.isFinite(stamp)||stamp>now+300000||now-stamp>36*3600000)return null;
 if(!Number.isFinite(price)||price<=0||!Number.isFinite(kg)||kg<=0||!Number.isFinite(g)||g<=0||g>100000)return null;
 const daily=price/kg*g/1000;
 return {daily,month30:daily*30,days:kg*1000/g};
}
function mount(offer){
 const details=document.createElement('details'),summary=document.createElement('summary');summary.textContent='Quanto costa al giorno?';details.className='daily-cost';details.append(summary);
 const note=document.createElement('p');note.className='micro';note.textContent='Inserisci la razione totale giornaliera indicata sulla confezione o concordata con il veterinario. Non stimiamo il fabbisogno del tuo animale.';
 const label=document.createElement('label');label.textContent='Razione giornaliera (g) ';
 const input=document.createElement('input');input.type='number';input.min='0.01';input.max='100000';input.step='any';input.inputMode='decimal';label.append(input);
 const output=document.createElement('p');output.className='micro';output.setAttribute('role','status');output.setAttribute('aria-live','polite');
 const money=new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR',minimumFractionDigits:2,maximumFractionDigits:4});
 function render(){const value=estimate(offer,input.value);output.textContent=input.value===''?'Inserisci i grammi: nessuna razione preimpostata.':value?money.format(value.daily)+' al giorno · '+money.format(value.month30)+' per 30 giorni. Solo alimento, spedizione esclusa; prezzo rilevato, non in tempo reale.':'Stima non disponibile: verifica razione, peso netto, disponibilità e data del prezzo.';}
 input.addEventListener('input',render);details.addEventListener('toggle',render);details.append(note,label,output);render();return details;
}
if(typeof module==='object'&&module.exports)module.exports={estimate};
if(root&&root.document){root.O4ZDaily={mount};for(const node of document.querySelectorAll('[data-daily-offer]')){try{node.replaceChildren(mount(JSON.parse(node.dataset.dailyOffer)))}catch{node.textContent='Calcolo giornaliero non disponibile.'}}}
})(typeof window==='undefined'?null:window);
