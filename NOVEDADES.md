# Cómo actualizar la sección Novedades (Actualidad)

La sección **Novedades** en [Actualidad](actualidad.qmd#novedades) informa al público sobre las últimas cargas realizadas en la página del CVEA. Solo debe incluir contenido de **consumo público**: lo que a visitantes, estudiantes y profesionales les interesa ver o usar.

---

## Qué SÍ incluir en Novedades

- **Artículo nuevo** en la RVEA (versión preliminar o publicada): título, autor, tema breve y enlace a HTML/PDF.
- **Libro nuevo** publicado en la web: título, autores o editores, enlace a la ficha o descarga.
- **Curso o sección nueva** (p. ej. nuevo módulo de docencia, nueva oferta): nombre, breve descripción y enlace.
- **Noticia o evento** de interés general: convocatorias, defensas de TFPG anunciadas, webinars, colaboraciones con instituciones.

Cada entrada debe tener: **Fecha** (mes y año), **Tipo** (Artículo RVEA / Libro / Curso / Noticia), **Novedad** (título y una línea descriptiva) y **Enlace** (URL o ruta dentro del sitio).

---

## Qué NO incluir en Novedades

- Cambios en **repositorios privados** o internos.
- Actualizaciones de **código** de la página (Quarto, estilos, scripts).
- Detalles de **sincronización entre repos** (cvea-platform, cvea-rvea, cvea-libros).
- **Bugs** corregidos o mejoras técnicas que no cambian lo que el usuario ve (nuevos contenidos o funcionalidades).

Si un cambio no es algo que un visitante buscaría o usaría directamente, no va en Novedades.

---

## Dónde editar

- **Tabla de Novedades:** archivo `actualidad.qmd`, sección `## Novedades {#novedades}`.
- Añade una **nueva fila** al inicio de la tabla (después del encabezado) con: Fecha | Tipo | Novedad | Enlace.
- Mantén las entradas en orden **cronológico inverso** (la más reciente primero).

---

## Ejemplo de nueva fila

Para un artículo:

```markdown
| Marzo 2026 | Artículo RVEA | **Autor** — Título breve. Versión preliminar/publicado. | [Ver artículo](rvea/vol1-xxx.html) · [PDF](rvea/vol1-xxx.pdf) |
```

Para un libro publicado:

```markdown
| Abril 2026 | Libro | **Introducción a las Matemáticas Actuariales I** — CVEA / Prof. Felipe Moreno. | [Ver libro](libro/intro-matematicas-actuariales/index.html) |
```

Para una noticia:

```markdown
| Mayo 2026 | Noticia | Defensa pública TFPG — Nombre del tesista, título. | [Eventos](actualidad.qmd#calendario) |
```
