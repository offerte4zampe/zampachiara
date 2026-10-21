(()=>{'use strict';const $=id=>document.getElementById(id),money=new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR'}),integer=new Intl.NumberFormat('it-IT');
const el=(tag,value,cls)=>{const e=document.createElement(tag);e.textContent=value;if(cls)e.className=cls;return e};
const url=s=>{try{const u=new URL(s);return u.protocol==='https:'?u.href:''}catch{return ''}};
function link(label,params,cls){const a=el('a',label,cls);a.href='confronta-cibo.html?'+new URLSearchParams(params);return a}
function productTitle(o,tag){const h=el(tag,''),a=el('a',o.title,'product-title-link'),dest='prodotto.html?'+new URLSearchParams({id:o.id});if(!dest)return el(tag,o.title);a.href=dest;h.append(a);return h}
function card(o,spotlight=false){const a=document.createElement('article');a.className=spotlight?'spotlight-product':'home-deal';a.dataset.homeOffer=o.checked_at;const im=url(o.image);if(im){const img=document.createElement('img');img.src=im;img.alt='';img.loading=spotlight?'eager':'lazy';img.width=160;img.height=145;a.append(img)}
a.append(el('p',o.merchant+' · '+o.brand,'micro'),productTitle(o,spotlight?'h2':'h3'),el('p',o.variant,'micro'));const p=el('p','','catalog-price');p.append(el('strong',money.format(o.price)));if(O4ZTrade.discount(o)){p.append(el('del',money.format(o.previous_price)),el('span','−'+Math.round((1-o.price/o.previous_price)*100)+'%','catalog-sale'))}a.append(p);
if(o.weight_kg)a.append(el('p',money.format(o.price/o.weight_kg)+'/kg · spedizione esclusa','micro'));
a.append(el('p','Rilevato: '+new Date(o.checked_at).toLocaleString('it-IT'),'micro'));
const detail=el('a','Confronta nei negozi →','btn secondary');detail.href='prodotto.html?'+new URLSearchParams({id:o.id});a.append(detail);const report=el('a','Prezzo o dati sbagliati? Segnala','micro');report.href=O4ZTrade.reportUrl(o);a.append(report);return a}
O4ZSuggest.mount($('home-query'),O4ZSuggest.catalog,o=>{if(o.id){$('home-query').dataset.selectedProduct=o.id;location.assign('prodotto.html?'+new URLSearchParams({id:o.id}))}});
$('home-query').addEventListener('input',()=>{delete $('home-query').dataset.selectedProduct});
$('home-query').form.addEventListener('submit',e=>{const id=$('home-query').dataset.selectedProduct;if(id){e.preventDefault();location.assign('prodotto.html?'+new URLSearchParams({id}))}});
$('home-query').addEventListener('focus',()=>{O4ZSuggest.catalog().catch(()=>{})},{once:true});
const fresh=s=>Number.isFinite(Date.parse(s))&&Date.now()-Date.parse(s)<=36*3600000&&Date.now()-Date.parse(s)>=-300000;
for(const node of document.querySelectorAll('[data-home-offer]'))if(!fresh(node.dataset.homeOffer))node.replaceChildren(el('p','Rilevazione da aggiornare. Consulta il catalogo per verificare il prezzo.','micro'),link('Apri il catalogo →',{},'btn secondary'));
(async()=>{try{const r=await fetch('data/home.json',{cache:'no-cache'});if(!r.ok)throw Error();const d=await r.json();if(document.getElementById('main').dataset.homeGenerated===d.generated_at)return;const rows=d.offers.filter(o=>Number.isFinite(o.price)&&o.price>0&&o.available&&url(o.url));
$('home-stats').replaceChildren(el('span',integer.format(d.stats.offers)+' offerte importate'),el('span',d.stats.brands+' marche'),el('span',(d.sources||[]).filter(s=>s.offers>0).length+' negozi'),el('span','Aggiornamenti ogni '+d.refresh_hours+' ore'));
const recent=rows.filter(o=>fresh(o.checked_at));const sales=recent.filter(o=>o.image);
const picked=[],brands=new Set();for(const source of d.sources||[]){const found=sales.find(o=>o.merchant_id===source.id&&!brands.has(o.brand));if(found){picked.push(found);brands.add(found.brand)}}for(const o of sales){if(picked.length>=6)break;if(!brands.has(o.brand)){picked.push(o);brands.add(o.brand)}}
$('home-deals').replaceChildren(...picked.map(o=>card(o)));$('home-deals-status').textContent=picked.length?'Ultimo aggiornamento catalogo: '+new Date(d.generated_at).toLocaleString('it-IT')+'. Una selezione di offerte, non una classifica dell’intero mercato.':'Al momento non ci sono offerte recenti da mostrare. Consulta il catalogo completo.';
const hero=recent.find(o=>/royal canin|purina|trainer/i.test(o.brand)&&o.price>=15&&o.image)||picked[0];if(hero)$('home-spotlight').replaceChildren(card(hero,true));else $('home-spotlight').replaceChildren(link('Esplora il catalogo →',{} ,'btn secondary'));
$('home-brands').replaceChildren(...d.top_brands.map(brand=>link(brand,{brand})));
$('home-shops').replaceChildren(...(d.sources||[]).filter(s=>s.offers>0).map(s=>link(s.name+' · '+integer.format(s.offers)+' offerte →',{shop:s.name})));
}catch{$('home-deals-status').textContent+=' Aggiornamento online non disponibile: controlla la data delle offerte e verifica nel negozio.';}})();})();
