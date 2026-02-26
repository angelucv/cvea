# Guía paso a paso: desplegar CVEA en Cloudflare Pages (gratis)

Tu proyecto ya se publica en **GitHub Pages** con un workflow que genera el sitio con Quarto y lo sube a la rama `gh-pages`. En Cloudflare solo vamos a **usar esa misma rama** como origen, sin volver a construir nada. Así no pagas nada y todo sigue siendo automático.

---

## Requisitos previos

- Proyecto en **GitHub** (por ejemplo `angel-colmenares/cvea-platform`).
- El workflow en `.github/workflows/publish.yml` debe estar activo (cada push a `main` genera y sube el sitio a la rama `gh-pages`).

Si aún no has subido el repo o no tienes el workflow, hazlo antes de seguir.

---

## Paso 1: Crear cuenta en Cloudflare (si no la tienes)

1. Entra en **[dash.cloudflare.com](https://dash.cloudflare.com)**.
2. Pulsa **Sign Up** y regístrate con tu email (o con Google/GitHub).
3. Verifica el correo si te lo piden.

No hace falta añadir ningún dominio ni pagar nada.

---

## Paso 2: Crear un proyecto en Cloudflare Pages

1. En el panel de Cloudflare, en el menú izquierdo entra en **Workers & Pages**.
2. Pulsa **Create** → **Pages**.
3. Elige **Connect to Git** (conectar con Git).
4. Si es la primera vez, autoriza **GitHub**:
   - Pulsa **Connect GitHub**.
   - Inicia sesión en GitHub si hace falta y autoriza el acceso a **Cloudflare Pages**.
   - Puedes dar acceso a todos los repos o solo al repo del CVEA.

---

## Paso 3: Elegir el repositorio y la rama

1. En **Select repository** elige tu repo (ej. `angel-colmenares/cvea-platform`).
2. Pulsa **Begin setup**.
3. Configura así:
   - **Project name:** por ejemplo `cvea` o `cvea-platform` (será la parte de la URL: `cvea.pages.dev`).
   - **Production branch:** **`gh-pages`** (importante: la rama donde GitHub Actions ya publica el sitio).
   - **Build settings:**
     - **Build command:** déjalo **vacío** (no queremos que Cloudflare ejecute Quarto).
     - **Build output directory:** escribe **`/`** (raíz de la rama; en `gh-pages` el contenido del sitio ya está en la raíz).
4. Pulsa **Save and Deploy**.

Cloudflare va a leer la rama `gh-pages` y desplegar ese contenido. No ejecuta ningún build.

---

## Paso 4: Esperar el primer despliegue

1. En la página del proyecto verás un despliegue **Building** y luego **Success**.
2. Cuando termine, te dará un enlace tipo:
   - **https://cvea.pages.dev** (o el nombre que hayas puesto al proyecto).

Abre ese enlace y comprueba que el sitio se ve igual que en GitHub Pages.

---

## Paso 5: Despliegues automáticos a partir de ahora

- Cada vez que hagas **push a la rama `main`** de GitHub:
  1. El workflow de GitHub Actions genera el sitio con Quarto y actualiza la rama **`gh-pages`**.
  2. Cloudflare Pages detecta el cambio en `gh-pages` y hace un **nuevo despliegue** automáticamente.

No tienes que hacer nada más en Cloudflare; solo seguir trabajando y haciendo push a `main` como hasta ahora.

---

## Resumen de configuración en Cloudflare

| Campo                    | Valor      |
|--------------------------|------------|
| Production branch        | `gh-pages` |
| Build command            | *(vacío)*  |
| Build output directory   | `/`        |

---

## (Opcional) Dominio propio (ej. cvea.com)

Si más adelante compras un dominio:

1. En el proyecto de Pages, ve a **Custom domains**.
2. Pulsa **Set up a custom domain** e introduce tu dominio (ej. `cvea.com`).
3. Sigue las instrucciones de Cloudflare para añadir los registros DNS en tu registrador (o en Cloudflare si el dominio está ahí).

El alojamiento en Cloudflare Pages sigue siendo gratis; solo pagas el dominio al registrador.

---

## Si algo falla

- **El sitio no se actualiza:** Comprueba que el workflow de GitHub se ejecuta en cada push a `main` y que la rama `gh-pages` existe y tiene los últimos archivos (carpeta del sitio en la raíz).
- **Error en Cloudflare:** Revisa que **Production branch** sea exactamente **`gh-pages`** y que **Build output directory** sea **`/`**.
- **Página en blanco o 404:** Confirma que en la rama `gh-pages` hay un `index.html` en la raíz (así lo deja el workflow de Quarto).

Con esto puedes desplegar tu proyecto actual en Cloudflare Pages sin pagar nada y con la mayor capacidad (ancho de banda ilimitado en el plan gratuito).
