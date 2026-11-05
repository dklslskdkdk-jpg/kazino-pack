import pathlib,base64,hashlib,zipfile,io
data=base64.b64decode(pathlib.Path(".github/hearts-101/mod.b64").read_text(),validate=True)
assert len(data)==14761
assert hashlib.sha256(data).hexdigest()=="9af92721751b6a742308a1989d74c0d4aa4e8885599c552cfbd19f450bc8e18e"
with zipfile.ZipFile(io.BytesIO(data)) as z:
 assert z.testzip() is None
 meta=z.read("META-INF/mods.toml").decode()
 assert 'modId="crewsafiohearts"' in meta and 'version="1.0.1"' in meta
old=pathlib.Path("mods/CrewSafio-Hearts-Forge-1.20.1-1.0.0.jar")
assert hashlib.sha256(old.read_bytes()).hexdigest()=="d3eb58ed3b5f1401f93737b329cbfcb8e0bcef17eb9a16717d017bf0d79d6d81"
pathlib.Path("mods/CrewSafio-Hearts-Forge-1.20.1-1.0.1.jar").write_bytes(data)
old.unlink()
print("Verified original Hearts 1.0.1; removed only Hearts 1.0.0")
