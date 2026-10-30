(function(root){'use strict';
const money=new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR'});
function name(value){let text=String(value||'').replace(/\bgr\b/gi,'g').replace(/\s+/g,' ').trim();const repeated=/(\d+(?:[.,]\d+)?)\s*(kg|g|ml|l)\b(?:\s*[·|/]\s*|\s+)\1\s*\2\b/gi;for(let i=0;i<3;i++)text=text.replace(repeated,'$1 $2');return text}
function title(value,brand='',format=''){
 let text=name(value),unit=String(format||'').trim();if(unit.length>20)unit='';
 if(unit){const escaped=unit.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/\s+/g,'\\s*');text=text.replace(new RegExp('(?:\\s*[·|]\\s*|\\s+)'+escaped+'$','i'),'').trim();}
 if(brand&&!text.toLocaleLowerCase('it').includes(String(brand).toLocaleLowerCase('it')))text=brand+' '+text;
 const suffix=(unit?' '+unit:'')+' | Prezzo e storico',budget=Math.max(8,60-suffix.length);
 if(text.length>budget){const cut=text.slice(0,budget),space=cut.lastIndexOf(' ');text=(space>budget*.6?cut.slice(0,space):cut).replace(/[\s·|,:;—-]+$/,'');}
 return text+suffix;
}
function description(offers,shops){
 const rows=(offers||[]).filter(o=>o.available&&Number.isFinite(o.price)&&o.price>0);if(!rows.length)return 'Offerte recenti non disponibili. Consulta lo storico dei prezzi osservati e verifica la disponibilità nel negozio.';
 const low=rows.reduce((a,b)=>a.price<=b.price?a:b),unit=Number.isFinite(low.unit_price)&&low.unit_price>0&&low.unit_price_unit?' ('+money.format(low.unit_price)+'/'+low.unit_price_unit+')':'';
 return (shops>=2?'Confronta '+shops+' negozi: da ':'Prezzo rilevato: ')+money.format(low.price)+unit+'. Spedizione stimata e storico prezzi.';
}
const api={name,title,description};if(typeof module!=='undefined')module.exports=api;else root.O4ZProductMetadata=api;
})(typeof window!=='undefined'?window:null);
