import pathlib,base64,hashlib,zipfile,io
stage=pathlib.Path(".github/creeper-132-runtime")
data=base64.b64decode("".join((stage/f"{i}.b64").read_text() for i in range(2)),validate=True)
assert len(data)==170783
assert hashlib.sha256(data).hexdigest()=="5bf0ef67d95ff3ee6d975643b49955f55270a84fdc87071920c3c6179b8fe925"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 assert not any(n.startswith("META-INF/sources/") or n.endswith(".java") for n in z.namelist())
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="creeperpastel"' in meta and 'version="1.3.2"' in meta
old=pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.3.1.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="b0efbbe8be1253c8b8e3dcd84a1c45192bc562acccc9c2e0b142c25541b4e455"
pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.3.2.jar").write_bytes(data)
old.unlink()
print("PASS CreeperPastel 1.3.2 runtime only; replaced only 1.3.1")
