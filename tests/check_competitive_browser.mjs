import assert from 'node:assert/strict';
export async function checkCompetitive(page,origin,catalog){
 await page.goto(origin+'/confronta-cibo.html',{waitUntil:'domcontentloaded'});
 await page.click('#catalog-load');
 await page.waitForSelector('#catalog-grid article',{timeout:30000});
 assert.equal(await page.$eval('#catalog-sort',e=>e.value),'matched');
 for(const key of ['animal','type','age','size','pack'])assert(await page.$eval('#catalog-'+key,e=>e.options.length>1));
 const brands=await page.$$eval('#catalog-brand option',es=>es.map(e=>e.value));assert(brands.includes('Monge'));assert(!brands.includes('MONGE'));
 await page.select('#catalog-animal','Cane');await page.select('#catalog-type','Cibo secco');
 await page.waitForSelector('#catalog-grid article');
 assert(await page.$eval('#catalog-grid',e=>e.textContent.length>0));
 await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{window.facetLink=value}}}));
 await page.click('#catalog-share');await page.waitForFunction(()=>Boolean(window.facetLink));
 const shared=await page.evaluate(()=>window.facetLink);assert.equal(new URL(shared).searchParams.get('animal'),'Cane');assert.equal(new URL(shared).searchParams.get('type'),'Cibo secco');
 await page.goto(shared,{waitUntil:'domcontentloaded'});await page.waitForSelector('#catalog-grid article',{timeout:30000});
 assert.equal(await page.$eval('#catalog-animal',e=>e.value),'Cane');assert.equal(await page.$eval('#catalog-type',e=>e.value),'Cibo secco');
 await page.click('#catalog-reset');for(const key of ['animal','type','age','size','pack'])assert.equal(await page.$eval('#catalog-'+key,e=>e.value),'');
 assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1));
 // Regression: the exact reviewed 30 x 1 g offers must share one product view.
 const ids=['bauzaar:56820111606085','isola-dei-tesori:000132103'];
 const rows=ids.map(id=>catalog.offers.find(o=>o.id===id));
 if(rows.every(o=>o&&o.weight_kg===.03&&o.gtin===rows[0].gtin)){
  await page.goto(origin+'/prodotto.html?id='+encodeURIComponent(ids[0]),{waitUntil:'domcontentloaded'});
  await page.waitForSelector('#product-price-table [data-comparison-offer]',{timeout:30000});
  const offers=await page.$$eval('#product-price-table [data-comparison-offer]',es=>es.map(e=>e.dataset.comparisonOffer));
  for(const id of ids)assert(offers.includes(id),'Missing Fortiflora store: '+id);
  assert(!(await page.$eval('#product-shops',e=>e.textContent)).includes('Non presente nel catalogo'));
  assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1));
  await page.screenshot({path:'browser-reports/fortiflora-comparison-mobile.png',fullPage:true});
  await page.goto(origin+'/confronta-cibo.html?q=fortiflora',{waitUntil:'domcontentloaded'});
  await page.waitForSelector('#catalog-grid .catalog-group',{timeout:30000});
  const cards=await page.$$eval('#catalog-grid .catalog-group',es=>es.map(e=>({text:e.textContent,titles:e.querySelectorAll('h3').length})));
  assert(cards.some(c=>c.text.includes('Bauzaar')&&c.text.includes('Isola dei Tesori')&&c.titles===1));
 }

 // Every connected store must be independently reachable through the catalog.
 for(const source of catalog.sources.filter(s=>['bauzaar','webpet','animaliapet','isola-dei-tesori','paco'].includes(s.id))){
  await page.goto(origin+'/confronta-cibo.html?shop='+encodeURIComponent(source.name),{waitUntil:'domcontentloaded'});
  await page.waitForSelector('#catalog-grid article',{timeout:30000});
  assert.equal(await page.$eval('#catalog-shop',e=>e.value),source.name);
  const titles=await page.$$eval('#catalog-grid article h3 a',es=>es.map(e=>e.href));
  assert(titles.length>0,source.id+' has no visible offers');
  assert(titles.every(href=>new URL(href).origin===origin&&new URL(href).pathname==='/prodotto.html'));
 }
 const uncertain=catalog.offers.find(o=>o.merchant_id==='paco'&&o.quantity_verified===false&&o.available);
 if(uncertain){
  await page.goto(origin+'/prodotto.html?id='+encodeURIComponent(uncertain.id),{waitUntil:'domcontentloaded'});
  await page.waitForSelector('[data-product-basket]',{timeout:30000});
  assert(await page.$eval('[data-product-basket]',e=>e.disabled));
  assert((await page.$eval('#product-shops',e=>e.textContent)).includes('formato non verificato'));
 }

}
