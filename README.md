# Kazino

Pack para el launcher de Blu Studio, Minecraft Java Forge 1.20.1.

## Subir mods y listo

1. Sube, sustituye o borra archivos JAR dentro de `mods` en la rama main.
2. Confirma el cambio con Commit changes.
3. Espera a que Actions > Publicar pack de Kazino termine en verde.
4. Pulsa Jugar en el launcher nuevo: descargara y verificara los archivos autorizados.

No necesitas clave privada, secretos, comandos ni generar JSON a mano. GitHub Actions genera `pack-auto.json` con enlaces a un commit fijo y hashes SHA256. Texturas y shaders opcionales se suben como ZIP a `resourcepacks` y `shaderpacks`. No pongas subcarpetas ni archivos auxiliares dentro de estas carpetas.

## Verificacion

El launcher confia en este repositorio HTTPS, comprueba los hashes, aparta mods/texturas/shaders extra y vigila cambios durante la partida. Este modo no usa firma Ed25519 del pack. Quien tenga permisos de escritura aqui puede autorizar cambios: no des acceso de escritura a jugadores.

Los hashes no comprueban dependencias ni compatibilidad entre mods. Si Actions falla, el pack publicado previamente sigue activo. No es un anticheat infalible ni sustituye controles en el servidor.

## Cambio de sistema

Hay que sustituir una vez el ejecutable antiguo por el nuevo que lee `pack-auto.json`. Despues los cambios del pack no necesitan otro EXE. Puede haber demora de cache. `pack.json` firmado se conserva solo para clientes anteriores; ya no recibe actualizaciones automaticas. Las actualizaciones de la aplicacion son independientes.

Pack inicial: Morpher 1.0.9 y GeckoLib 4.8.4. No subir claves privadas ni herramientas de administracion a este repositorio publico.
