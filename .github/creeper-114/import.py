import pathlib,base64,hashlib,zipfile,io
stage=pathlib.Path(".github/creeper-114")
data=base64.b64decode("".join((stage/f"{i}.b64").read_text() for i in range(2)),validate=True)
assert len(data)==134862
assert hashlib.sha256(data).hexdigest()=="81b0fd1c241af3c68c42549dd442196e8246fee82127b061dc3701f4d653067d"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="creeperpastel"' in meta and 'version="1.1.4"' in meta
old=pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.1.3.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="b9cd5e64d3204a4006be139e0fd8b1edd5307480c955f623d366f9d6b1d4884f"
pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.1.4.jar").write_bytes(data)
old.unlink()
print("Verified exact CreeperPastel 1.1.4; replaced only 1.1.3")
