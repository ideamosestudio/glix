# Seguridad y mantenimiento

RevisiÃ³n: 29/09/2026. Alcance: las cinco pÃ¡ginas de la web comercial. El software ERP, sus servidores, cuentas y bases de datos no estÃ¡n incluidos.

## Implementado

- HTTPS obligatorio ya habilitado en GitHub Pages.
- CSP al principio de cada pÃ¡gina: scripts e imÃ¡genes locales; CSS y fuentes locales. Bloquea cÃ³digo inline, eval, objetos, iframes, conexiones programÃ¡ticas externas, cambios de URL base y formularios.
- Referrer Policy y enlaces externos con noopener/noreferrer.
- Sin dependencias JavaScript de terceros, backend, login ni base de datos.
- ValidaciÃ³n de recursos, anclas, CSP, imÃ¡genes y sintaxis JS en GitHub Actions. AcciÃ³n fijada a commit, permisos mÃ­nimos y Dependabot mensual.
- Secuencias con intervalos acotados, pausa fuera de pantalla y en segundo plano, movimiento reducido dinÃ¡mico y conservaciÃ³n del cuadro actual ante un fallo de carga.

## Pendiente fuera del cÃ³digo

La respuesta pÃºblica revisada no incluye HSTS, X-Content-Type-Options, Permissions-Policy ni protecciÃ³n anti-iframe. La CSP en meta tiene limitaciones: frame-ancestors requiere una cabecera HTTP. No se simulan esas cabeceras con etiquetas meta.

Para completar esa capa hace falta un alojamiento o proxy que permita configurar cabeceras. Revisar todos los subdominios antes de considerar HSTS includeSubDomains o preload. No se modificaron DNS ni correo.

Revisar MFA, permisos y protecciÃ³n de rama en GitHub. El workflow valida cambios pero la publicaciÃ³n actual desde main no espera esos controles; bloquear publicaciones fallidas exige protecciÃ³n de rama o despliegue condicionado. Estas configuraciones no se modificaron.

## OWASP Top 10:2025

| Riesgo | Alcance |
| --- | --- |
| A01 Acceso | Sitio pÃºblico; revisar cuentas del repositorio y ERP por separado. |
| A02 ConfiguraciÃ³n | CSP y HTTPS; cabeceras de infraestructura pendientes. |
| A03 Cadena de suministro | Sin librerÃ­as JS; acciÃ³n fijada y Dependabot. Fuentes locales con sus licencias OFL. |
| A04 CriptografÃ­a | HTTPS verificado; sin credenciales de usuarios en esta web. |
| A05 InyecciÃ³n | Sin entradas dinÃ¡micas ni sinks HTML; CSP restrictiva. |
| A06 DiseÃ±o | Nuevas integraciones necesitan revisar flujos y polÃ­tica. |
| A07 AutenticaciÃ³n | No hay login en este repositorio. |
| A08 Integridad | Recursos locales y validaciÃ³n; falta verificar protecciÃ³n de cuenta/rama. |
| A09 Registros | Resultados en Actions; monitorizaciÃ³n operativa del ERP fuera de alcance. |
| A10 Excepciones | Secuencias conservan cuadro actual ante fallo y acotan intervalos. |

Es una revisiÃ³n acotada, no una certificaciÃ³n de cumplimiento ni una auditorÃ­a del ERP.

## VerificaciÃ³n y mantenimiento

Ejecutar `python scripts/check-site.py` y `node --check script.js`. Revisar mÃ³vil/escritorio antes de publicar y medir rendimiento pÃºblico despuÃ©s. Revisar propuestas de Dependabot sin fusionar cambios mayores automÃ¡ticamente. No guardar secretos en archivos pÃºblicos ni en Git.

Referencias: https://top10.owasp.org/2025/ y https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
