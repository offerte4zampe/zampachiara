(()=>{'use strict';
const $=id=>document.getElementById(id),money=new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR'});
const el=(tag,value,cls)=>{const n=document.createElement(tag);n.textContent=value;if(cls)n.className=cls;return n};
const safe=s=>{try{const u=new URL(s);return u.protocol==='https:'&&!u.username&&!u.password?u.href:''}catch{return ''}};
let catalog,id,shippingRules=null,amazonLinks=null;const offerTools=new Map();
function render(){
 const quantity=Number($('product-quantity').value),territory=$('product-territory').value;
 const view=O4ZProduct.productView(catalog,id,Date.now(),shippingRules,quantity,territory);
 if(!view){$('product-status').textContent='Questo prodotto non è presente nel catalogo corrente. Non mostriamo prezzi precedenti come attuali.';return}
 const amazon=$('product-amazon');amazon.replaceChildren();amazon.hidden=true;
 const amazonLink=O4ZAmazon.comparisonLink(view.seed,catalog.offers,amazonLinks);
 amazon.hidden=false;amazon.append(el('h2','Amazon'),el('p','Prezzo: non disponibile · Disponibilità: non verificata','micro'));
 if(amazonLink){
  amazon.append(el('p','Prezzo e disponibilità da verificare su Amazon. Questa opzione non partecipa alla classifica dei prezzi.','micro'));
  const link=el('a','Verifica prezzo su Amazon ↗','btn secondary');link.href=amazonLink.url;link.target='_blank';link.rel='sponsored noopener noreferrer';amazon.append(link,el('p','Possiamo ricevere una commissione, senza costi aggiuntivi per te.','micro'));
 }
 else amazon.append(el('p','Corrispondenza esatta non ancora verificata: non proponiamo ricerche generiche o prodotti simili.','micro'));
 const o=view.seed;$('product-title').textContent=o.title;document.title=o.title+' — prezzi nei negozi | Offerte a 4 Zampe';
 $('product-format').textContent=[o.brand,o.variant,o.weight_kg?o.weight_kg+' kg':''].filter(Boolean).join(' · ');
 const image=safe(o.image);if(image){const img=document.createElement('img');img.src=image;img.alt=o.title;img.width=180;img.height=160;img.style.objectFit='contain';$('product-image').replaceChildren(img)}
 $('product-status').textContent=view.exact?'Confronto dello stesso GTIN, marca e peso netto. Verifica comunque ricetta e confezione prima di acquistare.':'Identità condivisa non verificabile: mostriamo la sola offerta selezionata, senza abbinare prodotti dai nomi simili.';
 const grid=$('product-shops');grid.replaceChildren();for(const shop of view.shops){
 const card=el('article','','panel');card.dataset.productShop=shop.source.id;card.append(el('h2',shop.source.name));
 if(shop.source.status==='pending-feed'){
 card.append(el('p','Prezzo: non disponibile · Disponibilità: non verificata','micro'),el('p','Catalogo '+shop.source.name+' non ancora collegato. Non possiamo confermare lo stesso prodotto e formato né indicarne il prezzo.','micro'));
 }
 else if(shop.state!=='listed'){const labels={missing:'Non presente nel catalogo di questo negozio',unknown:'Disponibilità non verificabile: catalogo non aggiornato o non disponibile',unmatched:'Corrispondenza non verificata in questo negozio',stale:'Dati da aggiornare: prezzo e disponibilità non confermati'};card.append(el('p',labels[shop.state]));}
 for(const offer of shop.offers){
 const row=el('section','','matched-offer');row.append(el('p',offer.variant||offer.title,'micro'),el('strong',money.format(offer.price)),el('p',offer.weight_kg?money.format(offer.price/offer.weight_kg)+'/kg · spedizione esclusa':'Spedizione esclusa','micro'),el('p',offer.available?'Disponibile al rilevamento':'Esaurito al rilevamento'),el('p','Rilevato: '+new Date(offer.checked_at).toLocaleString('it-IT'),'micro'));
 const quote=shop.quotes.get(offer.id);const estimate=el('p',quote.total!==undefined?'Totale stimato: '+money.format(quote.total)+' ('+quantity+' confezioni · spedizione '+money.format(quote.fee)+')':'Totale non calcolato: '+quote.reason,'micro');estimate.dataset.shippingEstimate=offer.id;row.append(estimate);
 if(quote.rule){const conditions=el('a','Condizioni di spedizione','micro');conditions.href=safe(quote.rule.source);conditions.target='_blank';conditions.rel='noopener noreferrer';conditions.dataset.shippingConditions='';row.append(conditions)}
 const target=safe(offer.affiliate_url||offer.url);
 if(offer.available&&target){const a=el('a','Vai al negozio ↗','btn');a.href=target;a.target='_blank';a.rel=offer.affiliate_url?'sponsored noopener noreferrer':'noopener noreferrer';row.append(a);if(offer.affiliate_url)row.append(el('p','Possiamo ricevere una commissione, senza costi aggiuntivi per te.','micro'))}
 if(!offerTools.has(offer.id)){
  const tools=el('div','','product-tools');tools.append(O4ZHistory.mount(offer.id),O4ZDaily.mount(offer));
  const add=el('button','Aggiungi una confezione alla lista','btn secondary');add.type='button';add.dataset.productBasket=offer.id;add.disabled=!offer.available;add.onclick=()=>{$('product-list-status').textContent=O4ZBasket.addProduct(offer,catalog.offers)};tools.append(add);
  const report=el('a','Prezzo o dati sbagliati? Segnala','micro');report.href=O4ZTrade.reportUrl(offer);report.dataset.productReport='';tools.append(report);
  offerTools.set(offer.id,tools);
 }
 row.append(offerTools.get(offer.id));
 card.append(row)}
 grid.append(card)}
 $('product-coverage').textContent='Confrontiamo '+view.shops.filter(s=>s.source.status!=='pending-feed').length+' cataloghi importati, non tutto il mercato. L’assenza dal catalogo non prova che il negozio non venda il prodotto. Prezzi non in tempo reale; conferma disponibilità e totale nel negozio.';
}
async function load(){try{
 id=new URLSearchParams(location.search).get('id');if(!id)throw Error('missing');
 const amazon=fetch('data/amazon-links.json',{cache:'no-cache'}).then(r=>r.ok?r.json():null).catch(()=>null);
 const rules=fetch('data/shipping-rules.json',{cache:'no-cache'}).then(r=>r.ok?r.json():null).catch(()=>null);
 const r=await fetch('data/catalog.json.gz',{cache:'no-cache'});if(!r.ok)throw Error('network');
 const bytes=await r.arrayBuffer(),raw=new Uint8Array(bytes);
 catalog=JSON.parse(raw[0]===31&&raw[1]===139?await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).text():new TextDecoder().decode(bytes));
 [shippingRules,amazonLinks]=await Promise.all([rules,amazon]);render();
 const selected=catalog.offers.find(o=>o.id===id);if(selected)O4ZShare.mount($('product-share'),selected);
 for(const control of ['product-quantity','product-territory'])$(control).addEventListener('change',render);
 }catch{$('product-status').textContent='Impossibile caricare questa scheda. Riprova tra poco oppure torna alla ricerca.'}}
load();
})();