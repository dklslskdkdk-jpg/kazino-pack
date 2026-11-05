import pathlib,base64,hashlib,zipfile,io,tomllib
data=base64.b64decode(pathlib.Path(".github/ficha-100/mod.b64").read_text(),validate=True)
assert len(data)==5431
assert hashlib.sha256(data).hexdigest()=="0e0457ae4f3c75ab38099f281743f8c34ccc733c294bbe4ae8b2ae5e39967426"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 meta=tomllib.loads(z.read("META-INF/mods.toml").decode())
 assert meta['mods'][0]['modId']=='fichakazino' and meta['mods'][0]['version']=='1.0.0'
for path in pathlib.Path("mods").glob("*.jar"):
 with zipfile.ZipFile(path) as z:
  meta=tomllib.loads(z.read("META-INF/mods.toml").decode())
  assert not any(m['modId']=='fichakazino' for m in meta['mods']),"FichaKazino already installed"
pathlib.Path("mods/FichaKazino-Forge-1.20.1-1.0.0.jar").write_bytes(data)
print("PASS original FichaKazino 1.0.0; no duplicate mod ID")
