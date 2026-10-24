import assert from 'node:assert/strict';import fs from 'node:fs/promises';
export async function checkThemes(page,origin,catalog){
 const results=[];
 const product=catalog.offers.find(o=>o.available);assert(product);
 for(const theme of ['light','dark']){
  await page.emulateMediaFeatures([{name:'prefers-color-scheme',value:theme}]);
  for(const route of ['/index.html','/confronta-cibo.html','/prodotto.html?id='+encodeURIComponent(product.id),'/prezzo-confezione-o-prezzo-kg.html','/calcolatore.html','/newsletter.html','/preferiti.html']){
   await page.goto(origin+route,{waitUntil:'domcontentloaded'});
   const data=await page.evaluate(()=>{
    function rgb(s){const m=s.match(/[\d.]+/g);return m?m.slice(0,3).map(Number):[0,0,0]}
    function lum(c){return c.map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0)}
    function background(e){while(e){const c=getComputedStyle(e).backgroundColor;if(!c.endsWith(', 0)')&&c!=='transparent')return c;e=e.parentElement}return 'rgb(255,255,255)'}
    const rows=[];for(const selector of ['body','.navlinks a','.micro','.btn:not(:disabled)','.field input','.content p']){
     const e=[...document.querySelectorAll(selector)].find(e=>e.getClientRects().length);if(!e)continue;
     const fg=getComputedStyle(e).color,bg=background(e),a=lum(rgb(fg)),b=lum(rgb(bg));rows.push({selector,fg,bg,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)});
    }
    const targets=[...document.querySelectorAll('.btn:not(:disabled),select,input:not([type=checkbox]):not([type=radio])')].filter(e=>e.getClientRects().length).map(e=>({tag:e.tagName,id:e.id,height:e.getBoundingClientRect().height}));return {targets,rows,bg:getComputedStyle(document.body).backgroundColor,overflow:document.documentElement.scrollWidth-innerWidth,viewport:innerWidth};
   });
   assert.equal(data.bg,theme==='dark'?'rgb(16, 35, 38)':'rgb(255, 250, 242)');
   for(const row of data.rows)assert(row.ratio>=4.5,theme+' '+route+' '+JSON.stringify(row));
   for(const target of data.targets)assert(target.height>=44,theme+' '+route+' touch target '+JSON.stringify(target));
   assert(data.overflow<=1,route+' overflow');assert(data.viewport<=394);
   results.push({theme,route,...data});
   if(theme==='dark'&&route==='/index.html')await page.screenshot({path:'browser-reports/home-dark-mobile.png',fullPage:true});
  }
 }
 await page.emulateMediaFeatures([{name:'prefers-color-scheme',value:'light'}]);
 await fs.writeFile('browser-reports/theme-contrast.json',JSON.stringify({scope:'Representative computed colours, not full WCAG certification',results},null,2));
}

