# Manual de diseño GLIX

Este documento define las reglas visuales de la home y las páginas de módulos. Las reglas ejecutables están en `design-system.css`, cargado al final de cada página para que tengan prioridad sobre los estilos anteriores.

## 1. Grilla y aire

- Todo contenido principal vive dentro de `.wrap`. Ancho máximo: **1320 px**. Margen lateral: `clamp(24px, 5vw, 88px)` por lado; **20 px** en pantallas de hasta 760 px.
- Las franjas `.section-cta` son hijas directas de la sección y usan exactamente el mismo ancho que `.wrap`. Sus textos y botones nunca llegan al borde de la ventana.
- Las secciones principales usan `--section-space`: de **76 a 112 px** arriba y abajo en escritorio, **72 px** en móvil. La CTA se separa del contenido anterior entre **48 y 72 px** y comienza con una línea y **28 px** de espacio superior.
- Grillas de tarjetas: separación de **20 a 32 px** en escritorio y **16 px** en móvil. Evitar que imágenes, tarjetas o botones se toquen entre sí.
- El texto de una CTA ocupa un ancho razonable; el botón se alinea a la derecha dentro de la misma grilla. En móvil se apilan y el botón ocupa el ancho disponible.

## 2. Tipografía

- Títulos y botones: **Manrope**, usando pesos fuertes para jerarquía y pesos regulares en palabras de contraste.
- Párrafos: **Roboto Light 300, 15 px, negro `#000`**, con interlineado de 1,65. El fondo de las secciones con párrafos debe ser claro para conservar legibilidad.
- Los títulos pueden animarse al entrar en pantalla, pero la lectura y el orden visual tienen prioridad. Respetar `prefers-reduced-motion`.

## 3. Paleta

Los cuatro colores de marca se toman del logo y están definidos en `styles.css`:

| Color | Variable | Valor |
| --- | --- | --- |
| Verde | `--green` | `#10be08` |
| Violeta | `--purple` | `#a64c9e` |
| Azul | `--blue` | `#4779b9` |
| Naranja | `--orange` | `#ffa10b` |

El sitio conserva el blanco y los fondos claros como base. Los colores se usan en detalles, indicadores y acciones.

## 4. Botones y llamadas a la acción

- Todos los enlaces principales a WhatsApp usan `.tic-button`: forma de píldora, fondo degradado entre un color de marca y su tono oscuro, **texto blanco** y triángulo blanco hacia la derecha. El movimiento del degradado y del brillo es sutil y continuo.
- Al pasar el cursor, el fondo cambia a **otro** color de la paleta con su tono oscuro; la separación entre letras pasa de **0 a 1 px**.
- La combinación de colores depende de la sección. En las cuatro tarjetas de módulos se asigna exactamente un color distinto a cada botón: violeta, azul, naranja y verde. Las páginas internas alternan los colores en sus secciones.
- Cada CTA tiene un título que explica por qué contactar y un botón con verbo específico de **una o dos palabras**. Mantener el destino de WhatsApp existente y un mensaje contextual.
- Los botones conservan un foco visible para navegación con teclado.

## 5. Imágenes y componentes

- La portada muestra `assets/gallery/compu.png`, con proporción original, sin recortes ni deformación.
- Las capturas de los módulos se mantienen dentro de su tarjeta y con espacio respecto del texto.
- Una nueva sección debe reutilizar `.wrap`, el espaciado de sección y, si incluye contacto, el patrón `.section-cta`.
- Una nueva landing debe cargar `design-system.css` **después** de `styles.css`, `enhancements.css` y `modulos.css` cuando corresponda.

## 6. Revisión antes de publicar

Comprobar en escritorio y móvil: que ningún contenido toque los bordes; que todas las CTA se alineen a la grilla; que los botones tengan texto blanco, triángulo derecho, colores distintos, brillo y cambio de color con 1 px de espaciado entre letras al hover; que los párrafos se lean en negro sobre fondo claro; que no haya desplazamiento horizontal; y que imágenes y enlaces carguen en GitHub Pages bajo `/glix/`.
