const fs=require('node:fs'),zlib=require('node:zlib'),path=require('node:path');
const metadata=require('../site/assets/catalog-metadata.js');
const file=path.join(__dirname,'../site/data/catalog.json.gz');
const catalog=JSON.parse(zlib.gunzipSync(fs.readFileSync(file)));
catalog.offers=catalog.offers.map(metadata.normalize);
fs.writeFileSync(file,zlib.gzipSync(JSON.stringify(catalog),{mtime:0}));
console.log(JSON.stringify({offers:catalog.offers.length,brands:new Set(catalog.offers.map(o=>o.brand)).size}));
