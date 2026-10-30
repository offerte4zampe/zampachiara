import test from'node:test';import assert from'node:assert/strict';import history from'../site/assets/price-history.js';import{content,view}from'../worker/canonical-product.mjs';
const now=Date.parse('2026-10-30T12:00:00Z'),rows=Array.from({length:31},(_,i)=>({day:new Date(now-i*86400000).toISOString().slice(0,10),low:10,high:14,last:12,sum:12,count:1}));
test('extended charts require more than thirty observed dates and use real means',()=>{
 assert.equal(history.summarize(rows.slice(0,30),90,now).chart,false);assert.equal(history.summarize(rows,90,now).chart,true);assert.equal(history.summarize(rows,90,now).mean,12);
 const p={name:'Food',brand:'Brand',format:'2 kg',slug:'food',offers:[],history:rows};
 const full=content(p,view(p,null,now)).body;assert(full.includes('Ultimi 90 giorni'));assert(full.includes('media 12,00'));
 const short=content({...p,history:rows.slice(0,30)},view(p,null,now)).body;assert(!short.includes('Ultimi 90 giorni'));assert(short.includes('più di 30 giorni'));
});
