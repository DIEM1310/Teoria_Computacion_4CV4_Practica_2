# Guía 1: simplificar AFD (151 a 157) y describir AFN (158 a 161)

Los ejercicios 151 a 155 piden dibujar el autómata de la tabla y **quitar los estados inaccesibles**; los 156 y 157, simplificarlo con una **partición** y/o quitando los inaccesibles. Para todos se da también el AFD mínimo (opcional en 151 a 155).

## Ejercicio 151

Archivo(s): `automatas/lista3-afd/Ej_151_original.jff`, `automatas/lista3-afd/Ej_151_minimo.jff`

**Autómata del enunciado** — AFD · 10 estados · 20 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | C | E |
| `B` | F | E |
| `* C` | A | G |
| `D` | C | E |
| `* E` | I | B |
| `* F` | D | H |
| `G` | F | I |
| `H` | C | J |
| `I` | J | E |
| `J` | I | E |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Estados inaccesibles:** ninguno; todos se alcanzan desde el inicial. Quitarlos no cambia el autómata.

**Partición (método de refinamiento).** La primera ronda separa aceptación de no aceptación; cada ronda separa los estados que, con algún símbolo, van a clases distintas; termina cuando ya no cambia.

- Partición 0: {A, B, D, G, H, I, J}  {C, E, F}
- Partición 1: {A, B, D}  {C, E, F}  {G, H}  {I, J}
- Partición 2: {A, B, D}  {C, F}  {E}  {G, H}  {I, J}

**AFD mínimo** — AFD · 5 estados · 10 transiciones. Los estados de una misma clase son equivalentes.

| Estado | 0 | 1 |
|---|---|---|
| `→ {A,B,D}` | {C,F} | E |
| `* {C,F}` | {A,B,D} | {G,H} |
| `* E` | {I,J} | {A,B,D} |
| `{G,H}` | {C,F} | {I,J} |
| `{I,J}` | {I,J} | E |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (valen para el original y para el simplificado: reconocen el mismo lenguaje).

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `0` | acepta | {A} –0→ {C} |
| válida | `00010` | acepta | {A} –0→ {C} –0→ {A} –0→ {C} –1→ {G} –0→ {F} |
| válida | `10011000` | acepta | {A} –1→ {E} –0→ {I} –0→ {J} –1→ {E} –1→ {B} –0→ {F} –0→ {D} –0→ {C} |
| válida | `00010000110` | acepta | {A} –0→ {C} –0→ {A} –0→ {C} –1→ {G} –0→ {F} –0→ {D} –0→ {C} –0→ {A} –1→ {E} –1→ {B} –0→ {F} |
| válida | `00111101100101` | acepta | {A} –0→ {C} –0→ {A} –1→ {E} –1→ {B} –1→ {E} –1→ {B} –0→ {F} –1→ {H} –1→ {J} –0→ {I} –0→ {J} –1→ {E} –0→ {I} –1→ {E} |
| inválida | `λ` | rechaza | {A} |
| inválida | `1101` | rechaza | {A} –1→ {E} –1→ {B} –0→ {F} –1→ {H} |
| inválida | `0000100` | rechaza | {A} –0→ {C} –0→ {A} –0→ {C} –0→ {A} –1→ {E} –0→ {I} –0→ {J} |
| inválida | `011110000` | rechaza | {A} –0→ {C} –1→ {G} –1→ {I} –1→ {E} –1→ {B} –0→ {F} –0→ {D} –0→ {C} –0→ {A} |
| inválida | `100000001111` | rechaza | {A} –1→ {E} –0→ {I} –0→ {J} –0→ {I} –0→ {J} –0→ {I} –0→ {J} –0→ {I} –1→ {E} –1→ {B} –1→ {E} –1→ {B} |

## Ejercicio 152

Archivo(s): `automatas/lista3-afd/Ej_152_original.jff`, `automatas/lista3-afd/Ej_152_minimo.jff`

**Autómata del enunciado** — AFD · 6 estados · 18 transiciones

| Estado | 0 | 1 | 2 |
|---|---|---|---|
| `→ A` | C | E | B |
| `B` | D | E | B |
| `C` | A | D | F |
| `* D` | F | B | C |
| `* E` | F | B | A |
| `* F` | D | B | C |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Estados inaccesibles:** ninguno; todos se alcanzan desde el inicial. Quitarlos no cambia el autómata.

**Partición (método de refinamiento).** La primera ronda separa aceptación de no aceptación; cada ronda separa los estados que, con algún símbolo, van a clases distintas; termina cuando ya no cambia.

- Partición 0: {A, B, C}  {D, E, F}
- Partición 1: {A}  {B}  {C}  {D, E, F}
- Partición 2: {A}  {B}  {C}  {D, F}  {E}

**AFD mínimo** — AFD · 5 estados · 15 transiciones. Los estados de una misma clase son equivalentes.

| Estado | 0 | 1 | 2 |
|---|---|---|---|
| `→ A` | C | E | B |
| `B` | {D,F} | E | B |
| `C` | A | {D,F} | {D,F} |
| `* {D,F}` | {D,F} | B | C |
| `* E` | {D,F} | B | A |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (valen para el original y para el simplificado: reconocen el mismo lenguaje).

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `1` | acepta | {A} –1→ {E} |
| válida | `0111` | acepta | {A} –0→ {C} –1→ {D} –1→ {B} –1→ {E} |
| válida | `2100121` | acepta | {A} –2→ {B} –1→ {E} –0→ {F} –0→ {D} –1→ {B} –2→ {B} –1→ {E} |
| válida | `12222021210` | acepta | {A} –1→ {E} –2→ {A} –2→ {B} –2→ {B} –2→ {B} –0→ {D} –2→ {C} –1→ {D} –2→ {C} –1→ {D} –0→ {F} |
| válida | `21101222022022` | acepta | {A} –2→ {B} –1→ {E} –1→ {B} –0→ {D} –1→ {B} –2→ {B} –2→ {B} –2→ {B} –0→ {D} –2→ {C} –2→ {F} –0→ {D} –2→ {C} –2→ {F} |
| inválida | `λ` | rechaza | {A} |
| inválida | `00` | rechaza | {A} –0→ {C} –0→ {A} |
| inválida | `2020` | rechaza | {A} –2→ {B} –0→ {D} –2→ {C} –0→ {A} |
| inválida | `100212` | rechaza | {A} –1→ {E} –0→ {F} –0→ {D} –2→ {C} –1→ {D} –2→ {C} |
| inválida | `10211112` | rechaza | {A} –1→ {E} –0→ {F} –2→ {C} –1→ {D} –1→ {B} –1→ {E} –1→ {B} –2→ {B} |

## Ejercicio 153

Archivo(s): `automatas/lista3-afd/Ej_153_original.jff`, `automatas/lista3-afd/Ej_153_minimo.jff`

**Autómata del enunciado** — AFD · 7 estados · 14 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | B | C |
| `B` | D | E |
| `C` | F | G |
| `* D` | D | E |
| `E` | F | G |
| `* F` | E | D |
| `* G` | F | G |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Estados inaccesibles:** ninguno; todos se alcanzan desde el inicial. Quitarlos no cambia el autómata.

**Partición (método de refinamiento).** La primera ronda separa aceptación de no aceptación; cada ronda separa los estados que, con algún símbolo, van a clases distintas; termina cuando ya no cambia.

- Partición 0: {A, B, C, E}  {D, F, G}
- Partición 1: {A}  {B}  {C, E}  {D}  {F}  {G}

**AFD mínimo** — AFD · 6 estados · 12 transiciones. Los estados de una misma clase son equivalentes.

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | B | {C,E} |
| `B` | D | {C,E} |
| `{C,E}` | F | G |
| `* D` | D | {C,E} |
| `* F` | {C,E} | D |
| `* G` | F | G |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (valen para el original y para el simplificado: reconocen el mismo lenguaje).

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `10` | acepta | {A} –1→ {C} –0→ {F} |
| válida | `01110` | acepta | {A} –0→ {B} –1→ {E} –1→ {G} –1→ {G} –0→ {F} |
| válida | `10110100` | acepta | {A} –1→ {C} –0→ {F} –1→ {D} –1→ {E} –0→ {F} –1→ {D} –0→ {D} –0→ {D} |
| válida | `10001110010` | acepta | {A} –1→ {C} –0→ {F} –0→ {E} –0→ {F} –1→ {D} –1→ {E} –1→ {G} –0→ {F} –0→ {E} –1→ {G} –0→ {F} |
| válida | `10001011001110` | acepta | {A} –1→ {C} –0→ {F} –0→ {E} –0→ {F} –1→ {D} –0→ {D} –1→ {E} –1→ {G} –0→ {F} –0→ {E} –1→ {G} –1→ {G} –1→ {G} –0→ {F} |
| inválida | `λ` | rechaza | {A} |
| inválida | `100` | rechaza | {A} –1→ {C} –0→ {F} –0→ {E} |
| inválida | `010101` | rechaza | {A} –0→ {B} –1→ {E} –0→ {F} –1→ {D} –0→ {D} –1→ {E} |
| inválida | `011001011` | rechaza | {A} –0→ {B} –1→ {E} –1→ {G} –0→ {F} –0→ {E} –1→ {G} –0→ {F} –1→ {D} –1→ {E} |
| inválida | `011100010100` | rechaza | {A} –0→ {B} –1→ {E} –1→ {G} –1→ {G} –0→ {F} –0→ {E} –0→ {F} –1→ {D} –0→ {D} –1→ {E} –0→ {F} –0→ {E} |

## Ejercicio 154

Archivo(s): `automatas/lista3-afd/Ej_154_original.jff`, `automatas/lista3-afd/Ej_154_sin_inaccesibles.jff`, `automatas/lista3-afd/Ej_154_minimo.jff`

**Autómata del enunciado** — AFD · 11 estados · 22 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | D | K |
| `B` | H | K |
| `C` | I | E |
| `D` | C | G |
| `* E` | K | I |
| `F` | B | E |
| `* G` | C | I |
| `* H` | C | B |
| `I` | G | K |
| `* J` | F | B |
| `K` | C | F |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Estados inaccesibles:** J (ningún camino desde A llega a ellos).

**Sin inaccesibles** — AFD · 10 estados · 20 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | D | K |
| `B` | H | K |
| `C` | I | E |
| `D` | C | G |
| `* E` | K | I |
| `F` | B | E |
| `* G` | C | I |
| `* H` | C | B |
| `I` | G | K |
| `K` | C | F |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Partición (método de refinamiento).** La primera ronda separa aceptación de no aceptación; cada ronda separa los estados que, con algún símbolo, van a clases distintas; termina cuando ya no cambia.

- Partición 0: {A, B, C, D, F, I, K}  {E, G, H}
- Partición 1: {A, K}  {B, I}  {C, D, F}  {E, G, H}
- Partición 2: {A}  {B, I}  {C, F}  {D}  {E}  {G, H}  {K}

**AFD mínimo** — AFD · 7 estados · 14 transiciones. Los estados de una misma clase son equivalentes.

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | D | K |
| `{B,I}` | {G,H} | K |
| `{C,F}` | {B,I} | E |
| `D` | {C,F} | {G,H} |
| `* E` | K | {B,I} |
| `* {G,H}` | {C,F} | {B,I} |
| `K` | {C,F} | {C,F} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (valen para el original y para el simplificado: reconocen el mismo lenguaje).

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `01` | acepta | {A} –0→ {D} –1→ {G} |
| válida | `00110` | acepta | {A} –0→ {D} –0→ {C} –1→ {E} –1→ {I} –0→ {G} |
| válida | `01101010` | acepta | {A} –0→ {D} –1→ {G} –1→ {I} –0→ {G} –1→ {I} –0→ {G} –1→ {I} –0→ {G} |
| válida | `00010001001` | acepta | {A} –0→ {D} –0→ {C} –0→ {I} –1→ {K} –0→ {C} –0→ {I} –0→ {G} –1→ {I} –0→ {G} –0→ {C} –1→ {E} |
| válida | `01000101001011` | acepta | {A} –0→ {D} –1→ {G} –0→ {C} –0→ {I} –0→ {G} –1→ {I} –0→ {G} –1→ {I} –0→ {G} –0→ {C} –1→ {E} –0→ {K} –1→ {F} –1→ {E} |
| inválida | `λ` | rechaza | {A} |
| inválida | `011` | rechaza | {A} –0→ {D} –1→ {G} –1→ {I} |
| inválida | `001010` | rechaza | {A} –0→ {D} –0→ {C} –1→ {E} –0→ {K} –1→ {F} –0→ {B} |
| inválida | `101010100` | rechaza | {A} –1→ {K} –0→ {C} –1→ {E} –0→ {K} –1→ {F} –0→ {B} –1→ {K} –0→ {C} –0→ {I} |
| inválida | `110110010110` | rechaza | {A} –1→ {K} –1→ {F} –0→ {B} –1→ {K} –1→ {F} –0→ {B} –0→ {H} –1→ {B} –0→ {H} –1→ {B} –1→ {K} –0→ {C} |

## Ejercicio 155

Archivo(s): `automatas/lista3-afd/Ej_155_original.jff`, `automatas/lista3-afd/Ej_155_sin_inaccesibles.jff`, `automatas/lista3-afd/Ej_155_minimo.jff`

**Autómata del enunciado** — AFD · 12 estados · 24 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | B | C |
| `B` | D | E |
| `C` | K | G |
| `D` | H | E |
| `E` | F | D |
| `* F` | J | G |
| `G` | E | G |
| `H` | B | K |
| `I` | C | A |
| `J` | D | G |
| `K` | F | D |
| `L` | C | J |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Estados inaccesibles:** I, L (ningún camino desde A llega a ellos).

**Sin inaccesibles** — AFD · 10 estados · 20 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | B | C |
| `B` | D | E |
| `C` | K | G |
| `D` | H | E |
| `E` | F | D |
| `* F` | J | G |
| `G` | E | G |
| `H` | B | K |
| `J` | D | G |
| `K` | F | D |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Partición (método de refinamiento).** La primera ronda separa aceptación de no aceptación; cada ronda separa los estados que, con algún símbolo, van a clases distintas; termina cuando ya no cambia.

- Partición 0: {A, B, C, D, E, G, H, J, K}  {F}
- Partición 1: {A, B, C, D, G, H, J}  {E, K}  {F}
- Partición 2: {A, J}  {B, D, H}  {C, G}  {E, K}  {F}

**AFD mínimo** — AFD · 5 estados · 10 transiciones. Los estados de una misma clase son equivalentes.

| Estado | 0 | 1 |
|---|---|---|
| `→ {A,J}` | {B,D,H} | {C,G} |
| `{B,D,H}` | {B,D,H} | {E,K} |
| `{C,G}` | {E,K} | {C,G} |
| `{E,K}` | F | {B,D,H} |
| `* F` | {A,J} | {C,G} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (valen para el original y para el simplificado: reconocen el mismo lenguaje).

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `100` | acepta | {A} –1→ {C} –0→ {K} –0→ {F} |
| válida | `111100` | acepta | {A} –1→ {C} –1→ {G} –1→ {G} –1→ {G} –0→ {E} –0→ {F} |
| válida | `001001100` | acepta | {A} –0→ {B} –0→ {D} –1→ {E} –0→ {F} –0→ {J} –1→ {G} –1→ {G} –0→ {E} –0→ {F} |
| válida | `01010111010` | acepta | {A} –0→ {B} –1→ {E} –0→ {F} –1→ {G} –0→ {E} –1→ {D} –1→ {E} –1→ {D} –0→ {H} –1→ {K} –0→ {F} |
| válida | `01011111011110` | acepta | {A} –0→ {B} –1→ {E} –0→ {F} –1→ {G} –1→ {G} –1→ {G} –1→ {G} –1→ {G} –0→ {E} –1→ {D} –1→ {E} –1→ {D} –1→ {E} –0→ {F} |
| inválida | `λ` | rechaza | {A} |
| inválida | `110` | rechaza | {A} –1→ {C} –1→ {G} –0→ {E} |
| inválida | `101000` | rechaza | {A} –1→ {C} –0→ {K} –1→ {D} –0→ {H} –0→ {B} –0→ {D} |
| inválida | `110100101` | rechaza | {A} –1→ {C} –1→ {G} –0→ {E} –1→ {D} –0→ {H} –0→ {B} –1→ {E} –0→ {F} –1→ {G} |
| inválida | `010101001001` | rechaza | {A} –0→ {B} –1→ {E} –0→ {F} –1→ {G} –0→ {E} –1→ {D} –0→ {H} –0→ {B} –1→ {E} –0→ {F} –0→ {J} –1→ {G} |

## Ejercicio 156

Archivo(s): `automatas/lista3-afd/Ej_156_original.jff`, `automatas/lista3-afd/Ej_156_minimo.jff`

**Autómata del enunciado** — AFD · 5 estados · 10 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | B | C |
| `B` | C | E |
| `C` | D | C |
| `D` | C | E |
| `* E` | B | E |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Estados inaccesibles:** ninguno; todos se alcanzan desde el inicial. Quitarlos no cambia el autómata.

**Partición (método de refinamiento).** La primera ronda separa aceptación de no aceptación; cada ronda separa los estados que, con algún símbolo, van a clases distintas; termina cuando ya no cambia.

- Partición 0: {A, B, C, D}  {E}
- Partición 1: {A, C}  {B, D}  {E}

**AFD mínimo** — AFD · 3 estados · 6 transiciones. Los estados de una misma clase son equivalentes.

| Estado | 0 | 1 |
|---|---|---|
| `→ {A,C}` | {B,D} | {A,C} |
| `{B,D}` | {A,C} | E |
| `* E` | {B,D} | E |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (valen para el original y para el simplificado: reconocen el mismo lenguaje).

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `01` | acepta | {A} –0→ {B} –1→ {E} |
| válida | `11011` | acepta | {A} –1→ {C} –1→ {C} –0→ {D} –1→ {E} –1→ {E} |
| válida | `00111011` | acepta | {A} –0→ {B} –0→ {C} –1→ {C} –1→ {C} –1→ {C} –0→ {D} –1→ {E} –1→ {E} |
| válida | `00111000001` | acepta | {A} –0→ {B} –0→ {C} –1→ {C} –1→ {C} –1→ {C} –0→ {D} –0→ {C} –0→ {D} –0→ {C} –0→ {D} –1→ {E} |
| válida | `11100011101011` | acepta | {A} –1→ {C} –1→ {C} –1→ {C} –0→ {D} –0→ {C} –0→ {D} –1→ {E} –1→ {E} –1→ {E} –0→ {B} –1→ {E} –0→ {B} –1→ {E} –1→ {E} |
| inválida | `λ` | rechaza | {A} |
| inválida | `100` | rechaza | {A} –1→ {C} –0→ {D} –0→ {C} |
| inválida | `100111` | rechaza | {A} –1→ {C} –0→ {D} –0→ {C} –1→ {C} –1→ {C} –1→ {C} |
| inválida | `110100110` | rechaza | {A} –1→ {C} –1→ {C} –0→ {D} –1→ {E} –0→ {B} –0→ {C} –1→ {C} –1→ {C} –0→ {D} |
| inválida | `100011011001` | rechaza | {A} –1→ {C} –0→ {D} –0→ {C} –0→ {D} –1→ {E} –1→ {E} –0→ {B} –1→ {E} –1→ {E} –0→ {B} –0→ {C} –1→ {C} |

## Ejercicio 157

Archivo(s): `automatas/lista3-afd/Ej_157_original.jff`, `automatas/lista3-afd/Ej_157_minimo.jff`

**Autómata del enunciado** — AFD · 6 estados · 12 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | B | F |
| `B` | C | E |
| `C` | D | E |
| `D` | B | E |
| `E` | F | D |
| `* F` | F | B |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Estados inaccesibles:** ninguno; todos se alcanzan desde el inicial. Quitarlos no cambia el autómata.

**Partición (método de refinamiento).** La primera ronda separa aceptación de no aceptación; cada ronda separa los estados que, con algún símbolo, van a clases distintas; termina cuando ya no cambia.

- Partición 0: {A, B, C, D, E}  {F}
- Partición 1: {A}  {B, C, D}  {E}  {F}

**AFD mínimo** — AFD · 4 estados · 8 transiciones. Los estados de una misma clase son equivalentes.

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | {B,C,D} | F |
| `{B,C,D}` | {B,C,D} | E |
| `E` | F | {B,C,D} |
| `* F` | F | {B,C,D} |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Cadenas de prueba** (valen para el original y para el simplificado: reconocen el mismo lenguaje).

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `1` | acepta | {A} –1→ {F} |
| válida | `1110` | acepta | {A} –1→ {F} –1→ {B} –1→ {E} –0→ {F} |
| válida | `1110000` | acepta | {A} –1→ {F} –1→ {B} –1→ {E} –0→ {F} –0→ {F} –0→ {F} –0→ {F} |
| válida | `10110010100` | acepta | {A} –1→ {F} –0→ {F} –1→ {B} –1→ {E} –0→ {F} –0→ {F} –1→ {B} –0→ {C} –1→ {E} –0→ {F} –0→ {F} |
| válida | `11010111011100` | acepta | {A} –1→ {F} –1→ {B} –0→ {C} –1→ {E} –0→ {F} –1→ {B} –1→ {E} –1→ {D} –0→ {B} –1→ {E} –1→ {D} –1→ {E} –0→ {F} –0→ {F} |
| inválida | `λ` | rechaza | {A} |
| inválida | `011` | rechaza | {A} –0→ {B} –1→ {E} –1→ {D} |
| inválida | `100101` | rechaza | {A} –1→ {F} –0→ {F} –0→ {F} –1→ {B} –0→ {C} –1→ {E} |
| inválida | `111010001` | rechaza | {A} –1→ {F} –1→ {B} –1→ {E} –0→ {F} –1→ {B} –0→ {C} –0→ {D} –0→ {B} –1→ {E} |
| inválida | `001011111000` | rechaza | {A} –0→ {B} –0→ {C} –1→ {E} –0→ {F} –1→ {B} –1→ {E} –1→ {D} –1→ {E} –1→ {D} –0→ {B} –0→ {C} –0→ {D} |

# Ejercicios 158 a 161: qué hace cada autómata

Aunque el enunciado los llama AFN, **ninguno tiene dos transiciones con el mismo símbolo desde un estado**: son AFD parciales (si falta la transición, la cadena se rechaza).

## Ejercicio 158

Archivo(s): `automatas/lista3-afd/Ej_158_figura.jff`

AFD · 3 estados · 2 transiciones. **Lenguaje:** {01}: solo la cadena `01`.

| Estado | 0 | 1 |
|---|---|---|
| `→ q1` | q2 | ∅ |
| `q2` | ∅ | q3 |
| `* q3` | ∅ | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `01` | acepta | {q1} –0→ {q2} –1→ {q3} |
| inválida | `λ` | rechaza | {q1} |
| inválida | `011` | rechaza | {q1} –0→ {q2} –1→ {q3} –1→ ∅ |
| inválida | `101101` | rechaza | {q1} –1→ ∅ |
| inválida | `000110000` | rechaza | {q1} –0→ {q2} –0→ ∅ |
| inválida | `001111100010` | rechaza | {q1} –0→ {q2} –0→ ∅ |

*El lenguaje solo tiene 1 cadena(s) válida(s); no se pueden dar 5.*

## Ejercicio 159

Archivo(s): `automatas/lista3-afd/Ej_159_figura.jff`

AFD · 3 estados · 3 transiciones. **Lenguaje:** `1*01`: cualquier cantidad de unos, luego `01`.

| Estado | 0 | 1 |
|---|---|---|
| `→ q1` | q2 | q1 |
| `q2` | ∅ | q3 |
| `* q3` | ∅ | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `01` | acepta | {q1} –0→ {q2} –1→ {q3} |
| válida | `11101` | acepta | {q1} –1→ {q1} –1→ {q1} –1→ {q1} –0→ {q2} –1→ {q3} |
| válida | `11111101` | acepta | {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –0→ {q2} –1→ {q3} |
| válida | `11111111101` | acepta | {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –0→ {q2} –1→ {q3} |
| válida | `11111111111101` | acepta | {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –1→ {q1} –0→ {q2} –1→ {q3} |
| inválida | `λ` | rechaza | {q1} |
| inválida | `010` | rechaza | {q1} –0→ {q2} –1→ {q3} –0→ ∅ |
| inválida | `101100` | rechaza | {q1} –1→ {q1} –0→ {q2} –1→ {q3} –1→ ∅ |
| inválida | `011110000` | rechaza | {q1} –0→ {q2} –1→ {q3} –1→ ∅ |
| inválida | `011011010011` | rechaza | {q1} –0→ {q2} –1→ {q3} –1→ ∅ |

## Ejercicio 160

Archivo(s): `automatas/lista3-afd/Ej_160_figura.jff`

AFD · 3 estados · 4 transiciones. **Lenguaje:** `01(0+1)*`: las cadenas que empiezan con `01`.

| Estado | 0 | 1 |
|---|---|---|
| `→ q1` | q2 | ∅ |
| `q2` | ∅ | q3 |
| `* q3` | q3 | q3 |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `01` | acepta | {q1} –0→ {q2} –1→ {q3} |
| válida | `01110` | acepta | {q1} –0→ {q2} –1→ {q3} –1→ {q3} –1→ {q3} –0→ {q3} |
| válida | `01001110` | acepta | {q1} –0→ {q2} –1→ {q3} –0→ {q3} –0→ {q3} –1→ {q3} –1→ {q3} –1→ {q3} –0→ {q3} |
| válida | `01000010011` | acepta | {q1} –0→ {q2} –1→ {q3} –0→ {q3} –0→ {q3} –0→ {q3} –0→ {q3} –1→ {q3} –0→ {q3} –0→ {q3} –1→ {q3} –1→ {q3} |
| válida | `01010001111111` | acepta | {q1} –0→ {q2} –1→ {q3} –0→ {q3} –1→ {q3} –0→ {q3} –0→ {q3} –0→ {q3} –1→ {q3} –1→ {q3} –1→ {q3} –1→ {q3} –1→ {q3} –1→ {q3} –1→ {q3} |
| inválida | `λ` | rechaza | {q1} |
| inválida | `111` | rechaza | {q1} –1→ ∅ |
| inválida | `110000` | rechaza | {q1} –1→ ∅ |
| inválida | `110000001` | rechaza | {q1} –1→ ∅ |
| inválida | `100000010110` | rechaza | {q1} –1→ ∅ |

## Ejercicio 161

Archivo(s): `automatas/lista3-afd/Ej_161_figura.jff`

AFD · 3 estados · 3 transiciones. **Lenguaje:** `(010)*(λ+01)`: repeticiones de `010`, y a lo más un `01` al final.

| Estado | 0 | 1 |
|---|---|---|
| `→* q1` | q2 | ∅ |
| `q2` | ∅ | q3 |
| `* q3` | q1 | ∅ |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

| Tipo | Cadena | Esperado | Recorrido (estados activos tras cada símbolo) |
|---|---|---|---|
| válida | `λ` | acepta | {q1} |
| válida | `010` | acepta | {q1} –0→ {q2} –1→ {q3} –0→ {q1} |
| válida | `010010` | acepta | {q1} –0→ {q2} –1→ {q3} –0→ {q1} –0→ {q2} –1→ {q3} –0→ {q1} |
| válida | `01001001001` | acepta | {q1} –0→ {q2} –1→ {q3} –0→ {q1} –0→ {q2} –1→ {q3} –0→ {q1} –0→ {q2} –1→ {q3} –0→ {q1} –0→ {q2} –1→ {q3} |
| válida | `01001001001001` | acepta | {q1} –0→ {q2} –1→ {q3} –0→ {q1} –0→ {q2} –1→ {q3} –0→ {q1} –0→ {q2} –1→ {q3} –0→ {q1} –0→ {q2} –1→ {q3} –0→ {q1} –0→ {q2} –1→ {q3} |
| inválida | `1` | rechaza | {q1} –1→ ∅ |
| inválida | `0011` | rechaza | {q1} –0→ {q2} –0→ ∅ |
| inválida | `1100000` | rechaza | {q1} –1→ ∅ |
| inválida | `001100010` | rechaza | {q1} –0→ {q2} –0→ ∅ |
| inválida | `010101010100` | rechaza | {q1} –0→ {q2} –1→ {q3} –0→ {q1} –1→ ∅ |

