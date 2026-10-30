import test from 'node:test';import assert from 'node:assert/strict';import worker from '../worker/index.mjs';
test('brand query views retain user filters and are noindex',async()=>{
 let seen;const env={ASSETS:{fetch:async req=>{seen=req.url;return new Response('results',{headers:{'Content-Type':'text/html','ETag':'exact'}})}}};
 const url='https://offerte4zampe.it/confronta-cibo?brand=Marca&q=pollo',response=await worker.fetch(new Request(url),env,{});
 assert.equal(response.headers.get('X-Robots-Tag'),'noindex, follow');assert.equal(response.headers.get('ETag'),'exact');assert.equal(seen,url);assert.equal(await response.text(),'results');
});
