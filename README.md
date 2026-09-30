# GLIX — sitio web corporativo

Sitio estático de cinco páginas en HTML, CSS y JavaScript. No requiere compilación, dependencias de ejecución ni variables de entorno. El repositorio es la fuente de los cambios; cPanel mantiene una copia automática en `public_html`. Ver [CPANEL-COPY.md](CPANEL-COPY.md).

## Desarrollo y validación

Desde esta carpeta: `python -m http.server 8765`. Abrir http://localhost:8765.

Antes de publicar:

- `python scripts/check-site.py`
- `python scripts/test-cpanel-deploy.py`
- `node --check script.js`

Las mismas comprobaciones se ejecutan en GitHub Actions. Editar, confirmar los cambios y subirlos a `main`; no editar la copia del servidor a mano.

## Recursos y diseño

[MANUAL-DISENO.md](MANUAL-DISENO.md) documenta la grilla y componentes. `design-system.css` contiene los ajustes finales del diseño. Las capturas contienen datos de muestra y las llamadas de contacto usan WhatsApp 5491158305425.

Imágenes WebP, variantes de 640 px y fuentes locales con licencias OFL. Las secuencias de computadora y teléfono avanzan cada dos segundos y se pausan fuera de pantalla, en segundo plano y con movimiento reducido. La solución usa una imagen fija.

Se retiraron 40 imágenes originales o antiguas sin referencias (20.183.062 bytes); se pueden recuperar desde el historial Git. No borrar variantes responsivas, cuadros de animación ni licencias.

## Seguridad y alojamiento

Ver [SECURITY.md](SECURITY.md). La web no contiene el sistema ERP, cuentas de usuarios ni una base de datos. La publicación principal y la copia en cPanel tienen configuraciones de alojamiento independientes. Los cambios del sitio no modifican DNS ni correo.

## Contacto

Las cinco páginas comparten `contact.css` y `contact.js`. El formulario entrega consultas a info@glixerp.com mediante cPanel. Requiere PHP únicamente en el servidor de envío, no en la publicación estática. Los datos de muestra de las pruebas no representan clientes reales. Ver SECURITY.md para validación, antispam y límites.


## SEO, vista previa y rendimiento

Las cinco páginas incluyen URL canónica, metadatos Open Graph y Twitter, y datos estructurados Organization/WebSite/WebPage coherentes con el contenido visible. La imagen compartida está en `assets/social/glix-social-v1.png`. Los datos JSON-LD tienen un hash CSP exacto; al editarlos, actualizar el hash y ejecutar `python scripts/check-site.py`.

El contenido principal está en HTML y no depende de JavaScript para ser leído. `robots.txt` permite rastreo y enlaza el sitemap; `llms.txt` ofrece un resumen público opcional. Ninguno de estos mecanismos garantiza indexación, posicionamiento o citas de sistemas de IA.

Las fuentes principales se precargan desde el propio sitio. Los títulos inicialmente visibles no se ocultan esperando una animación; los títulos de secciones posteriores conservan su aparición al desplazarse. Los fotogramas secundarios de la portada tienen prioridad de descarga baja. Las animaciones siguen respetando movimiento reducido y pausa fuera de pantalla.

El crédito del pie utiliza el logo oficial de Ideamos y enlaza a https://ideamos.com.ar/. El formulario conserva su destino `info@glixerp.com`.

El brillo de los botones anima opacidad en capas independientes para evitar recalcular sombras en cada fotograma, conservando la iluminación y los colores de marca.
