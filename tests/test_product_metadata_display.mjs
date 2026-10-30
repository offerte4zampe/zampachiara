import test from 'node:test';import assert from 'node:assert/strict';import{createRequire}from'node:module';import fs from'node:fs/promises';import{gunzipSync}from'node:zlib';
const require=createRequire(import.meta.url),meta=require('../site/assets/product-metadata.js');
test('duplicate adjacent quantities disappear without conflating different formats',()=>{assert.equal(meta.name('Cibo 15 kg · 15kg'),'Cibo 15 kg');assert.equal(meta.name('Cibo 2 kg / 4 kg'),'Cibo 2 kg / 4 kg')});
test('fifty real product titles stay within 65 characters and keep format',async()=>{
 const model=JSON.parse(gunzipSync(await fs.readFile(new URL('../site/data/product-catalog.json.gz',import.meta.url))));
 const products=model.products.filter(p=>p.active_offer_count).sort((a,b)=>b.name.length-a.name.length).slice(0,50);assert.equal(products.length,50);
 for(const p of products){const title=meta.title(p.name,p.brand,p.format);assert(title.length<=65,title);assert(title.endsWith(' | Prezzo e storico'));if(p.format.length<=20)assert(title.includes(p.format));}
});
test('description uses the lowest visible available offer and its unit price',()=>{
 const rows=[{available:true,price:29.89,unit_price:1.99,unit_price_unit:'kg'},{available:true,price:35},{available:false,price:1}];
 assert.match(meta.description(rows,3),/^Confronta 3 negozi: da 29,89/);assert.match(meta.description(rows,1),/^Prezzo rilevato: 29,89/);assert(!meta.description(rows,1).includes('1 negozio'));assert(meta.description(rows,3).includes('/kg'));
});
