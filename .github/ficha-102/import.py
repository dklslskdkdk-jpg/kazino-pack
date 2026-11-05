import pathlib,base64,hashlib,zipfile,io
data=base64.b64decode(pathlib.Path(".github/ficha-102/mod.b64").read_text(),validate=True)
assert len(data)==5436
assert hashlib.sha256(data).hexdigest()=="39f054c5753da4c45e00de68cd58e7bcb1420e533532bf990d7962062243a21d"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="fichakazino"' in meta and 'version="1.0.2"' in meta
old=pathlib.Path("mods/FichaKazino-Forge-1.20.1-1.0.0.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="0e0457ae4f3c75ab38099f281743f8c34ccc733c294bbe4ae8b2ae5e39967426"
pathlib.Path("mods/FichaKazino-Forge-1.20.1-1.0.2.jar").write_bytes(data)
old.unlink()
print("PASS exact uploaded FichaKazino 1.0.2; replaced only 1.0.0")
