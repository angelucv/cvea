# Plataforma CVEA — Centro Venezolano de Estudios Actuariales

Sitio web del CVEA generado con **Quarto** y desplegado en **GitHub Pages**. Integra los ejes de Investigación (RVEA, Libros y Materiales Docentes), Docencia (Series de Tiempo con Python) y Extensión (Servicios y demos).

## Estructura

```
cvea-platform/
├── _quarto.yml          # Orquestador global de la web
├── _brand.yml           # Identidad visual (logos y colores)
├── index.qmd            # Landing page
├── assets/
│   ├── logos/           # cvea_teal.png, cvea_white.png
│   └── mathjax-config.html
├── rvea/                # Revista Venezolana de Actuariado
├── libro/               # Libros y Materiales Docentes (diagnóstico pensiones)
├── docencia/series-tiempo/  # Curso Series de Tiempo (Python)
├── servicios/           # Demos (IBNR, mapa de riesgo)
└── .github/workflows/publish.yml  # CI: render + GitHub Pages
```

## Requisitos

- [Quarto](https://quarto.org/docs/get-started/) instalado.
- Para publicar: repositorio en GitHub con la workflow habilitada.

## Uso local

```bash
cd cvea-platform
quarto preview
```

Por defecto el sitio se genera solo en HTML. Si en el futuro quieres generar PDF de artículos de la RVEA, hazlo por documento (por ejemplo `quarto render rvea/vol1-moreno.qmd --to pdf`) para evitar conflictos con el header HTML de MathJax.

## Publicación

1. Crea un repositorio `cvea-platform` en GitHub (o usa el tuyo).
2. En **Settings → Pages**, fuente: **GitHub Actions**.
3. Sube el proyecto y haz push a `main`. El workflow publicará en la rama `gh-pages`.

Actualiza la URL del navbar en `_quarto.yml` (`website.navbar.right.href`) con tu usuario/repo.

## Documentos de referencia

La carpeta **`Referencias/`** contiene la estructura general del centro, editores, modelos de revista y libro, y varios volúmenes/artículos:

- **`Referencias/README.md`** — Índice de la estructura: RVEA Volumen I (artículos Colmenares, Arlet Moreno), plantilla oficial (I-RL-M-R-D), Comité Editorial, Libros y Materiales Docentes.
- **`Referencias/Plantilla_RVEA/jfwm_template_raw.qmd`** — Plantilla oficial para manuscritos de la RVEA.
- **`Referencias/RVEA_Volumen I/`** — Artículos de referencia (Angel Colmenares, Arlet Moreno) con código reproducible.

La web integra ese contenido: los artículos aparecen en [rvea/index.qmd](rvea/index.qmd); el modelo editorial y la plantilla se describen en [rvea/index.qmd](rvea/index.qmd#modelo-editorial).

Opcionalmente puedes mantener copias adicionales en `docs/` (presentación, propuesta editorial PDF, etc.) para que Cursor u otras herramientas las lean desde el workspace.

## Licencia

Institucional — Centro Venezolano de Estudios Actuariales.
