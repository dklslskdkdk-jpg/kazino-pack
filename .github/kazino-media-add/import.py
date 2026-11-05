import pathlib,json,hashlib,base64,zlib,urllib.request,zipfile,io,shutil,tomllib
root=pathlib.Path.cwd();stage=root/'.github/kazino-media-add';sha=lambda b:hashlib.sha256(b).hexdigest()
copies={
'CreativeCore_FORGE_v2.12.40_mc1.20.1.jar':'936de62489c0d6fbe74202486cbe2b191b8629b02bab1d480acfdb03690f33f4',
'waterframes-FORGE-mc1.20.1-v2.1.22.jar':'e7727c11b4d32aa25a7f1176cddef5f230f6f6b6dda3e37bf418b7f025b39ed8',
'watermedia-2.1.37.jar':'cdd8e1b50e4dee0892c5ed02724cea6b1a74d2b718c7e974c9cfc0efa8c10389',
'watervision-FG-mc1.20.1-v0.1.0-alpha.jar':'c04fb6d0996061c2e9d03efd2dd8eea6434355dfcb9618670bd52d632e00b90b'}
prepared={}
for name,expected in copies.items():
 data=(root/'instances/crewsafio/mods'/name).read_bytes();assert sha(data)==expected,name;prepared[name]=data
base=(root/'instances/crewsafio/mods/watermedia_youtube_plugin-2.1.2.jar').read_bytes()
recipe=json.loads((stage/'recipe.json').read_text());assert sha(base)==recipe['baseSha256']
literal=zlib.decompress(base64.b64decode(''.join((stage/f'{i:03}.b64').read_text() for i in range(2)),validate=True));assert sha(literal)==recipe['literalSha256']
request=urllib.request.Request('https://github.com/yt-dlp/yt-dlp/releases/download/2026.10.26/yt-dlp.exe',headers={'User-Agent':'Kazino-Pack-Importer'})
with urllib.request.urlopen(request,timeout=120) as response: exe=response.read()
assert sha(exe)=='f5389d3698ecde4ef06f4e6b1ce0294fe9ac1396228c8990b8d3416d6d177a7d'
encoder=zlib.compressobj(6,zlib.DEFLATED,-15);packed=encoder.compress(exe)+encoder.flush()
pieces={'literal':literal,'base':base,'exe':packed}
plugin=b''.join(pieces[typ][off:off+size] for typ,off,size in recipe['recipe'])
assert sha(plugin)==recipe['pluginSha256']=='d5001b0a0abd35e5a8e349cce8e825a4b0456b68986b55f164fc5a06e4ec141d'
prepared['watermedia_youtube_plugin-2.1.2-CrewSafio-Social-FIX2-EXPERIMENTAL.jar']=plugin
expectedSmall={'CrewSafio-Pantallas-Forge-1.20.1-0.1.2-EXPERIMENTAL.jar':'c38e2855848c1fb7211165d07b65f0ee58e3fd48cdeec7569ee7b4d6bb9a8a28','TotemTung-Forge-1.20.1-1.5.1.jar':'d93601ce7eaafa3344af241be46adc23e95580aa3a416a874ea2554dae05e5bf'}
small=json.loads((stage/'small.json').read_text());assert {x['file'] for x in small}==set(expectedSmall)
for item in small:
 data=base64.b64decode(item['data'],validate=True);assert sha(data)==expectedSmall[item['file']];prepared[item['file']]=data
old=root/'mods/TotemTung-Forge-1.20.1-1.4.2.jar';assert sha(old.read_bytes())=='2bcd40aa403f7f4eac7493e39a384bb82ae6b712cb90c3936dbe23724341b943'
assert json.loads((root/'pack-settings.json').read_text())['forge']=='47.4.28'
ids=set()
for name,data in prepared.items():
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  assert z.testzip() is None,name
  metadata=tomllib.loads(z.read('META-INF/mods.toml').decode());modid=metadata['mods'][0]['modId'];assert modid not in ids;ids.add(modid)
for existing in (root/'mods').glob('*.jar'):
 if existing==old:continue
 with zipfile.ZipFile(existing) as z:
  metadata=tomllib.loads(z.read('META-INF/mods.toml').decode())
  assert not any(m['modId'] in ids for m in metadata['mods']),existing.name
for name,data in prepared.items():(root/'mods'/name).write_bytes(data)
old.unlink()
print('PASS: 7 verified JARs added or updated including CreativeCore; exact uploaded hashes; no duplicate mod IDs')
