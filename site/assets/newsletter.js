(()=>{'use strict';
const status=document.getElementById('newsletter-status'),link=document.getElementById('newsletter-signup'),frame=document.getElementById('newsletter-frame');
if(!status||!link)return;
fetch('/data/newsletter.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error();return r.json()}).then(config=>{
 if(config.double_opt_in_verified!==true||config.unsubscribe_verified!==true||!config.signup_url)return;
 const u=new URL(config.signup_url);if(u.protocol!=='https:'||u.username||u.password||!(u.hostname==='sibforms.com'||u.hostname.endsWith('.sibforms.com')))return;
 link.href=u.href;link.hidden=false;status.textContent='Iscrizioni aperte. Si apre il modulo Brevo: conferma la tua email per completare l’iscrizione.';
 if(frame){frame.src=u.href;frame.hidden=false;}
 const badge=document.getElementById('newsletter-availability');if(badge)badge.textContent='Una mail alla settimana';
}).catch(()=>{status.textContent='Le iscrizioni sono temporaneamente non disponibili. Riprova più tardi.'});
})();
