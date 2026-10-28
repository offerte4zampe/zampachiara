import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import fs from 'node:fs';
const source=fs.readFileSync(new URL('../site/assets/base.js',import.meta.url),'utf8');
function run(iso){
 const classes=new Set(),art={children:[],querySelector(){return this.children[0]},append(e){this.children.push(e)}},badge={},bubble={};
 const hero={querySelector(s){return s==='.eyebrow'?badge:s==='.pet-bubble'?bubble:s==='.pet-hero-art'?art:null}};
 const document={getElementById(){return null},querySelectorAll(){return []},querySelector(){return hero},documentElement:{classList:{add(c){classes.add(c)}}},createElement(){return {setAttribute(){}}}};
 class Clock extends Date{constructor(...args){super(...(args.length?args:[iso]))}}
 const context=vm.createContext({document,Date:Clock,Intl});vm.runInContext(source,context);vm.runInContext(source,context);
 return {active:classes.has('halloween'),art,badge,bubble};
}
test('Halloween follows Rome boundaries and expires without another deployment',()=>{
 for(const iso of ['2026-10-27T22:59:59Z','2026-11-01T23:00:00Z','2027-10-30T12:00:00Z']){const r=run(iso);assert.equal(r.active,false,iso);assert.equal(r.art.children.length,0)}
 for(const iso of ['2026-10-27T23:00:00Z','2026-10-31T12:00:00Z','2026-11-01T22:59:59Z']){const r=run(iso);assert.equal(r.active,true,iso);assert.equal(r.art.children.length,1);assert.equal(r.badge.textContent,'Halloween a 4 zampe');assert.equal(r.art.children[0].alt,'')}
});
