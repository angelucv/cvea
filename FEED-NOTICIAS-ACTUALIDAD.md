# Feed de noticias en la sección Actualidad — Opciones

## Dónde mostrar las noticias: inicio vs Actualidad

**Recomendación:** Mantener el **listado completo** de titulares en [Actualidad](actualidad.qmd) y, en la **página de inicio**, mostrar solo un **resumen** (2–3 titulares) con enlace a «Ver todas en Actualidad». Así la portada no se recarga de contenido y quien quiera más noticias va a Actualidad. En el index se ha añadido el bloque «Últimas noticias del sector» con ese teaser.

---

# Opciones técnicas (feeds)

Este documento resume las opciones para mostrar un **feed de noticias que se actualice automáticamente** en la sección "Noticias del sector en tiempo real" del sitio CVEA.

---

## 1. Investing.com — Widget de noticias financieras (recomendado para mercados/seguros)

**Qué es:** Investing.com ofrece **widgets gratuitos** para webmasters, entre ellos un **feed de noticias en tiempo real**.

- **URL:** [Investing.com Webmaster Tools — Real-Time News Feed](https://www.investing.com/webmaster-tools/real-time-news-feed)
- **Cómo funciona:** Entras en la página, eliges opciones (idioma, número de noticias, tamaño), y te dan un **código iframe** para pegar en tu sitio.
- **Ventajas:** Gratis, actualización en tiempo real, sin backend; solo copiar/pegar el iframe.
- **Limitaciones:** Contenido orientado a mercados/finanzas; hay que aceptar sus condiciones de uso.

**Pasos para integrarlo en el CVEA:**

1. Ir a https://www.investing.com/webmaster-tools/real-time-news-feed  
2. Configurar idioma (p. ej. español), cantidad de noticias y estilo.  
3. Copiar el código iframe que generan.  
4. En `actualidad.qmd`, en la sección "Noticias del sector en tiempo real", hay un bloque para **Feed embebido**. Pegar ahí el iframe dentro de un bloque HTML, por ejemplo:

   ```html   <div class="feed-embed">
     <!-- Pegar aquí el iframe de Investing.com -->
   </div>
   ```

Si quieres noticias más centradas en seguros/actuarial, en la misma herramienta suele poder restringirse por categoría (si lo ofrecen) o usar el feed general y complementar con los enlaces que ya tenemos (SOA, CAS, etc.).

---

## 2. Servicios de widget RSS (cualquier fuente con RSS)

Si tienes una **URL de feed RSS** (por ejemplo Google News, un blog o un medio), puedes usar un servicio que convierta ese RSS en un bloque embebible (iframe o script).

**Google News en formato RSS (para usar con un widget):**

- Noticias con la palabra "actuarial":  
  `https://news.google.com/rss/search?q=actuarial&hl=es`
- Noticias con "seguros":  
  `https://news.google.com/rss/search?q=seguros&hl=es`
- Combinado (actuarial O seguros):  
  `https://news.google.com/rss/search?q=actuarial+seguros&hl=es`

**Servicios que convierten RSS → widget embebible:**

| Servicio      | Uso básico |
|---------------|------------|
| **FeedWind**  | [feedwind.com](https://feedwind.com/) — Creas un widget con la URL del RSS, personalizas y obtienes código para embeber (iframe o script). |
| **Elfsight**  | [elfsight.com/rss-feed-widget/html](https://elfsight.com/rss-feed-widget/html) — Widget RSS para HTML; plan gratuito disponible. |
| **SociableKit** | Ofrece widget RSS para sitios HTML. |

**Flujo típico:**  
1) Obtener la URL del RSS (p. ej. Google News arriba).  
2) Entrar al servicio (FeedWind, Elfsight, etc.), crear widget con esa URL.  
3) Copiar el iframe o script que te den.  
4) Pegarlo en `actualidad.qmd` en el bloque "Feed embebido" (igual que con Investing.com).

---

## 3. Otras redes / fuentes de noticias

- **Reuters, Bloomberg, etc.:** Suelen tener widgets o APIs de pago; para un sitio institucional sin presupuesto, Investing.com o RSS + widget son más viables.
- **Redes sociales (Twitter/X, LinkedIn):** Se pueden embeber timelines o widgets oficiales si tienes cuenta; no son un “feed de noticias” genérico pero pueden complementar la sección.

---

## 4. Resumen práctico para el CVEA

| Objetivo                         | Opción recomendada |
|----------------------------------|---------------------|
| Noticias financieras/mercados (estilo Investing) | Widget Investing.com (iframe en Actualidad). |
| Noticias por palabras (actuarial, seguros)      | Google News RSS + FeedWind (u otro) → iframe en Actualidad. |
| Mantener enlaces a fuentes clave (SOA, CAS, etc.) | Dejar la tabla actual y añadir el feed encima o debajo. |

En `actualidad.qmd` está previsto un bloque para pegar el iframe (Investing.com o el que genere FeedWind/Elfsight). Solo hay que obtener el código en la web correspondiente y pegarlo ahí; no hace falta programar ni mantener un backend.
