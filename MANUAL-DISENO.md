# Manual de diseÃ±o GLIX

Este documento define las reglas visuales de la home y las pÃ¡ginas de mÃ³dulos. Las reglas ejecutables estÃ¡n en `design-system.css`, cargado al final de cada pÃ¡gina para que tengan prioridad sobre los estilos anteriores.

## 1. Grilla y aire

- En mÃ³vil (hasta **760 px**), los tÃ­tulos, pÃ¡rrafos, etiquetas y llamadas a la acciÃ³n se centran dentro de un ancho del **80%** de la pantalla: **10%** libre a cada lado. Las imÃ¡genes conservan las proporciones y tamaÃ±os de cada componente; no se fuerzan al ancho de la pantalla.
- Si una secciÃ³n muestra dos botones en escritorio, en mÃ³vil aparece **solo el primero**. El segundo se oculta sin alterar la versiÃ³n de escritorio.
- Todo contenido principal vive dentro de `.wrap`. Ancho mÃ¡ximo: **1320 px**. Margen lateral: `clamp(24px, 5vw, 88px)` por lado en escritorio; **10%** a cada lado en mÃ³vil.
- Las franjas `.section-cta` son hijas directas de la secciÃ³n y usan exactamente el mismo ancho que `.wrap`. Sus textos y botones nunca llegan al borde de la ventana.
- Las secciones principales usan `--section-space`: de **76 a 112 px** arriba y abajo en escritorio, **72 px** en mÃ³vil. La CTA se separa del contenido anterior entre **48 y 72 px** y comienza con una lÃ­nea y **28 px** de espacio superior.
- Grillas de tarjetas: separaciÃ³n de **20 a 32 px** en escritorio y **16 px** en mÃ³vil. Evitar que imÃ¡genes, tarjetas o botones se toquen entre sÃ­.
- El texto de una CTA ocupa un ancho razonable; el botÃ³n se alinea a la derecha dentro de la misma grilla en escritorio. En mÃ³vil se apilan y ambos quedan centrados.

## 2. TipografÃ­a

- TÃ­tulos y botones: **Manrope**, usando pesos fuertes para jerarquÃ­a y pesos regulares en palabras de contraste.
- El tÃ­tulo de la portada de la home usa `clamp(45px, 5.5vw, 80px)` en desktop (desde 761 px de ancho). Este rango no modifica las portadas internas ni el tamaÃ±o mÃ³vil.
- En ese tÃ­tulo, solo Â«gestionar tu empresaÂ» usa Manrope 800; Â«Una forma mÃ¡s clara deÂ» usa Manrope 400.
- PÃ¡rrafos: **Roboto Light 300, 15 px, negro `#000`**, con interlineado de 1,65. El fondo de las secciones con pÃ¡rrafos debe ser claro para conservar legibilidad.
- Los tÃ­tulos pueden animarse al entrar en pantalla, pero la lectura y el orden visual tienen prioridad. Respetar `prefers-reduced-motion`.
- En los encabezados de secciÃ³n con bajada, el orden es **eyebrow, tÃ­tulo y pÃ¡rrafo debajo del tÃ­tulo**, alineados al mismo margen izquierdo. El tÃ­tulo puede ocupar el ancho disponible de la grilla; la bajada se limita a **680 px** para facilitar la lectura y se separa **24 px** del tÃ­tulo. Las tarjetas o bloques de contenido comienzan debajo de todo el encabezado. Esta regla se aplica en la home y en todas las pÃ¡ginas internas; no se reparte el tÃ­tulo y el pÃ¡rrafo en columnas opuestas.

## 3. Paleta

Los cuatro colores de marca se toman del logo y estÃ¡n definidos en `styles.css`:

| Color | Variable | Valor |
| --- | --- | --- |
| Verde | `--green` | `#10be08` |
| Violeta | `--purple` | `#a64c9e` |
| Azul | `--blue` | `#4779b9` |
| Naranja | `--orange` | `#ffa10b` |

El sitio conserva el blanco y los fondos claros como base. Los colores se usan en detalles, indicadores y acciones.

## 4. Botones y llamadas a la acciÃ³n

- Todos los enlaces principales a WhatsApp usan `.tic-button`: forma de pÃ­ldora, fondo degradado entre un color de marca y su tono oscuro, **texto blanco** y triÃ¡ngulo blanco hacia la derecha. El movimiento del degradado y del brillo es sutil y continuo.
- Al pasar el cursor, el fondo cambia a **otro** color de la paleta con su tono oscuro; la separaciÃ³n entre letras pasa de **0 a 1 px**.
- La combinaciÃ³n de colores depende de la secciÃ³n. En las cuatro tarjetas de mÃ³dulos se asigna exactamente un color distinto a cada botÃ³n: violeta, azul, naranja y verde. Las pÃ¡ginas internas alternan los colores en sus secciones.
- Cada CTA tiene un tÃ­tulo que explica por quÃ© contactar y un botÃ³n con verbo especÃ­fico de **una o dos palabras**. Mantener el destino de WhatsApp existente y un mensaje contextual.
- Los botones conservan un foco visible para navegaciÃ³n con teclado.
- En secciones con dos acciones, se agrupan en `.feature-actions`: mantienen **14 px** de separaciÃ³n y colores de marca distintos. Si falta ancho, pasan a otra lÃ­nea sin tocar los bordes.

## 5. ImÃ¡genes y componentes

- La portada muestra tres cuadros de computadora (`compu-001.webp` a `compu-003.webp`) y la secciÃ³n de ventas dos cuadros de telÃ©fono (`phone-001.webp` y `phone-002.webp`). Cada secuencia cambia la imagen cada **2 segundos**, sin fundidos, conservando la misma proporciÃ³n y posiciÃ³n de la carcasa. Con movimiento reducido se conserva el primer cuadro.
- La soluciÃ³n usa una composiciÃ³n de dos mitades en escritorio: copy sobre gris suave a la izquierda y una secuencia continua de cuatro imÃ¡genes (`solution-01.webp` a `solution-04.webp`) a sangre a la derecha. Cambia cada **1,5 segundos**, sin fundidos. El tÃ­tulo combina el peso bold existente con el light existente. La secciÃ³n de contacto usa `formulario-bg.webp` con texto blanco.
- Las capturas de los mÃ³dulos se mantienen dentro de su tarjeta y con espacio respecto del texto.
- Las introducciones de las cuatro pÃ¡ginas internas usan dos mitades en escritorio: eyebrow, tÃ­tulo, bajada y dos acciones a la izquierda; imagen centrada a la derecha con espacio lateral. En pantallas pequeÃ±as se apilan texto e imagen. No se duplica la misma imagen a ancho completo debajo de esa composiciÃ³n.
- Una nueva secciÃ³n debe reutilizar `.wrap`, el espaciado de secciÃ³n y, si incluye contacto, el patrÃ³n `.section-cta`.
- Una nueva landing debe cargar `design-system.css` **despuÃ©s** de `styles.css`, `enhancements.css` y `modulos.css` cuando corresponda.

## 6. RevisiÃ³n antes de publicar

Comprobar en escritorio y mÃ³vil: que ningÃºn contenido toque los bordes; que todas las CTA se alineen a la grilla; que los botones tengan texto blanco, triÃ¡ngulo derecho, colores distintos, brillo y cambio de color con 1 px de espaciado entre letras al hover; que los pÃ¡rrafos se lean en negro sobre fondo claro; que no haya desplazamiento horizontal; y que imÃ¡genes y enlaces carguen en GitHub Pages bajo `/glix/`.
