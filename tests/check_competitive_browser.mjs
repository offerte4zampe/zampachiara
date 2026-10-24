import assert from 'node:assert/strict';
export async function checkCompetitive(page,origin){
 await page.goto(origin+'/confronta-cibo.html',{waitUntil:'domcontentloaded'});
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
}
