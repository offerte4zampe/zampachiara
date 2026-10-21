import test from 'node:test';import assert from 'node:assert/strict';import {createRequire} from 'node:module';const require=createRequire(import.meta.url);const {productView}=require('../site/assets/product-model.js');
const now=Date.parse('2026-10-21T10:00:00Z'),a={id:'a',merchant_id:'a',merchant:'A',title:'Cibo',brand:'Brand',variant:'2 kg',gtin:'4006381333931',weight_kg:2,available:true,price:20,checked_at:'2026-10-21T09:00:00Z',affiliate_url:'https://tc.tradetracker.net/?c=1'};
const sources=[{id:'a',name:'A',status:'ok'},{id:'b',name:'B',status:'ok'},{id:'c',name:'C',status:'ok'},{id:'d',name:'D',status:'stale'}];
test('exact product lists all stores, sold out and missing distinctly and preserves tracking',()=>{
 const b={...a,id:'b',merchant_id:'b',merchant:'B',available:false,price:10};
 const view=productView({offers:[a,b,{...a,id:'different',merchant_id:'c',weight_kg:4}],sources},'a',now);
 assert.equal(view.shops.length,4);assert.equal(view.shops[0].source.id,'a');assert.equal(view.shops.find(s=>s.source.id==='b').offers[0].available,false);
 assert.equal(view.shops.find(s=>s.source.id==='c').state,'missing');assert.equal(view.shops.find(s=>s.source.id==='d').state,'unknown');assert.equal(view.shops[0].offers[0].affiliate_url,a.affiliate_url);
});
test('missing identifiers never infer cross-store equivalence',()=>{const view=productView({offers:[{...a,gtin:''},{...a,id:'b',merchant_id:'b'}],sources},'a',now);assert.equal(view.exact,false);assert.equal(view.shops.find(s=>s.source.id==='b').state,'unmatched')});
test('stale selected offer hides prices and missing ID returns null',()=>{const catalog={offers:[{...a,checked_at:'2026-10-01'}],sources};assert.equal(productView(catalog,'a',now).shops.find(s=>s.source.id==='a').state,'stale');assert.equal(productView(catalog,'gone',now),null)});

test('shipping total drives shop order and quantity thresholds without changing tracking',()=>{
 const b={...a,id:'b',merchant_id:'b',merchant:'B',price:18};
 const rules={checked_at:'2026-10-21',merchants:{a:{fee:1,free_from:30},b:{fee:8,free_from:30}}};
 const catalog={offers:[a,b],sources:sources.slice(0,2)};
 const one=productView(catalog,'a',now,rules,1);
 assert.deepEqual(one.shops.map(s=>s.source.id),['a','b']);
 assert.equal(one.shops[0].quotes.get('a').total,21);
 const two=productView(catalog,'a',now,rules,2);
 assert.deepEqual(two.shops.map(s=>s.source.id),['b','a']);
 assert.equal(two.shops[0].quotes.get('b').total,36);
 assert.equal(two.shops[1].offers[0].affiliate_url,a.affiliate_url);
 const special=productView(catalog,'a',now,rules,1,'special');
 assert(special.shops.every(s=>s.quotes.get(s.offers[0].id).total===undefined));
});
test('unknown or stale shipping rules never produce a total',()=>{
 const catalog={offers:[a],sources:[sources[0]]};
 for(const rules of [null,{checked_at:'2026-09-01',merchants:{a:{fee:1}}},{checked_at:'2026-10-21',merchants:{a:{conflict:true}}}]){
  assert.equal(productView(catalog,'a',now,rules).shops[0].quotes.get('a').total,undefined);
 }
});
