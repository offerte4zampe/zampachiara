import assert from 'node:assert/strict';

export async function checkGuides(page, origin) {
  for (const slug of ['costo-crocchette-cane', 'confrontare-prezzi-lettiere', 'prezzo-confezione-o-prezzo-kg', 'spedizione-gratuita-conviene', 'leggere-storico-prezzi', 'stesso-prodotto-formato-gtin']) {
    await page.goto(origin+'/'+slug+'.html', {waitUntil:'domcontentloaded'});
    assert.equal(await page.$$eval('main h1', es=>es.length),1);
    assert(await page.$('.guide-table table caption'));
    assert(await page.$$eval('.guide-table a', es=>es.every(e=>e.href.startsWith('https://'))&&es.length>0));
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
  const quality=await page.evaluate(async()=>fetch('/data/site-quality.json').then(r=>r.json()));
  assert.equal(quality.method_version,2);
  assert.equal(quality.issues.length,0);
}
