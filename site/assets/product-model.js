(function(root){'use strict';
const trade=typeof module!=='undefined'&&module.exports?require('./trade.js'):root.O4ZTrade;
function productView(catalog,id,now=Date.now()){
 const offers=catalog.offers||[],seed=offers.find(o=>o.id===id);if(!seed)return null;
 const key=trade.matchKey(seed,now),rows=key?offers.filter(o=>trade.matchKey(o,now)===key):[seed];
 const sources=new Map((catalog.sources||[]).map(s=>[s.id,s]));
 for(const o of rows)if(!sources.has(o.merchant_id))sources.set(o.merchant_id,{id:o.merchant_id,name:o.merchant,status:'unknown'});
 const shops=[...sources.values()].map(source=>{
  const matches=rows.filter(o=>o.merchant_id===source.id).sort((a,b)=>Number(b.available)-Number(a.available)||a.price-b.price);
  const live=matches.filter(o=>{const stamp=Date.parse(o.checked_at);return Number.isFinite(stamp)&&now-stamp<=36*3600000&&stamp<=now+300000&&Number.isFinite(o.price)&&o.price>0});
  return {source,offers:live,state:live.length?'listed':matches.length?'stale':source.status!=='ok'?'unknown':key?'missing':'unmatched'};
 });
 shops.sort((a,b)=>{const price=s=>Math.min(...s.offers.filter(o=>o.available).map(o=>o.price));return price(a)-price(b)||String(a.source.name).localeCompare(String(b.source.name),'it')});
 return {seed,exact:Boolean(key),shops};
}
const api={productView};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.O4ZProduct=api;
})(typeof window!=='undefined'?window:null);
