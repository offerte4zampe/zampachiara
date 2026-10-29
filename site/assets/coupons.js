/* Expiration is enforced even when a cached document predates the next build. */
(function(){'use strict';
const cards=[...document.querySelectorAll('.coupon')],filters=[...document.querySelectorAll('.filter')];
let shop='all';
function refresh(){
 let count=0;
 for(const card of cards){const until=Date.parse(card.dataset.validUntil);card.hidden=!Number.isFinite(until)||Date.now()>=until||(shop!=='all'&&shop!==card.dataset.shop);if(!card.hidden)count++}
 document.querySelector('.count').textContent=count+(count===1?' codice disponibile':' codici disponibili');
 document.querySelector('#coupon-empty').hidden=count>0;
}
filters.forEach(b=>b.addEventListener('click',()=>{shop=b.dataset.shop;filters.forEach(f=>f.setAttribute('aria-pressed',String(f===b)));refresh()}));
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{
 const card=b.closest('.coupon');refresh();if(card.hidden)return;
 const toast=document.querySelector('.toast');
 try{await navigator.clipboard.writeText(b.dataset.code);toast.textContent='Codice '+b.dataset.code+' copiato. Controlla i requisiti e il totale nel negozio.'}
 catch{toast.textContent='Seleziona e copia il codice '+b.dataset.code+' dal riquadro.'}
}));
document.querySelectorAll('.coupon-visit').forEach(a=>a.addEventListener('click',e=>{refresh();if(a.closest('.coupon').hidden)e.preventDefault()}));
refresh();setInterval(refresh,60000);document.addEventListener('visibilitychange',refresh);
})();
