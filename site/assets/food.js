(function(){'use strict';
 const ids=['ap','ak','ag','as','bp','bk','bg','bs'];
 const defaults={ap:49.9,ak:10,ag:250,as:0,bp:42.9,bk:7,bg:210,bs:0};
 const euro=new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR',maximumFractionDigits:2});
 const num=new Intl.NumberFormat('it-IT',{maximumFractionDigits:1});
 const $=id=>document.getElementById(id);
 function compute(p,k,g,s){
   if(![p,k,g,s].every(Number.isFinite)||p<=0||k<=0||g<=0||s<0||p>100000||k>1000||g>20000||s>10000)return null;
   return {kg:(p+s)/k,day:(p+s)*g/(1000*k),days:1000*k/g};
 }
 function render(){
   const vals=Object.fromEntries(ids.map(id=>[id,Number($(id).value)]));
   const a=compute(vals.ap,vals.ak,vals.ag,vals.as),b=compute(vals.bp,vals.bk,vals.bg,vals.bs);
   const valid=ids.every(id=>$(id).value.trim()!=='' )&&a&&b;
   $('fooderror').hidden=Boolean(valid);$('foodresults').hidden=!valid;
   if(!valid){$('winner').textContent='Inserisci importi e quantità validi per confrontare.';return;}
   $('daya').textContent=euro.format(a.day);$('dayb').textContent=euro.format(b.day);
   $('montha').textContent=euro.format(a.day*30);$('monthb').textContent=euro.format(b.day*30);
   $('kga').textContent=euro.format(a.kg);$('kgb').textContent=euro.format(b.kg);
   $('lasta').textContent=num.format(a.days)+' giorni';$('lastb').textContent=num.format(b.days)+' giorni';
   const diff=Math.abs(a.day-b.day)*30;
   $('winner').textContent=diff<.005?'I due prodotti hanno lo stesso costo mensile stimato.':
      'Con questi valori, il prodotto '+(a.day<b.day?'A':'B')+' costa circa '+euro.format(diff)+' in meno ogni 30 giorni. Non è una valutazione nutrizionale.';
 }
 ids.forEach(id=>$(id).addEventListener('input',render));
 $('resetfood').addEventListener('click',()=>{ids.forEach(id=>$(id).value=defaults[id]);$('sharestatus').textContent='';render()});
 // Use hash, not query params: data in the fragment is not sent to the hosting server.
 function restore(){try{const h=new URLSearchParams(location.hash.replace(/^#/,''));if(h.get('v')!=='1')return;ids.forEach(id=>{const v=h.get(id);if(v!==null&&v.length<=15&&/^\d+(?:\.\d+)?$/.test(v))$(id).value=v})}catch{}}
 $('sharefood').addEventListener('click',async()=>{
   if(!$('fooderror').hidden){$('sharestatus').textContent='Correggi prima i valori.';return;}
   const p=new URLSearchParams({v:'1'});ids.forEach(id=>p.set(id,$(id).value));
   const url=location.href.split('#')[0]+'#'+p.toString();
   try{if(navigator.share)await navigator.share({title:'Confronto costo cibo · ZampaChiara',url});
     else if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(url);$('sharestatus').textContent='Link copiato. Le cifre sono visibili a chi lo riceve.'}
     else{$('sharestatus').textContent='Link da copiare: '+url}
   }catch(e){if(e.name!=='AbortError')$('sharestatus').textContent='Copia manualmente il link: '+url}
 });
 restore();render();
})();