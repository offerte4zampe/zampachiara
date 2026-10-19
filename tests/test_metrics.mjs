import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../worker/index.mjs';
const env={ASSETS:{fetch:async()=>new Response('asset')}};
const req=(body,origin='https://offerte4zampe.it')=>new Request('https://offerte4zampe.it/api/metrics',{method:'POST',headers:{Origin:origin,'Content-Type':'application/json'},body:JSON.stringify(body)});
test('assets are delegated without logging',async()=>{assert.equal(await (await worker.fetch(new Request('https://offerte4zampe.it/'),env)).text(),'asset')});
test('foreign origin, invalid events and oversized input rejected',async()=>{assert.equal((await worker.fetch(req({event:'page_view',page:'home'},'https://evil.example'),env)).status,403);assert.equal((await worker.fetch(req({event:'free text',page:'home'}),env)).status,400);assert.equal((await worker.fetch(req({event:'page_view',page:'home',extra:'x'.repeat(600)}),env)).status,413)});
test('only allowlisted fields are logged, even with private input',async()=>{const old=console.log;let logged;console.log=x=>{logged=x};try{assert.equal((await worker.fetch(req({event:'merchant_click',page:'catalog',merchant:'Bauzaar',query:'private search',ip:'secret',url:'secret'}),env)).status,204);assert.deepEqual(logged,{type:'usage',event:'merchant_click',page:'catalog',merchant:'Bauzaar'})}finally{console.log=old}});

import vm from 'node:vm';
import fs from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),trade=require('../site/assets/trade.js');
test('browser click listener counts approved tracking links only after consent',()=>{
 for(const consent of ['yes','no']){
  const callbacks={},events=[];
  const context={window:{O4ZTrade:trade},location:{pathname:'/confronta-cibo'},navigator:{},localStorage:{getItem:()=>consent},document:{querySelector:()=>null,addEventListener:(name,cb)=>{callbacks[name]=cb}},fetch:(url,options)=>{events.push(JSON.parse(options.body));return Promise.resolve({})},clearTimeout(){},setTimeout(){}};
  vm.runInNewContext(fs.readFileSync(new URL('../site/assets/metrics.js',import.meta.url),'utf8'),context);
  callbacks.click({target:{closest:tag=>tag==='a'?{href:'https://tc.tradetracker.net/?c=16143&a=518044&u=private-query'}:null}});
  assert.equal(events.filter(e=>e.event==='merchant_click').length,consent==='yes'?1:0);
  if(consent==='yes')assert.deepEqual(JSON.parse(JSON.stringify(events.at(-1))),{event:'merchant_click',page:'catalog',merchant:'Bauzaar',product:'confronta-cibo'});
 }
});
