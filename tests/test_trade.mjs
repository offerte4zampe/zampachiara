import test from 'node:test';import assert from 'node:assert/strict';import {createRequire} from 'node:module';const require=createRequire(import.meta.url);const {shipping,discount}=require('../site/assets/trade.js');
const now=Date.parse('2026-10-18T12:00:00Z'),rules={checked_at:'2026-10-18',merchants:{a:{fee:6.9,free_above:59,boundary_unknown:59,max_shipping_weight_kg:35},b:{fee:5.9,free_from:39.9},c:{conflict:true}}},o={price:30,merchant_id:'a',shipping_weight_kg:12,checked_at:'2026-10-18T10:00:00Z'};
test('shipping threshold and quantity use declared shipping weight',()=>{assert.equal(shipping(o,rules,1,'standard',now).total,36.9);assert.equal(shipping(o,rules,2,'standard',now).total,60);assert.equal(shipping(o,rules,3,'standard',now).total,undefined);assert.equal(shipping({...o,price:59},rules,1,'standard',now).total,undefined)});
test('unknown weights, conflicting rules, special destinations and stale prices never produce a total',()=>{for(const [offer,territory] of [[{...o,shipping_weight_kg:null},'standard'],[{...o,merchant_id:'c'},'standard'],[o,'special'],[{...o,checked_at:'2026-10-15'},'standard']])assert.equal(shipping(offer,rules,1,territory,now).total,undefined);assert.equal(shipping(o,{...rules,checked_at:'2026-10-01'},1,'standard',now).total,undefined)});
test('inclusive threshold and suspicious reference prices',()=>{assert.equal(shipping({...o,price:39.9,merchant_id:'b'},rules,1,'standard',now).fee,0);assert.equal(discount({price:1.7,previous_price:31.9}),false);assert.equal(discount({price:80,previous_price:100}),false)});

const {merchant,matchKey,groupOffers}=require('../site/assets/trade.js');
test('direct and approved affiliate clicks resolve to a merchant without sending URLs',()=>{
 assert.equal(merchant('https://tc.tradetracker.net/?c=16143&a=518044&u=%2Fproducts%2Ffoo'),'Bauzaar');
 assert.equal(merchant('https://www.bauzaar.it/products/foo'),'Bauzaar');
 assert.equal(merchant('https://tc.tradetracker.net/?c=31221&a=518044'),'Isola dei Tesori');
 assert.equal(merchant('https://www.isoladeitesori.it/prodotto/foo/123.html'),'Isola dei Tesori');
 assert.equal(merchant('https://tc.tradetracker.net/?c=31221&a=999'),'');
 for(const u of ['https://tc.tradetracker.net/?c=999&a=518044','https://evil.test/?c=16143&a=518044','http://www.bauzaar.it/'])assert.equal(merchant(u),'');
});
test('group only fresh same-code same-brand same-weight offers across different shops',()=>{
 const a={id:'a',merchant_id:'a',gtin:'4006381333931',brand:'Brand',weight_kg:2,checked_at:'2026-10-18T10:00:00Z'};
 const b={...a,id:'b',merchant_id:'b',gtin:'04006381333931',brand:'BRAND'};
 assert.equal(groupOffers([a,b],now).length,1);
 for(const bad of [{...b,weight_kg:4},{...b,brand:'Other'},{...b,gtin:'4006381333932'},{...b,checked_at:'2026-10-10'},{...b,gtin:''},{...b,merchant_id:'a'}])assert.equal(groupOffers([a,bad],now).length,2);
 assert.equal(matchKey({...a,checked_at:'not-a-date'},now),'');
});
test('expired supplementary shipment weights cannot produce totals',()=>{assert.equal(shipping({...o,shipping_weight_checked_at:'2026-10-01'},rules,1,'standard',now).total,undefined)});
