# Referencias CVEA — Estructura editorial y materiales de la plataforma

Esta carpeta contiene la **estructura general del Centro**, modelos de **revista (RVEA)** y **libro**, editores y múltiples volúmenes/artículos usados como referencia para integrar el contenido en la plataforma web.

## Estructura de carpetas

```
Referencias/
├── README.md                    # Este archivo
├── Plantilla_RVEA/             # Modelo de artículo para la revista
│   └── jfwm_template_raw.qmd   # Plantilla oficial RVEA (I-RL-M-R-D)
├── Plantilla_CVEA_Book_Applied Machine Learning Using mlr3 in R/   # Plantilla para libros
│   └── book/                   # Proyecto Quarto Book (mlr3); modelo para Libros y Materiales Docentes
│       ├── _quarto.yml         # type: book, chapters, PDF, sidebar, etc.
│       ├── index.qmd
│       └── chapters/           # Partes y capítulos
├── RVEA_Volumen I/             # Volumen I de la Revista Venezolana de Actuariado
│   ├── RVA_Vol_I_Angel_C/
│   │   └── V3/Art_Angel_Plantilla_RVEA.qmd
│   └── RVA_Vol_I_Arlet_M/
│       └── RVA-Arlet_Moreno1.qmd
└── [Demografía, Mortalidad y Previsión Social...]   # Libro compilado generado con la plantilla
    # Colocar aquí (o en libro/demografia-siglo-xxi/) el HTML y el PDF para publicar en la web
```

## Revista Venezolana de Actuariado (RVEA)

### Modelo editorial: I-RL-M-R-D

La RVEA utiliza la estructura **I-RL-M-R-D**:

| Sección | Contenido |
|---------|-----------|
| **I** | Introducción (contexto, problema, vacío, objetivo) |
| **RL** | Revisión literaria (síntesis analítica, no cronológica) |
| **M** | Métodos (diseño, datos, modelización, código reproducible) |
| **R** | Resultados (objetivos, figuras/tablas referenciadas) |
| **D** | Discusión y conclusiones |

- Política de **reproducibilidad**: código (R/Python/Julia) y datos en repositorio público.
- **Referencias**: `references.bib` + estilo APA (`.csl`).
- **Portada/encabezado**: logo CVEA (`cvea-logo.png` en PDF; en web se usa `assets/logos/`).

### Volumen I

| Artículo | Autor(es) | Tema |
|----------|-----------|------|
| Análisis espacio-temporal de la mortalidad en Venezuela (1996-2016) | Prof. Angel Colmenares | Riesgo Bayesiano (BYM/INLA), autocorrelación espacial, SMR, clusters K-means, IDW |
| Modelación y proyección de la mortalidad neonatal, postneonatal y en la niñez por entidad federal | Lic. Arlet Moreno, Prof. Angel Colmenares | Lee-Carter estocástico, desagregación por entidad federal y edad (días/meses) |

Tesistas y trabajos vinculados a este volumen: Daylin Moreno, José Raúl Gálvez, Daniel Azuaje, Arlet Moreno.

### Volumen II — Las dimensiones de la mortalidad (causa, género y territorio)

| Artículo / tema | Autor(es) |
|-----------------|-----------|
| Proyección de la mortalidad por causas (Lee-Carter y CoDa) | Iliria Herrera |
| Tablas de decrecimiento múltiple con Cadenas de Markov | Williams Fernandez |
| Principales causas de fallecimiento (población masculina) | Kelvin Guedez |
| Principales causas de fallecimiento (población femenina) | Dorielys Rangel |
| Tablas de decrecimiento múltiple (regiones Occidental, Andes, Central) | Kennya Briceño |
| Principales causas (regiones Los Llanos y Capital) | Daniela Godoy |
| Principales causas (regiones Oriental y Guayana) | Oriana Lopez |

### Volumen III — Perspectivas internacionales y fronteras en la modelización

| Artículo / tema | Autor(es) | Estado |
|-----------------|-----------|--------|
| Análisis comparativo de métodos de proyección (Chile y Japón) | Eleazar Domínguez | — |
| Medición del riesgo de longevidad (Portugal); impacto en rentas vitalicias y pensiones | Oliver Triveño | — |
| Comparativa internacional (Países Bajos, Bélgica) | Luis Alvarez | En desarrollo |
| Comparativa internacional (Italia, Grecia) | José Mendoza | En desarrollo |

### Comité editorial

- Comité Editorial de la RVEA referido en los manuscritos (p. ej. recomendaciones desde el CVEA a IVSS y Sudeaseg).
- Tutoría y coordinación de investigaciones del volumen: Prof. Jorge Dias y Prof. Angel Colmenares.

## Plantilla de Libros y Materiales Docentes

### Plantilla de libro (Quarto Book)

El **modelo para todos los libros del CVEA** es la plantilla basada en *Applied Machine Learning Using mlr3 in R* (Quarto Book):

- **Carpeta:** `Referencias/Plantilla_CVEA_Book_Applied Machine Learning Using mlr3 in R/`
- **Proyecto:** `book/` — `_quarto.yml` con `type: book`, partes, capítulos, descarga PDF, sidebar, búsqueda, estilo Krantz para PDF.
- Ya está adaptada al CVEA (título, logo, pie de página). Sirve como base para nuevos libros: copiar la estructura de `book/` y sustituir capítulos por el contenido propio.

### Libro compilado: Demografía, Mortalidad y Previsión Social en la Venezuela del Siglo XXI — Un Enfoque Actuarial

Ese libro fue **generado con la plantilla anterior** y está completamente compilado. Para publicarlo en la web:

- Colocar **solo el HTML** (por ejemplo `index.html` y los archivos/carpetas que genere el build de Quarto) y el **PDF** en la carpeta del proyecto indicada más abajo; la página enlazará "Ver en línea" y "Descargar PDF".
- Si el compilado está en Referencias, puedes copiar únicamente el HTML y el PDF a `libro/demografia-siglo-xxi/` (ver instrucciones en esa carpeta).

### Libros y Materiales Docentes (plan editorial)

- Los **libros y materiales docentes** en la plataforma siguen el plan editorial 2025-2026.
- Contenido: diagnóstico del sistema de pensiones, bases técnicas, actualización de tablas (Masjuán, CSO 1980, modelos dinámicos).
- Capítulos y volúmenes adicionales se incorporan según ese plan, usando la misma plantilla de libro.

## Uso en la plataforma

- **Web**: Los artículos listados en `rvea/index.qmd` pueden apuntar a versiones publicadas en la web o a PDFs; los `.qmd` de Referencias sirven como fuente de contenido y estructura.
- **Plantilla**: La plantilla en `Plantilla_RVEA/jfwm_template_raw.qmd` es la base para nuevos manuscritos; se puede copiar a `rvea/plantilla/` o enlazarse desde la sección de autores/editorial.
- **Logo**: En PDFs de Referencias se usa `cvea-logo.png` en la misma carpeta; en la web del proyecto se usa `assets/logos/cvea_teal.png` (navbar) y `_brand.yml`.
- **Libros**: La plantilla de libro está en `Plantilla_CVEA_Book_Applied Machine Learning Using mlr3 in R/book/`. El libro *Demografía, Mortalidad y Previsión Social en la Venezuela del Siglo XXI — Un Enfoque Actuarial* se publica en la web colocando su HTML y PDF en `libro/demografia-siglo-xxi/`.
