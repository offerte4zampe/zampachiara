import {scheduledTelegram} from './telegram.mjs';
export {TelegramPublisher} from './telegram.mjs';
import {canonicalProduct,slugForOffer} from './canonical-product.mjs';
import {productPreview} from './product-preview.mjs';
const EVENTS = new Set(['page_view','catalog_search','compare_add','merchant_click']);
const PRODUCTS = new Set(['monge-maxi-adult-pollo','monge-medium-adult-pollo','monge-adult-manzo-riso','monge-adult-cat-pollo','royal-canin-medium-adult','royal-canin-maxi-adult','pro-plan-large-athletic-agnello','pro-plan-medium-sensitive-skin-salmone']);
const SHOPS = new Set(['Bauzaar','WebPet','Animaliapet','Isola dei Tesori','Paco Pet Shop','Amazon']);
export default {
  scheduled(event,env,ctx){ctx.waitUntil(scheduledTelegram(env));},
  async fetch(request, env) {
    const url = new URL(request.url);
    if(url.pathname==='/api/telegram/status'){
      if(request.method!=='GET')return new Response(null,{status:405});
      if(!env.TELEGRAM_PUBLISHER)return Response.json({integration:'telegram-v1',configured:false},{status:503});
      const stub=env.TELEGRAM_PUBLISHER.get(env.TELEGRAM_PUBLISHER.idFromName('sconti4zampe-v1'));
      const result=await stub.fetch(new Request('https://internal/status'));
      return new Response(result.body,{headers:{'Content-Type':'application/json','Cache-Control':'no-store'}});
    }
    if(url.pathname.startsWith('/prodotto/'))return canonicalProduct(request,env);
    if (['/prodotto','/prodotto.html'].includes(url.pathname)){
      const ids=url.searchParams.getAll('id');
      if(['GET','HEAD'].includes(request.method)&&ids.length===1&&ids[0]&&ids[0].length<=200){
        try{const slug=await slugForOffer(env,url.origin,ids[0]);if(slug&&/^[a-z0-9-]{1,200}$/.test(slug))return Response.redirect(new URL('/prodotto/'+slug,url.origin).href,301)}catch{}
      }
      return productPreview(request,env);
    }
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
