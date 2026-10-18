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
 if(r.max_shipping_weight_kg&&(!(o.shipping_weight_kg>0)||o.shipping_weight_kg*quantity>r.max_shipping_weight_kg))return {reason:'Peso di spedizione mancante o supplementi possibili',rule:r};
 const fee=(r.free_from!==undefined&&subtotal>=r.free_from)||(r.free_above!==undefined&&subtotal>r.free_above)?0:r.fee;
 return {subtotal,fee,total:Math.round((subtotal+fee)*100)/100,rule:r};
}
function discount(o){return o.previous_price>o.price&&o.price/o.previous_price>=.4;}
const api={shipping,discount};if(typeof module!=='undefined')module.exports=api;else root.O4ZTrade=api;
})(typeof window!=='undefined'?window:this);
