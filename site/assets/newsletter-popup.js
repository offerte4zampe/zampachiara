/* Optional invitation; no email collection or third-party requests on the home. */
(function(root){'use strict';
const KEY='o4z-newsletter-popup-until-v1',DAY=86400000;
function shouldShow(now,until){return Number.isFinite(now)&&Number.isFinite(until)&&until<=now}
function mount(win){
 const doc=win.document;if(!['/','/index.html'].includes(win.location.pathname)||doc.getElementById('newsletter-popup'))return;
 let storage;for(const name of ['localStorage','sessionStorage']){try{const candidate=win[name];candidate.getItem(KEY);storage=candidate;break}catch{}}
 if(!storage)return;
 function until(){try{const raw=storage.getItem(KEY);if(raw===null)return 0;const value=Number(raw);return Number.isFinite(value)&&value>=0?value:Infinity}catch{return Infinity}}
 if(!shouldShow(Date.now(),until()))return;
 const dialog=doc.createElement('dialog');if(typeof dialog.showModal!=='function')return;
 dialog.id='newsletter-popup';dialog.className='newsletter-popup';dialog.setAttribute('aria-labelledby','newsletter-popup-title');dialog.setAttribute('aria-describedby','newsletter-popup-description');
 dialog.innerHTML='<div class="newsletter-popup-card"><button type="button" class="newsletter-popup-close" aria-label="Chiudi invito newsletter" autofocus>×</button><span class="newsletter-popup-icon" aria-hidden="true">🐾</span><p class="newsletter-popup-eyebrow">Offerte da fiutare</p><h2 id="newsletter-popup-title">Guide, offerte e sconti.<br>Ogni settimana.</h2><p id="newsletter-popup-description">Consigli pratici, offerte selezionate e codici sconto per cani e gatti, direttamente nella tua email.</p><a class="btn newsletter-popup-signup" href="/newsletter">Iscriviti gratis alla newsletter →</a><p class="newsletter-popup-note">Una mail alla settimana. Puoi disiscriverti quando vuoi.</p><button type="button" class="newsletter-popup-later">Non ora</button><a class="newsletter-popup-privacy" href="/privacy">Privacy</a></div>';
 doc.body.append(dialog);let previous=null,timer;
 function dismiss(days){try{storage.setItem(KEY,String(Date.now()+days*DAY))}catch{}if(dialog.open)dialog.close();}
 dialog.querySelector('.newsletter-popup-close').addEventListener('click',()=>dismiss(14));dialog.querySelector('.newsletter-popup-later').addEventListener('click',()=>dismiss(14));
 dialog.querySelector('.newsletter-popup-signup').addEventListener('click',()=>dismiss(90));
 dialog.addEventListener('cancel',e=>{e.preventDefault();dismiss(14)});
 dialog.addEventListener('close',()=>{if(previous?.isConnected)previous.focus({preventScroll:true})});
 dialog.addEventListener('click',e=>{const r=dialog.getBoundingClientRect();if(e.target===dialog&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))dismiss(14)});
 function attempt(){if(!shouldShow(Date.now(),until())||dialog.open)return;if(doc.hidden||['INPUT','TEXTAREA','SELECT'].includes(doc.activeElement?.tagName)||doc.querySelector('dialog[open]')){timer=win.setTimeout(attempt,5000);return}previous=doc.activeElement;dialog.showModal();}
 timer=win.setTimeout(attempt,10000);win.addEventListener('pagehide',()=>win.clearTimeout(timer),{once:true});
}
const api={KEY,DAY,shouldShow,mount};if(typeof module!=='undefined'&&module.exports)module.exports=api;else if(root?.document)mount(root);
})(typeof window!=='undefined'?window:null);
