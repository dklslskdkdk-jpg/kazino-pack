import pathlib,base64,lzma,hashlib,zipfile,io
stage=pathlib.Path(".github/creeper-160-runtime")
packed=base64.b64decode("".join((stage/f"{i:03}.b64").read_text() for i in range(25)),validate=True)
assert hashlib.sha256(packed).hexdigest()=="1fe8493b42e4c51956399756b28c697876face90a48ba434e7bebe45beeac426"
data=lzma.decompress(packed)
assert len(data)==30514847
assert hashlib.sha256(data).hexdigest()=="90404c01d33aa1db2f679fcfe17298120b7b2b314231b9e6eb60ca6ef41a1c4c"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 assert not any(n.startswith("META-INF/sources/") or n.endswith(".java") for n in z.namelist())
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="creeperpastel"' in meta and 'version="1.6.0"' in meta
old=pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.3.2.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="5bf0ef67d95ff3ee6d975643b49955f55270a84fdc87071920c3c6179b8fe925"
pathlib.Path("mods/CreeperPastel-Forge-1.20.1-1.6.0.jar").write_bytes(data)
old.unlink()
print("PASS CreeperPastel 1.6.0 runtime: 197 original entries; replaced only 1.3.2")
