(function(root){'use strict';
const gates=['double_opt_in_verified','unsubscribe_verified','privacy_notice_verified','separate_consent_verified','provider_permissions_verified'];
function readiness(config){
 const missing=gates.filter(key=>config?.[key]!==true);let signup=null;
 try{const u=new URL(config?.signup_url);if(u.protocol==='https:'&&!u.username&&!u.password&&(u.hostname==='sibforms.com'||u.hostname.endsWith('.sibforms.com')))signup=u.href;}catch{}
 if(!signup)missing.push('hosted_signup_url');
 return {ready:missing.length===0,signup_url:missing.length?null:signup,missing};
}
function unsubscribeUrl(config){
 if(config?.unsubscribe_form_configured!==true)return null;
 try{const u=new URL(config.unsubscribe_url);return u.protocol==='https:'&&!u.username&&!u.password&&(u.hostname==='sibforms.com'||u.hostname.endsWith('.sibforms.com'))?u.href:null;}catch{return null;}
}
if(typeof module==='object'&&module.exports)module.exports={readiness,unsubscribeUrl};
if(root)root.O4ZNewsletter={readiness,unsubscribeUrl};
})(typeof window==='undefined'?null:window);
