# Subir el proyecto CVEA a GitHub (repo «cvea»)

Sigue estos pasos para crear el repositorio **cvea** en GitHub y subir tu proyecto.

---

## Paso 1: Crear cuenta en GitHub (si no la tienes)

1. Entra en **[github.com](https://github.com)**.
2. Pulsa **Sign up** y crea una cuenta (email, contraseña, etc.).
3. Verifica tu correo si te lo piden.

---

## Paso 2: Crear el repositorio «cvea» en GitHub (vacío)

1. Inicia sesión en GitHub.
2. Arriba a la derecha, clic en **+** → **New repository**.
3. Rellena:
   - **Repository name:** `cvea` (solo eso, en minúsculas).
   - **Description:** opcional, por ejemplo: *Sitio web del Centro Venezolano de Estudios Actuariales*.
   - **Public**.
   - **No** marques "Add a README", "Add .gitignore" ni "Choose a license" (el proyecto ya tiene sus archivos).
4. Pulsa **Create repository**.

Dejarás la página que dice "…or push an existing repository from the command line". No cierres esa página; la usarás en el Paso 4.

---

## Paso 3: Abrir la terminal en la carpeta del proyecto

1. Abre **PowerShell** o **Terminal** (o **CMD**).
2. Ve a la carpeta del proyecto (ajusta la ruta si la tienes en otro sitio):

```powershell
cd C:\Users\Angel\cvea-platform
```

---

## Paso 4: Inicializar Git y subir el código

Copia y pega estos comandos **uno por uno** (o todos seguidos). Sustituye `TU_USUARIO` por tu usuario de GitHub (por ejemplo `angel-colmenares`).

**4.1 — Inicializar el repositorio (solo la primera vez):**

```powershell
git init
```

**4.2 — Añadir todos los archivos:**

```powershell
git add .
```

**4.3 — Primer commit:**

```powershell
git commit -m "Sitio CVEA con Quarto - primera subida"
```

**4.4 — Nombrar la rama principal «main»:**

```powershell
git branch -M main
```

**4.5 — Conectar con tu repo en GitHub (cambia TU_USUARIO por tu usuario):**

```powershell
git remote add origin https://github.com/TU_USUARIO/cvea.git
```

Ejemplo si tu usuario es `angel-colmenares`:

```powershell
git remote add origin https://github.com/angel-colmenares/cvea.git
```

**4.6 — Subir el código:**

```powershell
git push -u origin main
```

Te pedirá **usuario y contraseña**. En GitHub ya no se usa contraseña por defecto; hay que usar un **Personal Access Token (PAT)**.

---

## Paso 5: Token de acceso (cuando pida usuario/contraseña)

1. En GitHub: **Settings** (tu foto arriba a la derecha) → **Developer settings** → **Personal access tokens** → **Tokens (classic)**.
2. **Generate new token (classic)**.
3. **Note:** por ejemplo `cvea-push`.
4. **Expiration:** 90 days o No expiration, como prefieras.
5. Marca al menos: **repo** (acceso a repositorios).
6. **Generate token** y **copia el token** (solo se muestra una vez).
7. Cuando en la terminal te pida:
   - **Username:** tu usuario de GitHub.
   - **Password:** pega el **token** (no tu contraseña de GitHub).

Si ya tienes **GitHub CLI** (`gh`) instalado y hecho `gh auth login`, no te pedirá token al hacer `git push`.

---

## Paso 6: Comprobar que todo está en GitHub

1. Entra en **https://github.com/TU_USUARIO/cvea**.
2. Deberías ver todos los archivos del proyecto.
3. El **workflow** (`.github/workflows/publish.yml`) se ejecutará y en unos minutos el sitio estará en:
   - **https://TU_USUARIO.github.io/cvea/**

---

## Resumen de comandos (todo junto)

Ajusta `TU_USUARIO` y ejecuta en la carpeta del proyecto:

```powershell
cd C:\Users\Angel\cvea-platform
git init
git add .
git commit -m "Sitio CVEA con Quarto - primera subida"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/cvea.git
git push -u origin main
```

Cuando pida contraseña, usa el **Personal Access Token** (Paso 5).

---

## Si algo falla

- **"git no se reconoce"**: Instala Git: [git-scm.com/download/win](https://git-scm.com/download/win). Luego cierra y abre de nuevo la terminal.
- **"remote origin already exists"**: Ya tienes un remote; para cambiarlo:  
  `git remote set-url origin https://github.com/TU_USUARIO/cvea.git`
- **"Authentication failed"**: Usa el token (Paso 5), no la contraseña de la cuenta de GitHub.

Cuando tengas el repo **cvea** en GitHub, puedes seguir la guía **DEPLOY-CLOUDFLARE.md** para desplegarlo también en Cloudflare Pages.
