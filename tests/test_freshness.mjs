import test from 'node:test';import assert from 'node:assert/strict';import {createRequire} from 'node:module';
const trade=createRequire(import.meta.url)('../site/assets/trade.js'),now=Date.parse('2026-10-30T12:00:00Z');
test('freshness labels use observed timestamp and strict twelve-hour threshold',()=>{
 assert.equal(trade.freshnessLabel('2026-10-29T23:00:00Z',now),'Dati non aggiornati da 13 ore');
 assert.equal(trade.freshnessLabel('2026-10-30T00:00:00Z',now),'');
 assert.equal(trade.freshnessLabel(null,now),'Data aggiornamento non disponibile');
 assert.equal(trade.freshnessLabel('2026-10-30T13:00:00Z',now),'Data aggiornamento non disponibile');
});
