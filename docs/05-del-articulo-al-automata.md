# 5. Del artículo al autómata: el fantasma de Pac-Man

## 5.1 Aplicación elegida y fuente

La aplicación es el **comportamiento de un fantasma de Pac-Man**, que Gribkoff (2013, sección 4 y Figura 3) presenta como un AFD de cuatro estados. El enunciado propone esta fuente para el Ejercicio 5. Es un documento de curso y no un artículo con DOI, así que no sirve como fuente de la investigación del Ejercicio 4; aquí se usa solo porque el enunciado lo pide.

Lo que dice la fuente: el fantasma tiene cuatro comportamientos, que corresponden a un AFD de cuatro estados, y las transiciones las dicta la situación del juego. Los estados son «Wander the Maze» (inicial), «Chase Pac-Man», «Flee Pac-Man» y «Return to Base». La Figura 3 tiene siete flechas:

| De | Evento (nombre en la figura) | A |
|---|---|---|
| Wander the Maze | Spot Pac-Man | Chase Pac-Man |
| Chase Pac-Man | Lose Pac-Man | Wander the Maze |
| Wander the Maze | Pac-Man Eats Power Pellet | Flee Pac-Man |
| Chase Pac-Man | Pac-Man Eats Power Pellet | Flee Pac-Man |
| Flee Pac-Man | Power Pellet Expires | Wander the Maze |
| Flee Pac-Man | Eaten by Pac-Man | Return to Base |
| Return to Base | Reach Central Base | Wander the Maze |

En la figura, las dos flechas curvas entre «Wander the Maze» y «Flee Pac-Man» se distinguen por la punta: la que termina en «Flee» es «Pac-Man Eats Power Pellet» y la que termina en «Wander» es «Power Pellet Expires».

## 5.2 El modelo: un AFD

Sí basta un **AFD**: en cada estado, cada evento lleva a exactamente un estado. La figura de Gribkoff no define todas las flechas (por ejemplo, qué pasa con «Spot Pac-Man» cuando el fantasma ya huye). Para tener una función de transición total, se decidió que **un evento que no aparece en la figura deja el estado igual** (es un lazo): el evento ocurre, pero no cambia el comportamiento.

El alfabeto Σ es el conjunto de **eventos del juego**; una cadena es una secuencia de eventos en el orden en que ocurren. Cada evento es un solo carácter, porque el simulador lee la cadena símbolo por símbolo.

| Símbolo | Evento |
|---|---|
| `v` | el fantasma ve a Pac-Man (*Spot Pac-Man*) |
| `p` | el fantasma pierde a Pac-Man (*Lose Pac-Man*) |
| `c` | Pac-Man come una pastilla de poder (*Pac-Man Eats Power Pellet*) |
| `e` | se acaba el efecto de la pastilla (*Power Pellet Expires*) |
| `m` | Pac-Man se come al fantasma (*Eaten by Pac-Man*) |
| `b` | el fantasma llega a la base central (*Reach Central Base*) |
| `a` | **nuevo:** quedan pocos segundos de pastilla (alerta de fin) |
| `r` | **nuevo:** el fantasma termina de regenerarse |

### Quíntupla M = (Q, Σ, δ, q₀, F)

- Q = {q0, q1, q2, q3, q4, q5}
- Σ = {v, p, c, e, m, b, a, r}
- q₀ = q0
- F = {q1}
- δ: tabla de abajo (es total: 6 × 8 = 48 transiciones).

| Estado | Nombre | Significado | Origen |
|---|---|---|---|
| q0 | Vagar | recorre el laberinto sin objetivo; estado inicial | Figura 3 |
| q1 | Perseguir | Pac-Man está a la vista y el fantasma lo persigue; **único estado de aceptación** | Figura 3 |
| q2 | Huir | Pac-Man comió una pastilla: el fantasma es vulnerable y huye | Figura 3 |
| q3 | Regresar | Pac-Man se comió al fantasma: solo vuelve a la base | Figura 3 |
| q4 | Parpadear | quedan pocos segundos de pastilla; el fantasma sigue vulnerable | **nuevo** |
| q5 | Regenerar | el fantasma está en la base, regenerándose, y no se puede comer | **nuevo** |

Tabla de transiciones (solo cambian de estado las celdas marcadas con →; las demás son lazos):

| δ | v | p | c | e | m | b | a | r |
|---|---|---|---|---|---|---|---|---|
| **q0** | → q1 | q0 | → q2 | q0 | q0 | q0 | q0 | q0 |
| **q1** | q1 | → q0 | → q2 | q1 | q1 | q1 | q1 | q1 |
| **q2** | q2 | q2 | q2 | q2 | → q3 | q2 | → q4 | q2 |
| **q3** | q3 | q3 | q3 | q3 | q3 | → q5 | q3 | q3 |
| **q4** | q4 | q4 | → q2 | → q0 | → q3 | q4 | q4 | q4 |
| **q5** | q5 | q5 | q5 | q5 | q5 | q5 | q5 | → q0 |

**Por qué F = {q1}.** La figura de Gribkoff no marca estados de aceptación, y un AFD los necesita. Se eligió «el fantasma persigue a Pac-Man» porque da una pregunta con sentido: *¿esta secuencia de eventos deja a Pac-Man siendo perseguido?* El lenguaje aceptado es el de las secuencias de eventos que terminan en q1. Es una decisión de modelado, no algo que diga la fuente.

## 5.3 Ampliación: dos estados y dos eventos nuevos

El enunciado pide ampliar el modelo con **al menos dos estados y dos eventos nuevos** y justificarlo. Las dos ampliaciones **parten en dos pasos una flecha de la figura**:

1. **Regenerar (q5) y el evento `r`.** La figura lleva «Return to Base» directo a «Wander» con «Reach Central Base». Pero el propio texto de Gribkoff dice que el fantasma regresa a la base central «to regenerate», y esa regeneración no aparece en la figura. Ahora `b` lleva a Regenerar y `r` (termina de regenerarse) lleva a Vagar. Se gana una propiedad que el modelo original no puede expresar: **un fantasma recién devorado no persigue, aunque vea a Pac-Man** (casos 11 y 12).
2. **Parpadear (q4) y el evento `a`.** En la figura, «Power Pellet Expires» sale de «Flee» directo. Ahora Huir pasa a Parpadear con `a` (quedan pocos segundos) y solo de ahí se sale con `e`. Se gana la distinción entre el principio y el final del efecto de la pastilla: desde Parpadear, otra pastilla (`c`) reinicia la huida (caso 13) y `e` ya no tiene efecto en Huir (caso 8).

Con esto el autómata pasa de 4 a 6 estados y de 6 a 8 eventos. Siguen siendo estados que se pueden alcanzar y distinguir: el simulador lo confirma (6 accesibles, 6 tras minimizar).

Las dos ampliaciones son **decisiones de diseño propias**: el texto de Gribkoff apoya solo la regeneración. No se afirma que coincidan con las reglas del Pac-Man original, porque no se usó ninguna fuente sobre ellas; Parpadear es una ampliación propuesta.

## 5.4 Archivos y verificación en el simulador

- Autómata: `automatas/aplicacion/Pacman_fantasma.jff` (y `.json`, `.xml`, idénticos entre sí). Se genera con `python herramientas/generar_aplicacion.py`.
- El simulador lo lee como **AFD completo de 6 estados y 8 símbolos**; en la interfaz se carga con *Abrir* y se prueba cada cadena con *Simular*.
- Las pruebas automáticas están en `tests/test_aplicacion.py`: comprueban los 14 casos de abajo, que los tres formatos den lo mismo, que el autómata sea completo, que tenga las flechas de la Figura 3 y que desde cualquier estado se pueda volver a Vagar.

### Cadenas de prueba

El resultado **esperado** se razonó a mano con la figura y la ampliación, antes de usar el simulador; el **obtenido** es el del simulador al leer el `.jff`.

| # | Cadena de eventos | Estado final esperado | Esperado | Estado final obtenido | Obtenido | Qué prueba |
|---|---|---|---|---|---|---|
| 1 | `λ` | Vagar (q0) | Rechaza | Vagar (q0) | Rechaza | sin eventos el fantasma sigue en Vagar |
| 2 | `v` | Perseguir (q1) | Acepta | Perseguir (q1) | Acepta | ve a Pac-Man y lo persigue |
| 3 | `vp` | Vagar (q0) | Rechaza | Vagar (q0) | Rechaza | lo pierde y vuelve a vagar |
| 4 | `vpv` | Perseguir (q1) | Acepta | Perseguir (q1) | Acepta | lo pierde y lo vuelve a ver |
| 5 | `vvvv` | Perseguir (q1) | Acepta | Perseguir (q1) | Acepta | ver a Pac-Man persiguiéndolo no cambia nada |
| 6 | `vc` | Huir (q2) | Rechaza | Huir (q2) | Rechaza | Pac-Man come pastilla mientras lo persigue: huye |
| 7 | `cam` | Regresar (q3) | Rechaza | Regresar (q3) | Rechaza | huye, alerta de fin, Pac-Man se lo come |
| 8 | `ce` | Huir (q2) | Rechaza | Huir (q2) | Rechaza | la pastilla no expira sin pasar por la alerta (ampliación) |
| 9 | `caebv` | Perseguir (q1) | Acepta | Perseguir (q1) | Acepta | alerta, expira, `b` no cambia nada en Vagar, ve a Pac-Man |
| 10 | `cmbrv` | Perseguir (q1) | Acepta | Perseguir (q1) | Acepta | se lo comen, llega a la base, se regenera y persigue |
| 11 | `cmv` | Regresar (q3) | Rechaza | Regresar (q3) | Rechaza | convertido en ojos, no persigue aunque vea a Pac-Man |
| 12 | `cmbv` | Regenerar (q5) | Rechaza | Regenerar (q5) | Rechaza | regenerándose en la base, tampoco persigue |
| 13 | `cacm` | Regresar (q3) | Rechaza | Regresar (q3) | Rechaza | otra pastilla en la alerta reinicia la huida; luego lo comen |
| 14 | `vcaev` | Perseguir (q1) | Acepta | Perseguir (q1) | Acepta | persigue, huye, alerta, expira y vuelve a perseguir |

## 5.5 Abstracción: qué captura el modelo y qué deja fuera

Un autómata finito modela **el modo de comportamiento** del fantasma y **cómo reacciona a eventos discretos**, y nada más. Lo que captura es un hecho sencillo pero útil: en cada momento el fantasma está en uno de unos pocos modos (vagar, perseguir, huir, regresar, parpadear, regenerar), y lo que hace ante un evento depende **solo del modo actual**, no de cómo llegó a él. Eso permite contestar preguntas sobre secuencias de eventos: por ejemplo, que un fantasma recién devorado nunca persigue, o que de cualquier modo se puede volver a vagar (ningún estado es una trampa).

Lo que deja fuera es casi todo el juego:

- **El espacio.** No hay laberinto, posiciones ni búsqueda de caminos. «Ve a Pac-Man» es un evento que alguien decidió fuera del autómata, mirando el mapa; el modelo solo sabe que ocurrió.
- **El tiempo.** No hay duración de la pastilla ni temporizadores: `e` y `a` son eventos que llegan, no cuentas regresivas que el autómata lleve.
- **Qué evento ocurre.** El autómata es **reactivo**: no decide cuándo Pac-Man come una pastilla ni cuándo el fantasma lo ve. Describe las respuestas, no el mundo que las provoca.
- **Los demás elementos del juego**: Pac-Man, los otros fantasmas, el puntaje, los niveles y todo lo aleatorio.
- **La simultaneidad.** Los eventos se tratan como una secuencia ordenada; dos cosas a la vez (Pac-Man come la pastilla en el instante en que el fantasma lo ve) hay que ordenarlas en una cadena.

Hay además un límite de fondo: un autómata finito **solo tiene memoria finita**, que es su estado. Cualquier comportamiento que exija contar sin cota (cuántos eventos de cierto tipo han ocurrido) no cabe en un número fijo de estados; para eso haría falta otro modelo. Y, como la figura no define todas las flechas, completar el AFD con lazos fue una decisión de modelado: se asumió que un evento irrelevante para el modo actual no cambia nada, lo cual es razonable, pero es una suposición mía y no una afirmación de la fuente.

## Referencias

Gribkoff, E. (2013). *Applications of deterministic finite automata* [Documento de curso, ECS 120]. University of California, Davis. https://www.cs.ucdavis.edu/~rogaway/classes/120/spring13/eric-dfa.pdf
