# Guía 3: de AFN a AFD (191 a 195 y 260 a 263)

El ejercicio 191 es el enunciado de los 192 a 195 (hallar el AFD equivalente y calcular δ̂ y δ̂_D). En JFLAP: *Convert → Convert to DFA*, *Complete* para ver cada paso y *Done?* al terminar. JFLAP nombra los estados del AFD con los conjuntos y no agrega el estado ∅ (el AFD resultante puede quedar incompleto).

## Ejercicio 192

Archivo(s): `automatas/lista3-afnd/Ej_192_tabla.jff`, `automatas/conversiones/Ej_192_afd.jff`

**AFN** — AFND · 3 estados · 7 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | B | B, C |
| `B` | A, B | ∅ |
| `* C` | A, C | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Construcción de subconjuntos, paso a paso** (δ' es la función del AFD; el estado inicial es la λ-clausura del inicial)

- δ'({A}, 0) = δ(A,0) = {B} = {B}
- δ'({A}, 1) = δ(A,1) = {B, C} = {B, C}
- δ'({B}, 0) = δ(B,0) = {A, B} = {A, B}
- δ'({B}, 1) = δ(B,1) = ∅ = ∅
- δ'({B,C}, 0) = δ(B,0) ∪ δ(C,0) = {A, B} ∪ {A, C} = {A, B, C}
- δ'({B,C}, 1) = δ(B,1) ∪ δ(C,1) = ∅ ∪ ∅ = ∅
- δ'({A,B}, 0) = δ(A,0) ∪ δ(B,0) = {B} ∪ {A, B} = {A, B}
- δ'({A,B}, 1) = δ(A,1) ∪ δ(B,1) = {B, C} ∪ ∅ = {B, C}
- δ'({A,B,C}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) = {B} ∪ {A, B} ∪ {A, C} = {A, B, C}
- δ'({A,B,C}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) = {B, C} ∪ ∅ ∪ ∅ = {B, C}

**AFD equivalente** — AFD · 5 estados · 8 transiciones. Cada estado es un conjunto de estados del AFN.

| Estado | 0 | 1 |
|---|---|---|
| `→ {A}` | {B} | {B,C} |
| `{B}` | {A,B} | ∅ |
| `* {B,C}` | {A,B,C} | ∅ |
| `{A,B}` | {A,B} | {B,C} |
| `* {A,B,C}` | {A,B,C} | {B,C} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Tamaños:** AFN 3 estados → AFD 5 estados (cota 2^3 = 8); el AFD mínimo tiene 5.

**Preguntas del ejercicio.** δ̂ es la función extendida del AFN; δ̂_D la del AFD, cuyos estados son conjuntos: δ̂_D(Z, ω) es el conjunto al que llega el AFD empezando en el estado Z. Coinciden, porque δ_D(S, a) = ∪ δ(q, a).

| Inciso | Pregunta | δ̂ en el AFN | δ̂_D en el AFD (y el camino de conjuntos) |
|---|---|---|---|
| a | δ̂({A}, 0111) | ∅ | ∅ (`{A} → {B} → ∅ → ∅ → ∅`) |
| b | δ̂({B, C}, 010111) | ∅ | ∅ (`{B, C} → {A, B, C} → {B, C} → {A, B, C} → {B, C} → ∅ → ∅`) |

**Cadenas de prueba**

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `1` | acepta | {A} –1→ {B, C} | 2 (aceptan: 1) |
| válida | `0001` | acepta | {A} –0→ {B} –0→ {A, B} –0→ {A, B} –1→ {B, C} | 4 (aceptan: 1) |
| válida | `0001010` | acepta | {A} –0→ {B} –0→ {A, B} –0→ {A, B} –1→ {B, C} –0→ {A, B, C} –1→ {B, C} –0→ {A, B, C} | 12 (aceptan: 2) |
| válida | `10100010001` | acepta | {A} –1→ {B, C} –0→ {A, B, C} –1→ {B, C} –0→ {A, B, C} –0→ {A, B, C} –0→ {A, B, C} –1→ {B, C} –0→ {A, B, C} –0→ {A, B, C} –0→ {A, B, C} –1→ {B, C} | 126 (aceptan: 32) |
| válida | `10001001000010` | acepta | {A} –1→ {B, C} –0→ {A, B, C} –0→ {A, B, C} –0→ {A, B, C} –1→ {B, C} –0→ {A, B, C} –0→ {A, B, C} –1→ {B, C} –0→ {A, B, C} –0→ {A, B, C} –0→ {A, B, C} –0→ {A, B, C} –1→ {B, C} –0→ {A, B, C} | 294 (aceptan: 48) |
| inválida | `λ` | rechaza | {A} | 1 (aceptan: 0) |
| inválida | `111` | rechaza | {A} –1→ {B, C} –1→ ∅ | 2 (aceptan: 0) |
| inválida | `111111` | rechaza | {A} –1→ {B, C} –1→ ∅ | 2 (aceptan: 0) |
| inválida | `001101111` | rechaza | {A} –0→ {B} –0→ {A, B} –1→ {B, C} –1→ ∅ | 3 (aceptan: 0) |
| inválida | `110100001010` | rechaza | {A} –1→ {B, C} –1→ ∅ | 2 (aceptan: 0) |

## Ejercicio 193

Archivo(s): `automatas/lista3-afnd/Ej_193_tabla.jff`, `automatas/conversiones/Ej_193_afd.jff`

**AFN** — AFND · 4 estados · 12 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | ∅ | B, C |
| `B` | A, D | B, C, D |
| `C` | C | A, C |
| `* D` | C | D |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Construcción de subconjuntos, paso a paso** (δ' es la función del AFD; el estado inicial es la λ-clausura del inicial)

- δ'({A}, 0) = δ(A,0) = ∅ = ∅
- δ'({A}, 1) = δ(A,1) = {B, C} = {B, C}
- δ'({B,C}, 0) = δ(B,0) ∪ δ(C,0) = {A, D} ∪ {C} = {A, C, D}
- δ'({B,C}, 1) = δ(B,1) ∪ δ(C,1) = {B, C, D} ∪ {A, C} = {A, B, C, D}
- δ'({A,C,D}, 0) = δ(A,0) ∪ δ(C,0) ∪ δ(D,0) = ∅ ∪ {C} ∪ {C} = {C}
- δ'({A,C,D}, 1) = δ(A,1) ∪ δ(C,1) ∪ δ(D,1) = {B, C} ∪ {A, C} ∪ {D} = {A, B, C, D}
- δ'({A,B,C,D}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(D,0) = ∅ ∪ {A, D} ∪ {C} ∪ {C} = {A, C, D}
- δ'({A,B,C,D}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(D,1) = {B, C} ∪ {B, C, D} ∪ {A, C} ∪ {D} = {A, B, C, D}
- δ'({C}, 0) = δ(C,0) = {C} = {C}
- δ'({C}, 1) = δ(C,1) = {A, C} = {A, C}
- δ'({A,C}, 0) = δ(A,0) ∪ δ(C,0) = ∅ ∪ {C} = {C}
- δ'({A,C}, 1) = δ(A,1) ∪ δ(C,1) = {B, C} ∪ {A, C} = {A, B, C}
- δ'({A,B,C}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) = ∅ ∪ {A, D} ∪ {C} = {A, C, D}
- δ'({A,B,C}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) = {B, C} ∪ {B, C, D} ∪ {A, C} = {A, B, C, D}

**AFD equivalente** — AFD · 7 estados · 13 transiciones. Cada estado es un conjunto de estados del AFN.

| Estado | 0 | 1 |
|---|---|---|
| `→ {A}` | ∅ | {B,C} |
| `{B,C}` | {A,C,D} | {A,B,C,D} |
| `* {A,C,D}` | {C} | {A,B,C,D} |
| `* {A,B,C,D}` | {A,C,D} | {A,B,C,D} |
| `{C}` | {C} | {A,C} |
| `{A,C}` | {C} | {A,B,C} |
| `{A,B,C}` | {A,C,D} | {A,B,C,D} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Tamaños:** AFN 4 estados → AFD 7 estados (cota 2^4 = 16); el AFD mínimo tiene 6.

**Preguntas del ejercicio.** δ̂ es la función extendida del AFN; δ̂_D la del AFD, cuyos estados son conjuntos: δ̂_D(Z, ω) es el conjunto al que llega el AFD empezando en el estado Z. Coinciden, porque δ_D(S, a) = ∪ δ(q, a).

| Inciso | Pregunta | δ̂ en el AFN | δ̂_D en el AFD (y el camino de conjuntos) |
|---|---|---|---|
| a | δ̂({A}, 01101) | ∅ | ∅ (`{A} → ∅ → ∅ → ∅ → ∅ → ∅`) |
| b | δ̂({A, B}, 1101) | {A, B, C, D} | {A, B, C, D} (`{A, B} → {B, C, D} → {A, B, C, D} → {A, C, D} → {A, B, C, D}`) |
| c | δ̂({C}, 1101) | {A, B, C, D} | {A, B, C, D} (`{C} → {A, C} → {A, B, C} → {A, C, D} → {A, B, C, D}`) |

**Cadenas de prueba**

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `11` | acepta | {A} –1→ {B, C} –1→ {A, B, C, D} | 5 (aceptan: 1) |
| válida | `11101` | acepta | {A} –1→ {B, C} –1→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, C, D} –1→ {A, B, C, D} | 20 (aceptan: 2) |
| válida | `11000110` | acepta | {A} –1→ {B, C} –1→ {A, B, C, D} –0→ {A, C, D} –0→ {C} –0→ {C} –1→ {A, C} –1→ {A, B, C} –0→ {A, C, D} | 22 (aceptan: 4) |
| válida | `10100111111` | acepta | {A} –1→ {B, C} –0→ {A, C, D} –1→ {A, B, C, D} –0→ {A, C, D} –0→ {C} –1→ {A, C} –1→ {A, B, C} –1→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} | 318 (aceptan: 60) |
| válida | `11101011101010` | acepta | {A} –1→ {B, C} –1→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, C, D} –1→ {A, B, C, D} –0→ {A, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, C, D} –1→ {A, B, C, D} –0→ {A, C, D} –1→ {A, B, C, D} –0→ {A, C, D} | 416 (aceptan: 24) |
| inválida | `λ` | rechaza | {A} | 1 (aceptan: 0) |
| inválida | `100` | rechaza | {A} –1→ {B, C} –0→ {A, C, D} –0→ {C} | 3 (aceptan: 0) |
| inválida | `001101` | rechaza | {A} –0→ ∅ | 1 (aceptan: 0) |
| inválida | `001101100` | rechaza | {A} –0→ ∅ | 1 (aceptan: 0) |
| inválida | `010111000010` | rechaza | {A} –0→ ∅ | 1 (aceptan: 0) |

## Ejercicio 194

Archivo(s): `automatas/lista3-afnd/Ej_194_tabla.jff`, `automatas/conversiones/Ej_194_afd.jff`

**AFN** — AFND · 4 estados · 13 transiciones

| Estado | 0 | 1 | 2 |
|---|---|---|---|
| `→ A` | A, B | A, C | A |
| `B` | ∅ | ∅ | ∅ |
| `* C` | A, B | A, B, C, D | ∅ |
| `* D` | B | A | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Construcción de subconjuntos, paso a paso** (δ' es la función del AFD; el estado inicial es la λ-clausura del inicial)

- δ'({A}, 0) = δ(A,0) = {A, B} = {A, B}
- δ'({A}, 1) = δ(A,1) = {A, C} = {A, C}
- δ'({A}, 2) = δ(A,2) = {A} = {A}
- δ'({A,B}, 0) = δ(A,0) ∪ δ(B,0) = {A, B} ∪ ∅ = {A, B}
- δ'({A,B}, 1) = δ(A,1) ∪ δ(B,1) = {A, C} ∪ ∅ = {A, C}
- δ'({A,B}, 2) = δ(A,2) ∪ δ(B,2) = {A} ∪ ∅ = {A}
- δ'({A,C}, 0) = δ(A,0) ∪ δ(C,0) = {A, B} ∪ {A, B} = {A, B}
- δ'({A,C}, 1) = δ(A,1) ∪ δ(C,1) = {A, C} ∪ {A, B, C, D} = {A, B, C, D}
- δ'({A,C}, 2) = δ(A,2) ∪ δ(C,2) = {A} ∪ ∅ = {A}
- δ'({A,B,C,D}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(D,0) = {A, B} ∪ ∅ ∪ {A, B} ∪ {B} = {A, B}
- δ'({A,B,C,D}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(D,1) = {A, C} ∪ ∅ ∪ {A, B, C, D} ∪ {A} = {A, B, C, D}
- δ'({A,B,C,D}, 2) = δ(A,2) ∪ δ(B,2) ∪ δ(C,2) ∪ δ(D,2) = {A} ∪ ∅ ∪ ∅ ∪ ∅ = {A}

**AFD equivalente** — AFD · 4 estados · 12 transiciones. Cada estado es un conjunto de estados del AFN.

| Estado | 0 | 1 | 2 |
|---|---|---|---|
| `→ {A}` | {A,B} | {A,C} | {A} |
| `{A,B}` | {A,B} | {A,C} | {A} |
| `* {A,C}` | {A,B} | {A,B,C,D} | {A} |
| `* {A,B,C,D}` | {A,B} | {A,B,C,D} | {A} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Tamaños:** AFN 4 estados → AFD 4 estados (cota 2^4 = 16); el AFD mínimo tiene 2.

**Preguntas del ejercicio.** δ̂ es la función extendida del AFN; δ̂_D la del AFD, cuyos estados son conjuntos: δ̂_D(Z, ω) es el conjunto al que llega el AFD empezando en el estado Z. Coinciden, porque δ_D(S, a) = ∪ δ(q, a).

| Inciso | Pregunta | δ̂ en el AFN | δ̂_D en el AFD (y el camino de conjuntos) |
|---|---|---|---|
| a | δ̂({A, C}, 0121) | {A, C} | {A, C} (`{A, C} → {A, B} → {A, C} → {A} → {A, C}`) |
| b | δ̂({B}, 20111) | ∅ | ∅ (`{B} → ∅ → ∅ → ∅ → ∅ → ∅`) |
| c | δ̂({C}, 02112) | {A} | {A} (`{C} → {A, B} → {A} → {A, C} → {A, B, C, D} → {A}`) |
| d | δ̂({A, B}, 0121) | {A, C} | {A, C} (`{A, B} → {A, B} → {A, C} → {A} → {A, C}`) |

**Cadenas de prueba**

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `1` | acepta | {A} –1→ {A, C} | 2 (aceptan: 1) |
| válida | `1211` | acepta | {A} –1→ {A, C} –2→ {A} –1→ {A, C} –1→ {A, B, C, D} | 7 (aceptan: 3) |
| válida | `1201021` | acepta | {A} –1→ {A, C} –2→ {A} –0→ {A, B} –1→ {A, C} –0→ {A, B} –2→ {A} –1→ {A, C} | 8 (aceptan: 2) |
| válida | `00111021211` | acepta | {A} –0→ {A, B} –0→ {A, B} –1→ {A, C} –1→ {A, B, C, D} –1→ {A, B, C, D} –0→ {A, B} –2→ {A} –1→ {A, C} –2→ {A} –1→ {A, C} –1→ {A, B, C, D} | 79 (aceptan: 27) |
| válida | `00100100201001` | acepta | {A} –0→ {A, B} –0→ {A, B} –1→ {A, C} –0→ {A, B} –0→ {A, B} –1→ {A, C} –0→ {A, B} –0→ {A, B} –2→ {A} –0→ {A, B} –1→ {A, C} –0→ {A, B} –0→ {A, B} –1→ {A, C} | 50 (aceptan: 8) |
| inválida | `λ` | rechaza | {A} | 1 (aceptan: 0) |
| inválida | `12` | rechaza | {A} –1→ {A, C} –2→ {A} | 2 (aceptan: 0) |
| inválida | `1210` | rechaza | {A} –1→ {A, C} –2→ {A} –1→ {A, C} –0→ {A, B} | 5 (aceptan: 0) |
| inválida | `112222` | rechaza | {A} –1→ {A, C} –1→ {A, B, C, D} –2→ {A} –2→ {A} –2→ {A} –2→ {A} | 6 (aceptan: 0) |
| inválida | `11222110` | rechaza | {A} –1→ {A, C} –1→ {A, B, C, D} –2→ {A} –2→ {A} –2→ {A} –1→ {A, C} –1→ {A, B, C, D} –0→ {A, B} | 24 (aceptan: 0) |

## Ejercicio 195

Archivo(s): `automatas/lista3-afnd/Ej_195_tabla.jff`, `automatas/conversiones/Ej_195_afd.jff`

**AFN** — AFND · 5 estados · 12 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | A, B | A |
| `B` | A | C |
| `* C` | A | D |
| `D` | D | E |
| `* E` | E | C, D |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Construcción de subconjuntos, paso a paso** (δ' es la función del AFD; el estado inicial es la λ-clausura del inicial)

- δ'({A}, 0) = δ(A,0) = {A, B} = {A, B}
- δ'({A}, 1) = δ(A,1) = {A} = {A}
- δ'({A,B}, 0) = δ(A,0) ∪ δ(B,0) = {A, B} ∪ {A} = {A, B}
- δ'({A,B}, 1) = δ(A,1) ∪ δ(B,1) = {A} ∪ {C} = {A, C}
- δ'({A,C}, 0) = δ(A,0) ∪ δ(C,0) = {A, B} ∪ {A} = {A, B}
- δ'({A,C}, 1) = δ(A,1) ∪ δ(C,1) = {A} ∪ {D} = {A, D}
- δ'({A,D}, 0) = δ(A,0) ∪ δ(D,0) = {A, B} ∪ {D} = {A, B, D}
- δ'({A,D}, 1) = δ(A,1) ∪ δ(D,1) = {A} ∪ {E} = {A, E}
- δ'({A,B,D}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(D,0) = {A, B} ∪ {A} ∪ {D} = {A, B, D}
- δ'({A,B,D}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(D,1) = {A} ∪ {C} ∪ {E} = {A, C, E}
- δ'({A,E}, 0) = δ(A,0) ∪ δ(E,0) = {A, B} ∪ {E} = {A, B, E}
- δ'({A,E}, 1) = δ(A,1) ∪ δ(E,1) = {A} ∪ {C, D} = {A, C, D}
- δ'({A,C,E}, 0) = δ(A,0) ∪ δ(C,0) ∪ δ(E,0) = {A, B} ∪ {A} ∪ {E} = {A, B, E}
- δ'({A,C,E}, 1) = δ(A,1) ∪ δ(C,1) ∪ δ(E,1) = {A} ∪ {D} ∪ {C, D} = {A, C, D}
- δ'({A,B,E}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(E,0) = {A, B} ∪ {A} ∪ {E} = {A, B, E}
- δ'({A,B,E}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(E,1) = {A} ∪ {C} ∪ {C, D} = {A, C, D}
- δ'({A,C,D}, 0) = δ(A,0) ∪ δ(C,0) ∪ δ(D,0) = {A, B} ∪ {A} ∪ {D} = {A, B, D}
- δ'({A,C,D}, 1) = δ(A,1) ∪ δ(C,1) ∪ δ(D,1) = {A} ∪ {D} ∪ {E} = {A, D, E}
- δ'({A,D,E}, 0) = δ(A,0) ∪ δ(D,0) ∪ δ(E,0) = {A, B} ∪ {D} ∪ {E} = {A, B, D, E}
- δ'({A,D,E}, 1) = δ(A,1) ∪ δ(D,1) ∪ δ(E,1) = {A} ∪ {E} ∪ {C, D} = {A, C, D, E}
- δ'({A,B,D,E}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(D,0) ∪ δ(E,0) = {A, B} ∪ {A} ∪ {D} ∪ {E} = {A, B, D, E}
- δ'({A,B,D,E}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(D,1) ∪ δ(E,1) = {A} ∪ {C} ∪ {E} ∪ {C, D} = {A, C, D, E}
- δ'({A,C,D,E}, 0) = δ(A,0) ∪ δ(C,0) ∪ δ(D,0) ∪ δ(E,0) = {A, B} ∪ {A} ∪ {D} ∪ {E} = {A, B, D, E}
- δ'({A,C,D,E}, 1) = δ(A,1) ∪ δ(C,1) ∪ δ(D,1) ∪ δ(E,1) = {A} ∪ {D} ∪ {E} ∪ {C, D} = {A, C, D, E}

**AFD equivalente** — AFD · 12 estados · 24 transiciones. Cada estado es un conjunto de estados del AFN.

| Estado | 0 | 1 |
|---|---|---|
| `→ {A}` | {A,B} | {A} |
| `{A,B}` | {A,B} | {A,C} |
| `* {A,C}` | {A,B} | {A,D} |
| `{A,D}` | {A,B,D} | {A,E} |
| `{A,B,D}` | {A,B,D} | {A,C,E} |
| `* {A,E}` | {A,B,E} | {A,C,D} |
| `* {A,C,E}` | {A,B,E} | {A,C,D} |
| `* {A,B,E}` | {A,B,E} | {A,C,D} |
| `* {A,C,D}` | {A,B,D} | {A,D,E} |
| `* {A,D,E}` | {A,B,D,E} | {A,C,D,E} |
| `* {A,B,D,E}` | {A,B,D,E} | {A,C,D,E} |
| `* {A,C,D,E}` | {A,B,D,E} | {A,C,D,E} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Tamaños:** AFN 5 estados → AFD 12 estados (cota 2^5 = 32); el AFD mínimo tiene 7.

**Preguntas del ejercicio.** δ̂ es la función extendida del AFN; δ̂_D la del AFD, cuyos estados son conjuntos: δ̂_D(Z, ω) es el conjunto al que llega el AFD empezando en el estado Z. Coinciden, porque δ_D(S, a) = ∪ δ(q, a).

| Inciso | Pregunta | δ̂ en el AFN | δ̂_D en el AFD (y el camino de conjuntos) |
|---|---|---|---|
| a | δ̂({A}, 10010) | {A, B} | {A, B} (`{A} → {A} → {A, B} → {A, B} → {A, C} → {A, B}`) |
| b | δ̂({A, D}, 0110) | {A, B, D} | {A, B, D} (`{A, D} → {A, B, D} → {A, C, E} → {A, C, D} → {A, B, D}`) |
| c | δ̂({B, E}, 0100) | {A, B, D} | {A, B, D} (`{B, E} → {A, E} → {A, C, D} → {A, B, D} → {A, B, D}`) |
| d | δ̂({B, C, D}, 10100) | {A, B, D, E} | {A, B, D, E} (`{B, C, D} → {C, D, E} → {A, D, E} → {A, C, D, E} → {A, B, D, E} → {A, B, D, E}`) |

**Cadenas de prueba**

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `01` | acepta | {A} –0→ {A, B} –1→ {A, C} | 2 (aceptan: 1) |
| válida | `01110` | acepta | {A} –0→ {A, B} –1→ {A, C} –1→ {A, D} –1→ {A, E} –0→ {A, B, E} | 3 (aceptan: 1) |
| válida | `10111000` | acepta | {A} –1→ {A} –0→ {A, B} –1→ {A, C} –1→ {A, D} –1→ {A, E} –0→ {A, B, E} –0→ {A, B, E} –0→ {A, B, E} | 6 (aceptan: 1) |
| válida | `11010110100` | acepta | {A} –1→ {A} –1→ {A} –0→ {A, B} –1→ {A, C} –0→ {A, B} –1→ {A, C} –1→ {A, D} –0→ {A, B, D} –1→ {A, C, E} –0→ {A, B, E} –0→ {A, B, E} | 11 (aceptan: 1) |
| válida | `01111011010111` | acepta | {A} –0→ {A, B} –1→ {A, C} –1→ {A, D} –1→ {A, E} –1→ {A, C, D} –0→ {A, B, D} –1→ {A, C, E} –1→ {A, C, D} –0→ {A, B, D} –1→ {A, C, E} –0→ {A, B, E} –1→ {A, C, D} –1→ {A, D, E} –1→ {A, C, D, E} | 14 (aceptan: 7) |
| inválida | `λ` | rechaza | {A} | 1 (aceptan: 0) |
| inválida | `111` | rechaza | {A} –1→ {A} –1→ {A} –1→ {A} | 1 (aceptan: 0) |
| inválida | `110010` | rechaza | {A} –1→ {A} –1→ {A} –0→ {A, B} –0→ {A, B} –1→ {A, C} –0→ {A, B} | 5 (aceptan: 0) |
| inválida | `101101010` | rechaza | {A} –1→ {A} –0→ {A, B} –1→ {A, C} –1→ {A, D} –0→ {A, B, D} –1→ {A, C, E} –0→ {A, B, E} –1→ {A, C, D} –0→ {A, B, D} | 7 (aceptan: 0) |
| inválida | `111110100000` | rechaza | {A} –1→ {A} –1→ {A} –1→ {A} –1→ {A} –1→ {A} –0→ {A, B} –1→ {A, C} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} –0→ {A, B} | 21 (aceptan: 0) |

# Ejercicios 260 a 263

## Ejercicio 260

Archivo(s): `automatas/lista3-afnd/Ej_260_tabla.jff`, `automatas/conversiones/Ej_260_afd.jff`

**AFN** — AFND · 5 estados · 15 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | ∅ | B, C |
| `B` | A, B, D | C, D |
| `C` | A, C | A, E |
| `* D` | ∅ | D, E |
| `E` | A, E | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Construcción de subconjuntos, paso a paso** (δ' es la función del AFD; el estado inicial es la λ-clausura del inicial)

- δ'({A}, 0) = δ(A,0) = ∅ = ∅
- δ'({A}, 1) = δ(A,1) = {B, C} = {B, C}
- δ'({B,C}, 0) = δ(B,0) ∪ δ(C,0) = {A, B, D} ∪ {A, C} = {A, B, C, D}
- δ'({B,C}, 1) = δ(B,1) ∪ δ(C,1) = {C, D} ∪ {A, E} = {A, C, D, E}
- δ'({A,B,C,D}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(D,0) = ∅ ∪ {A, B, D} ∪ {A, C} ∪ ∅ = {A, B, C, D}
- δ'({A,B,C,D}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(D,1) = {B, C} ∪ {C, D} ∪ {A, E} ∪ {D, E} = {A, B, C, D, E}
- δ'({A,C,D,E}, 0) = δ(A,0) ∪ δ(C,0) ∪ δ(D,0) ∪ δ(E,0) = ∅ ∪ {A, C} ∪ ∅ ∪ {A, E} = {A, C, E}
- δ'({A,C,D,E}, 1) = δ(A,1) ∪ δ(C,1) ∪ δ(D,1) ∪ δ(E,1) = {B, C} ∪ {A, E} ∪ {D, E} ∪ ∅ = {A, B, C, D, E}
- δ'({A,B,C,D,E}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(D,0) ∪ δ(E,0) = ∅ ∪ {A, B, D} ∪ {A, C} ∪ ∅ ∪ {A, E} = {A, B, C, D, E}
- δ'({A,B,C,D,E}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(D,1) ∪ δ(E,1) = {B, C} ∪ {C, D} ∪ {A, E} ∪ {D, E} ∪ ∅ = {A, B, C, D, E}
- δ'({A,C,E}, 0) = δ(A,0) ∪ δ(C,0) ∪ δ(E,0) = ∅ ∪ {A, C} ∪ {A, E} = {A, C, E}
- δ'({A,C,E}, 1) = δ(A,1) ∪ δ(C,1) ∪ δ(E,1) = {B, C} ∪ {A, E} ∪ ∅ = {A, B, C, E}
- δ'({A,B,C,E}, 0) = δ(A,0) ∪ δ(B,0) ∪ δ(C,0) ∪ δ(E,0) = ∅ ∪ {A, B, D} ∪ {A, C} ∪ {A, E} = {A, B, C, D, E}
- δ'({A,B,C,E}, 1) = δ(A,1) ∪ δ(B,1) ∪ δ(C,1) ∪ δ(E,1) = {B, C} ∪ {C, D} ∪ {A, E} ∪ ∅ = {A, B, C, D, E}

**AFD equivalente** — AFD · 7 estados · 13 transiciones. Cada estado es un conjunto de estados del AFN.

| Estado | 0 | 1 |
|---|---|---|
| `→ {A}` | ∅ | {B,C} |
| `{B,C}` | {A,B,C,D} | {A,C,D,E} |
| `* {A,B,C,D}` | {A,B,C,D} | {A,B,C,D,E} |
| `* {A,C,D,E}` | {A,C,E} | {A,B,C,D,E} |
| `* {A,B,C,D,E}` | {A,B,C,D,E} | {A,B,C,D,E} |
| `{A,C,E}` | {A,C,E} | {A,B,C,E} |
| `{A,B,C,E}` | {A,B,C,D,E} | {A,B,C,D,E} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Tamaños:** AFN 5 estados → AFD 7 estados (cota 2^5 = 32); el AFD mínimo tiene 6.

**Cadenas de prueba**

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `10` | acepta | {A} –1→ {B, C} –0→ {A, B, C, D} | 5 (aceptan: 1) |
| válida | `10100` | acepta | {A} –1→ {B, C} –0→ {A, B, C, D} –1→ {A, B, C, D, E} –0→ {A, B, C, D, E} –0→ {A, B, C, D, E} | 28 (aceptan: 2) |
| válida | `10011101` | acepta | {A} –1→ {B, C} –0→ {A, B, C, D} –0→ {A, B, C, D} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –0→ {A, B, C, D, E} –1→ {A, B, C, D, E} | 73 (aceptan: 6) |
| válida | `10111000001` | acepta | {A} –1→ {B, C} –0→ {A, B, C, D} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –0→ {A, B, C, D, E} –0→ {A, B, C, D, E} –0→ {A, B, C, D, E} –0→ {A, B, C, D, E} –0→ {A, B, C, D, E} –1→ {A, B, C, D, E} | 138 (aceptan: 6) |
| válida | `11001100011001` | acepta | {A} –1→ {B, C} –1→ {A, C, D, E} –0→ {A, C, E} –0→ {A, C, E} –1→ {A, B, C, E} –1→ {A, B, C, D, E} –0→ {A, B, C, D, E} –0→ {A, B, C, D, E} –0→ {A, B, C, D, E} –1→ {A, B, C, D, E} –1→ {A, B, C, D, E} –0→ {A, B, C, D, E} –0→ {A, B, C, D, E} –1→ {A, B, C, D, E} | 150 (aceptan: 6) |
| inválida | `λ` | rechaza | {A} | 1 (aceptan: 0) |
| inválida | `011` | rechaza | {A} –0→ ∅ | 1 (aceptan: 0) |
| inválida | `010000` | rechaza | {A} –0→ ∅ | 1 (aceptan: 0) |
| inválida | `000111011` | rechaza | {A} –0→ ∅ | 1 (aceptan: 0) |
| inválida | `011100001010` | rechaza | {A} –0→ ∅ | 1 (aceptan: 0) |

> En el 260 se pide describir a detalle cómo se obtuvo: la lista de «Construcción de subconjuntos» de arriba es esa descripción.

## Ejercicio 261

Archivo(s): `automatas/lista3-afnd/Ej_261_figura.jff`, `automatas/conversiones/Ej_261_afd.jff`

**AFN** — AFND · 5 estados · 6 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ q0` | q0, q1 | q0, q3 |
| `q1` | q2 | ∅ |
| `* q2` | ∅ | ∅ |
| `q3` | ∅ | q4 |
| `q4` | ∅ | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Construcción de subconjuntos, paso a paso** (δ' es la función del AFD; el estado inicial es la λ-clausura del inicial)

- δ'({q0}, 0) = δ(q0,0) = {q0, q1} = {q0, q1}
- δ'({q0}, 1) = δ(q0,1) = {q0, q3} = {q0, q3}
- δ'({q0,q1}, 0) = δ(q0,0) ∪ δ(q1,0) = {q0, q1} ∪ {q2} = {q0, q1, q2}
- δ'({q0,q1}, 1) = δ(q0,1) ∪ δ(q1,1) = {q0, q3} ∪ ∅ = {q0, q3}
- δ'({q0,q3}, 0) = δ(q0,0) ∪ δ(q3,0) = {q0, q1} ∪ ∅ = {q0, q1}
- δ'({q0,q3}, 1) = δ(q0,1) ∪ δ(q3,1) = {q0, q3} ∪ {q4} = {q0, q3, q4}
- δ'({q0,q1,q2}, 0) = δ(q0,0) ∪ δ(q1,0) ∪ δ(q2,0) = {q0, q1} ∪ {q2} ∪ ∅ = {q0, q1, q2}
- δ'({q0,q1,q2}, 1) = δ(q0,1) ∪ δ(q1,1) ∪ δ(q2,1) = {q0, q3} ∪ ∅ ∪ ∅ = {q0, q3}
- δ'({q0,q3,q4}, 0) = δ(q0,0) ∪ δ(q3,0) ∪ δ(q4,0) = {q0, q1} ∪ ∅ ∪ ∅ = {q0, q1}
- δ'({q0,q3,q4}, 1) = δ(q0,1) ∪ δ(q3,1) ∪ δ(q4,1) = {q0, q3} ∪ {q4} ∪ ∅ = {q0, q3, q4}

**AFD equivalente** — AFD · 5 estados · 10 transiciones. Cada estado es un conjunto de estados del AFN.

| Estado | 0 | 1 |
|---|---|---|
| `→ {q0}` | {q0,q1} | {q0,q3} |
| `{q0,q1}` | {q0,q1,q2} | {q0,q3} |
| `{q0,q3}` | {q0,q1} | {q0,q3,q4} |
| `* {q0,q1,q2}` | {q0,q1,q2} | {q0,q3} |
| `{q0,q3,q4}` | {q0,q1} | {q0,q3,q4} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Tamaños:** AFN 5 estados → AFD 5 estados (cota 2^5 = 32); el AFD mínimo tiene 3.

**Cadenas de prueba**

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `00` | acepta | {q0} –0→ {q0, q1} –0→ {q0, q1, q2} | 3 (aceptan: 1) |
| válida | `10000` | acepta | {q0} –1→ {q0, q3} –0→ {q0, q1} –0→ {q0, q1, q2} –0→ {q0, q1, q2} –0→ {q0, q1, q2} | 6 (aceptan: 1) |
| válida | `11001000` | acepta | {q0} –1→ {q0, q3} –1→ {q0, q3, q4} –0→ {q0, q1} –0→ {q0, q1, q2} –1→ {q0, q3} –0→ {q0, q1} –0→ {q0, q1, q2} –0→ {q0, q1, q2} | 9 (aceptan: 1) |
| válida | `00011100000` | acepta | {q0} –0→ {q0, q1} –0→ {q0, q1, q2} –0→ {q0, q1, q2} –1→ {q0, q3} –1→ {q0, q3, q4} –1→ {q0, q3, q4} –0→ {q0, q1} –0→ {q0, q1, q2} –0→ {q0, q1, q2} –0→ {q0, q1, q2} –0→ {q0, q1, q2} | 12 (aceptan: 1) |
| válida | `10010100000100` | acepta | {q0} –1→ {q0, q3} –0→ {q0, q1} –0→ {q0, q1, q2} –1→ {q0, q3} –0→ {q0, q1} –1→ {q0, q3} –0→ {q0, q1} –0→ {q0, q1, q2} –0→ {q0, q1, q2} –0→ {q0, q1, q2} –0→ {q0, q1, q2} –1→ {q0, q3} –0→ {q0, q1} –0→ {q0, q1, q2} | 15 (aceptan: 1) |
| inválida | `λ` | rechaza | {q0} | 1 (aceptan: 0) |
| inválida | `011` | rechaza | {q0} –0→ {q0, q1} –1→ {q0, q3} –1→ {q0, q3, q4} | 4 (aceptan: 0) |
| inválida | `111011` | rechaza | {q0} –1→ {q0, q3} –1→ {q0, q3, q4} –1→ {q0, q3, q4} –0→ {q0, q1} –1→ {q0, q3} –1→ {q0, q3, q4} | 7 (aceptan: 0) |
| inválida | `101111101` | rechaza | {q0} –1→ {q0, q3} –0→ {q0, q1} –1→ {q0, q3} –1→ {q0, q3, q4} –1→ {q0, q3, q4} –1→ {q0, q3, q4} –1→ {q0, q3, q4} –0→ {q0, q1} –1→ {q0, q3} | 10 (aceptan: 0) |
| inválida | `001101110011` | rechaza | {q0} –0→ {q0, q1} –0→ {q0, q1, q2} –1→ {q0, q3} –1→ {q0, q3, q4} –0→ {q0, q1} –1→ {q0, q3} –1→ {q0, q3, q4} –1→ {q0, q3, q4} –0→ {q0, q1} –0→ {q0, q1, q2} –1→ {q0, q3} –1→ {q0, q3, q4} | 13 (aceptan: 0) |

> Los estados `q3` y `q4` no llevan a ningún estado de aceptación: son una rama muerta del AFN. Aparecen en los conjuntos del AFD pero no cambian el lenguaje, que son las cadenas que terminan en `00`.

## Ejercicio 262

Archivo(s): `automatas/lista3-afd/Ej_262_ab_ba.jff`, `automatas/conversiones/Ej_262_afd.jff`

**AFN** — AFD · 4 estados · 4 transiciones

| Estado | a | b |
|---|---|---|
| `→ q0` | q1 | q2 |
| `q1` | ∅ | q3 |
| `q2` | q3 | ∅ |
| `* q3` | ∅ | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Construcción de subconjuntos, paso a paso** (δ' es la función del AFD; el estado inicial es la λ-clausura del inicial)

- δ'({q0}, a) = δ(q0,a) = {q1} = {q1}
- δ'({q0}, b) = δ(q0,b) = {q2} = {q2}
- δ'({q1}, a) = δ(q1,a) = ∅ = ∅
- δ'({q1}, b) = δ(q1,b) = {q3} = {q3}
- δ'({q2}, a) = δ(q2,a) = {q3} = {q3}
- δ'({q2}, b) = δ(q2,b) = ∅ = ∅
- δ'({q3}, a) = δ(q3,a) = ∅ = ∅
- δ'({q3}, b) = δ(q3,b) = ∅ = ∅

**AFD equivalente** — AFD · 4 estados · 4 transiciones. Cada estado es un conjunto de estados del AFN.

| Estado | a | b |
|---|---|---|
| `→ {q0}` | {q1} | {q2} |
| `{q1}` | ∅ | {q3} |
| `{q2}` | {q3} | ∅ |
| `* {q3}` | ∅ | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Tamaños:** AFN 4 estados → AFD 4 estados (cota 2^4 = 16); el AFD mínimo tiene 4.

**Cadenas de prueba**

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `ab` | acepta | {q0} –a→ {q1} –b→ {q3} |
| válida | `ba` | acepta | {q0} –b→ {q2} –a→ {q3} |
| inválida | `λ` | rechaza | {q0} |
| inválida | `bbb` | rechaza | {q0} –b→ {q2} –b→ ∅ |
| inválida | `bbaaaa` | rechaza | {q0} –b→ {q2} –b→ ∅ |
| inválida | `babbaaaaa` | rechaza | {q0} –b→ {q2} –a→ {q3} –b→ ∅ |
| inválida | `bababbbaaaab` | rechaza | {q0} –b→ {q2} –a→ {q3} –b→ ∅ |

*El lenguaje solo tiene 2 cadena(s) válida(s); no se pueden dar 5.*

> El AFN de {ab, ba} resulta determinista (un solo destino por símbolo); la conversión solo agrega el estado `∅` al completarlo (se pidió con `completo=True`). JFLAP dará el mismo autómata sin ese estado.

## Ejercicio 263

Archivo(s): `automatas/lista3-afnd/Ej_263_figura.jff`, `automatas/conversiones/Ej_263_afd.jff`

**AFN** — AFND · 3 estados · 4 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ q0` | q0, q1 | q0 |
| `q1` | ∅ | q2 |
| `* q2` | ∅ | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Construcción de subconjuntos, paso a paso** (δ' es la función del AFD; el estado inicial es la λ-clausura del inicial)

- δ'({q0}, 0) = δ(q0,0) = {q0, q1} = {q0, q1}
- δ'({q0}, 1) = δ(q0,1) = {q0} = {q0}
- δ'({q0,q1}, 0) = δ(q0,0) ∪ δ(q1,0) = {q0, q1} ∪ ∅ = {q0, q1}
- δ'({q0,q1}, 1) = δ(q0,1) ∪ δ(q1,1) = {q0} ∪ {q2} = {q0, q2}
- δ'({q0,q2}, 0) = δ(q0,0) ∪ δ(q2,0) = {q0, q1} ∪ ∅ = {q0, q1}
- δ'({q0,q2}, 1) = δ(q0,1) ∪ δ(q2,1) = {q0} ∪ ∅ = {q0}

**AFD equivalente** — AFD · 3 estados · 6 transiciones. Cada estado es un conjunto de estados del AFN.

| Estado | 0 | 1 |
|---|---|---|
| `→ {q0}` | {q0,q1} | {q0} |
| `{q0,q1}` | {q0,q1} | {q0,q2} |
| `* {q0,q2}` | {q0,q1} | {q0} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Tamaños:** AFN 3 estados → AFD 3 estados (cota 2^3 = 8); el AFD mínimo tiene 3.

**Cadenas de prueba**

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) | Caminos |
|---|---|---|---|---|
| válida | `01` | acepta | {q0} –0→ {q0, q1} –1→ {q0, q2} | 2 (aceptan: 1) |
| válida | `10101` | acepta | {q0} –1→ {q0} –0→ {q0, q1} –1→ {q0, q2} –0→ {q0, q1} –1→ {q0, q2} | 3 (aceptan: 1) |
| válida | `10000101` | acepta | {q0} –1→ {q0} –0→ {q0, q1} –0→ {q0, q1} –0→ {q0, q1} –0→ {q0, q1} –1→ {q0, q2} –0→ {q0, q1} –1→ {q0, q2} | 6 (aceptan: 1) |
| válida | `10011001001` | acepta | {q0} –1→ {q0} –0→ {q0, q1} –0→ {q0, q1} –1→ {q0, q2} –1→ {q0} –0→ {q0, q1} –0→ {q0, q1} –1→ {q0, q2} –0→ {q0, q1} –0→ {q0, q1} –1→ {q0, q2} | 7 (aceptan: 1) |
| válida | `11111100000001` | acepta | {q0} –1→ {q0} –1→ {q0} –1→ {q0} –1→ {q0} –1→ {q0} –1→ {q0} –0→ {q0, q1} –0→ {q0, q1} –0→ {q0, q1} –0→ {q0, q1} –0→ {q0, q1} –0→ {q0, q1} –0→ {q0, q1} –1→ {q0, q2} | 8 (aceptan: 1) |
| inválida | `λ` | rechaza | {q0} | 1 (aceptan: 0) |
| inválida | `011` | rechaza | {q0} –0→ {q0, q1} –1→ {q0, q2} –1→ {q0} | 2 (aceptan: 0) |
| inválida | `010010` | rechaza | {q0} –0→ {q0, q1} –1→ {q0, q2} –0→ {q0, q1} –0→ {q0, q1} –1→ {q0, q2} –0→ {q0, q1} | 5 (aceptan: 0) |
| inválida | `100101000` | rechaza | {q0} –1→ {q0} –0→ {q0, q1} –0→ {q0, q1} –1→ {q0, q2} –0→ {q0, q1} –1→ {q0, q2} –0→ {q0, q1} –0→ {q0, q1} –0→ {q0, q1} | 7 (aceptan: 0) |
| inválida | `110111110011` | rechaza | {q0} –1→ {q0} –1→ {q0} –0→ {q0, q1} –1→ {q0, q2} –1→ {q0} –1→ {q0} –1→ {q0} –1→ {q0} –0→ {q0, q1} –0→ {q0, q1} –1→ {q0, q2} –1→ {q0} | 4 (aceptan: 0) |

