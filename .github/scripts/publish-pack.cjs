'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const PUBLIC_KEY = '-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAA7tvH/gEhberzShs0/P80rRHIrANeBWYbhMmCAmRlcY=\n-----END PUBLIC KEY-----\n';
function build(root, pem, repository, commit) {
  if (!pem) throw Error('Falta el secreto KAZINO_SIGNING_KEY. Configuralo en Settings > Secrets and variables > Actions.');
  if (!/^[\w.-]+\/[\w.-]+$/.test(repository) || !/^[a-f0-9]{40}$/.test(commit)) throw Error('Repositorio o commit invalido.');
  const key = crypto.createPrivateKey(pem.trim());
  if (key.asymmetricKeyType !== 'ed25519' || !crypto.createPublicKey(key).equals(crypto.createPublicKey(PUBLIC_KEY))) throw Error('La clave no corresponde al launcher de Blu.');
  const pack = {minecraft: '1.20.1', forge: '47.4.0', version: commit};
  for (const [folder, ext] of [['mods', '.jar'], ['resourcepacks', '.zip'], ['shaderpacks', '.zip']]) {
    const dir = path.join(root, folder);
    pack[folder] = [];
    if (!fs.existsSync(dir)) continue;
    if (!fs.lstatSync(dir).isDirectory() || fs.lstatSync(dir).isSymbolicLink()) throw Error('Carpeta no permitida: ' + folder);
    const seen = new Set();
    for (const name of fs.readdirSync(dir).sort()) {
      const file = path.join(dir, name), stat = fs.lstatSync(file);
      if (!stat.isFile() || stat.isSymbolicLink() || !/^[a-zA-Z0-9_()+. -]+\.(jar|zip)$/.test(name) || !name.endsWith(ext) || name.length > 180 || /^(con|prn|aux|nul|com[1-9]|lpt[1-9])\./i.test(name)) throw Error('Archivo no permitido: ' + folder + '/' + name);
      if (seen.has(name.toLowerCase())) throw Error('Nombre duplicado: ' + name);
      seen.add(name.toLowerCase());
      const bytes = fs.readFileSync(file);
      if (bytes.length < 4 || bytes[0] !== 0x50 || bytes[1] !== 0x4b) throw Error('No es un JAR/ZIP valido: ' + name);
      pack[folder].push({file: name, url: 'https://raw.githubusercontent.com/' + repository + '/' + commit + '/' + folder + '/' + encodeURIComponent(name), sha256: crypto.createHash('sha256').update(bytes).digest('hex')});
    }
    if (pack[folder].length > 1000) throw Error('Demasiados archivos en ' + folder);
  }
  const data = Buffer.from(JSON.stringify(pack));
  return {payload: data.toString('base64'), signature: crypto.sign(null, data, key).toString('base64')};
}
if (require.main === module) {
  try {
    const result = build(process.cwd(), process.env.KAZINO_SIGNING_KEY, process.env.GITHUB_REPOSITORY, process.env.GITHUB_SHA);
    fs.writeFileSync('pack.json', JSON.stringify(result, null, 2) + '\n');
    const p = JSON.parse(Buffer.from(result.payload, 'base64'));
    console.log('Pack firmado: ' + p.mods.length + ' mods, ' + p.resourcepacks.length + ' texturas, ' + p.shaderpacks.length + ' shaders.');
  } catch (e) {
    // Never print key material or crypto exception internals.
    console.error(e.message.startsWith('Falta ') || e.message.startsWith('La clave ') || e.message.startsWith('Archivo ') || e.message.startsWith('Nombre ') || e.message.startsWith('No es ') || e.message.startsWith('Carpeta ') || e.message.startsWith('Demasiados ') ? e.message : 'No se pudo firmar el pack. Revisa el secreto y los archivos.');
    process.exitCode = 1;
  }
}
module.exports = {build};
