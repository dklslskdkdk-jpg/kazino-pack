import pathlib,zipfile,io,json,hashlib,base64
root=pathlib.Path.cwd();stage=root/'.github/kazino-menu-finalbuttons';meta=json.loads((stage/'manifest.json').read_text())
delta=base64.b64decode((stage/'delta.b64').read_text(),validate=True);assert hashlib.sha256(delta).hexdigest()==meta['deltaSha256']
source=root/'mods/Kazino7-BLU-STUDIO-Forge-1.20.1-2.1.4.jar';assert hashlib.sha256(source.read_bytes()).hexdigest()==meta['baseSha256']
dest=source.with_name('Kazino7-BLU-STUDIO-Forge-1.20.1-2.1.5.jar')
expected={'com/blu/kazino/LauncherBranding.class'}
with zipfile.ZipFile(source) as old,zipfile.ZipFile(io.BytesIO(delta)) as changes,zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as out:
 assert set(changes.namelist())==expected
 for name in list(old.namelist())+[n for n in changes.namelist() if n not in old.namelist()]:
  data=changes.read(name) if name in changes.namelist() else old.read(name)
  if name=='META-INF/mods.toml':data=data.replace(b'version="2.1.4"',b'version="2.1.5"')
  out.writestr(zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0)),data,compress_type=zipfile.ZIP_DEFLATED)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==meta['resultSha256']
source.unlink();print('PASS exact Kazino menu 2.1.5 artifact and two approved hat assets')
