const EVENTS = new Set(['page_view','catalog_search','compare_add','merchant_click']);
const PRODUCTS = new Set(['monge-maxi-adult-pollo','monge-medium-adult-pollo','monge-adult-manzo-riso','monge-adult-cat-pollo','royal-canin-medium-adult','royal-canin-maxi-adult','pro-plan-large-athletic-agnello','pro-plan-medium-sensitive-skin-salmone']);
const SHOPS = new Set(['Bauzaar','WebPet','Animaliapet','Isola dei Tesori','Amazon']);
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== '/api/metrics') return env.ASSETS.fetch(request);
    const headers = {'Cache-Control':'no-store'};
    if (request.method !== 'POST') return new Response(null,{status:405,headers});
    if (request.headers.get('Origin') !== url.origin) return new Response(null,{status:403,headers});
    if (!request.headers.get('Content-Type')?.startsWith('application/json')) return new Response(null,{status:415,headers});
    // Bound streamed input too: Content-Length alone is not trustworthy.
    const reader=request.body?.getReader(); if(!reader) return new Response(null,{status:400,headers});
    let size=0, parts=[];
    while(true){const {value,done}=await reader.read();if(done)break;size+=value.byteLength;if(size>512){await reader.cancel();return new Response(null,{status:413,headers});}parts.push(value);}
    let event; try {event=JSON.parse(await new Blob(parts).text());} catch{return new Response(null,{status:400,headers});}
    if(!EVENTS.has(event.event)||!['home','catalog','product','other'].includes(event.page))return new Response(null,{status:400,headers});
    // Never log request objects, URLs, query text, IPs, headers or visitor IDs.
    console.log({type:'usage',event:event.event,page:event.page,...(SHOPS.has(event.merchant)?{merchant:event.merchant}:{}),...(PRODUCTS.has(event.product)?{product:event.product}:{})});
    return new Response(null,{status:204,headers});
  }
};
