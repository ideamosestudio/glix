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
