(function(root){'use strict';
function shipping(o,rules,quantity=1,territory='standard',now=Date.now()){
 const r=rules?.merchants?.[o.merchant_id];if(!r)return {reason:'Condizioni non disponibili'};
 if(!rules.checked_at||!Number.isFinite(Date.parse(rules.checked_at))||now-Date.parse(rules.checked_at)>7*86400000)return {reason:'Condizioni da ricontrollare',rule:r};
 if(territory!=='standard')return {reason:'Località o servizi particolari: verifica nel negozio',rule:r};
 if(!Number.isInteger(quantity)||quantity<1||quantity>10)return {reason:'Quantità non valida',rule:r};
 if(r.conflict)return {reason:'Indicazioni del negozio non coerenti: verifica il checkout',rule:r};
 if(now-Date.parse(o.checked_at)>36*3600000||!Number.isFinite(Date.parse(o.checked_at)))return {reason:'Prezzo non recente: totale non calcolato',rule:r};
 const subtotal=Math.round(o.price*quantity*100)/100;
 if(r.boundary_unknown===subtotal)return {reason:'Soglia esatta da verificare nel negozio',rule:r};
 if(o.shipping_weight_checked_at&&(!Number.isFinite(Date.parse(o.shipping_weight_checked_at))||now-Date.parse(o.shipping_weight_checked_at)>7*86400000))return {reason:'Peso di spedizione da aggiornare',rule:r};
 if(r.max_shipping_weight_kg&&(!(o.shipping_weight_kg>0)||o.shipping_weight_kg*quantity>r.max_shipping_weight_kg))return {reason:'Peso di spedizione mancante o supplementi possibili',rule:r};
 const fee=(r.free_from!==undefined&&subtotal>=r.free_from)||(r.free_above!==undefined&&subtotal>r.free_above)?0:r.fee;
 return {subtotal,fee,total:Math.round((subtotal+fee)*100)/100,rule:r};
}
// The feeds expose comparison/list prices, not a verified reduction basis.
// Keep promotional percentages disabled until an evidenced source is integrated.
function discount(o){return false;}
function merchant(url){
 try{const u=new URL(url);if(u.protocol!=='https:')return '';const shops={'www.isoladeitesori.it':'Isola dei Tesori','isoladeitesori.it':'Isola dei Tesori','www.bauzaar.it':'Bauzaar','bauzaar.it':'Bauzaar','webpet.it':'WebPet','www.webpet.it':'WebPet','animaliapet.eu':'Animaliapet','www.animaliapet.eu':'Animaliapet'};if(shops[u.hostname])return shops[u.hostname];if(u.hostname==='tc.tradetracker.net'&&u.searchParams.get('c')==='16143'&&u.searchParams.get('a')==='518044')return 'Bauzaar';if(u.hostname==='tc.tradetracker.net'&&u.searchParams.get('c')==='31221'&&u.searchParams.get('a')==='518044')return 'Isola dei Tesori';return ''}catch{return ''}
}
function matchKey(o,now=Date.now()){
 const code=String(o.gtin||''),stamp=Date.parse(o.checked_at);if(![8,12,13,14].includes(code.length)||!/^\d+$/.test(code)||new Set(code).size===1||!Number.isFinite(stamp)||now-stamp>36*3600000||stamp>now+300000||!(o.weight_kg>0)||!o.brand?.trim())return '';
 const digits=[...code.slice(0,-1)].reverse();const check=(10-digits.reduce((n,d,i)=>n+Number(d)*(i%2?1:3),0)%10)%10;if(check!==Number(code.at(-1)))return '';
 return JSON.stringify([code.padStart(14,'0'),o.weight_kg,o.brand.trim().toLowerCase()]);
}
function groupOffers(rows,now=Date.now()){
 const index=new Map(),keys=[];
 for(const o of rows){const k=matchKey(o,now);keys.push(k);if(k){let group=index.get(k);if(!group){group={offers:[],merchants:new Set()};index.set(k,group)}group.offers.push(o);group.merchants.add(o.merchant_id)}}
 const used=new Set(),result=[];
 for(let i=0;i<rows.length;i++){const k=keys[i],group=index.get(k);if(!group||group.merchants.size<2){result.push([rows[i]]);continue}if(!used.has(k)){used.add(k);result.push(group.offers)}}
 return result;
}
function reportUrl(o){const p=new URLSearchParams();for(const [key,source,limit] of [['id','id',100],['title','title',240],['shop','merchant',100],['price','price',30],['checked','checked_at',60]])p.set(key,String(o[source]??'').slice(0,limit));return 'segnala-errore.html?'+p;}
const api={shipping,discount,merchant,matchKey,groupOffers,reportUrl};if(typeof module!=='undefined')module.exports=api;else root.O4ZTrade=api;
})(typeof window!=='undefined'?window:this);
