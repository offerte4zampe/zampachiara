import test from'node:test';import assert from'node:assert/strict';import vm from'node:vm';import fs from'node:fs';
test('automated advertising makes no config, script or image request without a CMP',()=>{
 const calls=[];const document={querySelectorAll:()=>[{dataset:{adPlacement:'home-between-sections'}}],createElement:()=>{throw Error('Unexpected ad element')}};
 vm.runInNewContext(fs.readFileSync(new URL('../site/assets/advertising.js',import.meta.url),'utf8'),{document,fetch:url=>{calls.push(url);throw Error('No ad request')}});assert.deepEqual(calls,[]);
});
