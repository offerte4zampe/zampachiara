(function(root){'use strict';
async function download(fetchImpl){
 const r=await fetchImpl('data/catalog.json.gz',{cache:'no-cache',credentials:'omit'});if(!r.ok)throw Error('network');
 return r.blob();
}
async function decode(blob){
 const bytes=await blob.arrayBuffer(),raw=new Uint8Array(bytes),start=performance.now();
 const decoded=raw[0]===31&&raw[1]===139?await new Response(blob.stream().pipeThrough(new DecompressionStream('gzip'))).text():new TextDecoder().decode(bytes);
 const decodedAt=performance.now(),payload=JSON.parse(decoded);if(!Array.isArray(payload.offers))throw Error('catalog');
 return {payload,thread:'main-fallback',metrics:[{stage:'decode_decompress',ms:decodedAt-start,thread:'main'},{stage:'parse',ms:performance.now()-decodedAt,thread:'main'}]};
}
async function direct(fetchImpl){return decode(await download(fetchImpl))}
async function load({WorkerImpl=root?.Worker,fetchImpl=fetch,fallback,timeoutMs=30000,blob:providedBlob}={}){
 // Download once in the page; the Worker only decodes. Keep the immutable Blob
 // available for fallback without another network request or a detached buffer.
 if(typeof WorkerImpl!=='function'){const result=await(fallback?fallback():providedBlob?decode(providedBlob):direct(fetchImpl));return {...result,fallback_reason:'unsupported'};}
 const blob=providedBlob||await download(fetchImpl);
 return new Promise((resolve,reject)=>{
  let worker,timer,settled=false;
  const clean=()=>{clearTimeout(timer);worker?.terminate()};
  const fail=reason=>{if(settled)return;settled=true;clean();Promise.resolve().then(()=>fallback?fallback():decode(blob)).then(result=>resolve({...result,fallback_reason:reason}),reject)};
  try{
   worker=new WorkerImpl('assets/catalog-loader.worker.js?v=2');
   worker.onmessage=e=>{if(settled)return;const value=e.data;if(!value?.ok||!Array.isArray(value.payload?.offers)){fail('decode');return}settled=true;clean();resolve({payload:value.payload,metrics:value.metrics||[],thread:'worker'})};
   worker.onerror=()=>fail('worker-error');worker.onmessageerror=()=>fail('message-error');
   timer=setTimeout(()=>fail('timeout'),timeoutMs);worker.postMessage({type:'decode',blob});
  }catch{fail('worker-start')}
 });
}
async function loadIndex({fetchImpl=fetch,WorkerImpl=root?.Worker}={}){
 const response=await fetchImpl('data/catalog-index.json',{cache:'no-cache',credentials:'omit'});
 if(!response.ok)throw Error('index-network');
 const manifest=await response.json();
 if(manifest.version!==1||!Array.isArray(manifest.shards)||manifest.shards.length>100||!Number.isInteger(manifest.rows))throw Error('index-manifest');
 const parts=new Array(manifest.shards.length),metrics=[];let next=0,thread='worker';
 async function consume(){while(next<manifest.shards.length){const index=next++,shard=manifest.shards[index];
  if(!/^data\/catalog-index\/[a-f0-9]{24}\.json\.gz$/.test(shard.path)||shard.rows>1000||shard.bytes>2000000)throw Error('index-shard');
  const r=await fetchImpl(shard.path,{cache:'force-cache',credentials:'omit'});if(!r.ok)throw Error('index-network');
  const result=await load({fetchImpl,WorkerImpl,blob:await r.blob()});
  if(result.payload.offers.length!==shard.rows)throw Error('index-count');
  parts[index]=result.payload.offers;metrics.push(...result.metrics);if(result.thread!=='worker')thread=result.thread;
 }}
 await Promise.all(Array.from({length:Math.min(3,manifest.shards.length)},consume));
 const offers=parts.flat().sort((a,b)=>a._order-b._order);if(offers.length!==manifest.rows)throw Error('index-count');
 return {payload:{...manifest,offers},metrics,thread};
}
function createFilter(rows,{WorkerImpl=root?.Worker,timeoutMs=5000}={}){
 if(rows.length<=5000||typeof WorkerImpl!=='function')return null;
 let worker,id=0;const pending=new Map();
 function fail(){worker?.terminate();for(const p of pending.values()){clearTimeout(p.timer);p.resolve(null)}pending.clear();worker=null}
 try{worker=new WorkerImpl('assets/catalog-filter.worker.js');worker.onerror=fail;worker.onmessageerror=fail;
 worker.onmessage=e=>{const p=pending.get(e.data?.id);if(!p)return;clearTimeout(p.timer);pending.delete(e.data.id);p.resolve(Array.isArray(e.data.ids)?new Set(e.data.ids):null)};
 worker.postMessage({type:'init',rows});}catch{fail();return null}
 return {filter:filters=>{if(!worker)return Promise.resolve(null);return new Promise(resolve=>{const key=++id,timer=setTimeout(fail,timeoutMs);pending.set(key,{resolve,timer});try{worker.postMessage({type:'filter',id:key,filters})}catch{fail()}})},close:fail};
}
const api={load,direct,decode,loadIndex,createFilter};if(typeof module!=='undefined')module.exports=api;else root.O4ZCatalogLoad=api;
})(typeof window!=='undefined'?window:null);
