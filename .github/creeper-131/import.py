import pathlib,base64,hashlib,zipfile,io
stage=pathlib.Path(".github/creeper-131")
data=base64.b64decode("".join((stage/f"{i}.b64").read_text() for i in range(2)),validate=True)
assert len(data)==172284
assert hashlib.sha256(data).hexdigest()=="b0efbbe8be1253c8b8e3dcd84a1c45192bc562acccc9c2e0b142c25541b4e455"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="creeperpastel"' in meta and 'version="1.3.1"' in meta
old=pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.3.0.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="518ecbae8cf0a37e8cc62e27d2b0f0dc5e82a10fdbc8c0feed23da45479fb6d5"
pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.3.1.jar").write_bytes(data)
old.unlink()
print("PASS exact uploaded CreeperPastel 1.3.1; replaced only 1.3.0")
