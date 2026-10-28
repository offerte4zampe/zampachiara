(function(){'use strict';const m=document.getElementById('mobilemenu');const n=document.getElementById('navlinks');if(m&&n)m.addEventListener('click',()=>{const v=n.classList.toggle('open');m.setAttribute('aria-expanded',String(v))});document.querySelectorAll('[data-year]').forEach(x=>x.textContent=String(new Date().getFullYear()));})();
/* Seasonal decoration: Rome calendar, automatically ends after Halloween 2026. */
(function(){'use strict';
 const today=new Intl.DateTimeFormat('sv-SE',{timeZone:'Europe/Rome',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
 if(today<'2026-10-28'||today>'2026-11-01')return;
 document.documentElement.classList.add('halloween');
 const hero=document.querySelector('.shopping-hero');
 if(hero){
  const badge=hero.querySelector('.eyebrow');if(badge)badge.textContent='Halloween a 4 zampe';
  const bubble=hero.querySelector('.pet-bubble');if(bubble)bubble.textContent='Dolcetto o crocchetta?';
  const art=hero.querySelector('.pet-hero-art');
  if(art&&!art.querySelector('.halloween-art')){
   const decor=document.createElement('img');decor.className='halloween-art';decor.src='/assets/halloween.svg';decor.alt='';decor.setAttribute('aria-hidden','true');decor.width=640;decor.height=560;art.append(decor);
  }
 }
})();
