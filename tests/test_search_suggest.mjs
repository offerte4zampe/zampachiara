import {createRequire} from 'node:module';
import test from 'node:test';import assert from 'node:assert/strict';
const {candidates}=createRequire(import.meta.url)('../site/assets/search-suggest.js');
const now=Date.parse('2026-10-20T12:00:00Z'),offer={id:'a',title:'Cibo Cane Agnèllo',variant:'2 kg',brand:'Brand',gtin:'123',available:true,checked_at:'2026-10-20T10:00:00Z'};
test('partial multiword and accent-insensitive search, bounded deterministic list without commission ranking',()=>{
 assert.equal(candidates([offer],'ca agn',now).length,1);assert.equal(candidates([offer],'x',now).length,0);
 const rows=Array.from({length:12},(_,i)=>({...offer,id:String(i),title:'Cibo '+String(i).padStart(2,'0'),commission:12-i}));
 assert.equal(candidates(rows,'cibo',now).length,8);assert.deepEqual(candidates(rows,'cibo',now).map(o=>o.id),candidates(rows.map(o=>({...o,commission:999})),'cibo',now).map(o=>o.id));
});
test('unknown, unavailable, stale and future observations cannot become suggestions',()=>{
 for(const patch of [{available:false},{checked_at:'2020-01-01'},{checked_at:'2026-10-21'},{checked_at:'bad'},{title:''}])assert.equal(candidates([{...offer,...patch}],'cibo',now).length,0);
});
test('duplicate labels collapse but explicit formats remain distinct',()=>{
 const rows=candidates([offer,{...offer,id:'b',merchant:'Other'},{...offer,id:'c',variant:'10 kg'}],'cibo',now);
 assert.equal(rows.length,2);assert.deepEqual(new Set(rows.map(o=>o.variant)),new Set(['2 kg','10 kg']));
});
