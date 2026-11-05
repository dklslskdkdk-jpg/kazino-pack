import base64, hashlib, io, json, pathlib, zipfile
root = pathlib.Path(__file__).resolve().parent
parts = sorted((root / "parts").glob("*.b64"))
assert [p.name for p in parts] == [f"{i:03}.b64" for i in range(79)], "Missing parts"
data = base64.b64decode("".join(p.read_text() for p in parts), validate=True)
assert len(data) == 9414964, "Incorrect size"
assert hashlib.sha256(data).hexdigest() == "a3c4cf58ed15e3abb8e607de23a018edc6cce0600970d0908ebf8498a3445e0c", "Incorrect SHA256"
with zipfile.ZipFile(io.BytesIO(data)) as archive:
    assert archive.testzip() is None, "Corrupt ZIP"
    assert json.loads(archive.read("pack.mcmeta"))["pack"]["pack_format"] == 15, "Incorrect Minecraft version"
destination = pathlib.Path("resourcepacks/Icons-v1.14.zip")
destination.parent.mkdir(exist_ok=True)
destination.write_bytes(data)
print("Verified Icons v1.14: Minecraft 1.20.1, original ZIP unchanged")
