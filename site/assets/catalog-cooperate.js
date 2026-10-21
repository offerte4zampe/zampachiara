(function(root){'use strict';
function yieldToMain(){return typeof globalThis.scheduler?.yield==='function'?globalThis.scheduler.yield():new Promise(resolve=>setTimeout(resolve,0))}
async function each(rows,visit,{chunkSize=500,yieldTask=yieldToMain,isCurrent=()=>true,onChunk=null}={}){
 if(!Number.isInteger(chunkSize)||chunkSize<1)throw Error('Invalid chunk size');
 for(let start=0;start<rows.length;start+=chunkSize){
  if(!isCurrent())return false;
  const began=performance.now(),end=Math.min(start+chunkSize,rows.length);
  for(let i=start;i<end;i++)visit(rows[i]);
  if(onChunk)onChunk(performance.now()-began);
  if(end<rows.length)await yieldTask();
 }
 return isCurrent();
}
const api={each,yieldToMain};if(typeof module!=='undefined')module.exports=api;else root.O4ZCooperate=api;
})(typeof window!=='undefined'?window:null);
