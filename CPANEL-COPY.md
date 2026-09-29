# Copia automática en cPanel

El servidor consulta `main` cada minuto y actualiza `/home5/glixcpanel/public_html` cuando encuentra una versión nueva. No depende de una computadora encendida ni de conexiones SSH entrantes desde GitHub Actions.

- Repositorio cPanel: `/home5/glixcpanel/repositories/glix`.
- Origen: `https://github.com/ideamosestudio/glix.git`.
- Tarea visible en **cPanel → Trabajos de cron**, identificada con `# glix-website-mirror`.
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
