import pathlib,base64,hashlib,zipfile,io
data=base64.b64decode(pathlib.Path(".github/ficha-103/mod.b64").read_text(),validate=True)
assert len(data)==5434
assert hashlib.sha256(data).hexdigest()=="a7d663338f54c01f01fd9bdb7915324d74c56b473b4ae5f02ca5e30c1b391f72"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="fichakazino"' in meta and 'version="1.0.3"' in meta
old=pathlib.Path("mods/FichaKazino-Forge-1.20.1-1.0.2.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="39f054c5753da4c45e00de68cd58e7bcb1420e533532bf990d7962062243a21d"
pathlib.Path("mods/FichaKazino-Forge-1.20.1-1.0.3.jar").write_bytes(data)
old.unlink()
print("PASS exact uploaded FichaKazino 1.0.3; replaced only 1.0.2")
