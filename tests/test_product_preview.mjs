import test from 'node:test';import assert from 'node:assert/strict';import{productPreview,rewrite}from'../worker/product-preview.mjs';
const html='<title>Generic</title><meta name="description" content="old"><meta property="og:title" content="old"><meta property="og:description" content="old"><meta property="og:url" content="old"><meta name="robots" content="noindex,follow"><main>UNCHANGED</main>';
test('escape title and attributes without changing visible comparison or noindex',()=>{const s=rewrite(html,'<img x="bad">&','shop:1');assert(!s.includes('<img'));assert(s.includes('&lt;img'));assert(s.includes('id=shop%3A1'));assert(s.includes('<main>UNCHANGED</main>'));assert(s.includes('noindex,follow'))});
test('reads one title-only shard, no external fetch and no request headers forwarded',async()=>{
 const seen=[],env={ASSETS:{fetch:async r=>{seen.push(r);return r.url.includes('product-meta')?Response.json({'shop:1':'Exact name'}):new Response(html,{headers:{'Content-Type':'text/html','ETag':'old','Content-Length':'1'}})}}};
 const r=await productPreview(new Request('https://offerte4zampe.it/prodotto?id=shop%3A1&utm_source=private',{headers:{Cookie:'private'}}),env);
 assert.equal(r.status,200);assert((await r.text()).includes('Exact name'));assert.equal(r.headers.get('ETag'),null);assert.equal(seen.length,2);assert(seen.every(r=>!r.headers.get('Cookie')&&!r.url.includes('private')));
});
test('missing, ambiguous or unavailable metadata delegates safely',async()=>{
 for(const query of ['','?id=x&id=y','?id=unknown']){
  let calls=0;const env={ASSETS:{fetch:async r=>{calls++;return r.url.includes('product-meta')?Response.json({}):new Response('fallback')}}};
  assert.equal(await(await productPreview(new Request('https://offerte4zampe.it/prodotto'+query),env)).text(),'fallback');assert(calls<=2);
 }
 const env={ASSETS:{fetch:async r=>r.url.includes('product-meta')?new Response('bad json'):new Response('fallback')}};
 assert.equal(await(await productPreview(new Request('https://offerte4zampe.it/prodotto?id=x'),env)).text(),'fallback');
});
