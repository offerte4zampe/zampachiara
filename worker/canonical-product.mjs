import trade from '../site/assets/trade.js';
import {shippingSource} from './shipping-source.mjs';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money=n=>new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR'}).format(n);
const safe=u=>{try{const url=new URL(u);return url.protocol==='https:'&&!url.username&&!url.password?url.href:''}catch{return ''}};
async function prefix(value){const bytes=new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(value)));return bytes[0].toString(16).padStart(2,'0')}
async function jsonAsset(env,origin,path){const r=await env.ASSETS.fetch(new Request(new URL(path,origin)));if(!r.ok)return null;try{return await r.json()}catch{return null}}
export async function slugForOffer(env,origin,id){const shard=await jsonAsset(env,origin,'/data/canonical-routes/'+await prefix(id)+'.json');return shard&&Object.hasOwn(shard,id)&&typeof shard[id]==='string'?shard[id]:null}
function live(o,now){const stamp=Date.parse(o.checked_at);if(o.identity_review&&(!Number.isFinite(Date.parse(o.identity_expires_at))||Date.parse(o.identity_expires_at)<now))return false;return Number.isFinite(stamp)&&stamp<=now+300000&&now-stamp<=36*3600000}
export function view(product,rules,now=Date.now(),quantity=1,territory='standard'){
 const rows=product.offers.filter(o=>live(o,now));const available=rows.filter(o=>o.available),shops=new Set(available.filter(o=>o.quantity?.verified!==false).map(o=>o.merchant_id));
 const quotes=new Map(rows.map(o=>[o.id,trade.shipping(o,rules,quantity,territory,now)]));
 rows.sort((a,b)=>Number(b.available)-Number(a.available)||(quotes.get(a.id).total??Infinity)-(quotes.get(b.id).total??Infinity)||a.price-b.price||a.merchant.localeCompare(b.merchant,'it'));
 const comparable=available.filter(o=>quotes.get(o.id).total!==undefined);const best=comparable.length?Math.min(...comparable.map(o=>quotes.get(o.id).total)):null;
 return {now,rows,quotes,shops:shops.size,visibleShops:new Set(available.map(o=>o.merchant_id)).size,available,best,indexable:product.indexable&&shops.size>=2,quantity,territory};
}
export function historySummary(rows,days,now){
 const today=Math.floor(now/86400000)*86400000,cutoff=today-(days-1)*86400000;
 const valid=(rows||[]).filter(r=>/^\d{4}-\d{2}-\d{2}$/.test(r.day)&&Date.parse(r.day+'T00:00:00Z')>=cutoff&&Date.parse(r.day+'T00:00:00Z')<=today&&r.low>0&&r.high>=r.low&&r.count>0&&Number.isFinite(r.sum));
 const count=valid.reduce((n,r)=>n+r.count,0);
 return {rows:valid,low:valid.length?Math.min(...valid.map(r=>r.low)):null,high:valid.length?Math.max(...valid.map(r=>r.high)):null,mean:count?valid.reduce((n,r)=>n+r.sum,0)/count:null,days};
}
function historyHTML(product,state){
 return [30,90].map(days=>{const h=historySummary(product.history,days,state.now);if(!h.rows.length)return '<p>Nessuna rilevazione valida negli ultimi '+days+' giorni.</p>';
 const low=h.low,range=h.high-low||1,end=Math.floor(state.now/86400000)*86400000,start=end-(days-1)*86400000;
 const dots=h.rows.map(r=>'<circle cx="'+(10+(Date.parse(r.day+'T00:00:00Z')-start)/(end-start)*280).toFixed(2)+'" cy="'+(85-(r.low-low)/range*70).toFixed(2)+'" r="3" fill="currentColor"/>').join('');
 return '<section class="panel"><h3>Ultimi '+days+' giorni</h3><p>Minimo '+money(h.low)+' · massimo '+money(h.high)+' · media '+money(h.mean)+'. '+h.rows.length+' giorni con rilevazioni.</p><svg viewBox="0 0 300 100" role="img" aria-label="Minimi giornalieri osservati: ogni punto è un giorno realmente rilevato" style="max-width:420px;width:100%">'+dots+'</svg><p class="micro">Media delle ultime osservazioni giornaliere disponibili, una per negozio; giorni mancanti non ricostruiti. Spedizione esclusa.</p></section>';
 }).join('');
}
export function content(product,state){
 const url='https://offerte4zampe.it/prodotto/'+product.slug;
 const single=state.shops<2;
 const rows=state.rows.map(o=>{
  const q=state.quotes.get(o.id),unknown=o.quantity?.verified===false;
  const target=trade.merchantUrl(o)?trade.goUrl(o,'product'):'',rel=o.affiliate_url?'sponsored nofollow noopener noreferrer':'nofollow noopener noreferrer';
  const badge=o.available&&state.best!==null&&q.total===state.best?'<span class="tag">Totale più basso verificabile</span>':'';
  const age=Math.max(0,Math.floor((state.now-Date.parse(o.checked_at))/3600000));
  const status=unknown?'Formato non verificato':o.available?'Disponibile al rilevamento':'Esaurito al rilevamento';
  const report='/segnala-errore#'+new URLSearchParams({id:o.id,title:o.title,shop:o.merchant,price:o.price,checked:o.checked_at});
  return '<tr><th scope="row">'+esc(o.merchant)+badge+(o.identity_review?'<small>Abbinamento revisionato</small>':'')+'</th><td data-label="Prezzo">'+money(o.price)+'</td><td data-label="Spedizione">'+(q.fee!==undefined?money(q.fee):'Da verificare')+'</td><td data-label="Totale"><strong>'+(q.total!==undefined?money(q.total):'Non calcolabile')+'</strong></td><td data-label="Prezzo unitario">'+(o.unit_price!==null&&o.unit_price!==undefined?money(o.unit_price)+'/'+esc(o.unit_price_unit):'Non verificato')+'</td><td data-label="Disponibilità">'+status+'<small><time datetime="'+esc(o.checked_at)+'">'+esc(new Date(o.checked_at).toLocaleString('it-IT',{timeZone:'Europe/Rome'}))+'</time> · '+age+' ore fa</small></td><td data-label="Negozio">'+(target&&o.available?'<a class="btn secondary" href="'+esc(target)+'" target="_blank" rel="'+rel+'">Vai al negozio ↗</a>':'')+'<a class="micro" href="'+esc(report)+'" rel="nofollow">Segnala errore</a></td></tr>';
 }).join('');
 const schema={'@context':'https://schema.org','@type':'Product',name:product.name,brand:{'@type':'Brand',name:product.brand},url};
 if(product.gtin)schema['gtin'+product.gtin.length]=product.gtin;
 if(safe(product.image))schema.image=product.image;
 if(state.available.length)schema.offers={'@type':'AggregateOffer',priceCurrency:'EUR',lowPrice:Math.min(...state.available.map(o=>o.price)),highPrice:Math.max(...state.available.map(o=>o.price)),offerCount:state.available.length,offers:state.available.map(o=>({'@type':'Offer',priceCurrency:'EUR',price:o.price,url:safe(o.url),availability:'https://schema.org/InStock',seller:{'@type':'Organization',name:o.merchant}}))};
 const name=product.name+(state.available.length?': prezzi da '+money(Math.min(...state.available.map(o=>o.price)))+' in '+state.visibleShops+' negoz'+(state.visibleShops===1?'io':'i'):' · offerte non disponibili');
 const options=Array.from({length:10},(_,i)=>'<option value="'+(i+1)+'"'+(state.quantity===i+1?' selected':'')+'>'+(i+1)+'</option>').join('');
 const image=safe(product.image)?'<img class="canonical-image" src="'+esc(product.image)+'" width="240" height="210" alt="'+esc(product.name)+'" fetchpriority="high">':'';
 const message=state.rows.length?(state.shops===0?'Formato non verificato: l’offerta non partecipa ai confronti di prezzo totale.':single?'Una sola offerta identificata: questa scheda non è un confronto tra negozi.':'Confronta lo stesso prodotto e formato in '+state.shops+' negozi.'):'Nessuna offerta recente disponibile. I vecchi prezzi non sono presentati come attuali.';
 const body='<section class="pagehero"><div class="wrap"><nav aria-label="Percorso"><a href="/">Home</a> / <a href="/confronta-cibo">Prodotti</a></nav><h1>'+esc(product.name)+'</h1><p>'+esc(product.brand)+' · '+esc(product.format)+(product.gtin?' · GTIN '+esc(product.gtin):'')+'</p></div></section><section class="section"><div class="wrap"><div class="canonical-intro">'+image+'<div><p class="notice">'+message+'</p><p>Prezzi rilevati, da confermare nel negozio. Il totale comprende soltanto la spedizione standard verificabile; le spese sconosciute non valgono zero.</p></div></div><h2>Offerte e prezzi nei negozi</h2><form class="panel canonical-controls" method="get" action="'+esc(url)+'"><label>Confezioni <select name="quantity">'+options+'</select></label><label>Consegna <select name="territory"><option value="standard"'+(state.territory==='standard'?' selected':'')+'>Standard Italia</option><option value="special"'+(state.territory==='special'?' selected':'')+'>Località o servizi particolari</option></select></label><button class="btn secondary">Ricalcola totale</button></form>'+(rows?'<div class="comparison-scroll"><table class="comparison-table canonical-offers"><caption>Prezzo, costo di consegna e totale per la quantità selezionata</caption><thead><tr>'+['Negozio','Prezzo','Spedizione','Totale','Prezzo unitario','Disponibilità e aggiornamento','Offerta'].map(n=>'<th scope="col">'+n+'</th>').join('')+'</tr></thead><tbody>'+rows+'</tbody></table></div>':'<p><a href="/confronta-cibo?brand='+encodeURIComponent(product.brand)+'">Cerca altre offerte della marca →</a></p>')+'<p class="micro">I collegamenti affiliati possono generare una commissione, senza costi aggiuntivi. Le commissioni non determinano l’ordine. '+(product.reviewed?'Alcuni collegamenti tra offerte derivano da una revisione delle schede, con provenienza e scadenza conservate.':'')+'</p><h2>Storico prezzi</h2><p>Rilevazioni effettive per negozio e confezione; nessun prezzo storico inventato.</p>'+historyHTML(product,state)+state.rows.map(o=>'<section class="panel"><h3>'+esc(o.merchant)+'</h3><div data-history-offer="'+esc(o.id)+'"></div></section>').join('')+(product.related?.length?'<h2>Altri formati della stessa linea</h2><ul>'+product.related.map(p=>'<li><a href="/prodotto/'+esc(p.slug)+'">'+esc(p.name)+' · '+esc(p.format)+'</a></li>').join('')+'</ul>':'')+'<p><a href="/confronta-cibo?brand='+encodeURIComponent(product.brand)+'">Altri prodotti '+esc(product.brand)+' →</a> · <a href="/chi-siamo">Metodo e fonti</a></p></div></section>';
 return {body,schema,title:name,description:message+' '+product.brand+' · '+product.format+'. Consulta prezzi, spedizione e storico delle rilevazioni.',url};
}
export async function canonicalProduct(request,env,now=Date.now()){
 const url=new URL(request.url);if(!['GET','HEAD'].includes(request.method))return new Response(null,{status:405,headers:{Allow:'GET, HEAD'}});
 let slug;try{slug=decodeURIComponent(url.pathname.slice('/prodotto/'.length))}catch{return new Response('URL non valido',{status:400})}
 if(!/^[a-z0-9][a-z0-9-]{1,200}$/.test(slug))return new Response('Prodotto non trovato',{status:404});
 const shard=await jsonAsset(env,url.origin,'/data/canonical-products/'+await prefix(slug)+'.json');const p=shard&&Object.hasOwn(shard,slug)?shard[slug]:null;
 if(!p)return new Response('Prodotto non trovato',{status:404,headers:{'Content-Type':'text/plain; charset=utf-8'}});
 if(p.redirect_slug&&/^[a-z0-9][a-z0-9-]{1,200}$/.test(p.redirect_slug)&&p.redirect_slug!==slug)return Response.redirect(new URL('/prodotto/'+p.redirect_slug,url.origin).href,301);
 const rules=await jsonAsset(env,url.origin,'/data/shipping-rules.json');const quantity=Number(url.searchParams.get('quantity')||1),territory=url.searchParams.get('territory')==='special'?'special':'standard';
 if(!Number.isInteger(quantity)||quantity<1||quantity>10)return new Response('Quantità non valida',{status:400});
 const loaded=await shippingSource(env,p.offers,rules,{now,quantity,territory});
 const state=view(p,loaded.rules,now,quantity,territory),page=content(p,state);
 const template=await env.ASSETS.fetch(new Request(new URL('/prodotto',url.origin)));if(!template.ok)return template;
 let html=await template.text();
 html=html.replace('<head>','<head><base href="/">').replace(/<main\b[\s\S]*?<\/main>/,()=>'<main id="main" data-canonical-product="'+esc(p.id)+'">'+page.body+'</main>')
 .replace(/<title>[^<]*<\/title>/,()=>'<title>'+esc(page.title)+' | Offerte a 4 Zampe</title>')
 .replace(/<meta name="description" content="[^"]*">/,()=>'<meta name="description" content="'+esc(page.description)+'">')
 .replace(/<meta name="robots" content="[^"]*">/,()=>'<meta name="robots" content="'+(state.indexable&&quantity===1&&territory==='standard'?'index,follow':'noindex,follow')+'">')
 .replace(/<link rel="canonical" href="[^"]*">/,()=>'<link rel="canonical" href="'+page.url+'">')
 .replace(/<meta property="og:(title|description|url)" content="[^"]*">/g,(_,key)=>'<meta property="og:'+key+'" content="'+esc(key==='title'?page.title:key==='url'?page.url:page.description)+'">')
 .replace(/<script src="assets\/product\.js[^\"]*" defer><\/script>/,'')
 .replace('</head>','<script type="application/ld+json">'+JSON.stringify(page.schema).replace(/</g,'\\u003c')+'</script></head>');
 const headers={'Content-Type':'text/html; charset=utf-8','Cache-Control':'public, max-age=300','X-Product-Model':'canonical-v1'};
 return new Response(request.method==='HEAD'?null:html,{status:200,headers});
}
