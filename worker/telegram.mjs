// No public publishing route. Only the Worker's scheduled handler reaches this object.
export const TEST_POST = {id:'telegram-test-v1',kind:'test',text:'🧪 MESSAGGIO DI PROVA — Offerte a 4 Zampe\nIl collegamento automatico al canale è attivo. Qui troverai consigli per risparmiare e segnalazioni verificate per cane e gatto.',path:'/'};
export const POSTS = [
 {id:'guide-unit-price-v1',kind:'guide',path:'/prezzo-confezione-o-prezzo-kg',text:'🐾 Il sacco meno caro è davvero il più conveniente?\nConfronta il prezzo al kg e lo stesso formato: il prezzo della confezione da solo può ingannare. Ecco come fare il confronto.',image:'/assets/social-guide.png'},
 {id:'guide-shipping-v1',kind:'guide',path:'/spedizione-gratuita-conviene',text:'📦 Spedizione gratuita: controlla il totale\nPrima di aggiungere prodotti per raggiungere la soglia, confronta quanto spenderesti pagando la consegna. La nostra guida ti aiuta a fare i conti.'},
 {id:'guide-identity-v1',kind:'guide',path:'/stesso-prodotto-formato-gtin',text:'🔎 Due confezioni simili possono essere prodotti diversi.\nRicetta, peso e codice prodotto contano: verifica che il confronto riguardi davvero lo stesso articolo prima di scegliere.'}
];
// A price report is not a claimed discount. Use only fresh available records
// from a successful current source; expose source/time and exclude delivery.
export function offerPost(offer,sources,now){
 const source=sources?.find(s=>s.id===offer?.merchant_id&&s.status==='ok');
 const stamp=Date.parse(offer?.checked_at),sourceStamp=Date.parse(source?.checked_at);
 if(!source||!Number.isFinite(stamp)||stamp>now||now-stamp>24*3600000||!Number.isFinite(sourceStamp)||sourceStamp>now||now-sourceStamp>24*3600000)return null;
 if(offer.available!==true||!Number.isFinite(offer.price)||offer.price<=0||!Number.isFinite(offer.weight_kg)||offer.weight_kg<=0)return null;
 if(typeof offer.id!=='string'||offer.id.length>200||typeof offer.title!=='string'||!offer.title.trim()||offer.title.length>240||typeof offer.variant!=='string'||!offer.variant.trim())return null;
 const euro=new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR'});
 const time=new Intl.DateTimeFormat('it-IT',{timeZone:'Europe/Rome',dateStyle:'short',timeStyle:'short'}).format(stamp);
 return {id:'catalog:'+offer.id,kind:'price_report',verified_at:stamp,path:'/prodotto?id='+encodeURIComponent(offer.id),text:'🐾 Prezzo rilevato sul comparatore\n'+offer.title+'\nFormato: '+offer.variant+'\n'+euro.format(offer.price)+' · '+euro.format(offer.price/offer.weight_kg)+'/kg\nNegozio: '+offer.merchant+'\nRilevazione catalogo: '+time+' (ora italiana). Spedizione esclusa. Prezzo e disponibilità da ricontrollare nel negozio prima dell’acquisto.'};
}
export function trackedUrl(post){
 const url=new URL(post.path,'https://offerte4zampe.it');
 if(url.origin!=='https://offerte4zampe.it'||url.username||url.password)throw new Error('invalid_site_link');
 url.searchParams.set('utm_source','telegram');url.searchParams.set('utm_medium','social');
 url.searchParams.set('utm_campaign',post.kind==='test'?'integration_test':'channel_editorial');url.searchParams.set('utm_content',post.id);
 return url.href;
}
export function payload(post,channel){
 if(channel!=='@sconti4zampe')throw new Error('invalid_channel');
 const text=post.text+'\n\n'+trackedUrl(post)+'\n\nTrasparenza: il sito contiene link affiliati; gli acquisti idonei possono generare una commissione.';
 if(text.length>(post.image?1024:4096))throw new Error('message_too_long');
 if(post.image){const image=new URL(post.image,'https://offerte4zampe.it');if(image.origin!=='https://offerte4zampe.it')throw new Error('invalid_image');return {method:'sendPhoto',body:{chat_id:channel,photo:image.href,caption:text,disable_notification:post.kind==='test'}};}
 return {method:'sendMessage',body:{chat_id:channel,text,disable_notification:post.kind==='test',link_preview_options:{is_disabled:true}}};
}
export async function telegramCall(token,method,body,transport=fetch){
 // Never return/log raw exceptions, response descriptions, request URLs or token.
 try{
  const response=await transport(`https://api.telegram.org/bot${token}/${method}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),signal:AbortSignal.timeout(12000)});
  const data=await response.json();
  if(response.ok&&data.ok&&Number.isSafeInteger(data.result?.message_id)&&data.result?.chat?.username?.toLowerCase()==='sconti4zampe')return {status:'sent',message_id:data.result.message_id};
  if(data.ok===false&&(response.status===429||data.error_code===429))return {status:'retry',retry_after:Math.min(86400,Math.max(1,Number(data.parameters?.retry_after)||60))};
  // 5xx/network timeouts may have succeeded remotely. Never retry automatically.
  return {status:response.status>=500||data.ok===true?'uncertain':'failed',code:Number(data.error_code)||response.status};
 }catch{return {status:'uncertain',code:'transport_or_response_error'};}
}
export class TelegramPublisher {
 constructor(state,env){this.state=state;this.env=env;this.chain=Promise.resolve();}
 fetch(request){
  // Internal binding only; request body cannot supply text, recipient or URLs.
  if(request.method==='GET')return this.state.storage.get('post:'+TEST_POST.id).then(test=>Response.json({integration:'telegram-v1',configured:Boolean(this.env.TELEGRAM_BOT_TOKEN)&&this.env.TELEGRAM_CHANNEL_ID==='@sconti4zampe',token_present:Boolean(this.env.TELEGRAM_BOT_TOKEN),channel_present:Boolean(this.env.TELEGRAM_CHANNEL_ID),channel_matches:this.env.TELEGRAM_CHANNEL_ID==='@sconti4zampe',test_status:test?.status||'pending',test_message_id:test?.message_id||null}));
  if(request.method!=='POST')return Promise.resolve(new Response(null,{status:405}));
  const run=this.chain.then(()=>this.tick());this.chain=run.catch(()=>{});
  return run.then(result=>Response.json(result));
 }
 async tick(now=Date.now()){
  const store=this.state.storage;
  if(!this.env.TELEGRAM_BOT_TOKEN||this.env.TELEGRAM_CHANNEL_ID!=='@sconti4zampe')return {status:'not_configured'};
  if(await store.get('halted'))return {status:'halted'};
  const test=await store.get('post:'+TEST_POST.id);
  let post;
  if(test?.status!=='sent')post=TEST_POST;
  else if(await store.get('retry_post'))post=await store.get('retry_post');
  else {
   // At most one ordinary post daily, 09:15 Europe/Rome; first ordinary post next day.
   const day=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Rome',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);
   const time=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Rome',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).format(now);
   if(time!=='09:15'||await store.get('last_day')===day)return {status:'idle'};
   // Two price-report days for each guide day, with safe guide fallback.
   if(new Date(now).getUTCDate()%3!==0){
    try{
     const data=await this.env.ASSETS.fetch(new Request('https://offerte4zampe.it/data/home.json'));
     if(data.ok){const home=await data.json();for(const offer of home.offers||[]){const candidate=offerPost(offer,home.sources,now);if(candidate&&!(await store.get('post:'+candidate.id))){post=candidate;break;}}}
    }catch{/* unavailable/invalid catalog: no fabricated prices */}
   }
   if(!post)for(const item of POSTS){if(!(await store.get('post:'+item.id))){post=item;break;}}
   if(!post)return {status:'queue_empty'};
  }
  const key='post:'+post.id,prior=await store.get(key);
  if(post.kind==='price_report'&&now-post.verified_at>24*3600000){await store.put(key,{id:post.id,status:'expired',finished_at:new Date(now).toISOString()});await store.delete('retry_post');return {status:'expired'};}
  if(prior&&prior.status!=='retry')return {status:prior.status};
  if(prior?.next_at>now)return {status:'waiting'};
  if((prior?.attempts||0)>=4){await store.put('halted',true);return {status:'halted'};}
  // Verify the linked page/image exists before reserving the send.
  for(const path of [post.path,...(post.image?[post.image]:[])]){
   const asset=await this.env.ASSETS.fetch(new Request(new URL(path,'https://offerte4zampe.it')));
   if(!asset.ok)return {status:'asset_unavailable'};
  }
  const request=payload(post,this.env.TELEGRAM_CHANNEL_ID);
  const pending={id:post.id,status:'sending',attempts:(prior?.attempts||0)+1,attempted_at:new Date(now).toISOString()};
  await store.put(key,pending); // persisted before network: restart cannot send twice
  const outcome=await telegramCall(this.env.TELEGRAM_BOT_TOKEN,request.method,request.body);
  const record={...pending,...outcome,finished_at:new Date().toISOString()};
  if(outcome.status==='retry'){record.next_at=Date.now()+outcome.retry_after*1000;await store.put('retry_post',post);}
  else await store.delete('retry_post');
  await store.put(key,record);
  if(outcome.status==='sent'){
   await store.put('last_day',new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Rome',year:'numeric',month:'2-digit',day:'2-digit'}).format(now));
  }else if(outcome.status!=='retry')await store.put('halted',true);
  console.log({type:'telegram_publish',id:post.id,status:outcome.status,...(outcome.message_id?{message_id:outcome.message_id}:{})});
  return {status:outcome.status};
 }
}
export async function scheduledTelegram(env){
 if(!env.TELEGRAM_PUBLISHER)return;
 const object=env.TELEGRAM_PUBLISHER.get(env.TELEGRAM_PUBLISHER.idFromName('sconti4zampe-v1'));
 await object.fetch(new Request('https://internal/tick',{method:'POST'}));
}
