# Enlaces Box — Artículos completos RVEA

Los artículos completos (HTML autocontenidos) no se sirven correctamente desde GitHub Pages. Se usan **enlaces a Box** para que los lectores puedan abrirlos.

## Archivos a subir a Box

1. **Angel Colmenares** — Análisis espacio-temporal de la mortalidad (BYM/INLA)  
   - Archivo local: `assets/articulos/articulo-colmenares-espacio-temporal.html`  
   - Subir a Box y obtener enlace de compartir (ej. `https://ucv.box.com/s/xxxx`).

2. **Arlet Moreno y Angel Colmenares** — Mortalidad neonatal, postneonatal y en la niñez (Lee-Carter)  
   - Archivo local: `assets/articulos/articulo-moreno-colmenares-mortalidad-infantil.html`  
   - Subir a Box y obtener enlace de compartir.

## Dónde pegar los enlaces

Cuando tengas los dos enlaces de Box, reemplaza en **todo el proyecto** (buscar y reemplazar):

| Buscar (placeholder) | Reemplazar por |
|----------------------|----------------|
| `https://app.box.com/s/COLMENARES_ESPACIO_TEMPORAL_REEMPLAZAR` | Tu enlace Box del artículo de Colmenares (espacio-temporal) |
| `https://app.box.com/s/MORENO_COLMENARES_MORTALIDAD_REEMPLAZAR` | Tu enlace Box del artículo de Moreno-Colmenares (mortalidad infantil) |

Archivos que contienen estos placeholders:

- `rvea/index.qmd`
- `rvea/vol1-colmenares.qmd`
- `rvea/vol1-moreno-arlet.qmd`

Después de reemplazar, ejecuta `quarto render` y haz commit + push.
