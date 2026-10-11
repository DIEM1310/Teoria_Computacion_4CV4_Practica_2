# Guía 5: expresión regular de un autómata (254 a 258)

Método de **eliminación de estados**: se agregan un estado `inicio` y un estado `fin`, y se van eliminando los estados del autómata; al quitar `k`, cada camino `p → k → q` se reemplaza por `R(p,k) R(k,k)* R(k,q)`, que se une a lo que ya hubiera en `p → q`. JFLAP lo hace con *Convert → Convert FA to RE*. Las expresiones se comprobaron contra el autómata con todas las cadenas hasta longitud 9 o más.

## Ejercicio 254

Archivo(s): `automatas/lista3-afd/Ej_254_tabla.jff`

AFD · 2 estados · 4 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | A | B |
| `* B` | A | B |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Orden de eliminación:** A, B. Aristas que quedan tras cada paso:

- quitar `A`: B → B: `1+00*1`; B → fin: `λ`; inicio → B: `0*1`
- quitar `B`: inicio → fin: `0*1(1+00*1)*`

**Expresión regular:** `0*1(1+00*1)*`

| Tipo | Cadena | Autómata | La expresión la genera |
|---|---|---|---|
| válida | `1` | acepta | sí |
| válida | `1101` | acepta | sí |
| válida | `0100001` | acepta | sí |
| válida | `01100100001` | acepta | sí |
| válida | `00100101110111` | acepta | sí |
| inválida | `λ` | rechaza | no |
| inválida | `000` | rechaza | no |
| inválida | `100110` | rechaza | no |
| inválida | `000110010` | rechaza | no |
| inválida | `000110101100` | rechaza | no |

## Ejercicio 255

Archivo(s): `automatas/lista3-afd/Ej_255_tabla.jff`

AFD · 2 estados · 4 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→* A` | B | B |
| `B` | A | B |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Orden de eliminación:** B, A. Aristas que quedan tras cada paso:

- quitar `B`: A → A: `(0+1)1*0`; A → fin: `λ`; inicio → A: `λ`
- quitar `A`: inicio → fin: `((0+1)1*0)*`

**Expresión regular:** `((0+1)1*0)*`

| Tipo | Cadena | Autómata | La expresión la genera |
|---|---|---|---|
| válida | `λ` | acepta | sí |
| válida | `1110` | acepta | sí |
| válida | `0001000` | acepta | sí |
| válida | `01110010010` | acepta | sí |
| válida | `10111110111000` | acepta | sí |
| inválida | `0` | rechaza | no |
| inválida | `0100` | rechaza | no |
| inválida | `1011111` | rechaza | no |
| inválida | `110011111` | rechaza | no |
| inválida | `111010000011` | rechaza | no |

## Ejercicio 256

Archivo(s): `automatas/lista3-afd/Ej_256_tabla.jff`

AFD · 2 estados · 6 transiciones

| Estado | 0 | 1 | 2 |
|---|---|---|---|
| `→ A` | B | A | A |
| `* B` | B | B | A |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Orden de eliminación:** A, B. Aristas que quedan tras cada paso:

- quitar `A`: B → B: `0+1+2(1+2)*0`; B → fin: `λ`; inicio → B: `(1+2)*0`
- quitar `B`: inicio → fin: `(1+2)*0(0+1+2(1+2)*0)*`

**Expresión regular:** `(1+2)*0(0+1+2(1+2)*0)*`

| Tipo | Cadena | Autómata | La expresión la genera |
|---|---|---|---|
| válida | `0` | acepta | sí |
| válida | `0010` | acepta | sí |
| válida | `1011111` | acepta | sí |
| válida | `21002001210` | acepta | sí |
| válida | `00101010000011` | acepta | sí |
| inválida | `λ` | rechaza | no |
| inválida | `11` | rechaza | no |
| inválida | `0221` | rechaza | no |
| inválida | `101021` | rechaza | no |
| inválida | `02112002` | rechaza | no |

## Ejercicio 257

Archivo(s): `automatas/lista3-afd/Ej_257_tabla.jff`

AFD · 3 estados · 6 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | B | C |
| `* B` | C | B |
| `* C` | A | A |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Orden de eliminación:** B, C, A. Aristas que quedan tras cada paso:

- quitar `B`: A → C: `1+01*0`; A → fin: `01*`; C → A: `0+1`; C → fin: `λ`; inicio → A: `λ`
- quitar `C`: A → A: `(1+01*0)(0+1)`; A → fin: `01*+1+01*0`; inicio → A: `λ`
- quitar `A`: inicio → fin: `((1+01*0)(0+1))*(01*+1+01*0)`

**Expresión regular:** `((1+01*0)(0+1))*(01*+1+01*0)`

| Tipo | Cadena | Autómata | La expresión la genera |
|---|---|---|---|
| válida | `1` | acepta | sí |
| válida | `0011` | acepta | sí |
| válida | `0000011` | acepta | sí |
| válida | `01110100001` | acepta | sí |
| válida | `11111101100011` | acepta | sí |
| inválida | `λ` | rechaza | no |
| inválida | `0100` | rechaza | no |
| inválida | `0100001` | rechaza | no |
| inválida | `111000011` | rechaza | no |
| inválida | `110001100110` | rechaza | no |

## Ejercicio 258

Archivo(s): `automatas/lista3-afd/Ej_258_tabla.jff`

AFD · 3 estados · 6 transiciones

| Estado | 0 | 1 |
|---|---|---|
| `→ A` | C | C |
| `B` | A | C |
| `* C` | B | A |

`→` estado inicial, `*` estado de aceptación, `∅` ninguna transición.

**Orden de eliminación:** B, A, C. Aristas que quedan tras cada paso:

- quitar `B`: A → C: `0+1`; C → A: `1+00`; C → C: `01`; C → fin: `λ`; inicio → A: `λ`
- quitar `A`: C → C: `01+(1+00)(0+1)`; C → fin: `λ`; inicio → C: `0+1`
- quitar `C`: inicio → fin: `(0+1)(01+(1+00)(0+1))*`

**Expresión regular:** `(0+1)(01+(1+00)(0+1))*`

| Tipo | Cadena | Autómata | La expresión la genera |
|---|---|---|---|
| válida | `1` | acepta | sí |
| válida | `10111` | acepta | sí |
| válida | `11111001` | acepta | sí |
| válida | `11001011011` | acepta | sí |
| válida | `10011100000110` | acepta | sí |
| inválida | `λ` | rechaza | no |
| inválida | `0110` | rechaza | no |
| inválida | `0001100` | rechaza | no |
| inválida | `011011000` | rechaza | no |
| inválida | `011100000000` | rechaza | no |

