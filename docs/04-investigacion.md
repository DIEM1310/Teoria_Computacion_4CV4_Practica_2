# Ejercicio 4. Investigación y estado del arte

> **Borrador.** Por ahora solo está completo el apartado **4.3** (las dos fichas). Los apartados 4.1 y 4.2 están pendientes. Las fichas se redactaron a partir del texto de los artículos: el primero, de la versión de arXiv; el segundo, de la versión publicada (con sus páginas). Los recuadros **«Para verificar»** son para que contrastes cada ficha con el original (unos 20 minutos por artículo); bórralos antes de entregar.

## 4.1. Investigación

*(Pendiente: las siete preguntas del enunciado, entre tres y cinco cuartillas.)*

## 4.2. Artículo asignado: Rabin y Scott (1959)

*(Pendiente: ubicar dónde se prueba que todo autómata no determinista tiene uno determinista equivalente, una diferencia de notación con tu libro y la mención oficial de la ACM del Premio Turing 1976.)*

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

> **Para verificar (Ficha 1).** Lee la Sec. 1 (problema), la Sec. 2.3 (Hopcroft y Brzozowski, Teoremas 2 y 3), la Sec. 4.2 (benchmarks y resultados) y la Sec. 5 (por qué falla Brzozowski). Comprueba que la cita coincida con la portada de la versión publicada (páginas 117-134, editores Ganty y Bresolin) y confirma en el sitio de GandALF 2021 que es un simposio con comité de programa (las páginas que leí no lo dicen).

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

> **Para verificar (Ficha 2).** Todas las cifras de la ficha se contrastaron con el texto completo del artículo. Para comprobarlas tú, lee: el resumen y la introducción (p. 443), la Sec. 2.2 (p. 444), la Sec. 4.2 (p. 445), la Tabla 3 y la Sec. 7.1.2 (p. 448), la Sec. 7.2.2 y 7.2.3 (pp. 449-450) y la Sec. 12 (p. 452).

## Referencias

Davis, J. C., Michael IV, L. G., Coghlan, C. A., Servant, F. y Lee, D. (2019). Why aren't regular expressions a lingua franca? An empirical study on the re-use and portability of regular expressions. En *Proceedings of the 2019 27th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering* (pp. 443-454). ACM. https://doi.org/10.1145/3338906.3338909

Zhu, S., Tabajara, L. M., Pu, G. y Vardi, M. Y. (2021). On the power of automata minimization in reactive synthesis. En P. Ganty y D. Bresolin (Eds.), *Proceedings of the 12th International Symposium on Games, Automata, Logics, and Formal Verification (GandALF 2021)* (EPTCS, Vol. 346, pp. 117-134). https://doi.org/10.4204/EPTCS.346.8
