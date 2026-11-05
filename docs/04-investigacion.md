# Ejercicio 4. Investigación y estado del arte

## 4.1. Investigación

### 4.1.1 El no determinismo: AFN y AFN-λ

Un **AFD** es una quíntupla (Q, Σ, δ, q₀, F) con δ: Q × Σ → Q: en cada estado, cada símbolo lleva a **exactamente un** estado. Un **AFN** conserva la quíntupla, pero δ: Q × Σ → 𝒫(Q) devuelve un **conjunto** de estados, que puede ser vacío o tener varios. Un **AFN-λ** permite además moverse sin leer nada: δ: Q × (Σ ∪ {λ}) → 𝒫(Q).

Para hablar de cadenas se extiende δ a δ̂. En un AFN:

- δ̂(q, λ) = {q}
- δ̂(q, xa) = ⋃ { δ(p, a) : p ∈ δ̂(q, x) }, con x ∈ Σ\* y a ∈ Σ

En un AFN-λ la extensión incluye la λ-clausura (apartado siguiente): δ̂(q, λ) = λ-cl(q) y δ̂(q, xa) = λ-cl( ⋃ { δ(p, a) : p ∈ δ̂(q, x) } ).

**Qué significa aceptar.** Una cadena w es aceptada si **existe al menos un camino** de q₀ a un estado de F que lee w; es decir, si δ̂(q₀, w) ∩ F ≠ ∅. Hay que notar dos cosas. Primero, la aceptación es existencial: basta un camino bueno, aunque otros se bloqueen o terminen en estados que no son de aceptación; w se rechaza solo cuando **todos** los caminos fallan. Segundo, el autómata no «adivina» ni ejecuta cosas en paralelo en un sentido físico: «seguir todos los caminos a la vez» es un modo de **calcular** δ̂, que es lo que hace el simulador de este trabajo (apartado 3.3). El lenguaje del autómata es L(M) = { w : δ̂(q₀, w) ∩ F ≠ ∅ }.

### 4.1.2 La λ-clausura

La **λ-clausura** de un estado q, λ-cl(q), es el conjunto de estados que se alcanzan desde q siguiendo **cero o más** transiciones λ. Es el menor conjunto S tal que q ∈ S y, si p ∈ S y r ∈ δ(p, λ), entonces r ∈ S. Para un conjunto T de estados, λ-cl(T) = ⋃ { λ-cl(q) : q ∈ T }.

**Algoritmo.** Es una búsqueda en el grafo formado solo por las flechas λ:

1. S ← {q}; pila ← [q].
2. Mientras la pila no esté vacía: sacar p; para cada r ∈ δ(p, λ) con r ∉ S, añadir r a S y a la pila.
3. Devolver S.

Cada estado entra una vez a la pila y cada flecha λ se mira una vez, así que el costo es proporcional a (|Q| + número de flechas λ). Importa que se lleve la cuenta de lo ya visitado (r ∉ S): sin ella, un ciclo de transiciones λ no termina. La λ-clausura se usa dos veces al simular: al empezar (λ-cl(q₀)) y después de cada símbolo leído.

### 4.1.3 La construcción de subconjuntos

**Teorema (equivalencia entre AFD y AFN).** Un lenguaje es aceptado por algún AFN si y solo si es aceptado por algún AFD (Rabin y Scott, 1959; Hopcroft et al., 2007, cap. 2).

**Construcción.** Dado un AFN N = (Q_N, Σ, δ_N, q₀, F_N), se define el AFD D = (Q_D, Σ, δ_D, {q₀}, F_D) con:

- Q_D = 𝒫(Q_N); es decir, **cada estado de D es un conjunto de estados de N**;
- δ_D(S, a) = ⋃ { δ_N(p, a) : p ∈ S };
- F_D = { S : S ∩ F_N ≠ ∅ }.

Si N es un AFN-λ, el estado inicial de D es λ-cl(q₀) y δ_D(S, a) = λ-cl( ⋃ { δ_N(p, a) : p ∈ S } ).

**Esbozo de la demostración.** Se prueba por inducción sobre |w| que δ̂_D({q₀}, w) = δ̂_N(q₀, w). Para w = λ ambos lados son {q₀}. Si vale para x, entonces para w = xa: δ̂_D({q₀}, xa) = δ_D(δ̂_D({q₀}, x), a) = ⋃ { δ_N(p, a) : p ∈ δ̂_N(q₀, x) } = δ̂_N(q₀, xa). Como D acepta w exactamente cuando ese conjunto corta a F_N, que es la condición de aceptación de N, se tiene L(D) = L(N). La otra dirección es trivial: un AFD es un AFN cuyos conjuntos tienen un solo estado.

En la práctica no se construyen los 2ⁿ conjuntos sino solo los **alcanzables** desde el inicial, calculándolos por demanda: se empieza con {q₀} (o λ-cl(q₀)) y se aplica δ_D a cada conjunto nuevo hasta que no aparezcan más.

### 4.1.4 El costo de la conversión y la cota 2ⁿ

Como Q_D = 𝒫(Q_N), el AFD tiene **a lo más 2ⁿ estados** si el AFN tiene n. La cota **se alcanza**: sea L_n el lenguaje de las cadenas sobre {0, 1} cuyo n-ésimo símbolo desde el final es 1. Un AFN lo reconoce con n + 1 estados (adivina cuál es el símbolo n-ésimo desde el final y cuenta n − 1 símbolos más), pero cualquier AFD necesita recordar los **últimos n símbolos**, que son 2ⁿ posibilidades distintas, y por eso su versión mínima tiene 2ⁿ estados. En el simulador del trabajo se midió: para n = 4, 8 y 12 el AFN tiene 5, 9 y 13 estados y el AFD, 16, 256 y 4 096 (apartado 3.3). Es decir, **el crecimiento exponencial no es solo una cota teórica**: aparece en familias muy sencillas.

### 4.1.5 El teorema de Kleene

**Teorema de Kleene.** Un lenguaje es regular (aceptado por un autómata finito) si y solo si es denotado por una expresión regular (Hopcroft et al., 2007, cap. 3). Tiene dos mitades:

- **Expresión regular → autómata** (construcción de Thompson). Por inducción sobre la estructura de la expresión se construye un AFN-λ con un estado inicial y uno final: para ∅, λ y un símbolo a se dibujan autómatas de dos estados o menos; la unión R + S agrega un estado inicial con dos flechas λ hacia los autómatas de R y de S; la concatenación RS une el final de R con el inicio de S mediante una flecha λ; la estrella R\* agrega flechas λ para repetir R o saltarla. El resultado tiene a lo más del orden de 2 veces el tamaño de la expresión en estados.
- **Autómata → expresión regular** (eliminación de estados o fórmula R_ij^(k)). Se agregan un inicio y un final nuevos, y se elimina un estado intermedio a la vez: al quitar el estado s, por cada par de flechas p → s y s → r se agrega una flecha p → r con la etiqueta (p→s)(s→s)\*(s→r), unida con la que ya hubiera. Al final queda una sola flecha entre el inicio y el final, cuya etiqueta es la expresión. La expresión puede ser muy grande, y su forma depende del orden en que se eliminen los estados (el módulo `expresiones.py` del trabajo permite elegir ese orden).

Por tanto AFD, AFN, AFN-λ y expresiones regulares definen **la misma clase de lenguajes**.

### 4.1.6 Minimización: Myhill-Nerode y el algoritmo de Hopcroft

**Teorema de Myhill-Nerode.** Dado L ⊆ Σ\*, se definen x ≡_L y si y solo si, para todo z ∈ Σ\*, xz ∈ L ⇔ yz ∈ L (dos cadenas son equivalentes si ninguna extensión las distingue). Entonces L es regular **si y solo si ≡_L tiene un número finito de clases de equivalencia**, y ese número es el de estados del **AFD mínimo** de L, que es único salvo renombrar los estados. La demostración usa que ≡_L es una congruencia por la derecha: las clases se vuelven los estados y δ([x], a) = [xa]; en sentido contrario, un AFD con k estados separa las cadenas en a lo más k clases compatibles con ≡_L, por lo que ≡_L tiene a lo más k clases. Dos consecuencias prácticas: sirve para probar que un lenguaje **no** es regular (si hay infinitas cadenas distinguibles de a pares) y para saber de antemano cuántos estados necesita el mejor AFD.

**Algoritmo de Hopcroft.** Parte de un AFD completo y sin estados inaccesibles, y busca las clases de estados equivalentes por **refinamiento de particiones**: dos estados son equivalentes si ninguna cadena los separa (uno llega a F y el otro no).

1. P ← { F, Q ∖ F } (se descarta el bloque vacío). W ← { el menor de los dos bloques }.
2. Mientras W no esté vacío: sacar un bloque A de W. Para cada símbolo c, sea X el conjunto de estados que **llegan a A leyendo c**. Para cada bloque Y de P que X corte (Y ∩ X ≠ ∅ y Y ∖ X ≠ ∅), partir Y en Y ∩ X y Y ∖ X. Si Y estaba en W, sustituirlo por sus dos partes; si no, añadir a W solo la **más pequeña** de las dos.
3. Al terminar, cada bloque de P es un estado del AFD mínimo.

La idea clave es el último punto: basta añadir la parte pequeña, porque el efecto de la grande se deduce de la del bloque original. Con esto el costo es **O(|Σ| · n · log n)**, mejor que los métodos de refinamiento ingenuos (Moore, o la tabla de pares del libro), que cuestan del orden de n² · |Σ|. El simulador del trabajo usa el refinamiento más sencillo de la familia de Moore y muestra las particiones paso a paso (`docs/03-simulador.md`); lo importante para el curso es que **ambos dan el mismo AFD mínimo**, y la diferencia es solo de eficiencia. Zhu et al. (2021; ficha 1 de 4.3) miden la minimización de AFD en la práctica y comparan el algoritmo de Hopcroft con otros.

### 4.1.7 Qué significa, en términos prácticos, que el no determinismo no aumente el poder

Que AFD y AFN reconozcan **los mismos lenguajes** significa que cualquier cosa que se pueda describir con un AFN se puede ejecutar con un AFD: un programa con una tabla de transición y un solo estado actual, que lee cada símbolo una vez, en **tiempo lineal** y con memoria constante respecto a la longitud de la cadena. El no determinismo no añade capacidad; lo que aporta es **comodidad y concisión**:

- **Diseño.** Es más fácil escribir un AFN para «contiene `abbbab`» o «el n-ésimo símbolo desde el final es 1», y más fácil combinar autómatas (unión, concatenación y estrella son directas con transiciones λ). Esto es justo lo que usa la construcción de Thompson.
- **Tamaño.** Un AFN puede ser **exponencialmente** más pequeño que su AFD (apartado 4.1.4). Si el costo de la conversión es prohibitivo, se puede **simular el AFN** manteniendo el conjunto de estados activos, con costo de a lo más n² operaciones por símbolo, o construir el AFD por demanda y guardar solo los subconjuntos que se visitan.
- **Implementaciones reales.** Los motores de expresiones regulares eligen entre estas estrategias: unos simulan el AFN en paralelo (estilo Thompson, tiempo lineal en la entrada) y otros retroceden por un camino a la vez (estilo Spencer, que puede ser muy lento en ciertas expresiones); Davis et al. (2019; ficha 2 de 4.3) documentan esa diferencia en motores usados en la industria.

Hay que distinguir **poder** de **eficiencia**: los dos modelos tienen el mismo poder, pero no el mismo tamaño ni el mismo costo. Y la igualdad de poder es una propiedad de los autómatas **finitos**: en los autómatas de pila, el no determinismo sí aumenta el poder (los AFD con pila reconocen menos lenguajes que los no deterministas).

## 4.2. Artículo asignado: Rabin y Scott (1959)

Rabin y Scott (1959) estudian los autómatas finitos y sus problemas de decisión (si un autómata acepta alguna cinta, si acepta infinitas y si dos autómatas aceptan lo mismo). En su sección 5 introducen el no determinismo y prueban que no aumenta el poder de los autómatas finitos, que es lo que se hace en el Ejercicio 2.

### Dónde se prueba que todo AFN tiene un AFD equivalente

La prueba está en la **sección 5, «Nondeterministic operation»** (pp. 120-121), y se compone de cuatro piezas:

- **Definición 9** (p. 120): un autómata no determinista es un sistema 𝔄 = (S, M, S₀, F), donde M asigna a cada par (estado, símbolo) un **subconjunto** de S, y tanto S₀ como F son subconjuntos de S.
- **Definición 10** (pp. 120-121): una cinta x = σ₀σ₁…σₙ₋₁ se acepta si existe una sucesión de estados s₀, s₁, …, sₙ con s₀ ∈ S₀, sᵢ ∈ M(sᵢ₋₁, σᵢ₋₁) y sₙ ∈ F. Es la aceptación existencial: basta un camino ganador.
- **Definición 11** (p. 121): el autómata 𝔇(𝔄) = (T, N, t₀, G), donde T es el conjunto de **todos los subconjuntos** de S, N(t, σ) es la unión de los M(s, σ) para s en t, t₀ = S₀ y G es el conjunto de subconjuntos que contienen al menos un estado de F. Es un autómata ordinario (determinista).
- **Teorema 11** (p. 121): T(𝔄) = T(𝔇(𝔄)). Su demostración se hace en dos sentidos. Si x ∈ T(𝔄), se prueba por inducción sobre k que el estado sₖ del camino ganador pertenece a N(t₀, σ₀…σₖ₋₁); en particular sₙ ∈ N(t₀, x) y, como sₙ ∈ F, ese conjunto está en G. Recíprocamente, si x ∈ T(𝔇(𝔄)), el conjunto final tₙ está en G, así que contiene un estado sₙ de F; como sₙ está en N(tₙ₋₁, σₙ₋₁), hay un sₙ₋₁ en tₙ₋₁ con sₙ ∈ M(sₙ₋₁, σₙ₋₁); se repite hacia atrás hasta llegar a s₀ ∈ t₀ = S₀, y se obtiene un camino ganador de 𝔄.

Antes de la definición 9, los autores explican por qué la introducen: la principal ventaja de estas máquinas es el **pequeño número de estados** que requieren en muchos casos y la facilidad para describir máquinas concretas (p. 120). Después del teorema señalan una consecuencia (p. 121): un autómata con varios estados iniciales puede sustituirse por otro equivalente con uno solo.

**La construcción con la notación del curso.** Sea N = (Q, Σ, δ, q₀, F) un AFN. El AFD equivalente es D = (Q_D, Σ, δ_D, {q₀}, F_D), con Q_D = 𝒫(Q), δ_D(S, a) = ⋃ {δ(p, a) : p ∈ S} y F_D = {S : S ∩ F ≠ ∅}. Es la construcción de subconjuntos del apartado 4.1.3, y la que implementa el simulador de este trabajo: cada estado de D es un conjunto de estados de N. La inducción de Rabin y Scott demuestra, con otra notación, que δ̂_D({q₀}, w) contiene exactamente los estados que alcanza algún camino de N que lee w.

### Diferencias de notación con el libro de texto

| Concepto | Rabin y Scott (1959) | Curso (Hopcroft et al., 2007) |
|---|---|---|
| Autómata | 𝔄 = (S, M, s₀, F); el alfabeto Σ se declara aparte («sobre el alfabeto Σ») | A = (Q, Σ, δ, q₀, F); el alfabeto forma parte de la quíntupla |
| Estados y transición | S y M | Q y δ |
| Estado inicial del AFN | un **conjunto** S₀ ⊆ S | un **único** estado q₀ |
| Cadena y cadena vacía | «cinta» (tape), x = σ₀σ₁…σₙ₋₁; la vacía es Λ | cadena o palabra, w = a₁…aₙ; la vacía es ε (λ en este trabajo) |
| Extensión a cadenas | M(s, x), con M(s, Λ) = s y M(s, xσ) = M(M(s, x), σ) | δ̂(q, w), con δ̂(q, ε) = q y δ̂(q, xa) = δ(δ̂(q, x), a) |
| Lenguaje | T(𝔄), el conjunto de cintas aceptadas | L(A) |
| Estado inicial del AFD construido | t₀ = S₀ | {q₀} |

Me resulta más clara la notación del curso. Primero, la quíntupla (Q, Σ, δ, q₀, F) incluye el alfabeto, de modo que todo lo que hace falta para ejecutar el autómata está en la definición. Segundo, los nombres recuerdan lo que representan: δ para la transición, δ̂ para su extensión, L(A) para el lenguaje, q₀ para el estado en el que se empieza. Tercero, un único estado inicial hace que el inicial del AFD sea simplemente {q₀}. La notación de Rabin y Scott tiene, en cambio, una ventaja teórica: permitir un conjunto S₀ de estados iniciales hace que la construcción sea más corta (t₀ = S₀ sin casos aparte) y deja ver la simetría entre estados iniciales y finales que usan en el Teorema 12 para invertir autómatas. Para leer el artículo hay que acostumbrarse a «cinta» y «M», pero el contenido de las definiciones coincide con las del libro.

### La mención del Premio Turing de 1976

La página oficial de la ACM da la mención compartida de Rabin y Scott (1976). Reconoce el artículo conjunto porque «introduced the idea of nondeterministic machines», un concepto que, según la mención, ha resultado enormemente valioso, y añade que el artículo ha sido una fuente continua de inspiración para el trabajo posterior en este campo (ACM, s. f.).

La distinción se justifica, por tanto, por una idea y no por un resultado concreto: el no determinismo. El Teorema 11 muestra que esa idea no aumenta el poder de reconocimiento, pero sí la comodidad y la concisión con que se describen los autómatas, como dicen los propios autores. La semblanza de la ACM da el contexto: Rabin y Scott se apartaron de los modelos inspirados en redes neuronales y trabajaron con máquinas de estados finitos, en particular con una máquina que no tiene una sola transición posible desde cada estado, sino varias. La idea se mostró útil mucho más allá de los autómatas finitos: la ACM destaca que sigue inspirando el estudio teórico de muchos problemas.

## 4.3. Dos artículos localizados

Ambos tienen DOI y se publicaron después de 2018. El primero describe una implementación evaluada con experimentos (el enunciado pide que al menos uno lo haga); el segundo es un estudio empírico.

### Ficha 1. Zhu, Tabajara, Pu y Vardi (2021): la minimización de AFD en la práctica

**1. Cita (APA 7).** Zhu, S., Tabajara, L. M., Pu, G. y Vardi, M. Y. (2021). On the power of automata minimization in reactive synthesis. En P. Ganty y D. Bresolin (Eds.), *Proceedings of the 12th International Symposium on Games, Automata, Logics, and Formal Verification (GandALF 2021)* (EPTCS, Vol. 346, pp. 117-134). https://doi.org/10.4204/EPTCS.346.8

**2. Problema que aborda.** La *síntesis reactiva* a partir de especificaciones LTLf (lógica temporal sobre trazas finitas) se resuelve compilando la fórmula a un AFD y jugando un juego de alcanzabilidad sobre él. Esa compilación es el cuello de botella: en el peor caso el AFD es doblemente exponencial en la longitud de la fórmula, y minimizarlo ayuda a los cálculos posteriores. La pregunta es cuál es la mejor forma, *en la práctica*, de construir el AFD mínimo de una fórmula LTLf. El trabajo previo había comparado los algoritmos solo en AFN aleatorios, no en fórmulas LTLf. (Sec. 1)

**3. Método.** Se comparan tres configuraciones:

- **Hopcroft** (Sec. 2.3, Teorema 2): primero se determiniza por subconjuntos y luego se refina una partición de los estados, que empieza como {aceptación, no aceptación} y se divide en cada iteración hasta que ya no se puede.
- **Brzozowski, explícito y simbólico** (Sec. 2.3 y Sec. 3): se invierte el autómata, se determiniza quitando los estados inalcanzables y se repite una segunda vez. Para LTLf se aprovecha la fórmula inversa: se construye el AFD mínimo del lenguaje inverso y se invierte (Teorema 4). La versión explícita usa SPOT; la simbólica codifica los estados como variables booleanas y usa BDD.
- **Autómatas semisimbólicos** (Sec. 2.2): estados explícitos y transiciones etiquetadas con fórmulas proposicionales; con ellos trabaja MONA, que implementa Hopcroft.

La evaluación (Sec. 4.2) usa 1 000 conjunciones aleatorias de fórmulas LTLf y tres familias de juegos (Single-Counter, Double-Counters y Nim), en un nodo Intel Xeon E5-2650 v2, con límite de 1 000 s y 8 GB, y mide el tiempo total de compilar y resolver. El lenguaje de implementación no se indica en el texto.

**4. Resultado principal.** Hopcroft resuelve muchos más casos que las dos versiones de Brzozowski; la versión explícita supera ligeramente a la simbólica, y esta última se agota en casi todas las instancias de los juegos de contadores (Sec. 4.2). Los autores concluyen que Hopcroft es la mejor opción para esta aplicación. Explican por qué la ventaja teórica de Brzozowski no aparece (Sec. 5): el AFD del lenguaje inverso suele tener un tamaño parecido al del mínimo, no exponencialmente menor, y volver a invertir y determinizar provoca un crecimiento exponencial, que consideran la razón principal de los fallos. Como limitación, proponen confirmar la conjetura en otras aplicaciones. Los resultados están en figuras; el texto no da tablas con números exactos.

**5. Tema del temario.** Unidad I, autómatas finitos: el AFD, el AFN y la construcción de subconjuntos (que aquí es el paso que puede crecer exponencialmente) y la **minimización de un AFD por refinamiento de particiones**. El artículo no menciona el teorema de Myhill-Nerode, y la complejidad O(n log n) de Hopcroft solo aparece en el título de su referencia; esos dos puntos hay que tomarlos de tu libro. *(Consulta en el programa sintético el número exacto del tema.)*

**6. Aportación a tu trabajo.** Respalda dos cosas de la práctica. Primero, el apartado 2.4: la determinización por subconjuntos puede explotar, y el artículo lo observa en un problema real; en tu simulador, la familia «el n-ésimo símbolo desde el final es 1» pasa de 13 estados a 4 096 para n = 12. Segundo, el apartado 3: `minimizar()` de `src/automata.py` parte de {aceptación, no aceptación} y refina ronda por ronda, la misma idea del refinamiento de particiones; ojo, es el refinamiento básico (cuadrático), no la optimización O(n log n) de Hopcroft. El ejercicio 156 muestra el resultado: de 5 estados a 3.

### Ficha 2. Davis, Michael IV, Coghlan, Servant y Lee (2019): ¿por qué las expresiones regulares no son una *lingua franca*?

**1. Cita (APA 7).** Davis, J. C., Michael IV, L. G., Coghlan, C. A., Servant, F. y Lee, D. (2019). Why aren't regular expressions a lingua franca? An empirical study on the re-use and portability of regular expressions. En *Proceedings of the 2019 27th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering* (pp. 443-454). ACM. https://doi.org/10.1145/3338906.3338909

*(Las páginas que se indican abajo son las de la versión publicada, no las de arXiv.)*

**2. Problema que aborda.** Los desarrolladores copian expresiones regulares entre lenguajes de programación porque la sintaxis se parece, pero no hay una especificación común: PCRE y POSIX influyeron en los dialectos sin estandarizarlos (p. 444, Sec. 2.1). Las expresiones pueden compilar sin cambios y, aun así, reconocer conjuntos distintos de cadenas (error lógico) o tener un peor caso de rendimiento distinto (riesgo de denegación de servicio, ReDoS) (p. 443). El artículo plantea siete preguntas de investigación (p. 444, Sec. 3): RQ1 a RQ3, si los desarrolladores reutilizan expresiones, de dónde las toman y si creen que son una *lingua franca*; RQ4 y RQ5, qué tan común es la reutilización desde otro software y desde fuentes de Internet; RQ6, cuándo y por qué una expresión reconoce conjuntos distintos de cadenas en lenguajes distintos; RQ7, cuándo y por qué su peor caso de rendimiento cambia.

**3. Método.**

- **Encuesta** (pp. 444-445, Sec. 4): 33 preguntas, 158 respuestas válidas de desarrolladores profesionales (reclutados por conocidos, HackerNews y Reddit); se descartaron 253 respuestas, la mayoría de una campaña de suplantación.
- **Corpus** (pp. 445-446, Sec. 5): 537 806 expresiones únicas de 193 524 proyectos de ocho lenguajes (JavaScript, Java, PHP, Python, Ruby, Go, Perl y Rust), tomadas de los 25 000 módulos más destacados de cada registro de paquetes (todos los de Perl y Rust). Se considera reutilización una cadena idéntica de al menos 15 caracteres (p. 446, Sec. 6).
- **Portabilidad** (pp. 447-449, Sec. 7): un probador por lenguaje (versiones en la Tabla 2), usando solo las expresiones válidas en los dos lenguajes comparados. Para la **semántica** se generan hasta 10 000 cadenas por expresión con cinco generadores (Rex, MutRex, EGRET, ReScue y Brics) y se buscan «testigos» de diferencia: de coincidencia, de subcadena o de grupos de captura (p. 448). Para el **rendimiento** se usa un conjunto de detectores de expresiones de tiempo superlineal y se valida el peor caso sobre la expresión original, con 100 repeticiones del patrón para el caso exponencial y 100 000 para el polinomial (pp. 448-449). Los experimentos corrieron en un clúster de 10 nodos (p. 447).

**4. Resultado principal.**

- *Encuesta* (p. 445): el 94 % reutiliza expresiones; aproximadamente la mitad cree que son un lenguaje universal (el 47 % no tiene un proceso de diseño específico de cada lenguaje) y solo el 21 % (34 de 158) estaba seguro de no haberlo hecho nunca entre lenguajes.
- *Reutilización* (p. 446): alrededor del 20 % de los módulos comparten expresiones complejas, y el 15 % de los módulos de npm contiene una expresión tomada de Internet (p. 447).
- *Semántica* (p. 448): la mayoría compila en varios lenguajes (el 76 % es válida en los ocho y el 88 % en todos menos Rust, p. 447), pero **el 15,4 % (82 582 expresiones) tiene al menos un testigo de diferencia** (8,1 % de coincidencia, 4,2 % de subcadena y 7,5 % de captura). Aproximadamente el 98 % se explica con causas identificadas, y más de la mitad de los comportamientos inusuales no está documentada.
- *Rendimiento* (pp. 449-450): hay tres familias de motores. En Go y Rust no hay expresiones exponenciales (solo 6 polinomiales); en Perl hay 227 y en PHP ninguna; en Ruby, Java, JavaScript y Python hay más de 1 000 exponenciales. Las expresiones superlineales pueden ser hasta un orden de magnitud más comunes de lo que se había informado.
- *Errores* (pp. 448 y 451): se confirmaron errores en los motores de V8 (JavaScript), Python, Ruby y Rust; se identificaron 31 módulos de npm con una notación de anclas que en JavaScript significa otra cosa, y se inició la divulgación responsable a 14 495 módulos por posibles ReDoS.
- *Conclusión* (p. 452): la creencia en una *lingua franca* es «comprensible pero infundada»; alrededor del 92 % de las expresiones compila en la mayoría de los lenguajes, pero esa portabilidad aparente oculta problemas de corrección y de rendimiento.

*Limitaciones* (p. 452, Sec. 10): la encuesta no está validada; solo se analizan expresiones declaradas de forma estática y solo de módulos, no de aplicaciones; el umbral de 15 caracteres puede dejar fuera reutilizaciones cortas.

**5. Tema del temario.** Unidad I, expresiones regulares y su relación con los autómatas finitos. El artículo dice que la mayoría de los motores evalúan una expresión «simulando el comportamiento de un autómata finito equivalente (determinista o no)» (p. 444, Sec. 2.2). Los resultados distinguen dos algoritmos (p. 450, Sec. 7.2.3): Go y Rust usan el algoritmo de Thompson, de tiempo lineal y con menos funciones, que según los autores es parecido a un recorrido en anchura del grafo del AFN; los otros seis usan variantes del retroceso de Spencer, análogo a un recorrido en profundidad, que puede ser superlineal por revisar estados redundantes, y las expresiones con referencias hacia atrás pueden ser exponenciales (NP-completas). Esto se conecta con el no determinismo: el retroceso explora un camino a la vez, y la simulación de Thompson sigue todos a la vez.

**6. Aportación a tu trabajo.** Es la contrapartida práctica de la decisión de diseño del apartado 3.3 (`docs/03-simulador.md`): tu simulador sigue todos los caminos con el conjunto de estados activos, que es la idea de Thompson (en anchura), en vez de explorarlos uno por uno con retroceso. También ilustra la distancia entre el modelo teórico y los motores reales. *(Conexión tuya, no afirmación del artículo: las referencias hacia atrás que usan los motores reales no se pueden expresar con un autómata finito, y esa frontera es la que el curso estudia a partir de la Unidad II. El artículo no trata explícitamente la diferencia entre expresiones «regulares» y «extendidas».)*

## Referencias

ACM. (s. f.). *Michael O. Rabin*. A.M. Turing Award laureate. Recuperado el 4 de noviembre de 2026, de https://amturing.acm.org/award_winners/rabin_9681074.cfm

Davis, J. C., Michael IV, L. G., Coghlan, C. A., Servant, F. y Lee, D. (2019). Why aren't regular expressions a lingua franca? An empirical study on the re-use and portability of regular expressions. En *Proceedings of the 2019 27th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering* (pp. 443-454). ACM. https://doi.org/10.1145/3338906.3338909

Hopcroft, J. E., Motwani, R. y Ullman, J. D. (2007). *Teoría de autómatas, lenguajes y computación* (3.ª ed.). Pearson Educación. ISBN: 978-84-7829-088-8.

Rabin, M. O. y Scott, D. (1959). Finite automata and their decision problems. *IBM Journal of Research and Development, 3*(2), 114-125. https://doi.org/10.1147/rd.32.0114

Zhu, S., Tabajara, L. M., Pu, G. y Vardi, M. Y. (2021). On the power of automata minimization in reactive synthesis. En P. Ganty y D. Bresolin (Eds.), *Proceedings of the 12th International Symposium on Games, Automata, Logics, and Formal Verification (GandALF 2021)* (EPTCS, Vol. 346, pp. 117-134). https://doi.org/10.4204/EPTCS.346.8
