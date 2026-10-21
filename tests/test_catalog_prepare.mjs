import test from 'node:test';import assert from 'node:assert/strict';import {createRequire} from 'node:module';const require=createRequire(import.meta.url),{prepare,identity}=require('../site/assets/catalog-prepare.js');
const offer={id:'a',title:'Crocchette Èlite',price:12,url:'https://shop.test/a',brand:' Brand ',variant:'2 kg',weight_kg:2,gtin:'4006381333931',category:'Cibo',sku:'123'};
test('chunked preparation preserves eligibility, identity groups, text, order and references',async()=>{
 const b={...offer,id:'b',price:10},rows=[offer,{...offer,id:'bad',price:0},b,{...offer,id:'http',url:'http://shop.test'}],before=JSON.stringify(rows);let yields=0,chunks=0;
 const result=await prepare(rows,{chunkSize:2,yieldTask:async()=>{yields++},onChunk:ms=>{assert(ms>=0);chunks++}});
 assert.deepEqual(result.data,[offer,b]);assert.equal(result.data[0],offer);assert.deepEqual(result.identityIndex.get(identity(offer)),[offer,b]);assert.equal(result.searchText.get('a'),[offer.title,offer.variant,offer.brand,offer.category,offer.sku,offer.gtin].join(' ').toLocaleLowerCase('it'));
 assert.equal(yields,1);assert.equal(chunks,2);assert.equal(JSON.stringify(rows),before);
});
test('empty catalog and invalid batch size',async()=>{const r=await prepare([]);assert.equal(r.data.length,0);await assert.rejects(()=>prepare([offer],{chunkSize:0}));});
test('default yield permits a queued timer between preparation chunks',async()=>{let timer=false;const pending=setTimeout(()=>{timer=true},0);await prepare([offer,{...offer,id:'b'}],{chunkSize:1});assert(timer);clearTimeout(pending)});
