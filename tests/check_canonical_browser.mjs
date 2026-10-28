import assert from 'node:assert/strict';
export async function checkCanonical(page,origin,catalog){
 const seed=catalog.offers.find(o=>o.canonical_shop_count>=2&&o.product_slug&&o.available&&o.quantity?.verified);
 assert(seed,'A real canonical multishop product is required');
 const route=origin+'/prodotto/'+seed.product_slug;
 const response=await page.goto(route,{waitUntil:'domcontentloaded'});assert.equal(response.status(),200);
 assert.equal(response.headers()['x-product-model'],'canonical-v1');
 const source=await response.text();assert(source.includes('application/ld+json'));assert(source.includes('data-canonical-product'));assert(source.includes('Vai al negozio'));
 const rows=await page.$$eval('.canonical-offers tbody tr',es=>es.map(e=>e.textContent));assert(rows.length>=2);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1));
 assert.equal(await page.$eval('.canonical-offers',e=>getComputedStyle(e).minWidth),'0px');
 assert.equal(await page.$eval('link[rel=canonical]',e=>new URL(e.href).pathname),'/prodotto/'+seed.product_slug);
 await page.screenshot({path:'browser-reports/canonical-product-mobile.png',fullPage:true});
 const noJS=await page.browser().newPage();try{await noJS.setJavaScriptEnabled(false);await noJS.setViewport({width:393,height:852,isMobile:true});await noJS.setRequestInterception(true);noJS.on('request',r=>r.url().startsWith(origin)?r.continue():r.abort());await noJS.goto(route,{waitUntil:'domcontentloaded'});assert(await noJS.$$eval('.canonical-offers tbody tr',es=>es.length>=2));assert((await noJS.$eval('h1',e=>e.textContent)).length>0);}finally{await noJS.close()}
}
