import test from 'node:test';import assert from 'node:assert/strict';import worker from '../worker/index.mjs';
test('HTML revalidates and cannot be retained by Cloudflare CDN rules; hashed assets preserve immutable caching',async()=>{
 const env={ASSETS:{fetch:async req=>new Response('body',{headers:{'Content-Type':req.url.endsWith('.js')?'application/javascript':'text/html','Cache-Control':'public, max-age=31536000, immutable','ETag':'version'}})}};
 const html=await worker.fetch(new Request('https://offerte4zampe.it/confronta-cibo'),env,{});assert.equal(html.headers.get('Cache-Control'),'public, max-age=0, must-revalidate');assert.equal(html.headers.get('Cloudflare-CDN-Cache-Control'),'no-store');assert.equal(html.headers.get('ETag'),'version');
 const asset=await worker.fetch(new Request('https://offerte4zampe.it/assets/a.123456789abc.js'),env,{});assert.equal(asset.headers.get('Cache-Control'),'public, max-age=31536000, immutable');
});
test('brand aliases redirect to a local canonical landing with no query contamination',async()=>{
 const env={ASSETS:{fetch:async()=>Response.json({'/marca-aldog':'/marca-al-dog','/marca-evil':'https://evil.test/'})}};
 const response=await worker.fetch(new Request('https://offerte4zampe.it/marca-aldog'),env,{});assert.equal(response.status,301);assert.equal(response.headers.get('Location'),'https://offerte4zampe.it/marca-al-dog');
 const rejected=await worker.fetch(new Request('https://offerte4zampe.it/marca-evil'),env,{});assert.equal(rejected.status,200);
});
