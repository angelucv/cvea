# Mapeo de secciones y recomendaciones de fusión — Actuarial Cortex

## 1. Mapa actual del sitio

| Sección / URL | Contenido | En el menú |
|---------------|-----------|------------|
| **Raíz** | | |
| `index.qmd` | Inicio (hero, ejes, tiles, enlaces rápidos) | Inicio |
| `sobre-cortex.qmd` | Sobre Cortex (identidad, ejes del hub) | Sobre Cortex |
| `miembros.qmd` | Equipo, colaboradores, profesores EECA | Miembros |
| `cortex-suite.qmd` | Cortex Suite (demos Banca, Seguros, Retail, Salud, Control, telemática) | Demo Shiny + Cortex Suite *(duplicado)* |
| `observatorio.qmd` | Variables biométricas, financieras, previsión | Observatorio |
| `actualidad.qmd` | Noticias, eventos, Call for Papers | Actualidad |
| `contacto.qmd` | Canales de contacto | Contacto |
| **Investigación** | | |
| `investigacion/index.qmd` | Landing: Resources, Model Hub | — |
| `investigacion/model-hub.qmd` | Repositorio de herramientas | Model Hub |
| **Resources** | | |
| `resources/index.qmd` | Materiales académicos (hero, plantilla) | Resources |
| `resources/articulos.qmd` | Listado de artículos | (desde Resources) |
| `resources/portal.qmd` | Portal alternativo | (interno) |
| `resources/vol1-*.qmd` | Artículos Vol I | (desde articulos) |
| **Docencia** | | |
| `docencia/index.qmd` | Landing Cursos (Moodle hero, Series de Tiempo, Plataforma) | Cursos |
| `docencia/series-tiempo/index.qmd` | Curso Series de Tiempo (Python) | (desde Cursos) |
| `docencia/plataforma-cursos/index.qmd` | Plataforma Moodle, acceso | Plataforma de cursos |
| `docencia/plataforma-cursos/fase1-pasos.qmd` | Guía técnica Fase 1 | (interno) |
| `docencia/plataforma-cursos/alternativas-oracle.qmd` | Alternativas a Oracle Cloud | (interno) |
| **Servicios** | | |
| `servicios/index.qmd` | Landing Extensión + galería demos (IBNR, Mapa) | Servicios |
| `servicios/demo-ibnr.qmd` | Demo reservas IBNR | (desde Servicios) |
| `servicios/demo-mapa.qmd` | Demo mapa riesgo mortalidad | (desde Servicios) |
| **Sin render** | | |
| `cursos/index.qmd` | Página “Cursos y formación” (eliminada; unificado en docencia) | No en menú; no en `_quarto.yml` |

---

## 2. Recomendaciones de fusión y simplificación

### A) Menú: unificar ítems duplicados

- **Problema:** En el menú hay dos ítems que apuntan a la misma página:
  - «Demo Shiny tarificación telemática» → `cortex-suite.qmd`
  - «Cortex Suite» → `cortex-suite.qmd`
- **Recomendación:** Dejar un solo ítem **«Cortex Suite»**. El demo de tarificación telemática puede ser un enlace interno o bloque dentro de esa misma página (ya está en “Cortex Suite Lab”).

### B) Menú: Docencia con una sola entrada

- **Problema:** Dos ítems: «Cursos» (`docencia/index.qmd`) y «Plataforma de cursos» (`docencia/plataforma-cursos/index.qmd`). La página de Cursos ya enlaza a la plataforma y a Series de Tiempo.
- **Recomendación:** Un solo ítem **«Cursos»** que lleve a `docencia/index.qmd`. Desde ahí, enlaces visibles a “Plataforma Moodle” y “Series de Tiempo”. Quitar «Plataforma de cursos» del menú global para no duplicar rutas de entrada.

### C) No fusionar páginas de contenido

- **Investigación** → Hub (landing) que enlaza a Resources y Model Hub.
- **Resources** → Sección propia (materiales académicos / artículos). Investigación enlaza.
- **Servicios** → Mantener landing + demos (IBNR, Mapa). No fusionar con Cortex Suite.
- **Observatorio** → Mantener como página propia (eje distinto). Textos alineados con Actuarial Cortex y Resources.

### D) Carpeta `cursos/`

- **Situación:** Existe `cursos/index.qmd` pero **no** está en `render` de `_quarto.yml`, por tanto no se compila.
- **Recomendación:**  
  - **Opción 1:** Eliminar la carpeta `cursos/` y usar solo `docencia/` como sección de formación.  
  - **Opción 2:** Si quieres conservar una URL tipo `/cursos/`, añadir `cursos` al `render` y que `cursos/index.qmd` redirija o replique el contenido de `docencia/index.qmd` (duplicación de mantenimiento).  
  Recomendación: **Opción 1** (eliminar `cursos/` y unificar en Docencia).

### E) Ajustes solo de texto (sin fusionar)

- **investigacion/index.qmd:** Sustituir “Revista (RVEA)” por “Resources / Materiales académicos” y enlace a `resources/index.qmd`.
- **observatorio.qmd:** Sustituir “CVEA” por “Actuarial Cortex” y “RVEA” por “Resources”.
- **libro/index.qmd:** Sustituir “CVEA” por “Actuarial Cortex” en toda la página.
- **docencia/index.qmd:** Ya actualizado; revisar “Comité Editorial” en “Ecosistema de aprendizaje” → “equipo” o “Miembros”.

---

## 3. Mapeo recomendado del menú (después de cambios)

| Orden | Texto en menú | Destino | Nota |
|-------|----------------|---------|------|
| 1 | Inicio | `index.qmd` | |
| 2 | Sobre Cortex | `sobre-cortex.qmd` | |
| 3 | Miembros | `miembros.qmd` | |
| 4 | Resources | `resources/index.qmd` | |
| 7 | Model Hub | `investigacion/model-hub.qmd` | |
| 8 | Cursos | `docencia/index.qmd` | Única entrada docencia |
| 9 | Cortex Suite | `cortex-suite.qmd` | Una sola entrada (quitar “Demo Shiny…”) |
| 10 | Servicios | `servicios/index.qmd` | |
| 11 | Observatorio | `observatorio.qmd` | |
| 12 | Actualidad | `actualidad.qmd` | |
| 13 | Contacto | `contacto.qmd` | |

**Eliminados del menú en esta propuesta:**  
- «Plataforma de cursos» (acceso desde Cursos).  
- «Demo Shiny tarificación telemática» (contenido dentro de Cortex Suite).

---

## 4. Resumen de acciones sugeridas

1. **Menú (_website.yml):** Quitar ítem «Demo Shiny tarificación telemática» y ítem «Plataforma de cursos»; dejar una entrada «Cursos» y una «Cortex Suite».
2. **Textos:** Actualizar investigacion/index (RVEA → Resources), observatorio (CVEA/RVEA), libro/index (CVEA → Actuarial Cortex), y docencia si sigue “Comité Editorial”.
3. **Carpeta cursos:** Decidir si se elimina (recomendado) o se mantiene y se añade al render con redirección a docencia.

---

## 5. Cambios aplicados (actualización)

- **Menú (_website.yml):** Eliminados «Demo Shiny tarificación telemática» y «Plataforma de cursos»; una sola entrada «Cortex Suite».
- **investigacion/index.qmd:** Subtitle y sección «Resources / Materiales académicos».
- **observatorio.qmd:** Actuarial Cortex y Resources.
- **libro/index.qmd:** CVEA → Actuarial Cortex (y Centro → hub donde aplica); plantilla Quarto Book del hub.
- **docencia/index.qmd:** «Comité Editorial» → «equipo», «centro» → «hub», Resources.
- **cursos/index.qmd:** Archivo eliminado; formación unificada en `docencia/`.
