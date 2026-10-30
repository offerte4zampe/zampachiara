import test from 'node:test';import assert from 'node:assert/strict';import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),loader=require('../site/assets/catalog-load.js'),{matches}=require('../site/assets/catalog-filter.worker.js');
test('index downloads bounded shards without the full snapshot',async()=>{
 const path='data/catalog-index/'+'a'.repeat(24)+'.json.gz',calls=[];
 const fetchImpl=async url=>{calls.push(url);return new Response(JSON.stringify(url.endsWith('catalog-index.json')?{version:1,rows:1,shards:[{path,rows:1,bytes:20}],sources:[]}:{offers:[{id:'exact'}]}))};
 const result=await loader.loadIndex({fetchImpl,WorkerImpl:null});assert.equal(result.payload.offers[0].id,'exact');assert.deepEqual(calls,['data/catalog-index.json',path]);
});
test('invalid shard locations fail without requesting external or full catalogs',async()=>{
 const calls=[];await assert.rejects(loader.loadIndex({WorkerImpl:null,fetchImpl:async url=>{calls.push(url);return new Response(JSON.stringify({version:1,rows:1,shards:[{path:'https://external.example/a',rows:1,bytes:1}]}))}}));assert.equal(calls.length,1);
});
test('worker filter matches text, stock and exact facets without ranking changes',()=>{
 const row={id:'1',merchant:'Shop',brand:'Marca',available:true,search:'cibo pollo 12 kg',facets:{animal:'Cane'}};
 assert(matches(row,{words:['pollo','12'],brand:'Marca',stock:true,facets:{animal:'Cane'}}));
 for(const filters of [{words:['gatto']},{brand:'Altra'},{shop:'Altro'},{facets:{animal:'Gatto'}}])assert.equal(matches(row,filters),false);
 assert.equal(loader.createFilter(Array(5000).fill(row)),null);
});
test('worker errors resolve pending requests to the existing main-thread fallback',async()=>{
 class W{postMessage(m){if(m.type==='filter')queueMicrotask(()=>this.onerror())}terminate(){}}
 const filter=loader.createFilter(Array(5001).fill({id:'1'}),{WorkerImpl:W});assert.equal(await filter.filter({}),null);assert.equal(await filter.filter({}),null);
});

test('dual animal facets retain the exact catalog matching rule',()=>{
 assert(matches({facets:{animal:'Cane e gatto'},search:''},{facets:{animal:'Cane'}}));
 assert(matches({facets:{animal:'Cane e gatto'},search:''},{facets:{animal:'Gatto'}}));
});

test('real compact records preserve search, grouping and shipping results',async()=>{
 const {default:fs}=await import('node:fs/promises'),{gunzipSync}=await import('node:zlib');
 const metadata=require('../site/assets/catalog-metadata.js'),trade=require('../site/assets/trade.js'),{prepare}=require('../site/assets/catalog-prepare.js');
 const catalog=JSON.parse(gunzipSync(await fs.readFile(new URL('../site/data/catalog.json.gz',import.meta.url))));
 const fields='id title variant brand category price previous_price available image image_local sku gtin weight_kg shipping_weight_kg shipping_weight_checked_at shipping_weight_source quantity_verified weight_conflict checked_at merchant merchant_id canonical_title canonical_format canonical_shop_count product_slug product_id product_matching_method product_identity_verified identity_review identity_expires_at quantity unit_price unit_price_unit'.split(' ');
 const compact=catalog.offers.map(o=>Object.fromEntries(fields.filter(k=>k in o).map(k=>[k,o[k]])));
 const full=await prepare(catalog.offers),index=await prepare(compact,{index:true});
 assert.deepEqual(index.data.map(o=>o.id),full.data.map(o=>o.id));assert.deepEqual(index.searchText,full.searchText);
 const now=Date.parse(catalog.generated_at),rules=JSON.parse(await fs.readFile(new URL('../site/data/shipping-rules.json',import.meta.url)));
 assert.deepEqual(trade.groupOffers(index.data,now).map(g=>g.map(o=>o.id)),trade.groupOffers(full.data,now).map(g=>g.map(o=>o.id)));
 for(let i=0;i<full.data.length;i++){assert.deepEqual(metadata.facets(index.data[i]),metadata.facets(full.data[i]));for(const quantity of [1,3,10])assert.deepEqual(trade.shipping(index.data[i],rules,quantity,'standard',now),trade.shipping(full.data[i],rules,quantity,'standard',now));}
});
