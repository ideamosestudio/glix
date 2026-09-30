# Seguridad y mantenimiento

Revisión: 30/09/2026. Alcance: cinco páginas de la web comercial y su formulario. El software ERP, sus cuentas, servidores y bases de datos no forman parte de esta revisión.

## Sitio estático

- HTTPS habilitado en la publicación principal. CSP al principio del HTML: scripts, CSS, imágenes y fuentes locales; conexión exclusivamente al origen propio y al endpoint autorizado de cPanel. Sin inline, eval, objetos ni iframes.
- El formulario envía JSON mediante fetch; la CSP mantiene bloqueada la navegación mediante formularios HTML convencionales.
- Enlaces externos con noopener/noreferrer. Fuentes locales y licencias OFL. Sin dependencias JavaScript externas.
- Imágenes WebP y variantes responsivas; secuencias pausadas fuera de pantalla, en segundo plano y con movimiento reducido.
- GitHub Actions valida recursos, CSP, JavaScript, despliegue y servicio de contacto. Acción fijada por commit y Dependabot mensual.

## Copia en cPanel

Actualización por cron cada minuto, archivos verificados por SHA-256 y respaldos privados. Se preservan archivos ajenos, ajustes PHP y demás tareas programadas. La clave SSH dedicada permite únicamente operaciones de despliegue y consulta del sitio. GitHub ya no guarda los secretos SSH utilizados por el mecanismo anterior.

Se verificaron a través de Nginx: X-Content-Type-Options, Referrer-Policy, X-Frame-Options, CSP frame-ancestors y Permissions-Policy. HTML/CSS/JS requieren revalidación; imágenes y fuentes tienen caché de un día. Gzip comprobado. Las reglas solo cubren rutas del sitio y excluyen la API.

La publicación principal en GitHub Pages tiene una configuración independiente: las cabeceras agregadas en cPanel no cambian ese alojamiento. HSTS global, includeSubDomains o preload requieren revisar todos los servicios y no se activaron. La protección de rama y MFA quedan bajo administración del propietario; no se afirma que estén configuradas.

## Formulario comercial

Endpoint: `https://mail.glixerp.com/api/glix-contact.php`. Destinatario y remitente fijos: `info@glixerp.com`. Reply-To usa únicamente un email validado. Los datos del visitante nunca se usan como opciones del transporte ni como destinatarios adicionales.

Validación del servidor, rechazo de saltos de línea en cabeceras, CORS de orígenes explícitos, JSON y tamaño acotados, honeypot, token HMAC ligado a IP con espera mínima y vencimiento, bloqueo de concurrencia y límites de 5 intentos por IP/hora y 100 globales/hora. Reintentos con el mismo token y contenido no duplican envíos aceptados. Estas medidas son protección básica y no sustituyen mitigación especializada ante ataques distribuidos.

Clave, lógica y estado en `/home5/glixcpanel/.glix-contact`, fuera de public_html. Los límites conservan hashes y tiempos, no el contenido de las consultas; se podan al procesar solicitudes. El contenido se entrega al transporte de correo del hosting. No hay contraseñas SMTP en Git. El endpoint responde no-store y noindex.

`php server/test-contact.php` usa un transporte simulado: valida origen, inyección de cabeceras, tipos, honeypot, vencimiento, tiempo mínimo, IP, reintentos y límites. No envía correos.

El 30/09/2026 se realizó un único envío real autorizado a info@glixerp.com desde el formulario publicado: respuesta 200, aceptación del transporte y confirmación visual, sin errores JavaScript. `mail()` confirma aceptación para entrega, no recepción final en el buzón.

## Correo y soporte

MX apunta a mail.glixerp.com, 167.250.5.104. cPanel validó SPF y DKIM. DMARC está publicado con p=none. SMTP 465 e IMAP 993 verificaron TLS 1.3 y certificado válido. No se alteraron buzones ni contraseñas.

El proveedor confirmó Zammad mediante `soporte.glixerp.com CNAME servidor.yamanil.com`; el registro se verificó y se preservó. No fue necesario crear ni cambiar DNS para el formulario.

## Mantenimiento

Ejecutar `python scripts/check-site.py`, las pruebas de despliegue/configuración cPanel, `node --check script.js`, `node --check contact.js` y `php server/test-contact.php`. Revisar móvil/escritorio y propuestas de Dependabot. No guardar secretos ni información de clientes en Git. Las pruebas reales de envío necesitan autorización explícita.

Es una revisión acotada, no una certificación de cumplimiento ni una auditoría del ERP. Referencias: [OWASP Top 10:2025](https://top10.owasp.org/2025/), [PHP mail](https://www.php.net/manual/en/function.mail.php) y [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP).
