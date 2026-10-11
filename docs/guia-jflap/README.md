# Guía para hacer en JFLAP los autómatas de la Lista 3

Cada guía da, por autómata: la tabla de transiciones, cadenas de prueba válidas e inválidas con el resultado esperado y el recorrido (los estados activos tras cada símbolo, para comparar con la simulación paso a paso de JFLAP), y, en las conversiones, los pasos y los tamaños.

| Guía | Ejercicios |
|---|---|
| [01-simplificacion.md](01-simplificacion.md) | 151 a 157 (simplificar AFD), 158 a 161 (qué hace cada autómata) |
| [02-afn-lista2-y-189-190.md](02-afn-lista2-y-189-190.md) | 162 a 188 (AFN de la Lista 2), 189 y 190 |
| [03-afn-a-afd.md](03-afn-a-afd.md) | 191 a 195 y 260 a 263 (AFN a AFD) |
| [04-afnd-lambda.md](04-afnd-lambda.md) | 196 a 200 (AFND-λ, opcionales) |
| [05-expresiones-regulares.md](05-expresiones-regulares.md) | 254 a 258 (autómata a expresión regular) |

## Cómo trabajar cada autómata

1. En JFLAP: *File → New → Finite Automaton*. Crea los estados con la herramienta de estados; marca el inicial y los de aceptación con clic derecho. Usa **el mismo nombre de estado** que la tabla (clic derecho → *Set Name*).
2. Prueba las cadenas: *Input → Step…* (paso a paso, muestra las ramas del no determinismo) y *Input → Multiple Run* (todas las cadenas de la tabla de una vez).
3. Guarda como `automatas/<carpeta>/<nombre>.jff` con el nombre exacto que dice la guía.
4. Para generar su `.json` y `.xml`, y comprobar que tu dibujo reconoce el lenguaje correcto, ejecuta `python herramientas/verificar_entregas.py --formatos`.

Los `.jff` de esas carpetas **ya existen**, generados desde las tablas: puedes abrirlos en JFLAP para simular y hacer las capturas, o dibujar los tuyos y guardarlos con el mismo nombre (no se pisan).

## Resumen de conversiones (para la tabla del apartado 2.4)

Estados del AFN, del AFD que produce la construcción de subconjuntos, del AFD mínimo, y la cota 2ⁿ.

| Ejercicio | Autómata | Estados AFN | Estados AFD | AFD mínimo | Cota 2ⁿ |
|---|---|---|---|---|---|
| 099 | termina en 001001 (Lista 2) | 7 | 7 | 7 | 128 |
| 102 | contiene abbbab (Lista 2) | 7 | 12 | 7 | 128 |
| 103 | contiene aabbba (Lista 2) | 7 | 12 | 7 | 128 |
| 106 | contiene 1101001 (Lista 2) | 8 | 14 | 8 | 256 |
| 118 | forma axabya (Lista 2) | 5 | 5 | 5 | 32 |
| 120 | primer y último símbolo distintos (Lista 2) | 5 | 7 | 7 | 32 |
| 123 | forma wxw (Lista 2) | 12 | 15 | 15 | 4,096 |
| 189 | contiene 00101 o 00110 | 8 | 24 | 7 | 256 |
| 190 | contiene 11010 y 10100 | 21 | 48 | 19 | 2,097,152 |
| 192 | tabla del enunciado | 3 | 5 | 5 | 8 |
| 193 | tabla del enunciado | 4 | 7 | 6 | 16 |
| 194 | tabla del enunciado | 4 | 4 | 2 | 16 |
| 195 | tabla del enunciado | 5 | 12 | 7 | 32 |
| 260 | tabla del enunciado | 5 | 7 | 6 | 32 |
| 261 | figura: termina en 00 | 5 | 5 | 3 | 32 |
| 262 | {ab, ba} | 4 | 5 | 5 | 16 |
| 263 | figura: termina en 01 | 3 | 3 | 3 | 8 |
| 196 (λ) | AFND-λ de 3 estados | 3 | 3 | 2 | 8 |
| 197 (λ) | AFND-λ de 4 estados | 4 | 2 | 1 | 16 |
| 198 (λ) | AFND-λ de 4 estados | 4 | 3 | 2 | 16 |
| 199 (λ) | AFND-λ de 5 estados | 5 | 4 | 2 | 32 |
| 200 (λ) | AFND-λ de 6 estados | 6 | 6 | 2 | 64 |

En ningún caso la cota se alcanza. La familia de la bibliografía en la que sí se alcanza (el n-ésimo símbolo desde el final es 1) está comprobada en `tests/test_automata.py` para n = 1 a 6.

