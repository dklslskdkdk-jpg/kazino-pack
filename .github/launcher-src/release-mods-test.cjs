const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'source.json'),'utf8'));
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'crewsafio-release-'));
for(const file of ['pack.cjs','resource-packs.cjs'])fs.writeFileSync(path.join(dir,file),source[file]);
const {verifyGithubManifest}=require(path.join(dir,'pack.cjs'));
const repo='dklslskdkdk-jpg/kazino-pack',version='a'.repeat(40),file='DEDSAFIO4FAN-Forge-1.20.1-almas-keep-peak-FIX5.jar';
const pack=url=>({minecraft:'1.20.1',forge:'47.4.0',version,mods:[{file,url,sha256:'b'.repeat(64)}],resourcepacks:[],shaderpacks:[]});
const url=`https://github.com/${repo}/releases/download/crewsafio-mods-20261104/${file}`;
test('accepts exact release assets in the authorized repository',()=>assert.equal(verifyGithubManifest(pack(url),repo,'instances/crewsafio').mods.length,1));
test('retains pinned raw downloads',()=>assert.doesNotThrow(()=>verifyGithubManifest(pack(`https://raw.githubusercontent.com/${repo}/${version}/instances/crewsafio/mods/${file}`),repo,'instances/crewsafio')));
test('rejects other repositories, credentials, query strings and renamed assets',()=>{
 for(const bad of [url.replace(repo,'other/repo'),url.replace('github.com','github.com.evil.test'),url+'?x=1',url+'#x',url.replace('https://','https://user@'),url.replace(file,'other.jar')])assert.throws(()=>verifyGithubManifest(pack(bad),repo,'instances/crewsafio'));
});
test.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
