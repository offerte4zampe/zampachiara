(()=>{'use strict';const fallback='/assets/product-placeholder.svg';
function prepare(img){if(!(img instanceof HTMLImageElement))return;const card=img.closest('.catalog-card,.home-deal,.spotlight-product,.basket-offer,.matched-offer'),product=card||img.classList.contains('canonical-image')||img.closest('#product-image');if(!product)return;img.width=400;img.height=400;img.decoding='async';img.loading='lazy';if(!img.alt.trim()){const heading=card?.querySelector('h2,h3,.product-title-link');img.alt=heading?.textContent.trim()||'Immagine del prodotto';}}
function scan(root){if(root instanceof HTMLImageElement)prepare(root);root.querySelectorAll?.('img').forEach(prepare);}
document.addEventListener('error',e=>{const img=e.target;if(img instanceof HTMLImageElement&&img.src!==new URL(fallback,location.origin).href){img.src=fallback;img.dataset.imageFallback='true';}},true);
scan(document);new MutationObserver(rows=>{for(const row of rows)for(const node of row.addedNodes)if(node.nodeType===1)scan(node);}).observe(document.documentElement,{subtree:true,childList:true});
})();
