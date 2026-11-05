import pathlib,base64,hashlib,zipfile,io
stage=pathlib.Path(".github/creeper-130")
data=base64.b64decode("".join((stage/f"{i}.b64").read_text() for i in range(2)),validate=True)
assert len(data)==169835
assert hashlib.sha256(data).hexdigest()=="518ecbae8cf0a37e8cc62e27d2b0f0dc5e82a10fdbc8c0feed23da45479fb6d5"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="creeperpastel"' in meta and 'version="1.3.0"' in meta
old=pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.2.2.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="054a4c81f36ff9c23ab7dab0ff9f24a0e63fb7d12fc0466294cf3031a2769836"
pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.3.0.jar").write_bytes(data)
old.unlink()
print("PASS original CreeperPastel 1.3.0; replaced only 1.2.2")
