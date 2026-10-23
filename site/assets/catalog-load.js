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
async function load({WorkerImpl=root?.Worker,fetchImpl=fetch,fallback,timeoutMs=30000}={}){
 // Download once in the page; the Worker only decodes. Keep the immutable Blob
 // available for fallback without another network request or a detached buffer.
 if(typeof WorkerImpl!=='function'){const result=await(fallback?fallback():direct(fetchImpl));return {...result,fallback_reason:'unsupported'};}
 const blob=await download(fetchImpl);
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
const api={load,direct,decode};if(typeof module!=='undefined')module.exports=api;else root.O4ZCatalogLoad=api;
})(typeof window!=='undefined'?window:null);
