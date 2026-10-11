"""Núcleo de los autómatas finitos: AFD, AFND y AFND-λ.

No depende de Flet y no lee ni escribe archivos (de eso se encarga formatos.py),
por eso se puede probar de forma automática con pytest.

Convenciones:
  * La transición λ se guarda con la cadena vacía "" como símbolo leído, igual que
    en los archivos. En pantalla y en los textos se escribe λ (lenguajes.LAMBDA).
  * Un autómata es la quíntupla (Q, Σ, δ, q0, F): estados, alfabeto, función de
    transición, estado inicial y estados de aceptación. δ puede ser parcial: si
    falta una transición, la cadena se rechaza (como hace JFLAP).
  * El tipo (AFD, AFND o AFND-λ) no se declara: se deduce de las transiciones.

Decisión de diseño para el no determinismo (apartado 3.3 del enunciado): la
simulación sigue **todos los caminos a la vez**, es decir, avanza con el conjunto
de estados activos sin construir el AFD. Cuesta O(|w| · |δ|) en tiempo y O(|Q|) en
espacio. Convertir primero a AFD (a_afd) puede crear hasta 2^|Q| estados, pero
después cada cadena se simula con un solo estado activo. La conversión también
está disponible porque los ejercicios la piden.
"""

from collections import deque
from dataclasses import dataclass

from lenguajes import LAMBDA, LONGITUD_MAXIMA, LimiteExcedido

TIPO_AFD = "AFD"
TIPO_AFND = "AFND"
TIPO_AFND_LAMBDA = "AFND-lambda"
TIPOS = (TIPO_AFD, TIPO_AFND, TIPO_AFND_LAMBDA)

LIMITE_ESTADOS_AFD = 5_000    # máximo de estados que se acepta crear al convertir a AFD
LIMITE_CAMINOS = 10_000       # máximo de caminos que se enumeran para una cadena
NOMBRE_VACIO = "∅"            # nombre del estado que representa el conjunto vacío


class AutomataInvalido(ValueError):
    """La definición del autómata es incorrecta o incompleta."""


class SimboloFueraDelAlfabeto(ValueError):
    """La cadena tiene un símbolo que no pertenece al alfabeto."""


def formatear_conjunto(estados):
    """{q0, q1} para un conjunto no vacío y ∅ para el conjunto vacío."""
    estados = list(estados)
    return "{" + ", ".join(estados) + "}" if estados else NOMBRE_VACIO


def _nombre_subconjunto(estados):
    """Nombre de un estado del AFD que representa un conjunto de estados del AFND."""
    estados = list(estados)
    return "{" + ",".join(estados) + "}" if estados else NOMBRE_VACIO


# ---------------------------------------------------------------------------
# Resultados de la simulación y de las conversiones
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Paso:
    """Un paso de la simulación.

    simbolo es None en el paso inicial. tomadas son las transiciones usadas en el paso
    (primero las que leen el símbolo y después las λ de la clausura), como tuplas
    (desde, lee, hacia). conjunto son los estados activos al terminar el paso, ya con
    la λ-clausura.
    """
    simbolo: object
    tomadas: tuple
    conjunto: frozenset


@dataclass(frozen=True)
class Recorrido:
    """Recorrido completo del autómata para una cadena, siguiendo todos los caminos."""
    cadena: str
    pasos: tuple
    aceptada: bool
    consumida: bool           # False si el autómata se bloqueó antes de leer toda la cadena
    aceptacion: frozenset     # estados de aceptación del autómata, para explicar el resultado

    def texto(self, orden):
        """Texto del recorrido. orden es la lista de estados, para escribirlos en orden."""
        pos = {q: i for i, q in enumerate(orden)}

        def conj(c):
            return formatear_conjunto(sorted(c, key=pos.get))

        def flechas(tomadas):
            return ", ".join(f"{d} –{l if l else LAMBDA}→ {h}" for d, l, h in tomadas)

        lineas = [f"Cadena: {self.cadena if self.cadena else LAMBDA} ({len(self.cadena)} símbolos)"]
        for i, p in enumerate(self.pasos):
            if p.simbolo is None:
                lineas.append(f"Inicio: λ-clausura del estado inicial = {conj(p.conjunto)}"
                              + (f"   [{flechas(p.tomadas)}]" if p.tomadas else ""))
            else:
                detalle = flechas(p.tomadas) if p.tomadas else "ninguna transición"
                lineas.append(f"Paso {i}, lee «{p.simbolo}»: {detalle}   →   {conj(p.conjunto)}")
        if not self.consumida:
            lineas.append("El autómata se bloqueó: no quedó ningún estado activo antes de terminar la cadena.")
        finales = sorted(self.pasos[-1].conjunto & self.aceptacion, key=pos.get)
        if self.aceptada:
            lineas.append(f"ACEPTADA: el conjunto final contiene el estado de aceptación {', '.join(finales)}.")
        else:
            lineas.append("RECHAZADA: el conjunto final no contiene ningún estado de aceptación.")
        return "\n".join(lineas)


@dataclass(frozen=True)
class Camino:
    """Un camino de cómputo para una cadena (para mostrar bifurcaciones y caminos múltiples)."""
    estados: tuple
    transiciones: tuple       # tuplas (desde, lee, hacia)
    aceptado: bool
    motivo: str


@dataclass(frozen=True)
class ResultadoCaminos:
    caminos: tuple
    truncado: bool            # True si había más caminos que el límite


@dataclass(frozen=True)
class Conversion:
    """Resultado de la construcción de subconjuntos."""
    afd: "Automata"
    subconjuntos: dict        # nombre del estado del AFD -> frozenset de estados del autómata original


@dataclass(frozen=True)
class ResultadoParticion:
    """Particiones sucesivas de la minimización (la primera separa aceptación de no aceptación)."""
    rondas: tuple             # cada ronda es una tupla de clases; cada clase, una tupla de estados
    trampa: object            # nombre del estado trampa agregado para completar, o None


# ---------------------------------------------------------------------------
# El autómata
# ---------------------------------------------------------------------------

class Automata:
    """Autómata finito (Q, Σ, δ, q0, F) editable.

    Los métodos de edición mantienen la consistencia (no se puede usar un estado o un
    símbolo que no existe). Lo que puede faltar mientras se edita, como el estado
    inicial o el alfabeto, lo señala validar(); las operaciones de simulación y
    conversión exigen un autómata válido.
    """

    def __init__(self, alfabeto=(), estados=(), inicial=None, aceptacion=(), transiciones=(), nombre=""):
        self.nombre = nombre
        self.alfabeto = []
        self.estados = []
        self.inicial = None
        self._aceptacion = set()
        self._trans = {}                # (estado, símbolo o "") -> conjunto de estados
        self.posiciones = {}            # estado -> (x, y); solo sirve para dibujar
        self._indice = {}
        for simbolo in alfabeto:
            self.agregar_simbolo(simbolo)
        for estado in estados:
            self.agregar_estado(estado)
        if inicial is not None:
            self.establecer_inicial(inicial)
        for estado in aceptacion:
            self.marcar_aceptacion(estado)
        for desde, lee, hacia in transiciones:
            self.agregar_transicion(desde, lee, hacia)

    # ------------------------- edición -------------------------

    @staticmethod
    def _validar_simbolo(simbolo):
        if not isinstance(simbolo, str) or len(simbolo) != 1 or simbolo.isspace():
            raise AutomataInvalido(f"Cada símbolo debe ser un solo carácter visible: {simbolo!r}.")
        if simbolo == LAMBDA:
            raise AutomataInvalido(f"«{LAMBDA}» no puede ser símbolo del alfabeto: se reserva para la cadena vacía.")

    def _reindexar(self):
        self._indice = {q: i for i, q in enumerate(self.estados)}

    def _exigir_estado(self, estado):
        if estado not in self._indice:
            raise AutomataInvalido(f"El estado «{estado}» no existe.")

    def agregar_simbolo(self, simbolo):
        self._validar_simbolo(simbolo)
        if simbolo in self.alfabeto:
            raise AutomataInvalido(f"El símbolo «{simbolo}» ya está en el alfabeto.")
        self.alfabeto.append(simbolo)

    def quitar_simbolo(self, simbolo):
        """Quita el símbolo del alfabeto y todas las transiciones que lo leen."""
        if simbolo not in self.alfabeto:
            raise AutomataInvalido(f"El símbolo «{simbolo}» no está en el alfabeto.")
        self.alfabeto.remove(simbolo)
        for clave in [k for k in self._trans if k[1] == simbolo]:
            del self._trans[clave]

    def agregar_estado(self, nombre, inicial=False, aceptacion=False):
        if not isinstance(nombre, str) or not nombre or nombre != nombre.strip() or "\n" in nombre:
            raise AutomataInvalido(f"Nombre de estado no válido: {nombre!r}.")
        if nombre in self._indice:
            raise AutomataInvalido(f"El estado «{nombre}» ya existe.")
        self.estados.append(nombre)
        self._reindexar()
        if inicial:
            self.inicial = nombre
        if aceptacion:
            self._aceptacion.add(nombre)

    def quitar_estado(self, nombre):
        """Quita el estado y todas las transiciones que entran o salen de él."""
        self._exigir_estado(nombre)
        self.estados.remove(nombre)
        self._reindexar()
        self._aceptacion.discard(nombre)
        self.posiciones.pop(nombre, None)
        if self.inicial == nombre:
            self.inicial = None
        for (desde, lee) in list(self._trans):
            if desde == nombre:
                del self._trans[(desde, lee)]
            else:
                self._trans[(desde, lee)].discard(nombre)
                if not self._trans[(desde, lee)]:
                    del self._trans[(desde, lee)]

    def renombrar_estado(self, viejo, nuevo):
        self._exigir_estado(viejo)
        if viejo == nuevo:
            return
        if not isinstance(nuevo, str) or not nuevo or nuevo != nuevo.strip() or "\n" in nuevo:
            raise AutomataInvalido(f"Nombre de estado no válido: {nuevo!r}.")
        if nuevo in self._indice:
            raise AutomataInvalido(f"El estado «{nuevo}» ya existe.")
        self.estados[self.estados.index(viejo)] = nuevo
        self._reindexar()
        if self.inicial == viejo:
            self.inicial = nuevo
        if viejo in self._aceptacion:
            self._aceptacion.discard(viejo)
            self._aceptacion.add(nuevo)
        if viejo in self.posiciones:
            self.posiciones[nuevo] = self.posiciones.pop(viejo)
        nuevas = {}
        for (desde, lee), destinos in self._trans.items():
            clave = (nuevo if desde == viejo else desde, lee)
            nuevas[clave] = {nuevo if d == viejo else d for d in destinos}
        self._trans = nuevas

    def establecer_inicial(self, nombre):
        self._exigir_estado(nombre)
        self.inicial = nombre

    def marcar_aceptacion(self, nombre, valor=True):
        self._exigir_estado(nombre)
        if valor:
            self._aceptacion.add(nombre)
        else:
            self._aceptacion.discard(nombre)

    def agregar_transicion(self, desde, lee, hacia):
        """Agrega desde –lee→ hacia. lee es un símbolo del alfabeto, o "" para λ."""
        self._exigir_estado(desde)
        self._exigir_estado(hacia)
        if lee != "" and lee not in self.alfabeto:
            raise AutomataInvalido(f"El símbolo «{lee}» no está en el alfabeto.")
        self._trans.setdefault((desde, lee), set()).add(hacia)

    def quitar_transicion(self, desde, lee, hacia=None):
        """Quita desde –lee→ hacia; si hacia es None, quita todas las de (desde, lee)."""
        destinos = self._trans.get((desde, lee))
        if not destinos or (hacia is not None and hacia not in destinos):
            raise AutomataInvalido("Esa transición no existe.")
        if hacia is None:
            del self._trans[(desde, lee)]
        else:
            destinos.discard(hacia)
            if not destinos:
                del self._trans[(desde, lee)]

    def copiar(self):
        c = Automata(nombre=self.nombre)
        c.alfabeto = list(self.alfabeto)
        c.estados = list(self.estados)
        c._reindexar()
        c.inicial = self.inicial
        c._aceptacion = set(self._aceptacion)
        c._trans = {k: set(v) for k, v in self._trans.items()}
        c.posiciones = dict(self.posiciones)
        return c

    # ------------------------- consulta -------------------------

    @property
    def aceptacion(self):
        return frozenset(self._aceptacion)

    def es_aceptacion(self, estado):
        return estado in self._aceptacion

    def _ordenar(self, estados):
        return tuple(sorted(estados, key=self._indice.get))

    def destinos(self, estado, lee):
        """Estados a los que se llega desde estado leyendo lee ("" es λ), en el orden de Q."""
        return self._ordenar(self._trans.get((estado, lee), ()))

    def transiciones(self):
        """Todas las transiciones (desde, lee, hacia), en un orden estable."""
        simbolos = {s: i for i, s in enumerate([""] + self.alfabeto)}
        salida = []
        for (desde, lee), destinos in self._trans.items():
            for hacia in destinos:
                salida.append((desde, lee, hacia))
        salida.sort(key=lambda t: (self._indice[t[0]], simbolos.get(t[1], len(simbolos)), self._indice[t[2]]))
        return salida

    @property
    def tiene_lambda(self):
        return any(lee == "" for (_, lee) in self._trans)

    @property
    def tipo(self):
        """AFND-lambda si hay alguna transición λ; AFND si algún (estado, símbolo) tiene
        varios destinos; AFD en otro caso (un AFD parcial sigue siendo AFD)."""
        if self.tiene_lambda:
            return TIPO_AFND_LAMBDA
        if any(len(d) > 1 for d in self._trans.values()):
            return TIPO_AFND
        return TIPO_AFD

    def es_determinista(self):
        return self.tipo == TIPO_AFD

    def es_completo(self):
        """True si todo estado tiene exactamente una transición por cada símbolo."""
        if self.tipo != TIPO_AFD:
            return False
        return all((q, a) in self._trans for q in self.estados for a in self.alfabeto)

    def validar(self):
        """Lista de problemas de la definición; vacía si el autómata es válido."""
        problemas = []
        if not self.alfabeto:
            problemas.append("El alfabeto está vacío.")
        if not self.estados:
            problemas.append("No hay estados.")
        if self.inicial is None:
            problemas.append("Falta el estado inicial.")
        return problemas

    def _exigir_valido(self):
        problemas = self.validar()
        if problemas:
            raise AutomataInvalido(" ".join(problemas))

    def tabla(self):
        """Tabla de transiciones: (columnas, filas). columnas son los símbolos (y "" si hay λ);
        cada fila es (estado, {columna: tupla de destinos})."""
        columnas = ([""] if self.tiene_lambda else []) + list(self.alfabeto)
        filas = [(q, {c: self.destinos(q, c) for c in columnas}) for q in self.estados]
        return columnas, filas

    def __eq__(self, otro):
        """Igualdad estructural: mismos Σ, Q, q0, F y δ, sin importar el orden, el nombre
        ni las posiciones de dibujo."""
        if not isinstance(otro, Automata):
            return NotImplemented
        return (set(self.alfabeto) == set(otro.alfabeto) and set(self.estados) == set(otro.estados)
                and self.inicial == otro.inicial and self._aceptacion == otro._aceptacion
                and {k: frozenset(v) for k, v in self._trans.items()}
                == {k: frozenset(v) for k, v in otro._trans.items()})

    __hash__ = None

    def __repr__(self):
        return (f"Automata({self.tipo}, Σ={self.alfabeto}, Q={self.estados}, q0={self.inicial}, "
                f"F={sorted(self._aceptacion)}, {len(self.transiciones())} transiciones)")

    # ------------------------- λ-clausura y función de transición -------------------------

    def _exigir_estados(self, conjunto):
        for q in conjunto:
            self._exigir_estado(q)

    def clausura(self, conjunto):
        """λ-clausura de un conjunto de estados: los alcanzables solo con transiciones λ,
        incluidos los propios estados. Termina aunque haya ciclos de λ."""
        conjunto = frozenset(conjunto)
        self._exigir_estados(conjunto)
        visto = set(conjunto)
        pendientes = list(conjunto)
        while pendientes:
            q = pendientes.pop()
            for r in self._trans.get((q, ""), ()):
                if r not in visto:
                    visto.add(r)
                    pendientes.append(r)
        return frozenset(visto)

    def clausuras(self):
        """λ-clausura de cada estado, en el orden de Q."""
        return {q: self._ordenar(self.clausura({q})) for q in self.estados}

    def delta(self, estado, lee):
        """δ(q, a): destinos directos, sin λ-clausura (a puede ser "" para λ)."""
        self._exigir_estado(estado)
        return frozenset(self._trans.get((estado, lee), ()))

    def mover(self, conjunto, lee):
        """Unión de δ(q, a) para los q del conjunto, sin λ-clausura."""
        return frozenset(r for q in conjunto for r in self._trans.get((q, lee), ()))

    def _validar_cadena(self, w):
        if not isinstance(w, str):
            raise ValueError("La cadena debe ser texto.")
        if len(w) > LONGITUD_MAXIMA:
            raise LimiteExcedido(f"La cadena tiene {len(w):,} símbolos y el máximo permitido es {LONGITUD_MAXIMA:,}.")
        for simbolo in w:
            if simbolo not in self.alfabeto:
                raise SimboloFueraDelAlfabeto(
                    f"El símbolo «{simbolo}» no pertenece al alfabeto {formatear_conjunto(self.alfabeto)}.")

    def delta_hat(self, conjunto, w):
        """δ̂(Z, w): estados a los que se llega desde el conjunto Z leyendo w, con λ-clausura
        al inicio y después de cada símbolo. Para w vacía es la λ-clausura de Z."""
        self._exigir_valido()
        self._validar_cadena(w)
        actual = self.clausura(conjunto)
        for a in w:
            actual = self.clausura(self.mover(actual, a))
        return actual

    # ------------------------- simulación -------------------------

    def acepta(self, w):
        """True si el autómata acepta w, siguiendo todos los caminos a la vez."""
        self._exigir_valido()
        self._validar_cadena(w)
        actual = self.clausura({self.inicial})
        for a in w:
            actual = self.clausura(self.mover(actual, a))
            if not actual:
                return False
        return bool(actual & self._aceptacion)

    def _aristas_lambda(self, conjunto):
        """Transiciones λ que salen de los estados del conjunto (ya con su clausura)."""
        return tuple((q, "", r) for q in self._ordenar(conjunto) for r in self.destinos(q, ""))

    def simular(self, w):
        """Recorrido completo para w: el conjunto de estados activos tras cada símbolo y las
        transiciones usadas, incluidas las λ. Se detiene si no queda ningún estado activo."""
        self._exigir_valido()
        self._validar_cadena(w)
        actual = self.clausura({self.inicial})
        pasos = [Paso(None, self._aristas_lambda(actual), actual)]
        consumida = True
        for a in w:
            tomadas = tuple((q, a, r) for q in self._ordenar(actual) for r in self.destinos(q, a))
            siguiente = self.clausura(self.mover(actual, a))
            tomadas += self._aristas_lambda(siguiente) if siguiente else ()
            pasos.append(Paso(a, tomadas, siguiente))
            actual = siguiente
            if not actual:
                consumida = len(pasos) - 1 == len(w)
                break
        aceptada = consumida and bool(actual & self._aceptacion)
        return Recorrido(w, tuple(pasos), aceptada, consumida, self.aceptacion)

    def caminos(self, w, limite=LIMITE_CAMINOS):
        """Enumera los caminos de cómputo para w, para documentar las bifurcaciones.

        Un camino termina cuando se leyó toda la cadena (se acepta si acaba en un estado de
        aceptación) o cuando se bloquea. Un ciclo de λ no se recorre dos veces en el mismo
        camino. Si hay más de `limite` caminos se corta la enumeración y se avisa.
        """
        self._exigir_valido()
        self._validar_cadena(w)
        n = len(w)
        resultado = []
        pila = [((self.inicial,), (), 0, frozenset({(self.inicial, 0)}))]
        truncado = False
        while pila:
            if len(resultado) >= limite:
                truncado = True
                break
            estados, trans, i, visitados = pila.pop()
            q = estados[-1]
            hijos = []
            for r in self.destinos(q, ""):
                if (r, i) not in visitados:
                    hijos.append((estados + (r,), trans + ((q, "", r),), i, visitados | {(r, i)}))
            if i < n:
                for r in self.destinos(q, w[i]):
                    hijos.append((estados + (r,), trans + ((q, w[i], r),), i + 1, visitados | {(r, i + 1)}))
            if i == n:
                final = q in self._aceptacion
                resultado.append(Camino(estados, trans, final,
                                        "termina en un estado de aceptación" if final
                                        else "termina en un estado que no es de aceptación"))
            elif not hijos:
                resultado.append(Camino(estados, trans, False, f"se bloquea en {q} al leer «{w[i]}»"))
            pila.extend(reversed(hijos))
        return ResultadoCaminos(tuple(resultado), truncado)

    # ------------------------- conversiones -------------------------

    def quitar_lambda(self):
        """AFND sin transiciones λ equivalente, con los mismos estados.

        δ'(q, a) = Cl(δ(Cl({q}), a)) y q es de aceptación si Cl({q}) contiene un estado de
        aceptación. Es el paso previo a la construcción de subconjuntos en los AFND-λ.
        """
        self._exigir_valido()
        nuevo = Automata(self.alfabeto, self.estados, self.inicial, (), (), self.nombre)
        nuevo.posiciones = dict(self.posiciones)
        for q in self.estados:
            cl = self.clausura({q})
            if cl & self._aceptacion:
                nuevo.marcar_aceptacion(q)
            for a in self.alfabeto:
                for r in self.clausura(self.mover(cl, a)):
                    nuevo.agregar_transicion(q, a, r)
        return nuevo

    def a_afd(self, completo=False):
        """AFD equivalente por construcción de subconjuntos (con λ-clausura).

        Cada estado del AFD es un conjunto de estados del autómata original y se nombra
        {q0,q1}. Solo se crean los conjuntos alcanzables desde la λ-clausura del estado
        inicial. El conjunto vacío (∅) solo aparece si completo=True. Se rechaza lo que
        pase de LIMITE_ESTADOS_AFD estados, porque el AFD puede tener hasta 2^|Q|.
        """
        self._exigir_valido()
        inicio = self.clausura({self.inicial})
        nombres = {inicio: _nombre_subconjunto(self._ordenar(inicio))}
        orden = [inicio]
        trans = []
        cola = deque([inicio])
        while cola:
            s = cola.popleft()
            for a in self.alfabeto:
                t = self.clausura(self.mover(s, a))
                if not t and not completo:
                    continue
                if t not in nombres:
                    if len(nombres) >= LIMITE_ESTADOS_AFD:
                        raise LimiteExcedido(
                            f"El AFD equivalente tendría más de {LIMITE_ESTADOS_AFD:,} estados "
                            f"(el máximo teórico es 2^{len(self.estados)}).")
                    nombres[t] = _nombre_subconjunto(self._ordenar(t))
                    orden.append(t)
                    cola.append(t)
                trans.append((nombres[s], a, nombres[t]))
        afd = Automata(self.alfabeto, [nombres[s] for s in orden], nombres[inicio],
                       [nombres[s] for s in orden if s & self._aceptacion], trans,
                       self.nombre)
        return Conversion(afd, {nombres[s]: s for s in orden})

    # ------------------------- simplificación -------------------------

    def accesibles(self):
        """Estados alcanzables desde el inicial por cualquier transición (λ incluidas)."""
        self._exigir_valido()
        visto = {self.inicial}
        pendientes = [self.inicial]
        while pendientes:
            q = pendientes.pop()
            for (desde, _), destinos in self._trans.items():
                if desde == q:
                    for r in destinos - visto:
                        visto.add(r)
                        pendientes.append(r)
        return self._ordenar(visto)

    def quitar_inaccesibles(self):
        """Copia del autómata sin los estados inaccesibles."""
        alcanzables = set(self.accesibles())
        nuevo = self.copiar()
        for q in list(nuevo.estados):
            if q not in alcanzables:
                nuevo.quitar_estado(q)
        return nuevo

    def completar(self):
        """Copia a la que se le agrega un estado trampa para que cada estado tenga una
        transición por cada símbolo. Si ya está completa, no cambia."""
        nuevo = self.copiar()
        faltan = [(q, a) for q in nuevo.estados for a in nuevo.alfabeto if not nuevo._trans.get((q, a))]
        if not faltan:
            return nuevo, None
        trampa = NOMBRE_VACIO
        while trampa in nuevo._indice:
            trampa += "'"
        nuevo.agregar_estado(trampa)
        for q, a in faltan + [(trampa, a) for a in nuevo.alfabeto]:
            nuevo.agregar_transicion(q, a, trampa)
        return nuevo, trampa

    def particiones(self):
        """Particiones sucesivas del método de refinamiento (Moore) para un AFD.

        Se trabaja con los estados accesibles y con un estado trampa si el AFD es parcial.
        La primera ronda separa aceptación de no aceptación; cada ronda divide las clases
        cuyos estados van a clases distintas con algún símbolo; termina cuando no cambia.
        """
        self._exigir_valido()
        if not self.es_determinista():
            raise AutomataInvalido("Solo se simplifica un AFD: convierte antes el autómata (a_afd).")
        c, trampa = self.quitar_inaccesibles().completar()
        clase = {q: int(c.es_aceptacion(q)) for q in c.estados}
        rondas = []

        def agrupar():
            grupos = {}
            for q in c.estados:
                grupos.setdefault(clase[q], []).append(q)
            return tuple(tuple(g) for g in sorted(grupos.values(), key=lambda g: c._indice[g[0]]))

        rondas.append(agrupar())
        while True:
            firmas = {q: (clase[q], tuple(clase[c.destinos(q, a)[0]] for a in c.alfabeto)) for q in c.estados}
            ids = {}
            nueva = {}
            for q in c.estados:
                nueva[q] = ids.setdefault(firmas[q], len(ids))
            if len(ids) == len(set(clase.values())):
                break
            clase = nueva
            rondas.append(agrupar())
        return ResultadoParticion(tuple(rondas), trampa)

    def minimizar(self):
        """AFD mínimo equivalente: quita los inaccesibles y fusiona los estados equivalentes.

        Cada clase con varios estados se nombra {A,B}. Si el AFD original era parcial, el
        resultado también lo es (se descarta el estado trampa que solo servía para el cálculo).
        """
        resultado = self.particiones()
        c, trampa = self.quitar_inaccesibles().completar()
        clases = list(resultado.rondas[-1])
        nombre = {q: (g[0] if len(g) == 1 else _nombre_subconjunto(g)) for g in clases for q in g}
        descartada = nombre[trampa] if trampa else None
        if descartada == nombre[c.inicial]:     # lenguaje vacío: se conserva el único estado
            descartada = None
        nuevo = Automata(self.alfabeto, nombre=self.nombre)
        for g in clases:
            if nombre[g[0]] != descartada:
                nuevo.agregar_estado(nombre[g[0]], aceptacion=c.es_aceptacion(g[0]))
        nuevo.establecer_inicial(nombre[c.inicial])
        for g in clases:
            if nombre[g[0]] == descartada:
                continue
            for a in c.alfabeto:
                destino = nombre[c.destinos(g[0], a)[0]]
                if destino != descartada:
                    nuevo.agregar_transicion(nombre[g[0]], a, destino)
        return nuevo


# ---------------------------------------------------------------------------
# Comparación de lenguajes
# ---------------------------------------------------------------------------

def cadena_distintiva(a, b):
    """La cadena más corta que un autómata acepta y el otro no, o None si reconocen el
    mismo lenguaje. Recorre a la vez los conjuntos de estados activos de los dos autómatas
    (no construye ningún AFD completo), así que sirve para AFD, AFND y AFND-λ."""
    a._exigir_valido()
    b._exigir_valido()
    simbolos = list(dict.fromkeys(a.alfabeto + b.alfabeto))
    inicio = (a.clausura({a.inicial}), b.clausura({b.inicial}))
    vistos = {inicio}
    cola = deque([(inicio, "")])
    while cola:
        (sa, sb), w = cola.popleft()
        if bool(sa & a.aceptacion) != bool(sb & b.aceptacion):
            return w
        for s in simbolos:
            siguiente = (a.clausura(a.mover(sa, s)), b.clausura(b.mover(sb, s)))
            if siguiente not in vistos:
                vistos.add(siguiente)
                cola.append((siguiente, w + s))
    return None


def lenguajes_iguales(a, b):
    """True si los dos autómatas reconocen exactamente el mismo lenguaje."""
    return cadena_distintiva(a, b) is None
