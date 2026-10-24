(()=>{'use strict';
const status=document.getElementById('newsletter-status'),link=document.getElementById('newsletter-signup'),frame=document.getElementById('newsletter-frame');
if(!status||!link)return;
fetch('/data/newsletter.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error();return r.json()}).then(config=>{
 const cancel=document.getElementById('newsletter-unsubscribe'),url=O4ZNewsletter.unsubscribeUrl(config);if(cancel&&url){cancel.href=url;cancel.hidden=false;}
 const ready=O4ZNewsletter.readiness(config);if(!ready.ready)return;
 const u=new URL(ready.signup_url);
 link.href=u.href;link.hidden=false;status.textContent='Iscrizioni aperte. Si apre il modulo Brevo: conferma la tua email per completare l’iscrizione.';
 if(frame){frame.src=u.href;frame.hidden=false;}
 const badge=document.getElementById('newsletter-availability');if(badge)badge.textContent='Una mail alla settimana';
}).catch(()=>{status.textContent='Le iscrizioni sono temporaneamente non disponibili. Riprova più tardi.'});
})();
