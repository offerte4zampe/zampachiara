import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
export async function checkCoupons(page,origin){
 await page.goto(origin+'/codici-sconto.html',{waitUntil:'domcontentloaded'});
 assert.equal(await page.$$eval('main h1',es=>es.length),1);
 assert.equal(await page.$eval('link[rel=canonical]',e=>e.href),'https://offerte4zampe.it/codici-sconto');
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 const records=JSON.parse(await fs.readFile(new URL('../automation/coupons.json',import.meta.url),'utf8')).coupons;
 const active=records.filter(r=>r.status==='cart_tested'&&Date.now()<Math.min(Date.parse(r.expires_at),Date.parse(r.recheck_after),Date.parse(r.verified_at)+48*3600000)&&Date.now()>=Date.parse(r.starts_at));
 assert.equal(await page.$$eval('.coupon:not([hidden])',es=>es.length),active.length);
 await page.click('.filter[data-shop=isola]');
 assert.equal(await page.$$eval('.coupon:not([hidden])',es=>es.length),0);
 assert(await page.$eval('#coupon-empty',e=>!e.hidden));
 await page.click('.filter[data-shop=all]');
 for(const row of active)assert(await page.$eval('main', (e,code)=>e.textContent.includes(code),row.code));
}
