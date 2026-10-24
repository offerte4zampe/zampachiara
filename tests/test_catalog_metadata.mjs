import test from 'node:test';import assert from 'node:assert/strict';import {createRequire} from 'node:module';const require=createRequire(import.meta.url),m=require('../site/assets/catalog-metadata.js'),trade=require('../site/assets/trade.js');
test('explicit aliases merge spelling variants without merging product lines',()=>{
 for(const [a,b] of [['MONGE','Monge'],['Gimcat','GimCat'],['Edgard Cooper','Edgard & Cooper'],['Cats Best',"Cat's Best"]])assert.equal(m.brand(a),b);
 assert.notEqual(m.brand('Monge BWild'),m.brand('Monge'));assert.notEqual(m.brand('Royal Canin Veterinary Diet'),m.brand('Royal Canin'));
 const input={brand:'MONGE',price:12,gtin:'4006381333931',weight_kg:2,checked_at:new Date().toISOString()};const output=m.normalize(input);assert.equal(input.brand,'MONGE');assert.equal(output.brand,'Monge');assert.equal(trade.matchKey(input),trade.matchKey(output));
});
test('facets use explicit merchant words and leave uncertain values unset',()=>{
 assert.deepEqual(m.facets({title:'Crocchette cani adulti Maxi 12 kg',weight_kg:12}),{animal:'Cane',type:'Cibo secco',age:'Adulto',size:'Grande',pack:'Oltre 10 kg'});
 assert.equal(m.facets({title:'Gioco per gatti'}).size,'');assert.equal(m.facets({title:'Adult Senior cane'}).age,'');
 assert.equal(m.facets({title:'Hill’s special diet'}).animal,'');assert.equal(m.facets({title:'Cucciolo adulto cane'}).age,'');
 assert(m.matches({title:'Gioco cani e gatti'},{animal:'Gatto',type:'Giochi'}));assert(!m.matches({title:'Cibo cane'},{animal:'Gatto'}));
 assert(!m.matches({title:'Cibo cane'},{pack:'Fino a 1 kg'}));
});

test('grooming products are never classified as wet food or snacks',()=>{
 assert.equal(m.facets({title:'Shampoo mousse per cani'}).type,'');
 assert.equal(m.facets({title:'Dentifricio Dental per cane'}).type,'');
 assert.equal(m.facets({title:'Purina Dentalife snack cane'}).type,'Snack e premi');
});
