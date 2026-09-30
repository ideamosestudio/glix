# Copia automática en cPanel

El servidor consulta `main` cada minuto y actualiza `/home5/glixcpanel/public_html` cuando encuentra una versión nueva. No depende de una computadora encendida ni de conexiones SSH entrantes desde GitHub Actions.

- Repositorio cPanel: `/home5/glixcpanel/repositories/glix`.
- Origen: `https://github.com/ideamosestudio/glix.git`.
- Tarea visible en **cPanel â†’ Trabajos de cron**, identificada con `# glix-website-mirror`.
- Se ejecutan las comprobaciones de recursos, CSP y pruebas de despliegue antes de copiar. Actions añade la validación de sintaxis JavaScript. El servidor no espera el estado de Actions.
- Un bloqueo impide dos consultas simultáneas. Se despliega el último commit de main; varios cambios rápidos pueden agruparse.
- Estado privado: `.glix-mirror/manifest.json`, con commit y hash SHA-256 de cada archivo. `.glix-mirror/poll-last-success.json` registra la última actualización desde cron.
- Diagnóstico: `.glix-mirror/poll.log` y `poll.previous.log`, con rotación a 256 KiB. No están dentro de public_html.
- Solo se publican HTML, CSS, JavaScript, iconos, robots.txt, sitemap.xml y recursos del sitio. No se copian Git, scripts operativos ni documentación.
- Se preservan archivos ajenos, configuración PHP, correo y DNS. Solo se retiran archivos que el manifiesto identifica como propios y que no fueron modificados externamente.
- Los archivos reemplazados se respaldan en `.glix-mirror/backups`; no se purgan automáticamente.
- Reemplazos atómicos por archivo y restauración ante errores de copia; no es una transacción atómica del sitio completo ni protege frente a caída del servidor.

La clave SSH dedicada permite únicamente `glix-sync <commit>`, `glix-dry-run <commit>` y `glix-status`. No es una consola administrativa. Los secretos SSH ya no son necesarios en GitHub para esta modalidad.

`.cpanel.yml` permite una copia manual desde Control de versión de Git. La instalación conserva los demás trabajos de cron. Para pausar la sincronización, retirar su línea de cron y no ejecutar otro despliegue manual, que reinstala la tarea.

La publicación principal permanece independiente; esta configuración no cambia el destino del dominio ni el correo.

## Ajustes de la copia web

Un bloque identificado en `.htaccess` añade cabeceras de seguridad, caché de imágenes/fuentes por un día y compresión de texto únicamente para las rutas gestionadas por el sitio. HTML, CSS y JavaScript requieren revalidación para recibir actualizaciones. Se guarda una copia privada de la configuración anterior y se comprueba la respuesta del servidor; ante un error se restaura el archivo anterior. Se preservan las directivas del proveedor. No se cambian límites PHP ni se activa HSTS para otros subdominios.

Referencias de implementación: [cron en cPanel](https://docs.cpanel.net/knowledge-base/web-services/guide-to-git-set-up-deployment-cron-jobs/), [cabeceras Apache](https://httpd.apache.org/docs/2.4/mod/mod_headers.html) y [compresión Apache](https://httpd.apache.org/docs/2.4/mod/mod_deflate.html).

## Verificación del 30/09/2026

Se comprobó una actualización iniciada por cron, sin enviar una orden de despliegue desde el equipo. Las cinco páginas, incluida la portada raíz, coinciden con los archivos del commit publicado. `info@glixerp.com` aparece en los textos y enlaces de contacto de las cinco páginas.

El proxy HTTPS del hosting y Apache entregan las cabeceras configuradas. La comprobación interna usa el virtual host en el puerto 81 con X-Forwarded-Proto: https, porque las conexiones HTTP directas se redirigen a HTTPS. El contenido se verifica por SHA-256; ante una comprobación fallida se restaura la configuración anterior y se deja constancia en `.glix-mirror/web-verification.json`. La copia del sitio continúa disponible.

Nginx entrega gzip; imágenes/fuentes devuelven max-age=86400 y HTML devuelve no-cache. La caché Nginx se limpia mediante la API de cPanel después de desplegar. Las directivas originales de PHP se conservan.

## Servicio de contacto

El despliegue valida PHP y sus pruebas antes de instalar el servicio. Solo se admite `api/glix-contact.php` como endpoint PHP del sitio. La lógica, clave y límites se instalan fuera de public_html. Las reglas de caché estática excluyen `/api/`; el endpoint responde no-store. No se modifica el CNAME del soporte Zammad.
