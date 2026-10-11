# Ejercicio 2. AFND y AFND-λ en JFLAP

> **Borrador.** Las tablas se calcularon desde los archivos de `automatas/` con `python herramientas/generar_docs.py`, así que sus números coinciden con ellos. Los recuadros **«Tu parte»** marcan lo que debes redactar con tus palabras: la práctica no admite texto generado por modelos de lenguaje. Borra estas indicaciones antes de entregar.

## 2.0. Alcance y organización de los archivos

Se implementan los ejercicios con asterisco de la Lista 2 (94 a 150) y de la Lista 3 (151 a 263), más los ejercicios 196 a 200 de la Lista 3, que no llevan asterisco pero hacen falta para el apartado 2.3. Cada autómata se entrega en `.jff` (formato principal), `.json` y `.xml`; la convención para λ (cadena vacía como símbolo leído) está en el [README](../README.md).

| Carpeta de `automatas/` | Autómatas | Contenido |
|---|---|---|
| lista2-afd | 30 | AFD de los ejercicios con asterisco de la Lista 2 |
| lista3-afd | 26 | AFD de la Lista 3: simplificaciones, AFN deterministas (158–161, 262) y autómatas de 254–258 |
| lista3-afnd | 16 | AFN: 7 de la Lista 2, 189, 190, 192–195, 260, 261 y 263 |
| lista3-afnd-lambda | 5 | AFND-λ de 196–200 |
| conversiones | 27 | AFD resultantes de cada conversión (y los AFND sin λ intermedios) |

Para cada autómata, sus cadenas de prueba, sus recorridos y su tabla de transiciones están en [guia-jflap/](guia-jflap/README.md). La Lista 3 resuelta, con las figuras de ejecución, está en el documento de LaTeX que se entrega aparte.

## 2.1. Clasificación y cobertura

### Criterio

Todo lenguaje regular tiene un AFD, un AFND y un AFND-λ; por eso la clasificación no dice qué se *puede* construir, sino cuál es el **diseño natural**. Se aplicó el criterio del enunciado de los ejercicios 162 a 188 («busque que el diagrama del AFN sea más simple que el del AFD»):

| Sección | Cuándo se coloca ahí un ejercicio |
|---|---|
| **AFD** | El estado es un resumen determinista de lo leído (contadores, paridades, posición, un patrón que avanza, conjunción de dos condiciones), o el autómata ya viene dado como AFD. El AFN no mejora al AFD. |
| **AFND** | El lenguaje se define con un «existe» (existe una posición o una descomposición) y el AFN que *adivina* esa elección tiene menos estados o menos transiciones que el AFD, o el autómata viene dado con celdas de varios destinos. |
| **AFND-λ** | El autómata tiene transiciones λ. |

Cada resultado se midió: se diseñó el AFN candidato, se verificó contra la definición del lenguaje (todas las cadenas hasta una longitud dada, más cadenas largas al azar, y una comparación exacta con el AFD) y se contaron estados y transiciones.

### Lista 2 (ejercicios con asterisco)

En la Lista 2 todos los problemas piden un AFD, así que el AFD se entrega siempre en `lista2-afd/`. En los siete donde el AFN es más simple, el AFN se entrega además en `lista3-afnd/` (lo pide la Lista 3, ejercicios 162 a 188) y el AFD queda como su AFD equivalente.

| Ej. | Sección | Archivo(s) | Justificación |
|---|---|---|---|
| 97 | **AFD** | [Ej_097_longitud_multiplo_de_3.jff](../automatas/lista2-afd/Ej_097_longitud_multiplo_de_3.jff) | Contador módulo 3; no hay nada que adivinar y el AFN no mejora al AFD. |
| 99 | **AFND** | [Ej_099_afn_termina_en_001001.jff](../automatas/lista3-afnd/Ej_099_afn_termina_en_001001.jff) y [AFD](../automatas/lista2-afd/Ej_099_termina_en_001001.jff) | El AFN tiene 7 estados y 9 transiciones; el AFD, 7 y 21. La elección que se adivina simplifica el diagrama. El AFD de la Lista 2 es su AFD equivalente. |
| 102 | **AFND** | [Ej_102_afn_contiene_abbbab.jff](../automatas/lista3-afnd/Ej_102_afn_contiene_abbbab.jff) y [AFD](../automatas/lista2-afd/Ej_102_contiene_abbbab.jff) | El AFN tiene 7 estados y 10 transiciones; el AFD, 7 y 14. La elección que se adivina simplifica el diagrama. El AFD de la Lista 2 es su AFD equivalente. |
| 103 | **AFND** | [Ej_103_afn_contiene_aabbba.jff](../automatas/lista3-afnd/Ej_103_afn_contiene_aabbba.jff) y [AFD](../automatas/lista2-afd/Ej_103_contiene_aabbba.jff) | El AFN tiene 7 estados y 10 transiciones; el AFD, 7 y 14. La elección que se adivina simplifica el diagrama. El AFD de la Lista 2 es su AFD equivalente. |
| 106 | **AFND** | [Ej_106_afn_contiene_1101001.jff](../automatas/lista3-afnd/Ej_106_afn_contiene_1101001.jff) y [AFD](../automatas/lista2-afd/Ej_106_contiene_1101001.jff) | El AFN tiene 8 estados y 13 transiciones; el AFD, 8 y 24. La elección que se adivina simplifica el diagrama. El AFD de la Lista 2 es su AFD equivalente. |
| 107 | **AFD** | [Ej_107_contiene_0101_y_021.jff](../automatas/lista2-afd/Ej_107_contiene_0101_y_021.jff) | Conjunción de dos condiciones (producto de autómatas): el AFN, unión de los dos órdenes posibles, tiene 15 estados y el AFD 13. |
| 109 | **AFD** | [Ej_109_contiene_abbcb_y_cbaabb.jff](../automatas/lista2-afd/Ej_109_contiene_abbcb_y_cbaabb.jff) | Con traslape, el AFN necesita además las cadenas fundidas: 40 estados contra 22 del AFD. |
| 111 | **AFD** | [Ej_111_exactamente_3_veces_01002.jff](../automatas/lista2-afd/Ej_111_exactamente_3_veces_01002.jff) | «Exactamente tres» exige comprobar que no hay una cuarta aparición: es un contador, y un AFN no puede comprobar ausencias. |
| 112 | **AFD** | [Ej_112_dos_veces_010_sin_traslape.jff](../automatas/lista2-afd/Ej_112_dos_veces_010_sin_traslape.jff) | «Exactamente dos»: contador de apariciones (sin traslape). |
| 113 | **AFD** | [Ej_113_dos_veces_010_con_traslape.jff](../automatas/lista2-afd/Ej_113_dos_veces_010_con_traslape.jff) | «Exactamente dos»: contador de apariciones (con traslape). |
| 116 | **Ninguna** | — | No es regular (Myhill-Nerode): no existe autómata finito de ningún tipo. |
| 118 | **AFND** | [Ej_118_afn_forma_axabya.jff](../automatas/lista3-afnd/Ej_118_afn_forma_axabya.jff) y [AFD](../automatas/lista2-afd/Ej_118_forma_axabya.jff) | El AFN tiene 5 estados y 8 transiciones; el AFD, 6 y 12. La elección que se adivina simplifica el diagrama. El AFD de la Lista 2 es su AFD equivalente. |
| 120 | **AFND** | [Ej_120_afn_primer_y_ultimo_distintos.jff](../automatas/lista3-afnd/Ej_120_afn_primer_y_ultimo_distintos.jff) y [AFD](../automatas/lista2-afd/Ej_120_primer_y_ultimo_simbolo_distintos.jff) | El AFN tiene 5 estados y 18 transiciones; el AFD, 7 y 21. La elección que se adivina simplifica el diagrama. El AFD de la Lista 2 es su AFD equivalente. |
| 121 | **AFD** | [Ej_121_longitud_3n_y_contiene_un_0.jff](../automatas/lista2-afd/Ej_121_longitud_3n_y_contiene_un_0.jff) | Posición módulo 3 y una bandera; no hay elección que adivinar. |
| 122 | **AFD** | [Ej_122_toda_ventana_de_3_tiene_un_0.jff](../automatas/lista2-afd/Ej_122_toda_ventana_de_3_tiene_un_0.jff) | Ventana de memoria acotada de los últimos símbolos. |
| 123 | **AFND** | [Ej_123_afn_forma_wxw.jff](../automatas/lista3-afnd/Ej_123_afn_forma_wxw.jff) y [AFD](../automatas/lista2-afd/Ej_123_forma_wxw_con_w_de_longitud_2.jff) | El AFN tiene 12 estados y 22 transiciones; el AFD, 15 y 30. La elección que se adivina simplifica el diagrama. El AFD de la Lista 2 es su AFD equivalente. |
| 124 | **AFD** | [Ej_124_canicas_y_palancas.jff](../automatas/lista2-afd/Ej_124_canicas_y_palancas.jff) | Mecanismo físico determinista: el estado es la posición de las tres palancas y la última salida. |
| 125 | **AFD** | — | Teórico sobre un AFD genérico (complemento). |
| 126 | **AFD** | — | Teórico sobre un AFD genérico (F = ∅). |
| 127 | **AFD** | — | Teórico sobre un AFD genérico (F = Q). |
| 128 | **AFD** | [Ej_128_L2_sin_el_ultimo_simbolo.jff](../automatas/lista2-afd/Ej_128_L2_sin_el_ultimo_simbolo.jff) | Se conserva el AFD del diagrama y cambian los estados de aceptación. |
| 131 | **AFD** | [Ej_131_termina_en_1.jff](../automatas/lista2-afd/Ej_131_termina_en_1.jff) | AFD dado; el estado depende solo del último símbolo. |
| 133 | **AFD** | [Ej_133_diagrama_de_M.jff](../automatas/lista2-afd/Ej_133_diagrama_de_M.jff) | AFD dado por tabla de transiciones. |
| 135 | **AFD** | [Ej_135_b_m_a_b_n.jff](../automatas/lista2-afd/Ej_135_b_m_a_b_n.jff) | Fases secuenciales sin ambigüedad (bᵐ a bⁿ). |
| 137 | **AFD** | [Ej_137_empieza_con_ab.jff](../automatas/lista2-afd/Ej_137_empieza_con_ab.jff) | Prefijo fijo `ab`. |
| 139 | **AFD** | [Ej_139_numero_par_de_ceros.jff](../automatas/lista2-afd/Ej_139_numero_par_de_ceros.jff) | Paridad del número de ceros. |
| 141 | **AFD** | [Ej_141_cada_0_seguido_de_1.jff](../automatas/lista2-afd/Ej_141_cada_0_seguido_de_1.jff) | Se recuerda si el símbolo anterior fue un 0 pendiente de su 1. |
| 143 | **AFD** | [Ej_143a_todas_las_cadenas.jff](../automatas/lista2-afd/Ej_143a_todas_las_cadenas.jff) y [Ej_143b_empieza_y_termina_en_a_sin_bb.jff](../automatas/lista2-afd/Ej_143b_empieza_y_termina_en_a_sin_bb.jff) | Dos autómatas dados; el (b) es un AFD parcial. |
| 145 | **AFD** | [Ej_145_binario_der_a_izq_multiplo_de_5.jff](../automatas/lista2-afd/Ej_145_binario_der_a_izq_multiplo_de_5.jff) | Aritmética modular (módulo 5, leyendo de derecha a izquierda). |
| 147 | **AFD** | [Ej_147_binario_izq_a_der_multiplo_de_6.jff](../automatas/lista2-afd/Ej_147_binario_izq_a_der_multiplo_de_6.jff) | Residuo módulo 6 (4 estados tras minimizar). |
| 148 | **AFD** | [Ej_148_progreso_del_alumno.jff](../automatas/lista2-afd/Ej_148_progreso_del_alumno.jff) | Proceso determinista: cada evento lleva a un solo estado. |
| 149 | **AFD** | [Ej_149_tabla.jff](../automatas/lista2-afd/Ej_149_tabla.jff) | AFD dado por tabla; se piden valores de δ y δ̂. |
| 150 | **AFD** | [Ej_150_tabla.jff](../automatas/lista2-afd/Ej_150_tabla.jff) | AFD dado por tabla sobre {0, 1, a}; se piden valores de δ̂. |

### Lista 3 (ejercicios con asterisco, más 196 a 200)

| Ej. | Sección | Archivo(s) | Justificación |
|---|---|---|---|
| 151–157 | **AFD** | [Ej_151_original.jff](../automatas/lista3-afd/Ej_151_original.jff), [Ej_152_original.jff](../automatas/lista3-afd/Ej_152_original.jff) … | AFD dado por tabla (151–155) o figura (156–157), que se simplifica quitando estados inaccesibles y por partición. |
| 158–161 | **AFD** | [Ej_158_figura.jff](../automatas/lista3-afd/Ej_158_figura.jff), [Ej_159_figura.jff](../automatas/lista3-afd/Ej_159_figura.jff) … | El enunciado los llama AFN, pero ningún estado tiene dos transiciones con el mismo símbolo: son AFD parciales. |
| 162–188 (Lista 2) | **AFND** | [Ej_099_afn_termina_en_001001.jff](../automatas/lista3-afnd/Ej_099_afn_termina_en_001001.jff), [Ej_102_afn_contiene_abbbab.jff](../automatas/lista3-afnd/Ej_102_afn_contiene_abbbab.jff) … | Los siete AFN nuevos (99, 102, 103, 106, 118, 120, 123); en los demás se reutiliza el AFD, véase la Lista 2. |
| 189 | **AFND** | [Ej_189_afn_00101_o_00110.jff](../automatas/lista3-afnd/Ej_189_afn_00101_o_00110.jff) | Dos patrones que comparten el prefijo `001`; se adivina dónde empieza. |
| 190 | **AFND** | [Ej_190_afn_11010_y_10100.jff](../automatas/lista3-afnd/Ej_190_afn_11010_y_10100.jff) | Se adivina cuál patrón aparece primero; los patrones se traslapan en `1010` y en `10`. |
| 192–195 | **AFND** | [Ej_192_tabla.jff](../automatas/lista3-afnd/Ej_192_tabla.jff), [Ej_193_tabla.jff](../automatas/lista3-afnd/Ej_193_tabla.jff) … | AFN dado por tabla: hay celdas con varios destinos. |
| 196–200 | **AFND-λ** | [Ej_196_tabla.jff](../automatas/lista3-afnd-lambda/Ej_196_tabla.jff), [Ej_197_tabla.jff](../automatas/lista3-afnd-lambda/Ej_197_tabla.jff) … | Tabla con columna λ. Opcionales en la lista, pero necesarios para el apartado 2.3. |
| 254–258 | **AFD** | [Ej_254_tabla.jff](../automatas/lista3-afd/Ej_254_tabla.jff), [Ej_255_tabla.jff](../automatas/lista3-afd/Ej_255_tabla.jff) … | AFD dado por tabla; se pide su expresión regular. |
| 260 | **AFND** | [Ej_260_tabla.jff](../automatas/lista3-afnd/Ej_260_tabla.jff) | AFN dado por tabla. |
| 261 | **AFND** | [Ej_261_figura.jff](../automatas/lista3-afnd/Ej_261_figura.jff) | AFN dado por figura: `q0` va a `q0` y a `q1` con 0. |
| 262 | **AFD** | [Ej_262_ab_ba.jff](../automatas/lista3-afd/Ej_262_ab_ba.jff) | El enunciado pide un AFN para {ab, ba}; el diseño resulta determinista (AFD parcial), y la conversión solo agrega el estado ∅. |
| 263 | **AFND** | [Ej_263_figura.jff](../automatas/lista3-afnd/Ej_263_figura.jff) | AFN dado por figura: `q0` va a `q0` y a `q1` con 0. |

> **Tu parte:** el enunciado dice que la clasificación se evalúa. Revisa cada justificación y reescríbela con tus palabras; si el profesor espera otra clasificación para algún ejercicio, cámbialo aquí y mueve el archivo.

## 2.2. Diseño y validación

### Cómo se diseñó y se probó cada autómata

Para cada autómata se documenta: la idea de diseño, la tabla de transiciones, **cinco cadenas válidas y cinco inválidas** de distinta longitud con el resultado esperado, y el recorrido completo (los estados activos tras cada símbolo y, en los no deterministas, el número de caminos de cómputo y cuántos aceptan). Todo eso está en [guia-jflap/](guia-jflap/README.md). Donde el lenguaje tiene pocas cadenas válidas (el 158 solo acepta `01`; el 262 solo `ab` y `ba`) se dan las que existen.

La validación no depende de unos cuantos ejemplos:

- Cada autómata construido a partir de un enunciado en palabras se compara con un predicado independiente para **todas las cadenas hasta una longitud dada** (de 7 a 15 símbolos según el alfabeto) y con miles de cadenas largas al azar (`tests/test_lista2.py`, `tests/test_lista3.py`).
- Los AFN de la Lista 3 se comparan con el AFD de la Lista 2 con una comparación **exacta** (`cadena_distintiva`, que recorre a la vez los conjuntos de estados de los dos autómatas).
- Cada conversión se comprueba contra su AFN de origen.
- `python herramientas/verificar_entregas.py` revisa cualquier `.jff` dibujado a mano contra su definición y da la cadena más corta que los distingue.

### Corrección de siete autómatas de la Práctica 1

Al cargar con el lector nuevo los `.jff` de la Práctica 1 y probarlos con una longitud mayor a la de entonces (8 símbolos), siete no reconocían el lenguaje del enunciado. Se regeneraron; los otros 14 se conservan tal cual. En el 128, además, la transcripción del diagrama estaba mal (el diagrama tiene δ(D, 1) = E y δ(F, 0) = δ(F, 1) = D).

| Ej. (Lista 2) | Qué fallaba en el `.jff` de la Práctica 1 |
|---|---|
| 99 | Tenía una transición no determinista (`q5` con `1` iba a `q0` y a `q6`): no era un AFD y rechazaba `00101001001`. |
| 103 | No cubría el traslape del patrón: rechazaba `aabaabbba`. |
| 107 | Transición no determinista en `q3` con `1`: rechazaba `020101021`. |
| 109 | Fallaba desde longitud 9: rechazaba `abbcbaabb` y `abbcbcbaabb`. |
| 118 | Aceptaba cadenas que no son del lenguaje, como `aab`. |
| 121 | Tenía como final el estado trampa `q5` en lugar de `q0`. |
| 133 | Faltaba la transición δ(q2, b) = q3 que da el enunciado. |

### Simulación paso a paso en JFLAP

> **Tu parte:** el apartado 2.2 pide evidenciar el comportamiento con **la simulación paso a paso de JFLAP**. Abre los `.jff` en JFLAP (*Input → Step…*) y guarda las capturas en `evidencias/jflap/`. Como mínimo, una válida y una inválida de: un AFD, un AFND (por ejemplo el 99 o el 190, que muestran las bifurcaciones) y un AFND-λ (por ejemplo el 196). Enlázalas aquí con una línea que diga qué se ve en cada una.

## 2.3. Transiciones λ

Los cinco AFND-λ del enunciado (196 a 200) tienen las transiciones λ que se muestran; su ubicación viene dada en cada tabla.

| Ej. | Estados | Transiciones λ | Cuáles |
|---|---|---|---|
| 196 | 3 | 1 | A –λ→ B |
| 197 | 4 | 3 | A –λ→ C, B –λ→ D, C –λ→ B |
| 198 | 4 | 2 | A –λ→ C, C –λ→ B |
| 199 | 5 | 3 | A –λ→ B, A –λ→ C, C –λ→ E |
| 200 | 6 | 5 | A –λ→ B, C –λ→ E, D –λ→ E, D –λ→ F, F –λ→ E |

La λ-clausura de un estado `q`, Cl(q), es el conjunto de estados alcanzables desde `q` usando solo transiciones λ, incluido `q`. Para un conjunto, es la unión de las clausuras de sus estados.

| Ej. | Estado | Cl(estado) |
|---|---|---|
| 196 | A | {A, B} |
| 196 | B | {B} |
| 196 | C | {C} |
| 197 | A | {A, B, C, D} |
| 197 | B | {B, D} |
| 197 | C | {B, C, D} |
| 197 | D | {D} |
| 198 | A | {A, B, C} |
| 198 | B | {B} |
| 198 | C | {B, C} |
| 198 | D | {D} |
| 199 | A | {A, B, C, E} |
| 199 | B | {B} |
| 199 | C | {C, E} |
| 199 | D | {D} |
| 199 | E | {E} |
| 200 | A | {A, B} |
| 200 | B | {B} |
| 200 | C | {C, E} |
| 200 | D | {D, E, F} |
| 200 | E | {E} |
| 200 | F | {E, F} |

**Su papel en el reconocimiento.** El autómata no consume ningún símbolo al seguir una transición λ, así que, al empezar y después de leer cada símbolo, hay que añadir al conjunto de estados activos todo lo que se alcanza por λ. Formalmente, δ̂(Z, ε) = Cl(Z) y δ̂(Z, wa) = Cl(⋃ δ(q, a) para q en δ̂(Z, w)). Una cadena se acepta si δ̂({q₀}, w) contiene un estado de aceptación. Por eso la cadena vacía se acepta si y solo si Cl({q₀}) contiene uno, y por eso quitar las transiciones λ (δ'(q, a) = Cl(δ(Cl({q}), a)), con q de aceptación si Cl({q}) contiene un estado de aceptación) no cambia el lenguaje.

> **Tu parte:** el enunciado pide «justificar la necesidad de las transiciones λ y su ubicación» en cada AFND-λ. En estos cinco las λ vienen dadas; explica con tus palabras, para al menos uno (el 196 es el más sencillo), qué cadena dejaría de aceptarse si se quitara una transición λ concreta. El simulador permite comprobarlo: carga `Ej_196_tabla.jff`, simula `01` y observa en el paso inicial que la λ-clausura de `A` es {A, B}.

## 2.4. Conversiones y análisis comparativo

### Procedimiento

En JFLAP, un AFND estándar se convierte con *Convert → Convert to DFA* (se puede ver paso a paso con *Complete*). Un AFND-λ se convierte **primero a un AFND estándar** (se quitan las transiciones λ) **y después a un AFD**. Los AFD resultantes están en `automatas/conversiones/`; JFLAP nombra los estados del AFD con los conjuntos y no agrega el estado ∅, por lo que su resultado puede quedar incompleto. La construcción de subconjuntos, paso a paso, de cada ejercicio está en [guia-jflap/03-afn-a-afd.md](guia-jflap/03-afn-a-afd.md) y [04-afnd-lambda.md](guia-jflap/04-afnd-lambda.md).

> **Tu parte:** convierte en JFLAP al menos los casos de la tabla de abajo que presentes y guarda las capturas de la conversión en `evidencias/jflap/`.

### Tabla de conversiones

| Ejercicio | AFN (o AFND-λ): estados / transiciones | AFD: estados / transiciones | AFD mínimo | Cota 2ⁿ | AFD / AFN |
|---|---|---|---|---|---|
| 099 | 7 / 9 | 7 / 21 | 7 | 128 | 1.0× |
| 102 | 7 / 10 | 12 / 24 | 7 | 128 | 1.7× |
| 103 | 7 / 10 | 12 / 24 | 7 | 128 | 1.7× |
| 106 | 8 / 13 | 14 / 42 | 8 | 256 | 1.8× |
| 118 | 5 / 8 | 5 / 9 | 5 | 32 | 1.0× |
| 120 | 5 / 18 | 7 / 21 | 7 | 32 | 1.4× |
| 123 | 12 / 22 | 15 / 30 | 15 | 4,096 | 1.2× |
| 189 | 8 / 13 | 24 / 48 | 7 | 256 | 3.0× |
| 190 | 21 / 32 | 48 / 96 | 19 | 2,097,152 | 2.3× |
| 192 | 3 / 7 | 5 / 8 | 5 | 8 | 1.7× |
| 193 | 4 / 12 | 7 / 13 | 6 | 16 | 1.8× |
| 194 | 4 / 13 | 4 / 12 | 2 | 16 | 1.0× |
| 195 | 5 / 12 | 12 / 24 | 7 | 32 | 2.4× |
| 260 | 5 / 15 | 7 / 13 | 6 | 32 | 1.4× |
| 261 | 5 / 6 | 5 / 10 | 3 | 32 | 1.0× |
| 262 | 4 / 4 | 5 / 10 | 5 | 16 | 1.2× |
| 263 | 3 / 4 | 3 / 6 | 3 | 8 | 1.0× |
| 196 (λ → AFND → AFD) | 3 / 5 | 3 / 4 | 2 | 8 | 1.0× |
| 197 (λ → AFND → AFD) | 4 / 11 | 2 / 4 | 1 | 16 | 0.5× |
| 198 (λ → AFND → AFD) | 4 / 7 | 3 / 6 | 2 | 16 | 0.8× |
| 199 (λ → AFND → AFD) | 5 / 10 | 4 / 6 | 2 | 32 | 0.8× |
| 200 (λ → AFND → AFD) | 6 / 22 | 6 / 12 | 2 | 64 | 1.0× |

El AFD es el que produce la construcción de subconjuntos (solo los conjuntos alcanzables), no el mínimo; la columna «AFD mínimo» muestra cuánto se podría reducir. La conversión del 262 agrega el estado ∅, porque el AFN ya era determinista.

### Comparación

**Número de estados.** En las 22 conversiones el AFD tiene como máximo 3,0 veces los estados del AFN (el 189, de 8 a 24), y en ninguna se acerca a la cota 2ⁿ: el caso más grande, el 190, pasa de 21 a 48 estados, contra 2 097 152. En los ejercicios 099, 118, 194, 261, 263, 196, 200 el AFD tiene tantos estados como el AFN (o AFND).

**Complejidad de las transiciones.** Un AFD completo tiene |Σ| transiciones por estado; un AFN solo dibuja las que existen. Por eso los AFN de patrones tienen menos transiciones aunque no tengan menos estados (el 99: 9 contra 21).

**Facilidad de diseño e interpretación.**

> **Tu parte:** compara, con tu experiencia al dibujar los autómatas, la facilidad de diseñar y de leer cada tipo. Los datos objetivos: para «termina en `001001`» el AFN se obtiene por simple observación del sufijo (se adivina dónde empieza), mientras que el AFD exige llevar la cuenta de cuánto del patrón ya se emparejó.

**Eficiencia en el reconocimiento.** Simular un AFN siguiendo todos los caminos cuesta O(|w|·|δ|) en tiempo y O(|Q|) en espacio; con el AFD ya construido, O(|w|) con un solo estado activo. En las cadenas de prueba de los AFN de la Lista 3 hay entre 1,0 y 4,0 estados activos en promedio y entre 0,7 y 5,5 transiciones evaluadas por símbolo (frente a una en el AFD); el detalle está en [03-simulador.md](03-simulador.md#medición-del-costo).

### Por qué la cota 2ⁿ rara vez se alcanza

Cada estado del AFD es un subconjunto de estados del AFN que se alcanza desde el inicial por alguna cadena; solo se crean esos. La estructura de un AFN suele limitar qué subconjuntos pueden coincidir. En los AFN de patrones (99, 102, 103 y 106), los estados activos quedan determinados por el prefijo más largo del patrón que coincide con el final de lo leído (los demás prefijos que coinciden son sus bordes), así que el número de subconjuntos crece con la longitud del patrón y no como 2ⁿ: en el 102, 7 estados dan 12 subconjuntos, no 128. Además, estados distintos del AFD pueden ser equivalentes (por eso el AFD mínimo es todavía menor).

### Una familia en la que sí se alcanza

Hopcroft, Motwani y Ullman presentan el lenguaje de las cadenas sobre {0, 1} cuyo n-ésimo símbolo desde el final es 1: tiene un AFN de n + 1 estados y todo AFD que lo reconozca necesita al menos 2ⁿ estados (Hopcroft et al., 2007, sección 2.3.6; verifica el número de sección y de página en tu ejemplar). Se comprobó con el simulador: el AFN construido para n = 1 a 6 da, por subconjuntos, un AFD cuyo mínimo tiene exactamente 2ⁿ estados (`tests/test_automata.py`, `test_la_cota_2_a_la_n_se_alcanza_en_el_n_esimo_simbolo_desde_el_final`), y para n = 4, 8 y 12 el AFD mide 16, 256 y 4 096 estados (véase [03-simulador.md](03-simulador.md#medición-del-costo)).

> **Tu parte:** explica con tus palabras por qué, en esa familia, los 2ⁿ estados hacen falta (pista: para distinguir dos cadenas de longitud n que difieran en un símbolo, basta añadirles un sufijo de la longitud adecuada). Cita el libro con su ISBN en [bibliografia.md](bibliografia.md).

## Referencias

Hopcroft, J. E., Motwani, R. y Ullman, J. D. (2007). *Teoría de autómatas, lenguajes y computación* (3.ª ed.). Pearson Educación. ISBN: *(cópialo de la página legal de tu ejemplar)*.

Rodger, S. H. y Finley, T. W. (2006). *JFLAP: An interactive formal languages and automata package*. Jones & Bartlett.
