import assert from 'node:assert/strict';import fs from 'node:fs/promises';
export async function profileCatalog(page,origin,catalog){
 const runs=[];
 for(let i=0;i<3;i++){
  await page.goto(origin+'/confronta-cibo.html?profile=1',{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>Boolean(window.O4ZCatalogProfile),{timeout:30000});
  const result=await page.evaluate(()=>window.O4ZCatalogProfile);assert(result.offers>0);assert(result.cards>0);
  for(const sample of result.samples)assert(Number.isFinite(sample.ms)&&sample.ms>=0);
  runs.push(result);
 }
 const stages=[...new Set(runs.flatMap(r=>r.samples.map(s=>s.stage)))];
 for(const stage of ['decode_decompress','parse','prepare_indexes','prepare_controls','filter_sort','group','render_cards','render_comparison'])assert(stages.includes(stage),'Missing measured stage '+stage);
 const medians=Object.fromEntries(stages.map(stage=>{const values=runs.map(r=>r.samples.filter(s=>s.stage===stage).reduce((n,s)=>n+s.ms,0)).sort((a,b)=>a-b);return [stage,Number(values[1].toFixed(3))]}));
 const report={scope:'Local checkout, Chromium mobile viewport on GitHub runner; no CPU/network throttling, no production/INP measurement',catalog_generated_at:catalog.generated_at,offers:runs[0].offers,iterations:3,units:'milliseconds',medians,runs};
 await fs.writeFile('browser-reports/catalog-profile.json',JSON.stringify(report,null,2));console.log('CATALOG_PROFILE '+JSON.stringify({...report,runs:undefined}));
}
