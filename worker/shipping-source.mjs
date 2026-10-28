import trade from '../site/assets/trade.js';
export const RULE_QUERY=`SELECT r.*,s.name AS shop_name FROM shipping_rule r JOIN shop s ON s.id=r.shop_id
WHERE r.shop_id=?1 AND r.zone=?2 AND r.valid_from<=?3 AND (r.valid_to IS NULL OR r.valid_to>?3)
ORDER BY r.valid_from DESC LIMIT 1`;
export async function readShippingRows(db,shopIds,now=Date.now(),zone='IT'){
 if(!db)throw Error('missing_binding');
 const ids=[...new Set(shopIds)].sort();if(!ids.length)return {rows:[],meta:{rows_read:0,rows_written:0,queries:0}};
 const result=await db.batch(ids.map(id=>db.prepare(RULE_QUERY).bind(id,zone,new Date(now).toISOString())));
 if(result.length!==ids.length)throw Error('invalid_result');
 const rows=[];
 const meta={rows_read:0,rows_written:0,queries:result.length};
 for(let i=0;i<result.length;i++){
  const item=result[i];if(!item.success||!Array.isArray(item.results)||item.results.length!==1||item.results[0].shop_id!==ids[i])throw Error('missing_or_invalid_rule');
  const r=item.results[0];
  if(!['verified','uncertain','unknown'].includes(r.status)||!Number.isFinite(Date.parse(r.verified_at))||!Number.isFinite(Date.parse(r.verified_until)))throw Error('invalid_verification');
  rows.push(r);meta.rows_read+=item.meta?.rows_read||0;meta.rows_written+=item.meta?.rows_written||0;
 }
 return {rows,meta};
}
export function quoteDifferences(offers,left,right,quantity,territory,now){
 const differences=[];
 for(const o of offers){const a=trade.shipping(o,left,quantity,territory,now),b=trade.shipping(o,right,quantity,territory,now);
  if(a.fee!==b.fee||a.total!==b.total||a.subtotal!==b.subtotal)differences.push({shop_id:o.merchant_id,json_total:a.total??null,d1_total:b.total??null,json_fee:a.fee??null,d1_fee:b.fee??null});
 }
 return differences;
}
// JSON remains the default. No D1 request is made unless enabled explicitly.
export async function shippingSource(env,offers,jsonRules,{now=Date.now(),quantity=1,territory='standard',log=event=>console.log(JSON.stringify(event))}={}){
 const useD1=env.SHIPPING_RULES_SOURCE==='d1',shadow=env.SHIPPING_SHADOW==='true';
 if(!useD1&&!shadow)return {rules:jsonRules,source:'json',meta:null};
 try{
  const {rows,meta}=await readShippingRows(env.SHIPPING_DB||env.SHIPPING_DB_STAGING,offers.map(o=>o.merchant_id),now);
  const rules=trade.shippingRulesFromRows(rows,now);
  if(shadow){const differences=quoteDifferences(offers,jsonRules,rules,quantity,territory,now);if(differences.length)log({event:'shipping_shadow_difference',differences});}
  return {rules:useD1?rules:jsonRules,source:useD1?'d1':'json',meta};
 }catch{
  log({event:'shipping_d1_fallback',requested_source:useD1?'d1':'json',shadow});
  return {rules:jsonRules,source:'json',meta:null,fallback:true};
 }
}
