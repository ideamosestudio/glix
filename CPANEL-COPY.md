# Copia automática en cPanel

La web pública continúa en GitHub Pages. Este mecanismo mantiene una segunda copia de los archivos del sitio en `/home5/glixcpanel/public_html`.

- Repositorio administrado por cPanel: `/home5/glixcpanel/repositories/glix`.
- Origen: `https://github.com/ideamosestudio/glix.git`, rama `main`.
- Cada push a main ejecuta las validaciones y después el job **Update cPanel copy**. También se puede ejecutar manualmente el workflow **Validate website** sobre main.
- La copia no depende de que una computadora personal esté encendida.
- Solo se despliegan páginas HTML, CSS, JavaScript, iconos, robots.txt, sitemap.xml y recursos admitidos bajo assets. No se copian `.git`, workflows, scripts operativos ni documentación interna.
- Se conservan `.htaccess`, `.user.ini`, `php.ini`, `.well-known`, `cgi-bin` y archivos ajenos al sitio. Los archivos eliminados del repositorio solo se retiran si el manifiesto privado los identifica como gestionados anteriormente; si fueron modificados manualmente se detiene el despliegue.
- Los archivos sustituidos o retirados se respaldan en `/home5/glixcpanel/.glix-mirror/backups`. No se purgan automáticamente: revisar el espacio ocupado periódicamente.
- El manifiesto privado registra el commit y SHA-256 de cada archivo. La copia y el estado final se verifican por contenido.
- Se usan bloqueos contra ejecuciones simultáneas y reemplazos atómicos por archivo. Si una operación falla durante la copia, se intenta restaurar lo ya cambiado. No es un cambio atómico del sitio completo ni una protección contra caída total del servidor.
- La clave dedicada de GitHub solo permite `glix-sync <commit>`, `glix-dry-run <commit>` y `glix-status`. No sirve como consola general, túnel ni SFTP una vez restringida.

## Configuración de GitHub

Variables: `CPANEL_HOST`, `CPANEL_PORT`, `CPANEL_USER`, `CPANEL_SYNC_ENABLED=true`.
Secretos: `CPANEL_SSH_KEY` y `CPANEL_KNOWN_HOSTS`. La clave privada no está en el repositorio. La huella del servidor está fijada; no se acepta automáticamente un cambio de clave.

Para pausar solo esta copia, cambiar `CPANEL_SYNC_ENABLED` a `false`. GitHub Pages continúa funcionando de manera independiente.

## cPanel

El repositorio figura como **glix** en Control de versión de Git. `.cpanel.yml` permite también el despliegue manual desde esa interfaz. No editar su copia de trabajo a mano: GitHub es el origen de los cambios. Si cambia el script de acceso restringido, actualizar también su instalación privada en `.glix-mirror/ssh-gateway.py` desde una sesión administrativa independiente.

No se modifican DNS, MX, correo ni configuración PHP del hosting.
