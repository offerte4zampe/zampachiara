/* Filters precomputed search/facet records; no network or shipping calculations. */
(function(scope){'use strict';
function matches(o,f){return (!f.shop||o.merchant===f.shop)&&(!f.brand||o.brand===f.brand)&&(!f.stock||o.available)&&Object.entries(f.facets||{}).every(([k,v])=>!v||o.facets[k]===v||(k==='animal'&&o.facets.animal==='Cane e gatto'))&&(f.words||[]).every(w=>o.search.includes(w))}
let rows=[];
if(scope)scope.onmessage=e=>{const m=e.data;if(m.type==='init'){rows=m.rows;return}if(m.type==='filter')scope.postMessage({id:m.id,ids:rows.filter(o=>matches(o,m.filters)).map(o=>o.id)})};
if(typeof module!=='undefined')module.exports={matches};
})(typeof self!=='undefined'?self:null);
