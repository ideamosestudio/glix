# Copia automÃ¡tica en cPanel

El servidor consulta `main` cada minuto y actualiza `/home5/glixcpanel/public_html` cuando encuentra una versiÃ³n nueva. No depende de una computadora encendida ni de conexiones SSH entrantes desde GitHub Actions.

- Repositorio cPanel: `/home5/glixcpanel/repositories/glix`.
- Origen: `https://github.com/ideamosestudio/glix.git`.
- Tarea visible en **cPanel â†’ Trabajos de cron**, identificada con `# glix-website-mirror`.
- Se ejecutan las comprobaciones de recursos, CSP y pruebas de despliegue antes de copiar. Actions aÃ±ade la validaciÃ³n de sintaxis JavaScript. El servidor no espera el estado de Actions.
- Un bloqueo impide dos consultas simultÃ¡neas. Se despliega el Ãºltimo commit de main; varios cambios rÃ¡pidos pueden agruparse.
- Estado privado: `.glix-mirror/manifest.json`, con commit y hash SHA-256 de cada archivo. `.glix-mirror/poll-last-success.json` registra la Ãºltima actualizaciÃ³n desde cron.
- DiagnÃ³stico: `.glix-mirror/poll.log` y `poll.previous.log`, con rotaciÃ³n a 256 KiB. No estÃ¡n dentro de public_html.
- Solo se publican HTML, CSS, JavaScript, iconos, robots.txt, sitemap.xml y recursos del sitio. No se copian Git, scripts operativos ni documentaciÃ³n.
- Se preservan archivos ajenos, configuraciÃ³n PHP, correo y DNS. Solo se retiran archivos que el manifiesto identifica como propios y que no fueron modificados externamente.
- Los archivos reemplazados se respaldan en `.glix-mirror/backups`; no se purgan automÃ¡ticamente.
- Reemplazos atÃ³micos por archivo y restauraciÃ³n ante errores de copia; no es una transacciÃ³n atÃ³mica del sitio completo ni protege frente a caÃ­da del servidor.

La clave SSH dedicada permite Ãºnicamente `glix-sync <commit>`, `glix-dry-run <commit>` y `glix-status`. No es una consola administrativa. Los secretos SSH ya no son necesarios en GitHub para esta modalidad.

`.cpanel.yml` permite una copia manual desde Control de versiÃ³n de Git. La instalaciÃ³n conserva los demÃ¡s trabajos de cron. Para pausar la sincronizaciÃ³n, retirar su lÃ­nea de cron y no ejecutar otro despliegue manual, que reinstala la tarea.

La publicaciÃ³n principal permanece independiente; esta configuraciÃ³n no cambia el destino del dominio ni el correo.

## Ajustes de la copia web

Un bloque identificado en `.htaccess` añade cabeceras de seguridad, caché de imágenes/fuentes por un día y compresión de texto únicamente para las rutas gestionadas por el sitio. HTML, CSS y JavaScript requieren revalidación para recibir actualizaciones. Se guarda una copia privada de la configuración anterior y se comprueba la respuesta del servidor; ante un error se restaura el archivo anterior. Se preservan las directivas del proveedor. No se cambian límites PHP ni se activa HSTS para otros subdominios.

Referencias de implementación: [cron en cPanel](https://docs.cpanel.net/knowledge-base/web-services/guide-to-git-set-up-deployment-cron-jobs/), [cabeceras Apache](https://httpd.apache.org/docs/2.4/mod/mod_headers.html) y [compresión Apache](https://httpd.apache.org/docs/2.4/mod/mod_deflate.html).
