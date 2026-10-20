import test from 'node:test';import assert from 'node:assert/strict';
import history from '../site/assets/price-history.js';
const now=Date.parse('2026-10-20T12:00:00Z'),row=(day,low=10,high=12)=>({day,low,high,available:true});
test('windows count only observed days and preserve missing days',()=>{
 const rows=[row('2026-10-20'),row('2026-10-18',9,11),row('2026-09-20',8,15),row('2026-05-01')];
 const a=history.summarize(rows,30,now);assert.equal(a.observedDays,2);assert.equal(a.low,9);assert.equal(a.high,12);assert.equal(a.rows.length,2);
 assert.equal(history.summarize(rows,90,now).observedDays,3);assert.equal(history.summarize(rows,180,now).observedDays,4);
});
test('reject invalid, future and nonfinite prices; empty does not invent zero minimum',()=>{
 const a=history.summarize([row('2026-10-21'),row('2026-02-30'),row('2026-10-18',NaN,10),row('2026-10-19',12,10),row('2026-10-20',0,10)],30,now);
 assert.equal(a.low,null);assert.equal(a.high,null);assert.equal(a.observedDays,0);
});
