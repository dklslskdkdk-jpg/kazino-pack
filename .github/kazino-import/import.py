import base64,hashlib,io,json,pathlib,zipfile,tomllib
root=pathlib.Path.cwd();stage=root/'.github/kazino-import';manifest=json.loads((stage/'manifest.json').read_text())
parts=sorted((stage/'parts').glob('*.b64'))
assert len(parts)==manifest['parts'],'Incomplete upload'
archive=base64.b64decode(''.join(p.read_text() for p in parts),validate=True)
assert hashlib.sha256(archive).hexdigest()==manifest['zipSha256'],'Archive digest mismatch'
result={}
with zipfile.ZipFile(io.BytesIO(archive)) as z:
 expected={name for name,item in manifest['mods'].items() if 'source' not in item}
 assert set(z.namelist())==expected,'Unexpected archive entries'
 for name,item in manifest['mods'].items():
  assert '/' not in name and '\\' not in name and name.endswith('.jar')
  data=(root/item['source']).read_bytes() if 'source' in item else z.read(name)
  assert len(data)==item['size'] and hashlib.sha256(data).hexdigest()==item['sha256'],name
  result[name]=data
ids=set()
for name,data in result.items():
 with zipfile.ZipFile(io.BytesIO(data)) as jar:
  assert jar.testzip() is None,name
  meta=tomllib.loads(jar.read('META-INF/mods.toml').decode())
  for mod in meta['mods']:
   assert mod['modId'] not in ids,'Duplicate mod ID: '+mod['modId']
   ids.add(mod['modId'])
assert len(result)==11 and 'morpher' in ids
directory=root/'mods';assert directory.is_dir() and not directory.is_symlink()
for old in directory.iterdir():
 assert old.is_file() and not old.is_symlink(),'Unsafe existing mod entry'
for old in directory.iterdir():old.unlink()
for name,data in result.items():(directory/name).write_bytes(data)
(root/'pack-settings.json').write_text(json.dumps({'forge':'47.4.28'},indent=2)+'\n')
print('PASS: replaced Kazino mods with 11 exact uploaded JARs, unique mod IDs and valid ZIP contents; CrewSafío untouched.')
