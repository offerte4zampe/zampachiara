(function(root){'use strict';
async function direct(fetchImpl){
 const r=await fetchImpl('data/catalog.json.gz',{cache:'no-cache',credentials:'omit'});if(!r.ok)throw Error('network');
 const bytes=await r.arrayBuffer(),raw=new Uint8Array(bytes),start=performance.now();
 const decoded=raw[0]===31&&raw[1]===139?await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).text():new TextDecoder().decode(bytes);
 const decodedAt=performance.now(),payload=JSON.parse(decoded);
 if(!Array.isArray(payload.offers))throw Error('catalog');
 return {payload,thread:'main-fallback',metrics:[{stage:'decode_decompress',ms:decodedAt-start,thread:'main'},{stage:'parse',ms:performance.now()-decodedAt,thread:'main'}]};
}
async function load({WorkerImpl=root?.Worker,fetchImpl=fetch,fallback=()=>direct(fetchImpl),timeoutMs=30000}={}){
 if(typeof WorkerImpl!=='function')return fallback();
 return new Promise((resolve,reject)=>{
  let worker,timer,settled=false;
  const clean=()=>{clearTimeout(timer);worker?.terminate()};
  const fail=()=>{if(settled)return;settled=true;clean();Promise.resolve().then(fallback).then(resolve,reject)};
  try{
   worker=new WorkerImpl('assets/catalog-loader.worker.js');
   worker.onmessage=e=>{if(settled)return;const value=e.data;if(!value?.ok||!Array.isArray(value.payload?.offers)){fail();return}settled=true;clean();resolve({payload:value.payload,metrics:value.metrics||[],thread:'worker'})};
   worker.onerror=fail;worker.onmessageerror=fail;timer=setTimeout(fail,timeoutMs);worker.postMessage('load');
  }catch{fail()}
 });
}
const api={load,direct};if(typeof module!=='undefined')module.exports=api;else root.O4ZCatalogLoad=api;
})(typeof window!=='undefined'?window:null);
