import assert from 'node:assert/strict';
export async function checkMobileMenu(page,origin,catalog){
 const product=catalog.offers.find(o=>o.product_slug&&o.available);
 const reports=[];
 for(const route of ['/','/confronta-cibo','/prodotto/'+product.product_slug]){
  await page.goto(origin+route,{waitUntil:'domcontentloaded'});
  await page.waitForSelector('#mobilemenu',{visible:true});
  assert.equal(await page.$eval('#mobilemenu',e=>e.getAttribute('aria-expanded')),'false');
  await page.tap('#mobilemenu');
  assert.equal(await page.$eval('#mobilemenu',e=>e.getAttribute('aria-expanded')),'true');
  const targets=await page.$$eval('#navlinks a',links=>links.map(a=>{const r=a.getBoundingClientRect();const hit=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return {href:a.getAttribute('href'),height:r.height,hit:a===hit||a.contains(hit)}}));
  assert(targets.length>=7);for(const target of targets){assert(target.height>=44);assert(target.hit,'Menu link covered on '+route+': '+target.href)}
  await page.keyboard.press('Escape');
  assert.equal(await page.$eval('#mobilemenu',e=>e.getAttribute('aria-expanded')),'false');
  assert(await page.$eval('#mobilemenu',e=>e===document.activeElement));
  await page.tap('#mobilemenu');const viewport=page.viewport();await page.touchscreen.tap(viewport.width-5,viewport.height-5);
  assert.equal(await page.$eval('#mobilemenu',e=>e.getAttribute('aria-expanded')),'false');
  await page.tap('#mobilemenu');
  await Promise.all([page.waitForNavigation({waitUntil:'domcontentloaded'}),page.tap('#navlinks a[href="/prodotti"]')]);
  assert.equal(new URL(page.url()).pathname,'/prodotti');
  assert.equal(await page.$eval('#mobilemenu',e=>e.getAttribute('aria-expanded')),'false');
  reports.push({route,targets});
 }
 console.log('MOBILE_MENU '+JSON.stringify({viewport:await page.viewport(),reports}));
}
