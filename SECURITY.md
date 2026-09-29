# Seguridad y mantenimiento

Revisión: 29/09/2026. Alcance: las cinco páginas de la web comercial. El software ERP, sus servidores, cuentas y bases de datos no están incluidos.

## Implementado

- HTTPS obligatorio ya habilitado en GitHub Pages.
- CSP al principio de cada página: scripts e imágenes locales; CSS y fuentes locales. Bloquea código inline, eval, objetos, iframes, conexiones programáticas externas, cambios de URL base y formularios.
- Referrer Policy y enlaces externos con noopener/noreferrer.
- Sin dependencias JavaScript de terceros, backend, login ni base de datos.
- Validación de recursos, anclas, CSP, imágenes y sintaxis JS en GitHub Actions. Acción fijada a commit, permisos mínimos y Dependabot mensual.
- Secuencias con intervalos acotados, pausa fuera de pantalla y en segundo plano, movimiento reducido dinámico y conservación del cuadro actual ante un fallo de carga.

## Pendiente fuera del código

La respuesta pública revisada no incluye HSTS, X-Content-Type-Options, Permissions-Policy ni protección anti-iframe. La CSP en meta tiene limitaciones: frame-ancestors requiere una cabecera HTTP. No se simulan esas cabeceras con etiquetas meta.

Para completar esa capa hace falta un alojamiento o proxy que permita configurar cabeceras. Revisar todos los subdominios antes de considerar HSTS includeSubDomains o preload. No se modificaron DNS ni correo.

Revisar MFA, permisos y protección de rama en GitHub. El workflow valida cambios pero la publicación actual desde main no espera esos controles; bloquear publicaciones fallidas exige protección de rama o despliegue condicionado. Estas configuraciones no se modificaron.

## OWASP Top 10:2025

| Riesgo | Alcance |
| --- | --- |
| A01 Acceso | Sitio público; revisar cuentas del repositorio y ERP por separado. |
| A02 Configuración | CSP y HTTPS; cabeceras de infraestructura pendientes. |
| A03 Cadena de suministro | Sin librerías JS; acción fijada y Dependabot. Fuentes locales con sus licencias OFL. |
| A04 Criptografía | HTTPS verificado; sin credenciales de usuarios en esta web. |
| A05 Inyección | Sin entradas dinámicas ni sinks HTML; CSP restrictiva. |
| A06 Diseño | Nuevas integraciones necesitan revisar flujos y política. |
| A07 Autenticación | No hay login en este repositorio. |
| A08 Integridad | Recursos locales y validación; falta verificar protección de cuenta/rama. |
| A09 Registros | Resultados en Actions; monitorización operativa del ERP fuera de alcance. |
| A10 Excepciones | Secuencias conservan cuadro actual ante fallo y acotan intervalos. |

Es una revisión acotada, no una certificación de cumplimiento ni una auditoría del ERP.

## Verificación y mantenimiento

Ejecutar `python scripts/check-site.py` y `node --check script.js`. Revisar móvil/escritorio antes de publicar y medir rendimiento público después. Revisar propuestas de Dependabot sin fusionar cambios mayores automáticamente. No guardar secretos en archivos públicos ni en Git.

Referencias: https://top10.owasp.org/2025/ y https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
