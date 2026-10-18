import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../worker/index.mjs';
const env={ASSETS:{fetch:async()=>new Response('asset')}};
const req=(body,origin='https://offerte4zampe.it')=>new Request('https://offerte4zampe.it/api/metrics',{method:'POST',headers:{Origin:origin,'Content-Type':'application/json'},body:JSON.stringify(body)});
test('assets are delegated without logging',async()=>{assert.equal(await (await worker.fetch(new Request('https://offerte4zampe.it/'),env)).text(),'asset')});
test('foreign origin, invalid events and oversized input rejected',async()=>{assert.equal((await worker.fetch(req({event:'page_view',page:'home'},'https://evil.example'),env)).status,403);assert.equal((await worker.fetch(req({event:'free text',page:'home'}),env)).status,400);assert.equal((await worker.fetch(req({event:'page_view',page:'home',extra:'x'.repeat(600)}),env)).status,413)});
test('only allowlisted fields are logged, even with private input',async()=>{const old=console.log;let logged;console.log=x=>{logged=x};try{assert.equal((await worker.fetch(req({event:'merchant_click',page:'catalog',merchant:'Bauzaar',query:'private search',ip:'secret',url:'secret'}),env)).status,204);assert.deepEqual(logged,{type:'usage',event:'merchant_click',page:'catalog',merchant:'Bauzaar'})}finally{console.log=old}});
