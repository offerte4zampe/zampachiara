import assert from 'node:assert/strict';
export async function checkSuggestions(page,origin,catalog){
 const now=Date.parse(catalog.generated_at),o=catalog.offers.find(o=>o.available&&typeof o.title==='string'&&o.title.length>4&&Number.isFinite(Date.parse(o.checked_at))&&now-Date.parse(o.checked_at)<=36*3600000&&Date.parse(o.checked_at)<=now+300000);
 assert(o,'Fresh catalog fixture required');const query=o.title.slice(0,Math.min(8,o.title.length));
 await page.goto(origin+'/index.html',{waitUntil:'domcontentloaded'});
 await page.focus('#home-query');await page.type('#home-query',query);
 await page.waitForSelector('#home-query-suggestions [role=option]',{visible:true,timeout:30000});
 assert.equal(await page.$eval('#home-query',e=>e.getAttribute('aria-expanded')),'true');
 assert(await page.$$eval('#home-query-suggestions [role=option]',es=>es.length<=8));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1));
 await page.screenshot({path:'browser-reports/search-suggestions-mobile.png',fullPage:true});
 await page.keyboard.press('ArrowDown');
 const expected=await page.$eval('#home-query-suggestions [aria-selected=true]',e=>e.dataset.query);
 assert(await page.$eval('#home-query',e=>Boolean(e.getAttribute('aria-activedescendant'))));
 await Promise.all([page.waitForNavigation({waitUntil:'domcontentloaded'}),page.keyboard.press('Enter')]);
 assert.equal(new URL(page.url()).searchParams.get('q'),expected);
 await page.waitForSelector('#catalog-query[role=combobox]',{timeout:30000});
 await page.focus('#catalog-query');await page.$eval('#catalog-query',(e,q)=>{e.value=q;e.dispatchEvent(new Event('input',{bubbles:true}))},query);
 await page.waitForSelector('#catalog-query-suggestions [role=option]',{visible:true});
 await page.keyboard.press('Escape');assert.equal(await page.$eval('#catalog-query-suggestions',e=>e.hidden),true);
 await page.$eval('#catalog-query',(e,q)=>{e.value=q;e.dispatchEvent(new Event('input',{bubbles:true}))},query);
 await page.waitForSelector('#catalog-query-suggestions [role=option]',{visible:true});
 const selected=await page.$eval('#catalog-query-suggestions [role=option]',e=>e.dataset.query);
 await page.click('#catalog-query-suggestions [role=option]');
 assert.equal(await page.$eval('#catalog-query',e=>e.value),selected);
 assert.equal(await page.$eval('#catalog-query',e=>e.getAttribute('aria-expanded')),'false');
 await page.$eval('#catalog-query',e=>{e.value='';e.dispatchEvent(new Event('input',{bubbles:true}))});
 assert.equal(await page.$eval('#catalog-query-suggestions',e=>e.hidden),true);
}
