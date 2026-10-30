import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../worker/index.mjs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{productUrl}=require('../site/assets/trade.js');
test('legacy home and catalog routes redirect once, preserving search and fragments',async()=>{
 for(const method of ['GET','HEAD'])for(const [old,target] of [['/index.html','/'],['/confronta-cibo.html','/confronta-cibo']]){
  const r=await worker.fetch(new Request('https://offerte4zampe.it'+old+'?q=cat&shop=WebPet',{method}),{ASSETS:{fetch(){throw Error('Must redirect before assets')}}},{});
  assert.equal(r.status,301);assert.equal(r.headers.get('Location'),'https://offerte4zampe.it'+target+'?q=cat&shop=WebPet');
 }
});
test('known product links bypass legacy redirects; unsafe slugs use encoded compatibility route',()=>{
 assert.equal(productUrl({id:'a:1',product_slug:'food-2-kg'}),'/prodotto/food-2-kg');
 assert.equal(productUrl({id:'a:1',product_slug:'//evil.test'}),'/prodotto.html?id=a%3A1');
});
