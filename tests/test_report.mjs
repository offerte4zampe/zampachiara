import test from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),report=require('../site/assets/report.js'),trade=require('../site/assets/trade.js');
test('report context is allowlisted, bounded and never uses affiliate URLs',()=>{
 const url=trade.reportUrl({id:'a',title:'Food & format',merchant:'Shop',price:10,checked_at:'2026-10-20',affiliate_url:'https://tracking.example/id',email:'private@example.com'});
 assert(!url.includes('tracking'));assert(!url.includes('private'));const values=report.context(url.split('?')[1]);assert.equal(values.title,'Food & format');assert.equal(values.price,'10');
 const result=report.draft(values,'Formato errato','Il formato non coincide');assert(result.href.startsWith('mailto:offerte4zampe@gmail.com?'));assert(result.body.includes('Il formato non coincide'));
 assert.equal(report.context('?title='+encodeURIComponent('a'.repeat(500)+'\nOther: value')).title.length,240);
});
