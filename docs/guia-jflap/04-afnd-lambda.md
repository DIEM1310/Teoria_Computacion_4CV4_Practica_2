# Guía 4: AFND-λ (196 a 200)

Estos ejercicios no tienen asterisco, pero el apartado 2.3 de la práctica pide la λ-clausura de cada estado de cada AFND-λ y la conversión AFND-λ → AFND → AFD, y sin ellos esa parte quedaría vacía. En JFLAP, la transición λ se escribe dejando vacío el campo de la etiqueta (JFLAP muestra λ).

## Ejercicio 196

Archivo(s): `automatas/lista3-afnd-lambda/Ej_196_tabla.jff`, `automatas/conversiones/Ej_196_afnd.jff`, `automatas/conversiones/Ej_196_afd.jff`

**AFND-λ** — AFND-lambda · 3 estados · 5 transiciones

| Estado | λ | 0 | 1 |
|---|---|---|---|
| `→ A` | B | A | ∅ |
| `B` | ∅ | A, B | C |
| `* C` | ∅ | ∅ | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**λ-clausura de cada estado**

| Estado | Cl(estado) |
|---|---|
| `A` | {A, B} |
| `B` | {B} |
| `C` | {C} |

**Preguntas del ejercicio**

| Inciso | Pregunta | Respuesta |
|---|---|---|
| a | δ̂({A}, 110) | ∅ |
| b | Cl({A}) | {A, B} |
| c | Cl({B}) | {B} |
| d | Cl({A, B}) | {A, B} |
| e | δ(A, 0) | {A} |

**Paso 1: de AFND-λ a AFND** — δ'(q, a) = Cl(δ(Cl({q}), a)); q es de aceptación si su clausura contiene un estado de aceptación. AFND · 3 estados · 6 transiciones.

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | A, B | C |
| `B` | A, B | C |
| `* C` | ∅ | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Paso 2: de AFND a AFD** (subconjuntos)

- δ'({A}, 0) = δ(A,0) = {A, B} = {A, B}
- δ'({A}, 1) = δ(A,1) = {C} = {C}
- δ'({A,B}, 0) = δ(A,0) ∪ δ(B,0) = {A, B} ∪ {A, B} = {A, B}
- δ'({A,B}, 1) = δ(A,1) ∪ δ(B,1) = {C} ∪ {C} = {C}
- δ'({C}, 0) = δ(C,0) = ∅ = ∅
- δ'({C}, 1) = δ(C,1) = ∅ = ∅

**AFD** — AFD · 3 estados · 4 transiciones. Tamaños: AFND-λ 3 → AFND 3 → AFD 3 (cota 2^3 = 8).

| Estado | 0 | 1 |
|---|---|---|
| `→ {A}` | {A,B} | {C} |
| `{A,B}` | {A,B} | {C} |
| `* {C}` | ∅ | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (en el AFND-λ)

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `1` | acepta | {A, B} –1→ {C} | 1 (aceptan: 1) |
| válida | `0001` | acepta | {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –1→ {C} | 21 (aceptan: 21) |
| válida | `0000001` | acepta | {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –1→ {C} | 377 (aceptan: 377) |
| válida | `0000000001` | acepta | {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –1→ {C} | 500+ (aceptan: 500) |
| válida | `0000000000001` | acepta | {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –1→ {C} | 500+ (aceptan: 500) |
| inválida | `λ` | rechaza | {A, B} | 2 (aceptan: 0) |
| inválida | `101` | rechaza | {A, B} –1→ {C} –0→ ∅ | 1 (aceptan: 0) |
| inválida | `100000` | rechaza | {A, B} –1→ {C} –0→ ∅ | 1 (aceptan: 0) |
| inválida | `000001001` | rechaza | {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –1→ {C} –0→ ∅ | 144 (aceptan: 0) |
| inválida | `011001010011` | rechaza | {A, B} –0→ {A, B} –1→ {C} –1→ ∅ | 3 (aceptan: 0) |

## Ejercicio 197

Archivo(s): `automatas/lista3-afnd-lambda/Ej_197_tabla.jff`, `automatas/conversiones/Ej_197_afnd.jff`, `automatas/conversiones/Ej_197_afd.jff`

**AFND-λ** — AFND-lambda · 4 estados · 11 transiciones

| Estado | λ | 0 | 1 |
|---|---|---|---|
| `→ A` | C | B, D | ∅ |
| `B` | D | A, C | D |
| `C` | B | ∅ | A, C |
| `* D` | ∅ | ∅ | D |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**λ-clausura de cada estado**

| Estado | Cl(estado) |
|---|---|
| `A` | {A, B, C, D} |
| `B` | {B, D} |
| `C` | {B, C, D} |
| `D` | {D} |

**Preguntas del ejercicio**

| Inciso | Pregunta | Respuesta |
|---|---|---|
| a | Cl({A}) | {A, B, C, D} |
| b | Cl({B, D}) | {B, D} |
| c | Cl({A, B, C}) | {A, B, C, D} |
| d | δ(A, 0) | {B, D} |
| e | δ̂({A}, 010) | {A, B, C, D} |

**Paso 1: de AFND-λ a AFND** — δ'(q, a) = Cl(δ(Cl({q}), a)); q es de aceptación si su clausura contiene un estado de aceptación. AFND · 4 estados · 22 transiciones.

| Estado | 0 | 1 |
|---|---|---|
| `→* A` | A, B, C, D | A, B, C, D |
| `* B` | A, B, C, D | D |
| `* C` | A, B, C, D | A, B, C, D |
| `* D` | ∅ | D |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Paso 2: de AFND a AFD** (subconjuntos)

- δ'({A}, 0) = δ(A,0) = {A, B, C, D} = {A, B, C, D}
- δ'({A}, 1) = δ(A,1) = {A, B, C, D} = {A, B, C, D}
- δ'({A,B,C,D}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(D,0) = {A, B, C, D} ∪ {A, B, C, D} ∪ {A, B, C, D} ∪ ∅ = {A, B, C, D}
- δ'({A,B,C,D}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(D,1) = {A, B, C, D} ∪ {D} ∪ {A, B, C, D} ∪ {D} = {A, B, C, D}

**AFD** — AFD · 2 estados · 4 transiciones. Tamaños: AFND-λ 4 → AFND 4 → AFD 2 (cota 2^4 = 16).

| Estado | 0 | 1 |
|---|---|---|
| `→* {A}` | {A,B,C,D} | {A,B,C,D} |
| `* {A,B,C,D}` | {A,B,C,D} | {A,B,C,D} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (en el AFND-λ)

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `λ` | acepta | {A, B, C, D} | 4 (aceptan: 1) |
| válida | `1100` | acepta | {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B, C, D} –0→ {A, B, C, D} | 104 (aceptan: 28) |
| válida | `1011100` | acepta | {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B, C, D} –0→ {A, B, C, D} | 500+ (aceptan: 130) |
| válida | `1001011110` | acepta | {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B, C, D} –0→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B, C, D} | 500+ (aceptan: 127) |
| válida | `00110000110101` | acepta | {A, B, C, D} –0→ {A, B, C, D} –0→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B, C, D} –0→ {A, B, C, D} –0→ {A, B, C, D} –0→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B, C, D} –1→ {A, B, C, D} | 500+ (aceptan: 206) |

## Ejercicio 198

Archivo(s): `automatas/lista3-afnd-lambda/Ej_198_tabla.jff`, `automatas/conversiones/Ej_198_afnd.jff`, `automatas/conversiones/Ej_198_afd.jff`

**AFND-λ** — AFND-lambda · 4 estados · 7 transiciones

| Estado | λ | 0 | 1 |
|---|---|---|---|
| `→ A` | C | B | ∅ |
| `B` | ∅ | C | ∅ |
| `C` | B | ∅ | C, D |
| `* D` | ∅ | ∅ | B |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**λ-clausura de cada estado**

| Estado | Cl(estado) |
|---|---|
| `A` | {A, B, C} |
| `B` | {B} |
| `C` | {B, C} |
| `D` | {D} |

**Preguntas del ejercicio**

| Inciso | Pregunta | Respuesta |
|---|---|---|
| a | Cl({A}) | {A, B, C} |
| b | Cl({C, D}) | {B, C, D} |
| c | Cl({A, C, D}) | {A, B, C, D} |
| e | δ̂({B}, 0111) | {B, C, D} |

**Paso 1: de AFND-λ a AFND** — δ'(q, a) = Cl(δ(Cl({q}), a)); q es de aceptación si su clausura contiene un estado de aceptación. AFND · 4 estados · 13 transiciones.

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | B, C | B, C, D |
| `B` | B, C | ∅ |
| `C` | B, C | B, C, D |
| `* D` | ∅ | B |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Paso 2: de AFND a AFD** (subconjuntos)

- δ'({A}, 0) = δ(A,0) = {B, C} = {B, C}
- δ'({A}, 1) = δ(A,1) = {B, C, D} = {B, C, D}
- δ'({B,C}, 0) = δ(B,0) ∪ δ(C,0) = {B, C} ∪ {B, C} = {B, C}
- δ'({B,C}, 1) = δ(B,1) ∪ δ(C,1) = ∅ ∪ {B, C, D} = {B, C, D}
- δ'({B,C,D}, 0) = δ(B,0) ∪ δ(C,0) ∪ δ(D,0) = {B, C} ∪ {B, C} ∪ ∅ = {B, C}
- δ'({B,C,D}, 1) = δ(B,1) ∪ δ(C,1) ∪ δ(D,1) = ∅ ∪ {B, C, D} ∪ {B} = {B, C, D}

**AFD** — AFD · 3 estados · 6 transiciones. Tamaños: AFND-λ 4 → AFND 4 → AFD 3 (cota 2^4 = 16).

| Estado | 0 | 1 |
|---|---|---|
| `→ {A}` | {B,C} | {B,C,D} |
| `{B,C}` | {B,C} | {B,C,D} |
| `* {B,C,D}` | {B,C} | {B,C,D} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (en el AFND-λ)

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `1` | acepta | {A, B, C} –1→ {B, C, D} | 4 (aceptan: 1) |
| válida | `0001` | acepta | {A, B, C} –0→ {B, C} –0→ {B, C} –0→ {B, C} –1→ {B, C, D} | 8 (aceptan: 2) |
| válida | `0011111` | acepta | {A, B, C} –0→ {B, C} –0→ {B, C} –1→ {B, C, D} –1→ {B, C, D} –1→ {B, C, D} –1→ {B, C, D} –1→ {B, C, D} | 24 (aceptan: 2) |
| válida | `10000010001` | acepta | {A, B, C} –1→ {B, C, D} –0→ {B, C} –0→ {B, C} –0→ {B, C} –0→ {B, C} –0→ {B, C} –1→ {B, C, D} –0→ {B, C} –0→ {B, C} –0→ {B, C} –1→ {B, C, D} | 8 (aceptan: 1) |
| válida | `00100101011101` | acepta | {A, B, C} –0→ {B, C} –0→ {B, C} –1→ {B, C, D} –0→ {B, C} –0→ {B, C} –1→ {B, C, D} –0→ {B, C} –1→ {B, C, D} –0→ {B, C} –1→ {B, C, D} –1→ {B, C, D} –1→ {B, C, D} –0→ {B, C} –1→ {B, C, D} | 38 (aceptan: 4) |
| inválida | `λ` | rechaza | {A, B, C} | 3 (aceptan: 0) |
| inválida | `010` | rechaza | {A, B, C} –0→ {B, C} –1→ {B, C, D} –0→ {B, C} | 5 (aceptan: 0) |
| inválida | `001000` | rechaza | {A, B, C} –0→ {B, C} –0→ {B, C} –1→ {B, C, D} –0→ {B, C} –0→ {B, C} –0→ {B, C} | 8 (aceptan: 0) |
| inválida | `010010100` | rechaza | {A, B, C} –0→ {B, C} –1→ {B, C, D} –0→ {B, C} –0→ {B, C} –1→ {B, C, D} –0→ {B, C} –1→ {B, C, D} –0→ {B, C} –0→ {B, C} | 9 (aceptan: 0) |
| inválida | `101101110000` | rechaza | {A, B, C} –1→ {B, C, D} –0→ {B, C} –1→ {B, C, D} –1→ {B, C, D} –0→ {B, C} –1→ {B, C, D} –1→ {B, C, D} –1→ {B, C, D} –0→ {B, C} –0→ {B, C} –0→ {B, C} –0→ {B, C} | 23 (aceptan: 0) |

## Ejercicio 199

Archivo(s): `automatas/lista3-afnd-lambda/Ej_199_tabla.jff`, `automatas/conversiones/Ej_199_afnd.jff`, `automatas/conversiones/Ej_199_afd.jff`

**AFND-λ** — AFND-lambda · 5 estados · 10 transiciones

| Estado | λ | 0 | 1 |
|---|---|---|---|
| `→ A` | B, C | E | ∅ |
| `B` | ∅ | E | B |
| `C` | E | ∅ | A, C |
| `* D` | ∅ | ∅ | D |
| `* E` | ∅ | ∅ | D |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**λ-clausura de cada estado**

| Estado | Cl(estado) |
|---|---|
| `A` | {A, B, C, E} |
| `B` | {B} |
| `C` | {C, E} |
| `D` | {D} |
| `E` | {E} |

**Preguntas del ejercicio**

| Inciso | Pregunta | Respuesta |
|---|---|---|
| a | Cl({A}) | {A, B, C, E} |
| b | Cl({C}) | {C, E} |
| c | δ̂({A}, 011) | {D} |

**Paso 1: de AFND-λ a AFND** — δ'(q, a) = Cl(δ(Cl({q}), a)); q es de aceptación si su clausura contiene un estado de aceptación. AFND · 5 estados · 15 transiciones.

| Estado | 0 | 1 |
|---|---|---|
| `→* A` | E | A, B, C, D, E |
| `B` | E | B |
| `* C` | ∅ | A, B, C, D, E |
| `* D` | ∅ | D |
| `* E` | ∅ | D |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Paso 2: de AFND a AFD** (subconjuntos)

- δ'({A}, 0) = δ(A,0) = {E} = {E}
- δ'({A}, 1) = δ(A,1) = {A, B, C, D, E} = {A, B, C, D, E}
- δ'({E}, 0) = δ(E,0) = ∅ = ∅
- δ'({E}, 1) = δ(E,1) = {D} = {D}
- δ'({A,B,C,D,E}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(D,0) ∪ δ(E,0) = {E} ∪ {E} ∪ ∅ ∪ ∅ ∪ ∅ = {E}
- δ'({A,B,C,D,E}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(D,1) ∪ δ(E,1) = {A, B, C, D, E} ∪ {B} ∪ {A, B, C, D, E} ∪ {D} ∪ {D} = {A, B, C, D, E}
- δ'({D}, 0) = δ(D,0) = ∅ = ∅
- δ'({D}, 1) = δ(D,1) = {D} = {D}

**AFD** — AFD · 4 estados · 6 transiciones. Tamaños: AFND-λ 5 → AFND 5 → AFD 4 (cota 2^5 = 32).

| Estado | 0 | 1 |
|---|---|---|
| `→* {A}` | {E} | {A,B,C,D,E} |
| `* {E}` | ∅ | {D} |
| `* {A,B,C,D,E}` | {E} | {A,B,C,D,E} |
| `* {D}` | ∅ | {D} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (en el AFND-λ)

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `λ` | acepta | {A, B, C, E} | 4 (aceptan: 1) |
| válida | `1111` | acepta | {A, B, C, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} | 71 (aceptan: 31) |
| válida | `1011111` | acepta | {A, B, C, E} –1→ {A, B, C, D, E} –0→ {E} –1→ {D} –1→ {D} –1→ {D} –1→ {D} –1→ {D} | 6 (aceptan: 3) |
| válida | `1111111110` | acepta | {A, B, C, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –0→ {E} | 500+ (aceptan: 215) |
| válida | `11111111111110` | acepta | {A, B, C, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –0→ {E} | 500+ (aceptan: 216) |
| inválida | `00` | rechaza | {A, B, C, E} –0→ {E} –0→ ∅ | 3 (aceptan: 0) |
| inválida | `0100` | rechaza | {A, B, C, E} –0→ {E} –1→ {D} –0→ ∅ | 3 (aceptan: 0) |
| inválida | `0000011` | rechaza | {A, B, C, E} –0→ {E} –0→ ∅ | 3 (aceptan: 0) |
| inválida | `0000111101` | rechaza | {A, B, C, E} –0→ {E} –0→ ∅ | 3 (aceptan: 0) |
| inválida | `100001101010` | rechaza | {A, B, C, E} –1→ {A, B, C, D, E} –0→ {E} –0→ ∅ | 6 (aceptan: 0) |

## Ejercicio 200

Archivo(s): `automatas/lista3-afnd-lambda/Ej_200_tabla.jff`, `automatas/conversiones/Ej_200_afnd.jff`, `automatas/conversiones/Ej_200_afd.jff`

**AFND-λ** — AFND-lambda · 6 estados · 22 transiciones

| Estado | λ | 0 | 1 |
|---|---|---|---|
| `→ A` | B | F | A, C, F |
| `B` | ∅ | C, D | B, E |
| `C` | E | ∅ | A, C |
| `* D` | E, F | A, C | B, E |
| `* E` | ∅ | ∅ | D |
| `F` | E | B, E | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**λ-clausura de cada estado**

| Estado | Cl(estado) |
|---|---|
| `A` | {A, B} |
| `B` | {B} |
| `C` | {C, E} |
| `D` | {D, E, F} |
| `E` | {E} |
| `F` | {E, F} |

**Preguntas del ejercicio**

| Inciso | Pregunta | Respuesta |
|---|---|---|
| a | Cl({A}) | {A, B} |
| b | Cl({C, D}) | {C, D, E, F} |
| c | δ̂({C}, 1011) | {A, B, C, D, E, F} |

**Paso 1: de AFND-λ a AFND** — δ'(q, a) = Cl(δ(Cl({q}), a)); q es de aceptación si su clausura contiene un estado de aceptación. AFND · 6 estados · 37 transiciones.

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | C, D, E, F | A, B, C, E, F |
| `B` | C, D, E, F | B, E |
| `* C` | ∅ | A, B, C, D, E, F |
| `* D` | A, B, C, E | B, D, E, F |
| `* E` | ∅ | D, E, F |
| `* F` | B, E | D, E, F |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Paso 2: de AFND a AFD** (subconjuntos)

- δ'({A}, 0) = δ(A,0) = {C, D, E, F} = {C, D, E, F}
- δ'({A}, 1) = δ(A,1) = {A, B, C, E, F} = {A, B, C, E, F}
- δ'({C,D,E,F}, 0) = δ(C,0) ∪ δ(D,0) ∪ δ(E,0) ∪ δ(F,0) = ∅ ∪ {A, B, C, E} ∪ ∅ ∪ {B, E} = {A, B, C, E}
- δ'({C,D,E,F}, 1) = δ(C,1) ∪ δ(D,1) ∪ δ(E,1) ∪ δ(F,1) = {A, B, C, D, E, F} ∪ {B, D, E, F} ∪ {D, E, F} ∪ {D, E, F} = {A, B, C, D, E, F}
- δ'({A,B,C,E,F}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(E,0) ∪ δ(F,0) = {C, D, E, F} ∪ {C, D, E, F} ∪ ∅ ∪ ∅ ∪ {B, E} = {B, C, D, E, F}
- δ'({A,B,C,E,F}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(E,1) ∪ δ(F,1) = {A, B, C, E, F} ∪ {B, E} ∪ {A, B, C, D, E, F} ∪ {D, E, F} ∪ {D, E, F} = {A, B, C, D, E, F}
- δ'({A,B,C,E}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(E,0) = {C, D, E, F} ∪ {C, D, E, F} ∪ ∅ ∪ ∅ = {C, D, E, F}
- δ'({A,B,C,E}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(E,1) = {A, B, C, E, F} ∪ {B, E} ∪ {A, B, C, D, E, F} ∪ {D, E, F} = {A, B, C, D, E, F}
- δ'({A,B,C,D,E,F}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(D,0) ∪ δ(E,0) ∪ δ(F,0) = {C, D, E, F} ∪ {C, D, E, F} ∪ ∅ ∪ {A, B, C, E} ∪ ∅ ∪ {B, E} = {A, B, C, D, E, F}
- δ'({A,B,C,D,E,F}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(D,1) ∪ δ(E,1) ∪ δ(F,1) = {A, B, C, E, F} ∪ {B, E} ∪ {A, B, C, D, E, F} ∪ {B, D, E, F} ∪ {D, E, F} ∪ {D, E, F} = {A, B, C, D, E, F}
- δ'({B,C,D,E,F}, 0) = δ(B,0) ∪ δ(C,0) ∪ δ(D,0) ∪ δ(E,0) ∪ δ(F,0) = {C, D, E, F} ∪ ∅ ∪ {A, B, C, E} ∪ ∅ ∪ {B, E} = {A, B, C, D, E, F}
- δ'({B,C,D,E,F}, 1) = δ(B,1) ∪ δ(C,1) ∪ δ(D,1) ∪ δ(E,1) ∪ δ(F,1) = {B, E} ∪ {A, B, C, D, E, F} ∪ {B, D, E, F} ∪ {D, E, F} ∪ {D, E, F} = {A, B, C, D, E, F}

**AFD** — AFD · 6 estados · 12 transiciones. Tamaños: AFND-λ 6 → AFND 6 → AFD 6 (cota 2^6 = 64).

| Estado | 0 | 1 |
|---|---|---|
| `→ {A}` | {C,D,E,F} | {A,B,C,E,F} |
| `* {C,D,E,F}` | {A,B,C,E} | {A,B,C,D,E,F} |
| `* {A,B,C,E,F}` | {B,C,D,E,F} | {A,B,C,D,E,F} |
| `* {A,B,C,E}` | {C,D,E,F} | {A,B,C,D,E,F} |
| `* {A,B,C,D,E,F}` | {A,B,C,D,E,F} | {A,B,C,D,E,F} |
| `* {B,C,D,E,F}` | {A,B,C,D,E,F} | {A,B,C,D,E,F} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (en el AFND-λ)

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `1` | acepta | {A, B} –1→ {A, B, C, E, F} | 8 (aceptan: 3) |
| válida | `1010` | acepta | {A, B} –1→ {A, B, C, E, F} –0→ {B, C, D, E, F} –1→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} | 106 (aceptan: 38) |
| válida | `0000110` | acepta | {A, B} –0→ {C, D, E, F} –0→ {A, B, C, E} –0→ {C, D, E, F} –0→ {A, B, C, E} –1→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} | 500+ (aceptan: 197) |
| válida | `10000110111` | acepta | {A, B} –1→ {A, B, C, E, F} –0→ {B, C, D, E, F} –0→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} | 500+ (aceptan: 306) |
| válida | `00010011110000` | acepta | {A, B} –0→ {C, D, E, F} –0→ {A, B, C, E} –0→ {C, D, E, F} –1→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} –1→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} –0→ {A, B, C, D, E, F} | 500+ (aceptan: 190) |
| inválida | `λ` | rechaza | {A, B} | 2 (aceptan: 0) |

