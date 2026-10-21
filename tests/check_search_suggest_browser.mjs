import assert from 'node:assert/strict';
export async function checkSuggestions(page,origin,catalog){
 const now=Date.parse(catalog.generated_at),o=catalog.offers.find(o=>o.available&&typeof o.title==='string'&&o.title.length>4&&Number.isFinite(Date.parse(o.checked_at))&&now-Date.parse(o.checked_at)<=36*3600000&&Date.parse(o.checked_at)<=now+300000);
 assert(o,'Fresh catalog fixture required');const query=o.title.slice(0,Math.min(8,o.title.length));
 const homeRequests=[];const record=r=>homeRequests.push(r.url());page.on('request',record);
 await page.goto(origin+'/index.html',{waitUntil:'domcontentloaded'});
 await page.focus('#home-query');await page.type('#home-query',query);
 await page.waitForSelector('#home-query-suggestions [role=option]',{visible:true,timeout:30000});
 assert.equal(await page.$eval('#home-query',e=>e.getAttribute('aria-expanded')),'true');
 assert(await page.$$eval('#home-query-suggestions [role=option]',es=>es.length<=8));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1));
 assert(await page.$eval('#home-query-suggestions',e=>{const box=e.getBoundingClientRect(),y=Math.min(box.bottom-10,innerHeight-10),x=box.left+box.width/2;return y<=box.top||e.contains(document.elementFromPoint(x,y))}),'Suggestions must not be clipped by hero');
 await page.screenshot({path:'browser-reports/search-suggestions-mobile.png',fullPage:true});
 assert(homeRequests.some(url=>url.endsWith('/data/search-index.json')),'Home must use compact search index');
 assert(!homeRequests.some(url=>url.endsWith('/data/catalog.json.gz')),'Home search must not download the full catalog');
 page.off('request',record);
 await page.keyboard.press('ArrowDown');
 const expected=await page.$eval('#home-query-suggestions [aria-selected=true]',e=>e.dataset.productId);
 assert(await page.$eval('#home-query',e=>Boolean(e.getAttribute('aria-activedescendant'))));
 await Promise.all([page.waitForNavigation({waitUntil:'domcontentloaded'}),page.keyboard.press('Enter')]);
 assert.equal(new URL(page.url()).pathname,'/prodotto.html');assert.equal(new URL(page.url()).searchParams.get('id'),expected);
 await page.waitForSelector('#product-shops [data-product-shop]',{timeout:30000});
 assert.equal(await page.$$eval('#product-shops [data-product-shop]',rows=>rows.length),catalog.sources.length);
 const seed=catalog.offers.find(o=>o.id===expected);assert(seed);assert.equal(await page.$eval('#product-title',e=>e.textContent),seed.title);
 const outbound=await page.$$eval('#product-shops a',rows=>rows.map(a=>({href:a.href,rel:a.rel})));
 for(const a of outbound){assert(catalog.offers.some(o=>(o.affiliate_url||o.url)===a.href),'Exact catalog URL required');if(a.href.includes('tradetracker'))assert(a.rel.includes('sponsored'))}
 assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1));
 await page.screenshot({path:'browser-reports/product-mobile.png',fullPage:true});
 await page.goto(origin+'/index.html',{waitUntil:'domcontentloaded'});await page.focus('#home-query');await page.type('#home-query',query);await page.waitForSelector('#home-query-suggestions [role=option]',{visible:true});const clickedId=await page.$eval('#home-query-suggestions [role=option]',e=>e.dataset.productId);await Promise.all([page.waitForNavigation({waitUntil:'domcontentloaded'}),page.tap('#home-query-suggestions [role=option]')]);assert.equal(new URL(page.url()).searchParams.get('id'),clickedId);
 await page.goto(origin+'/confronta-cibo.html',{waitUntil:'domcontentloaded'});
 await page.waitForSelector('#catalog-query[role=combobox]',{timeout:30000});
 await page.focus('#catalog-query');await page.$eval('#catalog-query',(e,q)=>{e.value=q;e.dispatchEvent(new Event('input',{bubbles:true}))},query);
 await page.waitForSelector('#catalog-query-suggestions [role=option]',{visible:true});
 await page.keyboard.press('Escape');assert.equal(await page.$eval('#catalog-query-suggestions',e=>e.hidden),true);
 await page.$eval('#catalog-query',(e,q)=>{e.value=q;e.dispatchEvent(new Event('input',{bubbles:true}))},query);
 await page.waitForSelector('#catalog-query-suggestions [role=option]',{visible:true});
 const selected=await page.$eval('#catalog-query-suggestions [role=option]',e=>e.dataset.productId);
 await Promise.all([page.waitForNavigation({waitUntil:'domcontentloaded'}),page.tap('#catalog-query-suggestions [role=option]')]);
 assert.equal(new URL(page.url()).pathname,'/prodotto.html');
 assert.equal(new URL(page.url()).searchParams.get('id'),selected);

}
