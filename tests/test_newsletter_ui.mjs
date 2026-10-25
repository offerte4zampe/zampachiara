import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {createRequire} from 'node:module';
const O4ZNewsletter=createRequire(import.meta.url)('../site/assets/newsletter-readiness.js');
const script=fs.readFileSync(new URL('../site/assets/newsletter.js',import.meta.url),'utf8');
const config=JSON.parse(fs.readFileSync(new URL('../site/data/newsletter.json',import.meta.url),'utf8'));
async function render(value,{reject=false}={}){
 const nodes=Object.fromEntries(['newsletter-status','newsletter-signup','newsletter-unsubscribe','newsletter-availability'].map(id=>[id,{hidden:id.includes('signup')||id.includes('unsubscribe'),href:'#',textContent:''}]));
 vm.runInNewContext(script,{document:{getElementById:id=>nodes[id]},O4ZNewsletter,URL,fetch:async()=>{if(reject)throw Error('offline');return {ok:true,json:async()=>value}}});
 await new Promise(resolve=>setImmediate(resolve));return nodes;
}
test('verified production configuration exposes hosted opt-in without inline form',async()=>{
 assert.equal(O4ZNewsletter.readiness(config).ready,true);
 const nodes=await render(config);assert.equal(nodes['newsletter-signup'].hidden,false);assert.equal(nodes['newsletter-signup'].href,config.signup_url);assert.match(nodes['newsletter-status'].textContent,/Iscrizioni aperte/);assert.equal(nodes['newsletter-unsubscribe'].hidden,false);
});
test('missing verification closes opt-in while keeping configured cancellation',async()=>{
 for(const gate of ['double_opt_in_verified','unsubscribe_verified','privacy_notice_verified','separate_consent_verified','provider_permissions_verified']){
  const nodes=await render({...config,[gate]:false});assert.equal(nodes['newsletter-signup'].hidden,true);assert.equal(nodes['newsletter-signup'].href,'#');assert.equal(nodes['newsletter-unsubscribe'].hidden,false);assert.match(nodes['newsletter-status'].textContent,/temporaneamente non disponibili/);
 }
});
test('unsafe hosted form and network error never expose opt-in',async()=>{
 for(const value of [{...config,signup_url:'https://sibforms.com.evil.test/form'},{...config,signup_url:'http://example.sibforms.com/form'}]){
  const nodes=await render(value);assert.equal(nodes['newsletter-signup'].hidden,true);assert.equal(nodes['newsletter-signup'].href,'#');
 }
 const nodes=await render(null,{reject:true});assert.equal(nodes['newsletter-signup'].hidden,true);assert.match(nodes['newsletter-status'].textContent,/temporaneamente non disponibili/);
});
