"""Import the approved archive without executing any mod code."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import zipfile
from urllib.parse import quote

EXPECTED = 'ff3aaee4d042ee9d64930cc5309fd58c236d747f833fd116e99b871a1b4882d2'
TAG = 'crewsafio-mods-20261104'
archive = Path(os.environ['RUNNER_TEMP']) / 'crewsafio-import' / 'mods.zip'
with archive.open('rb') as stream:
    if hashlib.file_digest(stream, 'sha256').hexdigest() != EXPECTED:
        raise ValueError('El ZIP no coincide con el autorizado por Blu.')

staging = archive.parent / 'verified'
staging.mkdir()
external = []
repository = os.environ['GITHUB_REPOSITORY']
with zipfile.ZipFile(archive) as source:
    files = [item for item in source.infolist() if not item.is_dir()]
    if len(files) != 74:
        raise ValueError('Se esperaban exactamente 74 mods.')
    seen = set()
    for item in files:
        name = item.filename.removeprefix('mods/')
        if item.filename != 'mods/' + name or not re.fullmatch(r'[a-zA-Z0-9_()+. -]+\.jar', name) or name.lower() in seen:
            raise ValueError('Nombre de archivo inválido o duplicado.')
        seen.add(name.lower())
        data = source.read(item)
        if not data.startswith(b'PK'):
            raise ValueError('JAR inválido: ' + name)
        target = staging / name
        target.write_bytes(data)
        if len(data) >= 100 * 1024 * 1024:
            subprocess.run(['gh', 'release', 'upload', TAG, str(target), '--repo', repository, '--clobber'], check=True)
            external.append({'file': name, 'url': f'https://github.com/{repository}/releases/download/{TAG}/{quote(name, safe="")}', 'sha256': hashlib.sha256(data).hexdigest()})

root = Path('instances/crewsafio')
mods = root / 'mods'
if mods.exists():
    shutil.rmtree(mods)
mods.mkdir(parents=True)
for file in staging.iterdir():
    if file.stat().st_size < 100 * 1024 * 1024:
        shutil.copyfile(file, mods / file.name)
(root / 'external-mods.json').write_text(json.dumps(external, indent=2) + '\n')
print(f'Verificados: {len(files)} mods; {len(external)} publicado en Release.')
