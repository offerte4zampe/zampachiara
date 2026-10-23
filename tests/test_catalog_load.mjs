import test from'node:test';import assert from'node:assert/strict';import{createRequire}from'node:module';import fs from'node:fs/promises';import vm from'node:vm';import{gzipSync}from'node:zlib';
const require=createRequire(import.meta.url),loader=require('../site/assets/catalog-load.js');
const payload={offers:[{id:'exact',affiliate_url:'kept'}],sources:[{id:'shop'}]};
const response=()=>new Response(JSON.stringify(payload));
test('worker receives Blob after one page download and preserves exact payload',async()=>{
 let ended=0,falls=0,fetches=0;
 class W{constructor(url){assert.equal(url,'assets/catalog-loader.worker.js?v=2')}postMessage(m){assert.equal(m.type,'decode');assert(m.blob instanceof Blob);queueMicrotask(()=>this.onmessage({data:{ok:true,payload,metrics:[]}}))}terminate(){ended++}}
 const r=await loader.load({WorkerImpl:W,fetchImpl:async()=>{fetches++;return response()},fallback:()=>{falls++;throw Error()}});
 assert.equal(r.payload,payload);assert.equal(r.thread,'worker');assert.equal(ended,1);assert.equal(falls,0);assert.equal(fetches,1);
});
test('worker failures reuse downloaded compressed bytes exactly once with a non-sensitive reason',async()=>{
 for(const mode of ['throw','error','message','invalid','timeout']){
  let fetches=0,ended=0;
  class W{constructor(){if(mode==='throw')throw Error()}postMessage(){queueMicrotask(()=>{if(mode==='error'){this.onerror();this.onerror()}if(mode==='message')this.onmessageerror();if(mode==='invalid')this.onmessage({data:{ok:true,payload:{}}})})}terminate(){ended++}}
  const r=await loader.load({WorkerImpl:W,timeoutMs:2,fetchImpl:async()=>{fetches++;return new Response(gzipSync(JSON.stringify(payload)))}});
  assert.equal(r.thread,'main-fallback');assert.deepEqual(r.payload,payload);assert.equal(fetches,1);assert(r.fallback_reason);if(mode!=='throw')assert.equal(ended,1);
 }
});
test('unsupported browser and network failures do not duplicate download',async()=>{
 let fetches=0;const r=await loader.load({WorkerImpl:null,fetchImpl:async()=>{fetches++;return response()}});assert.equal(r.fallback_reason,'unsupported');assert.equal(fetches,1);
 let constructed=0;class W{constructor(){constructed++}}
 await assert.rejects(loader.load({WorkerImpl:W,fetchImpl:async()=>new Response('',{status:503})}));assert.equal(constructed,0);
});
test('plain JSON and corrupt data retain validation',async()=>{
 const r=await loader.direct(async()=>response());assert.deepEqual(r.payload,payload);assert.equal(r.metrics.length,2);
 await assert.rejects(loader.direct(async()=>new Response('{}')));await assert.rejects(loader.decode(new Blob(['invalid'])));
});
test('actual Worker script decodes gzip and plain JSON without network access',async()=>{
 const code=await fs.readFile(new URL('../site/assets/catalog-loader.worker.js',import.meta.url),'utf8');
 for(const data of [JSON.stringify(payload),gzipSync(JSON.stringify(payload))]){
  let result;const self={postMessage:m=>{result=m}};
  vm.runInNewContext(code,{self,Blob,Response,Uint8Array,TextDecoder,DecompressionStream,performance,fetch:()=>{throw Error('Worker must not fetch')}});
  await self.onmessage({data:{type:'decode',blob:new Blob([data])}});assert.equal(result.ok,true);assert.deepEqual(JSON.parse(JSON.stringify(result.payload)),payload);
 }
});
