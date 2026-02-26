# Guía para actualizar la página web del CVEA

Pasos para publicar los cambios del sitio en la web (GitHub Pages y/o Cloudflare Pages).

---

## 1. Revisar cambios localmente (opcional)

- Abre el proyecto en Cursor o tu editor.
- Asegúrate de que los archivos que editaste estén guardados (`index.qmd`, `libro/index.qmd`, `editores.qmd`, etc.).

## 2. Generar el sitio con Quarto (previsualización local)

En una terminal, desde la carpeta del proyecto:

```powershell
cd c:\Users\Angel\cvea-platform
quarto render
```

- El sitio se genera en la carpeta **`_site`**.
- Para verlo en el navegador sin subir nada:
  ```powershell
  quarto preview
  ```
  (Cierra con Ctrl+C cuando termines.)

## 3. Subir los cambios a GitHub

Si usas **Git** desde la terminal:

```powershell
cd c:\Users\Angel\cvea-platform
git status
git add .
git commit -m "Actualización: libros, colaboradores, servicios, guía de actualización"
git push origin main
```

*(Ajusta el mensaje del commit si quieres describir otros cambios.)*

Si usas la **interfaz de Cursor/VS Code**: haz *Commit* de los archivos modificados y luego *Push* a la rama `main`.

## 4. Publicación automática

- Con el **push a `main`**, GitHub Actions ejecuta el workflow `.github/workflows/publish.yml`.
- Quarto vuelve a renderizar el sitio y actualiza la rama **`gh-pages`** con el contenido de `_site`.
- La página se actualiza en:
  - **GitHub Pages:** https://angelucv.github.io/cvea/ (si el repo es `angelucv/cvea` y Pages está configurado con la rama `gh-pages`).
  - **Cloudflare Pages:** https://cvea.pages.dev (si tienes Cloudflare conectado a la rama `gh-pages` o al mismo repositorio).

## 5. Comprobar que todo esté en línea

- Entra a la URL de tu sitio (GitHub Pages o Cloudflare).
- Revisa que se vean las secciones actualizadas: Libros (Franklin Quero, Prof. Felipe Moreno), Editores/colaboradores, Servicios, etc.
- Si usas GitHub: en el repo, pestaña **Actions**, verifica que el último workflow "Quarto Publish" haya terminado en verde.

---

## Resumen rápido

| Paso | Acción |
|------|--------|
| 1 | Guardar cambios en los `.qmd` y archivos del proyecto |
| 2 | `quarto render` (y opcionalmente `quarto preview`) |
| 3 | `git add .` → `git commit -m "..."` → `git push origin main` |
| 4 | Esperar a que GitHub Actions actualice `gh-pages` |
| 5 | Revisar la URL pública del sitio |

---

*Nota: No hace falta subir la carpeta `_site` al repositorio; el workflow la genera en GitHub. Si tienes `.gitignore`, suele incluir `_site/` para no versionarla.*
