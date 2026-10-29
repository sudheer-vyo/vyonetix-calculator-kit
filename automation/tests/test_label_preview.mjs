import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const file=process.argv[2];
const html=fs.readFileSync(file,'utf8');
const source=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(x=>x[1]).join('\n');
const values={length:'30',height:'50',gap:'3',waste:'0.3',market:'AU'};
const elements={};
for(const id of ['calc','length','height','gap','waste','market','result','amazon','ebay','epn','copy','print','copyStatus'])elements[id]={value:values[id]??'',textContent:'',hidden:false,addEventListener(){}};
const ctx=vm.createContext({document:{getElementById:id=>elements[id]},URLSearchParams,window:{print(){}},navigator:{clipboard:{writeText:async()=>{}}},console});
vm.runInContext(source,ctx);
assert.match(elements.result.textContent,/560 complete labels/);
assert.equal(new URL(elements.amazon.href).searchParams.get('tag'),'vyonetixsave-22');
assert.equal(elements.ebay.hidden,true);
assert.equal(vm.runInContext('labelCount(30,50,3,30)',ctx),0);
for(const args of ['30,0,3,0','30,50,-1,0','30,50,3,31','Infinity,50,3,0','30,NaN,3,0'])assert.throws(()=>vm.runInContext(`labelCount(${args})`,ctx));
elements.height.value='';vm.runInContext('calculate()',ctx);assert.match(elements.result.textContent,/Fill all/);
elements.height.value='50';vm.runInContext('calculate()',ctx);assert.match(elements.result.textContent,/560/);
for(const [market,host,tag] of [['US','www.amazon.com','vyonetix20-20'],['UK','www.amazon.co.uk','vyonetix20-21'],['CA','www.amazon.ca','vyonetix2003-20']]){
  elements.market.value=market;vm.runInContext('routes()',ctx);const url=new URL(elements.amazon.href);assert.equal(url.hostname,host);assert.equal(url.searchParams.get('tag'),tag);assert.equal(elements.ebay.hidden,true);
}
elements.market.value='AU';vm.runInContext("CONFIG.campaign='11111111';routes()",ctx);assert.equal(elements.ebay.hidden,false);const epn=new URL(elements.ebay.href);for(const key of ['mkcid','mkevt','mkrid','campid','toolid','customid'])assert.ok(epn.searchParams.get(key));
console.log('PASS: default result; zero usable length; five invalid cases; blank input/recovery; four Amazon regions; eBay gating and campaign parameters.');
