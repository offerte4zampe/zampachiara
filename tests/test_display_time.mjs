import test from 'node:test';import assert from 'node:assert/strict';import {createRequire} from 'node:module';
const trade=createRequire(import.meta.url)('../site/assets/trade.js');
test('Rome display format agrees across summer and winter timestamps',()=>{
 assert.equal(trade.formatTimestamp('2026-07-01T12:00:00Z'),'01/07/2026, 14:00');
 assert.equal(trade.formatTimestamp('2026-01-01T12:00:00Z'),'01/01/2026, 13:00');
 assert.equal(trade.formatTimestamp('2026-10-30'),'30/10/2026');
 assert.equal(trade.formatTimestamp(null),'non disponibile');
});
test('Italian relative hours agree in singular and plural',()=>{
 const now=Date.parse('2026-10-30T12:00:00Z');
 assert.equal(trade.relativeTime('2026-10-30T11:00:00Z',now),'1 ora fa');
 assert.equal(trade.relativeTime('2026-10-30T10:00:00Z',now),'2 ore fa');
});
