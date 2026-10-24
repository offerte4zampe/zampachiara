import assert from 'node:assert/strict';
export async function checkWatchlist(page,origin,catalog){
 const now=Date.parse(catalog.generated_at),seed=catalog.offers.find(o=>o.available&&o.price>0&&o.price<99999&&now-Date.parse(o.checked_at)<=36*3600000);assert(seed);
 await page.goto(origin+'/preferiti.html',{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>document.querySelector('#watch-status')?.textContent.includes('prodotti salvati'),{timeout:30000});
 const prior=await page.evaluate(()=>localStorage.getItem('o4z-watchlist-v1'));await page.evaluate(()=>localStorage.removeItem('o4z-watchlist-v1'));await page.reload({waitUntil:'domcontentloaded'});await page.waitForFunction(()=>!document.querySelector('#watch-empty').hidden);
 await page.goto(origin+'/prodotto.html?id='+encodeURIComponent(seed.id),{waitUntil:'domcontentloaded'});await page.waitForSelector('[data-watch-save]',{timeout:30000});
 await page.$eval('#product-watch input',(e,value)=>e.value=value,String(Math.ceil(seed.price+1)));await page.click('[data-watch-save]');await page.waitForFunction(()=>document.querySelector('#product-watch [role=status]')?.textContent.includes('Preferito salvato'));
 await page.goto(origin+'/preferiti.html',{waitUntil:'domcontentloaded'});await page.waitForSelector('[data-watch-state=reached]',{timeout:30000});assert((await page.$eval('#watch-items',e=>e.textContent)).includes(seed.title));assert.equal(await page.$$eval('#watch-items article',es=>es.length),1);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth<=1));await page.reload({waitUntil:'domcontentloaded'});await page.waitForSelector('[data-watch-state=reached]',{timeout:30000});
 await page.screenshot({path:'browser-reports/watchlist-mobile.png',fullPage:true});
 await page.click('#watch-items button');await page.waitForFunction(()=>!document.querySelector('#watch-empty').hidden);assert.equal(await page.$$eval('#watch-items article',es=>es.length),0);
 await page.evaluate(value=>{if(value===null)localStorage.removeItem('o4z-watchlist-v1');else localStorage.setItem('o4z-watchlist-v1',value);},prior);
}
