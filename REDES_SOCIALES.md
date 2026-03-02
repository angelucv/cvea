# Redes sociales del CVEA — Instagram y conexión con la web

## ¿Se puede conectar la web con Instagram de forma automática?

**Resumen:** Instagram **no ofrece** una forma nativa ni gratuita para que “cada cambio en la web” publique solo en la cuenta. Hay opciones parciales y flujos semiautomáticos.

### Limitaciones de Instagram

- La API de Instagram (Meta) para publicar contenido está pensada para **cuentas Business/Creator** y suele requerir aprobación.
- No existe un “cuando mi página se actualice, publicar en Instagram” directo desde GitHub o desde el sitio.
- Publicar desde scripts o servicios externos suele requerir usar **Meta Business Suite** o la **Content Publishing API**, con restricciones y revisión.

### Opciones viables

1. **Flujo manual (recomendado al inicio)**  
   Cuando publiques una novedad en la web (artículo, libro, curso), añades una fila en [Actualidad → Novedades](actualidad.qmd#novedades) y, en paralelo, publicas tú mismo en Instagram (post o story) enlazando a la web. Es simple y sin dependencias técnicas.

2. **RSS de Novedades + herramienta externa**  
   Si en el futuro se expone un **feed RSS** con las novedades del sitio (por ejemplo solo la tabla de Novedades), podrías usar:
   - **IFTTT** o **Zapier**: “Cuando haya un nuevo ítem en el RSS → enviar notificación” o “crear borrador/post en otra red”.
   - Instagram no suele permitir “publicar solo por RSS” sin paso manual; lo más realista es usarlo para **recordatorios** (ej. “hay novedad en la web”) y tú publicas en Instagram.

3. **Buffer / Hootsuite / Meta Business Suite**  
   Puedes preparar posts con antelación y programarlos. Cuando actualices la web, añades la novedad en Actualidad y, en Buffer o Business Suite, programas un post que enlace a esa URL. Sigue siendo un paso manual por cada novedad, pero centralizado.

4. **Automatización “casi automática” (avanzado)**  
   Con un feed RSS de novedades + un script o servicio (por ejemplo en un servidor o GitHub Actions) que, al detectar un cambio, envíe un mensaje a Slack/Discord/email o cree un borrador en Meta Business Suite. La publicación en Instagram seguiría requiriendo un clic (revisión/approval) por políticas de Meta.

### Recomendación

- **Corto plazo:** Crear la cuenta de Instagram del CVEA y, cada vez que se añada algo en **Actualidad → Novedades**, publicar manualmente en Instagram con el enlace al sitio. Puedes indicar en la bio de Instagram: “Novedades y enlaces en [url del CVEA]”.
- **Mediano plazo:** Si se implementa un RSS de Novedades en el sitio, usarlo con IFTTT/Zapier para notificaciones o recordatorios; la publicación en Instagram seguirá siendo manual o semiautomática.

**Cuenta oficial del CVEA:** [@cvea_actuarial](https://instagram.com/cvea_actuarial) (Instagram). Correo oficial: [cvea.ucv@gmail.com](mailto:cvea.ucv@gmail.com). Este archivo se puede ampliar cuando se defina el flujo que se quiera usar (por ejemplo, si se usa Meta Business Suite o un gestor de redes).
