(()=>{'use strict';
const $=id=>document.getElementById(id),money=new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR'});
const el=(tag,value,cls)=>{const n=document.createElement(tag);n.textContent=value;if(cls)n.className=cls;return n};
const safe=s=>{try{const u=new URL(s);return u.protocol==='https:'&&!u.username&&!u.password?u.href:''}catch{return ''}};
async function load(){try{
 const id=new URLSearchParams(location.search).get('id');if(!id)throw Error('missing');
 const r=await fetch('data/catalog.json.gz',{cache:'no-cache'});if(!r.ok)throw Error('network');
 const bytes=await r.arrayBuffer(),raw=new Uint8Array(bytes);
 const catalog=JSON.parse(raw[0]===31&&raw[1]===139?await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).text():new TextDecoder().decode(bytes));
 const view=O4ZProduct.productView(catalog,id);if(!view){$('product-status').textContent='Questo prodotto non è presente nel catalogo corrente. Non mostriamo prezzi precedenti come attuali.';return}
 const o=view.seed;$('product-title').textContent=o.title;document.title=o.title+' — prezzi nei negozi | Offerte a 4 Zampe';
 $('product-format').textContent=[o.brand,o.variant,o.weight_kg?o.weight_kg+' kg':''].filter(Boolean).join(' · ');
 const image=safe(o.image);if(image){const img=document.createElement('img');img.src=image;img.alt=o.title;img.width=180;img.height=160;img.style.objectFit='contain';$('product-image').replaceChildren(img)}
 $('product-status').textContent=view.exact?'Confronto dello stesso GTIN, marca e peso netto. Verifica comunque ricetta e confezione prima di acquistare.':'Identità condivisa non verificabile: mostriamo la sola offerta selezionata, senza abbinare prodotti dai nomi simili.';
 const grid=$('product-shops');for(const shop of view.shops){
 const card=el('article','','panel');card.dataset.productShop=shop.source.id;card.append(el('h2',shop.source.name));
 if(shop.state!=='listed'){const labels={missing:'Non presente nel catalogo di questo negozio',unknown:'Disponibilità non verificabile: catalogo non aggiornato o non disponibile',unmatched:'Corrispondenza non verificata in questo negozio',stale:'Dati da aggiornare: prezzo e disponibilità non confermati'};card.append(el('p',labels[shop.state]));}
 for(const offer of shop.offers){
 const row=el('section','','matched-offer');row.append(el('p',offer.variant||offer.title,'micro'),el('strong',money.format(offer.price)),el('p',offer.weight_kg?money.format(offer.price/offer.weight_kg)+'/kg · spedizione esclusa':'Spedizione esclusa','micro'),el('p',offer.available?'Disponibile al rilevamento':'Esaurito al rilevamento'),el('p','Rilevato: '+new Date(offer.checked_at).toLocaleString('it-IT'),'micro'));
 const target=safe(offer.affiliate_url||offer.url);
 if(offer.available&&target){const a=el('a','Vai al negozio ↗','btn');a.href=target;a.target='_blank';a.rel=offer.affiliate_url?'sponsored noopener noreferrer':'noopener noreferrer';row.append(a);if(offer.affiliate_url)row.append(el('p','Possiamo ricevere una commissione, senza costi aggiuntivi per te.','micro'))}
 card.append(row)}
 grid.append(card)}
 $('product-coverage').textContent='Confrontiamo '+view.shops.length+' cataloghi importati, non tutto il mercato. L’assenza dal catalogo non prova che il negozio non venda il prodotto. Prezzi non in tempo reale; conferma disponibilità e totale nel negozio.';
 }catch{$('product-status').textContent='Impossibile caricare questa scheda. Riprova tra poco oppure torna alla ricerca.'}}
load();
})();