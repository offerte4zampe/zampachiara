import test from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import worker from '../worker/index.mjs';
const trade=createRequire(import.meta.url)('../site/assets/trade.js');
test('clean page redirects use 301 and retain query strings',async()=>{
 for(const [path,target] of [['/index.html?q=food','/?q=food'],['/confronta-cibo.html?brand=A','/confronta-cibo?brand=A'],['/offerte/index.html','/offerte/']]){
  for(const method of ['GET','HEAD']){
   const r=await worker.fetch(new Request('https://offerte4zampe.it'+path,{method}),{});
   assert.equal(r.status,301);assert.equal(r.headers.get('Location'),'https://offerte4zampe.it'+target);
  }
 }
});
test('verification token is served intact and clean pages do not loop',async()=>{
 const env={ASSETS:{fetch:async()=>new Response('asset')}};
 for(const path of ['/google123.html','/confronta-cibo'])assert.equal(await(await worker.fetch(new Request('https://offerte4zampe.it'+path),env)).text(),'asset');
});
test('product links use canonical slugs and reject unsafe paths',()=>{
 assert.equal(trade.productUrl({product_slug:'brand-2kg'}),'/prodotto/brand-2kg');
 assert.equal(trade.productUrl({product_url:'/prodotto/brand-2kg'}),'/prodotto/brand-2kg');
 assert.equal(trade.productUrl({product_slug:'//bad.test'}),'/confronta-cibo');
 assert.equal(trade.productUrl({id:'a:1',product_url:'https://bad.test'}),'/confronta-cibo');
});
