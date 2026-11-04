# Kazino

Pack para el launcher de Blu Studio, Minecraft Java Forge 1.20.1.

## Pack publicado

- Morpher 1.0.9 (`mods/morpher.jar`).
- GeckoLib 4.8.4 (`mods/geckolib-forge-1.20.1-4.8.4.jar`).
- `pack.json`: manifiesto firmado por Blu, compatible con el launcher conectado.

## Activacion unica de la automatizacion

1. Abre Settings > Secrets and variables > Actions > New repository secret.
2. Nombre: `KAZINO_SIGNING_KEY`.
3. Valor: contenido completo de `SOLO-BLU-private.pem`, del ZIP privado de administracion, incluidas las lineas BEGIN y END.
4. Guarda el secreto. Nunca subas el archivo PEM al repositorio ni lo pegues en comentarios.
5. Ve a Actions > Publicar pack de Kazino > Run workflow, en main.

La automatizacion esta instalada; no firmara hasta configurar el secreto. La clave debe ser la original del launcher.

## Anadir, cambiar o quitar mods

Sube o borra JAR directamente en `mods` en la rama main y confirma el cambio. GitHub Actions genera y publica el manifiesto firmado automaticamente. Espera a que Publicar pack de Kazino termine en verde antes de jugar. Tambien admite ZIP en `resourcepacks` y `shaderpacks` si Blu decide usarlos. No subas carpetas anidadas ni archivos auxiliares dentro de esas carpetas.

Si falla, el ultimo pack firmado sigue activo. Revisa Actions para ver el motivo. La firma comprueba integridad, no dependencias ni compatibilidad entre mods. Los enlaces apuntan al commit concreto para evitar mezclar versiones durante una actualizacion.

Los clientes reciben el pack al pulsar Jugar; no hace falta otro ejecutable para cambios del pack. Puede haber demora de cache. Las actualizaciones de la aplicacion son independientes.

No dar permisos de escritura a jugadores: quien puede modificar el workflow puede utilizar sus secretos. No subir claves privadas ni archivos de administracion a este repositorio publico. La verificacion local no sustituye los controles antitrampas del servidor.
