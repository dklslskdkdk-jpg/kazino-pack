import pathlib,base64,hashlib,zipfile,io
data=base64.b64decode(pathlib.Path(".github/creeper-160-runtime/totem.b64").read_text(),validate=True)
assert len(data)==24096
assert hashlib.sha256(data).hexdigest()=="829a18c348a0f06f82a56bb7625b0417f90e3e71fd3612e7816ab6b9a1bc977c"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 assert not any(n.startswith("META-INF/sources/") or n.endswith(".java") for n in z.namelist())
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="totemtung"' in meta and 'version="1.5.2"' in meta
old=pathlib.Path("mods/TotemTung-Forge-1.20.1-1.5.1.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="d93601ce7eaafa3344af241be46adc23e95580aa3a416a874ea2554dae05e5bf"
pathlib.Path("mods/TotemTung-Forge-1.20.1-1.5.2.jar").write_bytes(data)
old.unlink()
print("PASS TotemTung 1.5.2 runtime; replaced only 1.5.1")
