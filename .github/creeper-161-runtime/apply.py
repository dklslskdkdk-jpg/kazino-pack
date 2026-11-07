import base64, hashlib, io, json, pathlib, zipfile
root=pathlib.Path(__file__).resolve().parent
m=json.loads((root/'meta.json').read_text())
old=pathlib.Path('mods/CreeperPastel-Forge-1.20.1-1.6.0.jar')
new=pathlib.Path('mods/CreeperPastel-Forge-1.20.1-1.6.1.jar')
b=old.read_bytes()
d=base64.b64decode((root/'delta.b64').read_text(),validate=True)
assert hashlib.sha256(b).hexdigest()==m['base']
assert hashlib.sha256(d).hexdigest()==m['delta']
assert len(m['names'])==len(set(m['names']))
with zipfile.ZipFile(io.BytesIO(b)) as base, zipfile.ZipFile(io.BytesIO(d)) as delta:
 assert base.testzip() is None and delta.testzip() is None
 assert set(delta.namelist())<=set(m['names'])
 with zipfile.ZipFile(new,'w') as out:
  for name in m['names']:
   assert not name.startswith('/') and '..' not in name.split('/')
   assert not name.startswith('META-INF/sources/') and not name.endswith('.java')
   data=delta.read(name) if name in delta.namelist() else base.read(name)
   out.writestr(zipfile.ZipInfo(name,(1980,1,1,0,0,0)),data,compress_type=zipfile.ZIP_DEFLATED)
assert hashlib.sha256(new.read_bytes()).hexdigest()==m['result']
with zipfile.ZipFile(new) as z:
 assert z.testzip() is None
 assert 'version="1.6.1"' in z.read('META-INF/mods.toml').decode()
old.unlink()
print('CreeperPastel 1.6.1 verificado:',m['result'])
