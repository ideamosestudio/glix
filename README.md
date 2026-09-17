# GLIX — sitio web corporativo

Sitio estático en HTML, CSS y JavaScript. No requiere instalación, compilación ni variables de entorno. Incluye la portada y cuatro páginas de módulos: Transporte y liquidación, Compras y proveedores, Recursos Humanos y App móvil de ventas. El contenido comercial se basa en `Glix - Presentacion General.pptx`; la información de contacto fue proporcionada para este sitio.

La grilla, los márgenes, el ritmo vertical, la tipografía y los botones se documentan en [`MANUAL-DISENO.md`](MANUAL-DISENO.md) y se aplican desde `design-system.css`.

Las capturas de `assets/gallery/` se basan en imágenes de la presentación. Se reemplazaron los datos visibles por ejemplos inventados y se identifican como **Datos de muestra**. Todos los botones de contacto y el acceso flotante usan WhatsApp `5491161978997`.

La portada usa `assets/gallery/compu.png` tal como fue provista. La cabecera y el pie usan el símbolo de `assets/brand/glix-blanco.png`; ese archivo tiene un lienzo blanco amplio y el logo está recortado en su borde derecho.

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
