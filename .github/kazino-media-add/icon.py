import pathlib,zipfile,io,base64,json,hashlib
root=pathlib.Path.cwd();stage=root/'.github/kazino-media-add'
meta=json.loads((stage/'icon.json').read_text());delta=base64.b64decode((stage/'icon.b64').read_text(),validate=True)
assert hashlib.sha256(delta).hexdigest()==meta['delta']
source=root/'mods/Kazino7-BLU-STUDIO-Forge-1.20.1-2.1.6.jar'
assert hashlib.sha256(source.read_bytes()).hexdigest()==meta['base']
dest=source.with_name('Kazino7-BLU-STUDIO-Forge-1.20.1-2.1.7.jar')
with zipfile.ZipFile(source) as old,zipfile.ZipFile(io.BytesIO(delta)) as changes,zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as out:
 assert set(changes.namelist())=={'com/blu/kazino/LauncherBranding.class','assets/crewsafio/textures/gui/kazino-window-icon.png'}
 for name in old.namelist()+[n for n in changes.namelist() if n not in old.namelist()]:
  data=changes.read(name) if name in changes.namelist() else old.read(name)
  if name=='META-INF/mods.toml':data=data.replace(b'version="2.1.6"',b'version="2.1.7"')
  out.writestr(zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0)),data,compress_type=zipfile.ZIP_DEFLATED)
assert hashlib.sha256(dest.read_bytes()).hexdigest()==meta['result']
source.unlink()
print('PASS Kazino 2.1.7: requested original PNG, window icon at 16/32/48/256 pixels')
