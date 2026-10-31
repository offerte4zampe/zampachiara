import assert from'node:assert/strict';
export async function checkNewsletterPopup(browser,origin,now){
 const page=await browser.newPage();try{
 await page.setViewport({width:393,height:852,isMobile:true,hasTouch:true});await page.setRequestInterception(true);page.on('request',r=>r.url().startsWith(origin)?r.continue():r.abort());
 await page.evaluateOnNewDocument(now=>{Date.now=()=>now},now);await page.goto(origin+'/',{waitUntil:'domcontentloaded'});await page.bringToFront();
 await page.waitForSelector('#newsletter-popup[open]',{timeout:18000});
 const state=await page.$eval('#newsletter-popup',e=>({text:e.textContent,link:e.querySelector('.newsletter-popup-signup').getAttribute('href'),width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height}));
 for(const word of ['Guide','offerte','sconti'])assert(state.text.includes(word));assert.equal(state.link,'/newsletter');assert(state.width<=393&&state.height<=852);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.screenshot({path:'browser-reports/newsletter-popup-mobile.png',fullPage:false});await page.keyboard.press('Escape');assert.equal(await page.$eval('#newsletter-popup',e=>e.open),false);
 const until=await page.evaluate(()=>Number(localStorage.getItem('o4z-newsletter-popup-until-v1')));assert.equal(until,now+14*86400000);
 await page.reload({waitUntil:'domcontentloaded'});assert.equal(await page.$('#newsletter-popup'),null);
 }finally{await page.close()}
}
