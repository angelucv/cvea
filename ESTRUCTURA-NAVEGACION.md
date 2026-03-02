# Opciones de menú para portales (CVEA Suite, RVEA, Cursos) y lógica de agrupamiento

## 1. Menú en las páginas con animación (CVEA Suite, RVEA, Cursos)

En estas tres páginas el hero va a ancho completo y no hay barra lateral. Opciones para dar navegación fija **debajo de la animación** (no tipo móvil):

### Opción A — Barra horizontal fija debajo del hero
Una franja horizontal justo bajo el hero con enlaces principales, siempre visible (o fija al hacer scroll). Por ejemplo:
- **Inicio · El CVEA · Miembros · RVEA · Cursos · Actualidad · Contacto**
Se puede estilizar con el verde institucional y tipografía clara. Fácil de implementar en el HTML/CSS de cada página (o con un include común).

### Opción B — Pestañas (tabs) debajo del hero
Mismo contenido que A pero con estilo de pestañas: la sección actual (p. ej. «RVEA») resaltada y el resto como pestañas clicables. Transmite idea de “portal” con varias secciones.

### Opción C — Barra con desplegables
Una barra debajo del hero con pocos ítems y, en algunos, menú desplegable (p. ej. «Investigación» abre Libros, TFPG, RVEA, Model Hub). Reduce ruido pero mantiene acceso a todo sin usar barra lateral.

### Opción D — Breadcrumb + enlaces rápidos
Debajo del hero: breadcrumb (Inicio > RVEA) a la izquierda y a la derecha 3–4 enlaces rápidos (Artículos, Portal, Cursos, Contacto). Menú ligero sin duplicar todo el árbol.

### Opción E — Solo navbar superior
Dejar la navegación solo en la barra superior (como ahora). Opcional: hacer la navbar más visible en estas páginas (por ejemplo fondo sólido al hacer scroll) para que no se sienta “sin menú”.

**Recomendación:** La **Opción A** (barra horizontal fija debajo del hero) es la más clara y coherente con “algo fijo debajo de la animación” sin parecer menú móvil. Si quieres, se puede implementar A en las tres páginas con un fragmento HTML/CSS reutilizable.

---

## 2. Lógica de agrupamiento del contenido

Tu lectura es correcta:

- **Portales (contenido profundo):** CVEA Suite, RVEA, Cursos.
- **Presentación:** El CVEA, Miembros.
- **Información / dinámico:** Actualidad, Contacto.
- **Qué hacer con:** Libros, Observatorio, Extensión, Docencia, Investigación.

Una lógica que evita que queden “huérfanos” es agrupar por **los tres ejes del CVEA** (Investigación, Docencia, Extensión) y luego identidad e información:

| Agrupación | Contenido | Rol |
|------------|-----------|-----|
| **Inicio** | index | Punto de entrada. |
| **Identidad** | El CVEA, Miembros | Quiénes somos y equipo. |
| **Investigación** | Libros, TFPG, Revista RVEA, Model Hub | Producción científica y recursos. |
| **Docencia** | Cursos (y dentro: Series de Tiempo, Plataforma, Recursos, Próximas ofertas) | Formación y oferta académica. |
| **Extensión** | Servicios, Observatorio, CVEA Suite | Servicios, datos y herramientas. |
| **Información** | Actualidad, Contacto | Noticias y canal de contacto. |

Así:
- **Libros** y **Observatorio** no quedan sueltos: Libros dentro de Investigación, Observatorio dentro de Extensión.
- **Extensión** agrupa “lo que ofrecemos al sector” (servicios, observatorio, Suite).
- **Docencia** agrupa todo lo formativo; **Cursos** puede ser el ítem principal que lleve a la página portal de cursos.
- **Investigación** ya agrupa Libros, TFPG, RVEA y Model Hub.

### Propuesta concreta para la barra lateral

Orden y secciones sugeridos (sin duplicar ítems):

1. **Inicio**
2. **El CVEA**
3. **Miembros**
4. **Investigación** (sección desplegable)
   - Libros  
   - TFPG  
   - Revista RVEA  
   - Model Hub  
5. **Docencia** (sección desplegable)
   - Cursos (página portal)  
   - Series de Tiempo (Python)  
   - Plataforma de cursos  
   - Recursos para estudiantes  
   - Próximas ofertas  
6. **Extensión** (sección desplegable)
   - Servicios  
   - Observatorio  
   - CVEA Suite (o enlace a la página portal CVEA Suite)  
7. **Actualidad**
8. **Contacto**

Con esto se eliminan los ítems sueltos “Libros”, “Cursos” y la sección “RVEA” duplicada: **Libros** solo dentro de Investigación, **Cursos** como primer ítem de Docencia (portal), **RVEA** solo dentro de Investigación. CVEA Suite queda como parte de Extensión.

### Resumen

- **Menú en portales:** Opción A (barra fija debajo del hero) es la más directa; B, C, D son variantes de presentación; E es mantener solo navbar.
- **Agrupamiento:** Usar los tres ejes (Investigación, Docencia, Extensión) + Identidad (El CVEA, Miembros) + Información (Actualidad, Contacto) para que Libros, Observatorio, Extensión y Docencia tengan un lugar claro y nada quede huérfano.

**Estado:** Aplicada la **Opción A** (barra fija debajo del hero en RVEA, CVEA Suite y Cursos) y la **nueva distribución** de la barra lateral en `_website.yml` (Investigación, Docencia, Extensión sin duplicados).
