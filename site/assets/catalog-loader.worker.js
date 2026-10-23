'use strict';
self.onmessage=async event=>{
 if(event.data?.type!=='decode'||!(event.data.blob instanceof Blob))return;
 try{
  const blob=event.data.blob,bytes=await blob.arrayBuffer(),raw=new Uint8Array(bytes),start=performance.now();
  const decoded=raw[0]===31&&raw[1]===139?await new Response(blob.stream().pipeThrough(new DecompressionStream('gzip'))).text():new TextDecoder().decode(bytes);
  const decodedAt=performance.now(),payload=JSON.parse(decoded),parsedAt=performance.now();
  if(!Array.isArray(payload.offers))throw Error('catalog');
  self.postMessage({ok:true,payload,metrics:[{stage:'decode_decompress',ms:decodedAt-start,thread:'worker'},{stage:'parse',ms:parsedAt-decodedAt,thread:'worker'}]});
 }catch{self.postMessage({ok:false})}
};
