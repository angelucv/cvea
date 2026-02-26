# Configurar Cloudflare Pages para CVEA

Tu repo está en **https://github.com/angelucv/cvea**. El workflow de GitHub ya genera el sitio y lo sube a la rama **`gh-pages`**. En Cloudflare solo conectamos esa rama y servimos los archivos (sin volver a construir).

---

## Valores exactos para Cloudflare (cópialos al configurar)

| Campo | Valor que debes poner |
|-------|------------------------|
| **Repository** | `angelucv/cvea` |
| **Production branch** | `gh-pages` |
| **Build command** | *(dejar vacío)* |
| **Build output directory** | `/` |
| **Project name** | `cvea` (la URL será **https://cvea.pages.dev**) |

---

## Paso 1: Entrar en Cloudflare

1. Abre **[dash.cloudflare.com](https://dash.cloudflare.com)**.
2. Inicia sesión (o regístrate con email o GitHub).

---

## Paso 2: Crear proyecto en Pages

1. En el menú izquierdo, clic en **Workers & Pages**.
2. Clic en **Create**.
3. Elige **Pages**.
4. Elige **Connect to Git**.

---

## Paso 3: Conectar GitHub

1. Si te sale **Connect GitHub**, clic ahí.
2. Inicia sesión en GitHub si hace falta.
3. Autoriza **Cloudflare Pages** (puedes dar acceso solo al repo `cvea` o a todos).
4. Vuelve al panel de Cloudflare.

---

## Paso 4: Elegir repo y configurar

1. En **Select repository** busca y elige **`angelucv/cvea`**.
2. Clic en **Begin setup**.

Luego rellena así:

- **Project name:** `cvea`  
  (así la URL quedará **https://cvea.pages.dev**)

- **Production branch:** `gh-pages`  
  (es la rama donde GitHub Actions ya publica el sitio)

- **Build settings:**
  - **Framework preset:** *None* (o déjalo por defecto).
  - **Build command:** **borra todo** y déjalo vacío.
  - **Build output directory:** escribe **`/`** (solo la barra).

3. Clic en **Save and Deploy**.

---

## Paso 5: Esperar el primer despliegue

1. Verás un despliegue en estado **Building** y luego **Success** (unos segundos, porque no hay build).
2. Al terminar, clic en **Visit site** o abre **https://cvea.pages.dev**.

Ahí debería verse tu sitio igual que en **https://angelucv.github.io/cvea/**.

---

## A partir de ahora (automático)

- Cada **push a `main`** en GitHub → el workflow actualiza **`gh-pages`** → Cloudflare detecta el cambio y vuelve a desplegar.
- No tienes que hacer nada más en Cloudflare.

---

## Si la rama `gh-pages` aún no existe

Si acabas de crear el repo y todavía no se ha ejecutado el workflow de GitHub:

1. Ve a **[github.com/angelucv/cvea/actions](https://github.com/angelucv/cvea/actions)**.
2. Comprueba que el workflow **Quarto Publish** haya terminado correctamente (rama `gh-pages` creada).
3. Luego en Cloudflare haz **Retry deployment** o espera al siguiente push a `main`; cuando exista `gh-pages`, el despliegue funcionará.

---

## Resumen

- **Repositorio:** [github.com/angelucv/cvea](https://github.com/angelucv/cvea)
- **Rama en Cloudflare:** `gh-pages`
- **Build:** ninguno (comando vacío, output `/`)
- **URL del sitio en Cloudflare:** **https://cvea.pages.dev**

Si más adelante quieres un dominio propio (ej. cvea.com): en el proyecto de Pages → **Custom domains** → **Set up a custom domain** y sigue las instrucciones.
