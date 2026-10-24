import assert from 'node:assert/strict';
import fs from 'node:fs/promises';

export async function checkGuides(page, origin) {
  for (const slug of ['costo-crocchette-cane', 'confrontare-prezzi-lettiere', 'prezzo-confezione-o-prezzo-kg', 'spedizione-gratuita-conviene', 'leggere-storico-prezzi', 'stesso-prodotto-formato-gtin']) {
    await page.goto(origin+'/'+slug+'.html', {waitUntil:'domcontentloaded'});
    assert.equal(await page.$$eval('main h1', es=>es.length),1);
    assert(await page.$('.guide-table table caption'));
    const links=await page.$$eval('.guide-table a',es=>es.map(e=>e.href));assert(links.length>0,slug+' table needs source links');
    for(const href of links){const u=new URL(href);if(u.origin===origin){
      if(u.pathname==='/prodotto.html'){assert(u.searchParams.has('id'));}
      else{assert(/^\/prezzi-\d{14}-[a-f0-9]{10}\.html$/.test(u.pathname),'Unexpected internal guide destination: '+href);await fs.access(new URL('../site'+u.pathname,import.meta.url));}
    }else assert.equal(u.protocol,'https:');}
    assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1),'Guide causes page overflow');
    assert.equal(await page.$eval('main', e=>e.textContent.includes('prezzi inventati')),false);
  }
  await page.goto(origin+'/osservatorio-prezzi.html', {waitUntil:'domcontentloaded'});
  assert.equal(await page.$$eval('main h1', es=>es.length),1);
  assert(await page.$('a[download][href="data/price-observatory.json"]'));
  assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1),'Observatory causes page overflow');
  const data=await page.evaluate(async()=>fetch('/data/price-observatory.json').then(r=>r.json()));
  assert.equal(data.method_version,1);
  assert(data.months.every(row=>row.closed||row.index_previous_month_100===null));
  await page.goto(origin+'/linea-monge-bwild.html',{waitUntil:'domcontentloaded'});
  assert.equal(await page.$$eval('main h1',rows=>rows.length),1);
  const lineLinks=await page.$$eval('.catalog-card .product-title-link',rows=>rows.map(a=>a.href));assert(lineLinks.length>=12);
  for(const href of lineLinks){const u=new URL(href);assert.equal(u.origin,origin);assert.equal(u.pathname,'/prodotto.html');assert(u.searchParams.get('id'));}
  assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1),'Line page overflow');
  const quality=await page.evaluate(async()=>fetch('/data/site-quality.json').then(r=>r.json()));
  assert.equal(quality.method_version,2);
  assert.equal(quality.issues.length,0);
}

