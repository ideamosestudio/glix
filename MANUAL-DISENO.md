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
- El título de la portada de la home usa `clamp(45px, 5.5vw, 80px)` en desktop (desde 761 px de ancho). Este rango no modifica las portadas internas ni el tamaño móvil.
- En ese título, solo «gestionar tu empresa» usa Manrope 800; «Una forma más clara de» usa Manrope 400.
- Párrafos: **Roboto Light 300, 15 px, negro `#000`**, con interlineado de 1,65. El fondo de las secciones con párrafos debe ser claro para conservar legibilidad.
- Los títulos pueden animarse al entrar en pantalla, pero la lectura y el orden visual tienen prioridad. Respetar `prefers-reduced-motion`.
- En los encabezados de sección con bajada, el orden es **eyebrow, título y párrafo debajo del título**, alineados al mismo margen izquierdo. El título puede ocupar el ancho disponible de la grilla; la bajada se limita a **680 px** para facilitar la lectura y se separa **24 px** del título. Las tarjetas o bloques de contenido comienzan debajo de todo el encabezado. Esta regla se aplica en la home y en todas las páginas internas; no se reparte el título y el párrafo en columnas opuestas.

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
- En secciones con dos acciones, se agrupan en `.feature-actions`: mantienen **14 px** de separación y colores de marca distintos. Si falta ancho, pasan a otra línea sin tocar los bordes.

## 5. Imágenes y componentes

- La portada muestra tres cuadros de computadora (`compu-001.png` a `compu-003.png`) y la sección de ventas dos cuadros de teléfono (`phone-001.png` y `phone-002.png`). Cada secuencia cambia la imagen cada **2 segundos**, sin fundidos, conservando la misma proporción y posición de la carcasa. Con movimiento reducido se conserva el primer cuadro.
- La solución usa una composición de dos mitades en escritorio: copy sobre gris suave a la izquierda y una secuencia continua de cuatro imágenes (`solution-01.png` a `solution-04.png`) a sangre a la derecha. Cambia cada **1,5 segundos**, sin fundidos. El título combina el peso bold existente con el light existente. La sección de contacto usa `formulario-bg.jpg` con texto blanco.
- Las capturas de los módulos se mantienen dentro de su tarjeta y con espacio respecto del texto.
- Las introducciones de las cuatro páginas internas usan dos mitades en escritorio: eyebrow, título, bajada y dos acciones a la izquierda; imagen centrada a la derecha con espacio lateral. En pantallas pequeñas se apilan texto e imagen. No se duplica la misma imagen a ancho completo debajo de esa composición.
- Una nueva sección debe reutilizar `.wrap`, el espaciado de sección y, si incluye contacto, el patrón `.section-cta`.
- Una nueva landing debe cargar `design-system.css` **después** de `styles.css`, `enhancements.css` y `modulos.css` cuando corresponda.

## 6. Revisión antes de publicar

Comprobar en escritorio y móvil: que ningún contenido toque los bordes; que todas las CTA se alineen a la grilla; que los botones tengan texto blanco, triángulo derecho, colores distintos, brillo y cambio de color con 1 px de espaciado entre letras al hover; que los párrafos se lean en negro sobre fondo claro; que no haya desplazamiento horizontal; y que imágenes y enlaces carguen en GitHub Pages bajo `/glix/`.
