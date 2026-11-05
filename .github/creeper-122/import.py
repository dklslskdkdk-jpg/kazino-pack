import pathlib,base64,hashlib,zipfile,io
stage=pathlib.Path(".github/creeper-122")
data=base64.b64decode("".join((stage/f"{i}.b64").read_text() for i in range(2)),validate=True)
assert len(data)==160608
assert hashlib.sha256(data).hexdigest()=="054a4c81f36ff9c23ab7dab0ff9f24a0e63fb7d12fc0466294cf3031a2769836"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="creeperpastel"' in meta and 'version="1.2.2"' in meta
old=pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.1.4.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="81b0fd1c241af3c68c42549dd442196e8246fee82127b061dc3701f4d653067d"
pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.2.2.jar").write_bytes(data)
old.unlink()
print("PASS original CreeperPastel 1.2.2; replaced only 1.1.4")
