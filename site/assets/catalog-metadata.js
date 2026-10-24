(function(root){'use strict';
const names=['Monge','GimCat','GimDog','Beaphar','Askoll','Ferplast','NaturalPet','Petup','Prolife','Inodorina','JBL','KONG','IMAC','ICF','DRN','Gemon','Leopet','O-life','Stefanplast','Tetra','Zolux','Yuup!','Furminator','Exo Terra','Edgard & Cooper',"Cat's Best"];
const key=s=>String(s||'').normalize('NFKC').toLocaleLowerCase('it').replace(/[\s&’'!._-]+/g,'');
const aliases=new Map(names.map(s=>[key(s),s]));
function brand(value){const text=String(value||'').trim().replace(/\s+/g,' ');return aliases.get(key(text))||text;}
function facets(o){
 const s=[o.title,o.variant,o.category].join(' ').toLocaleLowerCase('it');
 const dog=/\b(?:cane|cani|dog|dogs|puppy)\b/.test(s),cat=/\b(?:gatto|gatti|cat|cats|kitten)\b/.test(s);
 const animal=dog&&cat?'Cane e gatto':dog?'Cane':cat?'Gatto':'';
 let type='';if(/shampoo|detergente|toelett|balsamo|dentifricio|profumo/.test(s))type='';else if(/lettier|litter/.test(s))type='Lettiere';else if(/snack|masticativ|biscott|premiet|dentalife|dentastix/.test(s))type='Snack e premi';else if(/umido|mousse|pat[eèé]|bocconcini|bustine? |in salsa/.test(s))type='Cibo umido';else if(/crocchett|croccantin|cibo secco|\bsecco\b|dry food/.test(s))type='Cibo secco';else if(/gioc|\btoy\b|\btoys\b/.test(s))type='Giochi';
 const ages=[];if(/cucciol|puppy|kitten|junior/.test(s))ages.push('Cucciolo');if(/adult|adulti|adulte/.test(s))ages.push('Adulto');if(/senior|ageing|mature/.test(s))ages.push('Senior');
 const age=ages.length===1?ages[0]:'';
 const sizes=[];if(/\bmini\b|\bsmall\b|taglia piccola/.test(s))sizes.push('Piccola');if(/\bmedium\b|taglia media/.test(s))sizes.push('Media');if(/\bmaxi\b|\blarge\b|\bgiant\b|taglia grande/.test(s))sizes.push('Grande');
 const size=dog&&!cat&&sizes.length===1?sizes[0]:'';
 const kg=o.weight_kg,weight=!(kg>0)?'':kg<=1?'Fino a 1 kg':kg<=5?'Oltre 1 fino a 5 kg':kg<=10?'Oltre 5 fino a 10 kg':'Oltre 10 kg';
 return {animal,type,age,size,pack:weight};
}
function normalize(o){return {...o,brand:brand(o.brand)};}
function matchesFacets(f,filters){return Object.entries(filters).every(([k,v])=>!v||f[k]===v||(k==='animal'&&f.animal==='Cane e gatto'));}
function matches(o,filters){return matchesFacets(facets(o),filters);}
const api={brand,facets,normalize,matches,matchesFacets};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.O4ZMetadata=api;
})(typeof window!=='undefined'?window:null);
