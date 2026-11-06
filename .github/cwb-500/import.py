import pathlib,base64,hashlib,zipfile,io,tomllib
stage=pathlib.Path(".github/cwb-500")
data=base64.b64decode("".join((stage/f"{i}.b64").read_text() for i in range(6)),validate=True)
assert len(data)==716234
assert hashlib.sha256(data).hexdigest()=="f7646364101881caf7b49bfd992cb1210f1e54b71b48a1b0e6f9a8939091e1e9"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 meta=tomllib.loads(z.read("META-INF/mods.toml").decode())
 assert meta['mods'][0]['modId']=='cwb' and meta['mods'][0]['version']=='5.0.0+1.20.0.forge'
conflicts={'cwb','borderlessmining','borderlesswindow','borderlesswindowed','borderlessfullscreen','concentration','windowstitlebardelete','fw'}
for path in pathlib.Path("mods").glob("*.jar"):
 with zipfile.ZipFile(path) as z:
  meta=tomllib.loads(z.read("META-INF/mods.toml").decode())
  assert not any(m['modId'] in conflicts for m in meta['mods']),"Duplicate or incompatible window mod"
assert __import__('json').loads(pathlib.Path('pack-settings.json').read_text())['forge']=='47.4.28'
pathlib.Path("mods/cwb-5.0.0-1.20.0-forge.jar").write_bytes(data)
print("PASS original CWB 5.0.0 client mod; compatible Minecraft range; no duplicate/window mod conflicts")
