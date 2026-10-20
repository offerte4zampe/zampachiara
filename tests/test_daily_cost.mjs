import test from 'node:test';
import assert from 'node:assert/strict';
import daily from '../site/assets/daily-cost.js';
const now=Date.parse('2026-10-20T05:00:00Z');
const offer={price:40,weight_kg:10,available:true,checked_at:'2026-10-20T04:00:00Z'};
test('manual grams use net weight and thirty days, never shipping weight',()=>{
 const result=daily.estimate({...offer,shipping_weight_kg:12},250,now);
 assert.deepEqual(result,{daily:1,month30:30,days:40});
});
test('no default ration or estimates from missing, stale, future, unavailable data',()=>{
 for(const g of ['',0,-1,Infinity,'invalid',100001])assert.equal(daily.estimate(offer,g,now),null);
 for(const patch of [{weight_kg:null},{weight_kg:-1},{price:NaN},{available:false},{checked_at:'bad'},{checked_at:'2026-10-18T00:00:00Z'},{checked_at:'2026-10-21T00:00:00Z'}])assert.equal(daily.estimate({...offer,...patch},250,now),null);
});
test('small portions retain precision rather than prematurely rounding to cents',()=>{
 assert.equal(daily.estimate({...offer,price:1,weight_kg:1},1,now).daily,0.001);
});
