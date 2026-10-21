import test from 'node:test';import assert from 'node:assert/strict';import {createRequire} from 'node:module';import fs from 'node:fs';
const require=createRequire(import.meta.url),{productLink}=require('../site/assets/amazon-links.js');
const config=JSON.parse(fs.readFileSync(new URL('../site/data/amazon-links.json',import.meta.url),'utf8')),row=config.links[0],offer={id:row.offer_id,...row};
const now=Date.parse('2026-10-21T12:00:00Z');
test('verified exact product uses direct tagged Amazon link without prices or stock',()=>{const value=productLink(offer,config,now);assert.deepEqual(value,{url:'https://www.amazon.it/dp/'+row.asin+'?tag=offerte4zam02-21',checked_at:row.checked_at});});
test('no fuzzy mapping, changed format, title, GTIN or brand',()=>{assert.equal(productLink({...offer,id:'other'},config,now),null);for(const key of ['title','brand','variant','gtin'])assert.equal(productLink({...offer,[key]:'changed'},config,now),null);});
test('expired, future, ambiguous or unsafe mapping never generates a link',()=>{for(const patch of [{checked_at:'2026-01-01'},{checked_at:'2027-01-01'},{asin:'bad'},{evidence_url:'https://www.amazon.it.evil.test/dp/'+row.asin}])assert.equal(productLink(offer,{...config,links:[{...row,...patch}]},now),null);assert.equal(productLink(offer,{...config,links:[row,row]},now),null);assert.equal(productLink(offer,null,now),null);});
