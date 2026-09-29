# GLIX — sitio web corporativo

Sitio estático en HTML, CSS y JavaScript. No requiere instalación, compilación ni variables de entorno. Incluye la portada y cuatro páginas de módulos: Transporte y liquidación, Compras y proveedores, Recursos Humanos y App móvil de ventas. El contenido comercial se basa en `Glix - Presentacion General.pptx`; la información de contacto fue proporcionada para este sitio.

La grilla, los márgenes, el ritmo vertical, la tipografía y los botones se documentan en [`MANUAL-DISENO.md`](MANUAL-DISENO.md) y se aplican desde `design-system.css`.

Las capturas de `assets/gallery/` se basan en imágenes de la presentación. Se reemplazaron los datos visibles por ejemplos inventados y se identifican como **Datos de muestra**. Todos los botones de contacto y el acceso flotante usan WhatsApp `5491158305425`.

La portada alterna `compu-001.png`, `compu-002.png` y `compu-003.png` cada dos segundos. La sección de ventas alterna `phone-001.png` y `phone-002.png` con el mismo intervalo. La sección de solución alterna cuatro imágenes `solution-01.png` a `solution-04.png` cada 1,5 segundos. Las secuencias cambian de cuadro sin fundido. La cabecera y el pie usan el símbolo de `assets/brand/glix-blanco.png`; ese archivo tiene un lienzo blanco amplio y el logo está recortado en su borde derecho.

## Verlo en tu computadora

Abrí `index.html` en el navegador. Para probarlo con un servidor local, desde esta carpeta podés ejecutar `npx serve .` si tenés Node.js instalado.

## Subirlo a GitHub y publicarlo con GitHub Pages

1. Creá en GitHub un repositorio público llamado `glix` **vacío**: no agregues README, licencia ni `.gitignore` desde GitHub. Si tu cuenta tiene un plan que permite Pages desde repositorios privados, también podés elegir privado.
2. En una terminal, dentro de esta carpeta, ejecutá lo siguiente. Reemplazá `TU_USUARIO` por tu usuario u organización de GitHub:

   ```bash
   git add .
   git commit -m "Crear sitio GLIX"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/glix.git
   git push -u origin main
   ```

   Si ya existe `origin`, usá `git remote set-url origin https://github.com/TU_USUARIO/glix.git` en lugar de `git remote add origin ...`.

3. En GitHub, abrí el repositorio y entrá a **Settings → Pages**.
4. En **Build and deployment**, seleccioná **Deploy from a branch**. En **Branch**, elegí `main` y la carpeta `/(root)`, y guardá con **Save**.
5. La URL será `https://TU_USUARIO.github.io/glix/`. La primera publicación puede tardar unos minutos. Revisá **Actions** si GitHub informa un error de publicación.

Los archivos usan rutas relativas, por lo que también funcionan bajo `/glix/`. El archivo `.nojekyll` indica a GitHub Pages que publique el HTML, CSS y JavaScript directamente.

### Actualizaciones

Después de editar el sitio, ejecutá `git add .`, `git commit -m "Actualizar sitio"` y `git push`. GitHub Pages volverá a publicar la rama `main`.

### Dominio propio, opcional

Si más adelante querés usar un dominio propio, configuralo en **Settings → Pages → Custom domain** y agregá los registros DNS que indique GitHub. No agregues un archivo `CNAME` hasta conocer el dominio exacto.

## Seguridad y rendimiento (septiembre de 2026)

Consultar SECURITY.md. Validar con `python scripts/check-site.py` y `node --check script.js`.

Se optimizaron 27 recursos gráficos: 8.914.138 a 2.071.560 bytes (76,76 % menos). Es el total de archivos únicos, no una puntuación PageSpeed ni la transferencia inicial de una página. Capturas y logos usan WebP sin pérdida; fotos usan calidad 88. Se conservan los originales para edición.

Las secuencias de computadora y teléfono conservan sus dos segundos y se pausan fuera de pantalla, en segundo plano o con movimiento reducido. La sección de solución actual es una imagen fija. La marca usa glix-real-negro.webp y glix-real-blanco.webp. Estas descripciones actualizan las referencias históricas de imágenes anteriores de este documento.

También se incluyen versiones de imágenes de 640 px seleccionadas mediante srcset, fuentes locales con sus licencias OFL, robots.txt y sitemap.xml. Los efectos decorativos se pausan fuera de pantalla.
