import assert from 'node:assert/strict';

export async function checkGuides(page, origin) {
  for (const slug of ['costo-crocchette-cane', 'confrontare-prezzi-lettiere', 'prezzo-confezione-o-prezzo-kg', 'spedizione-gratuita-conviene', 'leggere-storico-prezzi']) {
    await page.goto(origin+'/'+slug+'.html', {waitUntil:'domcontentloaded'});
    assert.equal(await page.$$eval('main h1', es=>es.length),1);
    assert(await page.$('.guide-table table caption'));
    assert(await page.$$eval('.guide-table a', es=>es.every(e=>e.href.startsWith('https://'))&&es.length>0));
    assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1),'Guide causes page overflow');
    assert.equal(await page.$eval('main', e=>e.textContent.includes('prezzi inventati')),false);
  }
}
