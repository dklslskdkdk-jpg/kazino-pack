# Kazino

Pack para el launcher de Blu Studio, Minecraft Java Forge 1.20.1.

## Pack publicado

- Morpher 1.0.9 (`mods/morpher.jar`).
- GeckoLib 4.8.4 (`mods/geckolib-forge-1.20.1-4.8.4.jar`).
- `pack.json`: manifiesto firmado por Blu, con SHA256 y enlaces a archivos de un commit fijo.

El launcher conectado descarga y verifica el pack al pulsar Jugar. Los archivos extra en mods, resourcepacks y shaderpacks se apartan. Actualmente no se autorizan texturas ni shaders adicionales.

## Actualizaciones

Blu debe subir los archivos primero y publicar el nuevo `pack.json` firmado al final. Subir un JAR por sí solo no lo autoriza. Los cambios del pack no requieren otro ejecutable.

Las actualizaciones de la aplicación son independientes de las del pack.

No subir claves privadas ni archivos de administración a este repositorio público. La verificación del launcher no sustituye los controles antitrampas del servidor.
