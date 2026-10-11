"""Lógica de la interfaz que no depende de Flet.

app.py solo arma la pantalla y llama a estas funciones y a las de automata.py, formatos.py
y lenguajes.py; lo que se puede probar sin abrir una ventana vive aquí.
"""

import re
from pathlib import Path

import formatos as F
from automata import LIMITE_CAMINOS, Automata, AutomataInvalido, formatear_conjunto
from dibujo import svg_automata
from lenguajes import LAMBDA, parsear_alfabeto

RAIZ = Path(__file__).resolve().parent.parent
CARPETA_AUTOMATAS = RAIZ / "automatas"
CARPETA_SALIDAS = RAIZ / "salidas"
CAMINOS_VISIBLES = 200          # caminos que se muestran en pantalla (se enumeran hasta LIMITE_CAMINOS)


def automata_nuevo():
    """Punto de partida para definir un autómata: alfabeto {a, b} y un estado inicial q0."""
    return Automata("ab", ["q0"], "q0", nombre="nuevo")


# ---------------------------------------------------------------------------
# Edición
# ---------------------------------------------------------------------------

def nombre_de_estado_libre(a):
    """q0, q1, ... el primero que no está en uso."""
    n = len(a.estados)
    while f"q{n}" in a.estados:
        n += 1
    return f"q{n}"


def aplicar_alfabeto(a, texto):
    """Cambia el alfabeto al que describe el texto ("a, b" o "ab"). Los símbolos que ya no
    están se quitan junto con sus transiciones. Devuelve (agregados, quitados, transiciones perdidas)."""
    nuevos = parsear_alfabeto(texto)          # ValueError si está vacío o tiene un símbolo no válido
    quitados = [s for s in a.alfabeto if s not in nuevos]
    perdidas = sum(1 for _, lee, _ in a.transiciones() if lee in quitados)
    for s in quitados:
        a.quitar_simbolo(s)
    agregados = [s for s in nuevos if s not in a.alfabeto]
    for s in agregados:
        a.agregar_simbolo(s)
    a.alfabeto = list(nuevos)                 # en el orden en que se escribió
    return agregados, quitados, perdidas


def _es_un_solo_grupo(texto):
    """True si la llave de apertura del principio se cierra justo en la última letra: {q0,q1}
    es un grupo, pero {q0}, {q1} son dos nombres."""
    if not (texto.startswith("{") and texto.endswith("}")):
        return False
    profundidad = 0
    for i, c in enumerate(texto):
        profundidad += (c == "{") - (c == "}")
        if profundidad == 0 and i < len(texto) - 1:
            return False
    return profundidad == 0


def destinos_de_texto(a, texto):
    """Estados que nombra el texto de una celda de la tabla ("q0, q1", "{q0,q1}" o "∅").

    Los nombres se separan por comas, punto y coma o espacios, salvo dentro de llaves, para
    que se pueda escribir un estado como {q0,q1} (así se llaman los del AFD de una conversión).
    """
    texto = (texto or "").strip()
    if texto in ("", "∅", "-"):
        return []
    if texto in a.estados:
        return [texto]
    if _es_un_solo_grupo(texto):
        texto = texto[1:-1]
    nombres, actual, profundidad = [], "", 0
    for c in texto:
        profundidad += (c == "{") - (c == "}")
        if profundidad <= 0 and (c in ",; " or c.isspace()):
            if actual:
                nombres.append(actual)
            actual = ""
        else:
            actual += c
    if actual:
        nombres.append(actual)
    for nombre in nombres:
        if nombre not in a.estados:
            raise AutomataInvalido(f"El estado «{nombre}» no existe.")
    return list(dict.fromkeys(nombres))


def texto_de_destinos(a, estado, lee):
    return ", ".join(a.destinos(estado, lee))


def fijar_transicion(a, desde, lee, texto):
    """Reemplaza los destinos de (desde, lee) por los que nombra el texto (vacío o ∅ los quita)."""
    destinos = destinos_de_texto(a, texto)     # se valida todo antes de cambiar nada
    if a.destinos(desde, lee):
        a.quitar_transicion(desde, lee)
    for destino in destinos:
        a.agregar_transicion(desde, lee, destino)
    return destinos


# ---------------------------------------------------------------------------
# Archivos
# ---------------------------------------------------------------------------

def archivos_disponibles():
    """Archivos de autómatas que se pueden cargar: (etiqueta, ruta), los de automatas/ y salidas/."""
    encontrados = []
    for carpeta in (CARPETA_AUTOMATAS, CARPETA_SALIDAS):
        if carpeta.is_dir():
            encontrados += [p for p in carpeta.rglob("*") if p.suffix.lower().lstrip(".") in F.FORMATOS]
    return [(p.relative_to(RAIZ).as_posix(), p) for p in sorted(encontrados, key=lambda p: p.as_posix().lower())]


def resolver_ruta(texto):
    """Ruta absoluta de lo que escribió el usuario (relativa a la carpeta del proyecto o absoluta)."""
    texto = (texto or "").strip().strip('"')
    if not texto:
        raise F.FormatoInvalido("Escribe la ruta de un archivo .jff, .json o .xml.")
    ruta = Path(texto)
    return ruta if ruta.is_absolute() else RAIZ / ruta


def cargar(texto_de_ruta):
    return F.leer_archivo(resolver_ruta(texto_de_ruta))


def nombre_de_archivo_valido(nombre):
    """Nombre seguro para un archivo dentro de salidas/ (sin carpetas ni extensión)."""
    base = Path((nombre or "").strip()).stem if "." in (nombre or "") else (nombre or "").strip()
    base = re.sub(r"[^\w\-]+", "_", base, flags=re.UNICODE).strip("_")
    if not base:
        raise F.FormatoInvalido("Escribe un nombre para el archivo.")
    return base[:80]


def guardar_en_salidas(a, nombre, formatos=F.FORMATOS):
    """Guarda el autómata en salidas/ en los formatos pedidos; devuelve las rutas relativas."""
    base = nombre_de_archivo_valido(nombre)
    CARPETA_SALIDAS.mkdir(exist_ok=True)
    rutas = []
    for formato in formatos:
        ruta = CARPETA_SALIDAS / f"{base}.{formato}"
        F.guardar_archivo(a, ruta)
        rutas.append(ruta.relative_to(RAIZ).as_posix())
    return rutas


def guardar_diagrama(a, nombre, activos=(), resaltadas=()):
    """Guarda el diagrama del autómata como .svg en salidas/."""
    base = nombre_de_archivo_valido(nombre)
    CARPETA_SALIDAS.mkdir(exist_ok=True)
    ruta = CARPETA_SALIDAS / f"{base}.svg"
    ruta.write_text(svg_automata(a, activos, resaltadas), encoding="utf-8", newline="\n")
    return ruta.relative_to(RAIZ).as_posix()


# ---------------------------------------------------------------------------
# Textos de la simulación
# ---------------------------------------------------------------------------

def _flechas(tomadas):
    return ", ".join(f"{d} –{l if l else LAMBDA}→ {h}" for d, l, h in tomadas)


def titulo_de_paso(recorrido, k):
    p = recorrido.pasos[k]
    return "Inicio" if p.simbolo is None else f"Paso {k}: lee «{p.simbolo}»"


def descripcion_de_paso(a, recorrido, k):
    """Texto del paso k: estado actual, transiciones tomadas y estados activos."""
    p = recorrido.pasos[k]
    activos = formatear_conjunto(a._ordenar(p.conjunto))
    if p.simbolo is None:
        partes = [f"Se parte del estado inicial {a.inicial}."]
        partes.append(f"λ-clausura: {activos}." if a.tiene_lambda else f"Estado actual: {activos}.")
        if p.tomadas:
            partes.append(f"Transiciones λ: {_flechas(p.tomadas)}.")
        return " ".join(partes)
    partes = [f"Se lee «{p.simbolo}»."]
    partes.append(f"Transiciones tomadas: {_flechas(p.tomadas)}." if p.tomadas else "No hay ninguna transición posible.")
    partes.append(f"Estados activos: {activos}." if len(p.conjunto) != 1 else f"Estado actual: {activos}.")
    if not p.conjunto:
        partes.append("El autómata se bloqueó: la cadena se rechaza.")
    return " ".join(partes)


def lineas_de_traza(a, recorrido):
    """Una línea por paso, para la traza completa del recorrido."""
    return [f"{titulo_de_paso(recorrido, k)}  →  {formatear_conjunto(a._ordenar(p.conjunto))}"
            for k, p in enumerate(recorrido.pasos)]


def veredicto(a, recorrido):
    """(texto corto, explicación) del resultado final."""
    final = recorrido.pasos[-1].conjunto
    if recorrido.aceptada:
        en = ", ".join(a._ordenar(final & a.aceptacion))
        return "ACEPTADA", f"Terminó de leer la cadena en un estado de aceptación ({en})."
    if not recorrido.consumida:
        return "RECHAZADA", "El autómata se bloqueó antes de terminar de leer la cadena."
    if not final:
        return "RECHAZADA", "Al leer el último símbolo no quedó ningún estado activo."
    return "RECHAZADA", f"Terminó de leer la cadena en {formatear_conjunto(a._ordenar(final))}, que no es de aceptación."


def caminos_en_texto(a, w):
    """Los caminos de cómputo de w, uno por línea: (líneas, mensaje sobre el límite o '')."""
    resultado = a.caminos(w)
    lineas = []
    for i, c in enumerate(resultado.caminos[:CAMINOS_VISIBLES], start=1):
        ruta = c.estados[0] + "".join(f" –{l if l else LAMBDA}→ {h}" for (_, l, h) in c.transiciones)
        lineas.append(f"{i}. {ruta}  [{'ACEPTA' if c.aceptado else 'rechaza'}: {c.motivo}]")
    aviso = ""
    if resultado.truncado:
        aviso = f"Hay más de {LIMITE_CAMINOS:,} caminos; se enumeraron solo los primeros."
    elif len(resultado.caminos) > CAMINOS_VISIBLES:
        aviso = f"Hay {len(resultado.caminos):,} caminos; se muestran los primeros {CAMINOS_VISIBLES}."
    return lineas, aviso


def texto_de_cadena(texto):
    """Cadena que escribió el usuario: «λ» o vacío es la cadena vacía."""
    texto = texto or ""
    return "" if texto.strip() == LAMBDA else texto


# ---------------------------------------------------------------------------
# Textos de las conversiones
# ---------------------------------------------------------------------------

def filas_de_clausuras(a):
    """(estado, λ-clausura) para cada estado."""
    return [(q, formatear_conjunto(cl)) for q, cl in a.clausuras().items()]


def filas_de_subconjuntos(a, conversion):
    """(estado del AFD, conjunto de estados del original) en el orden de la construcción."""
    return [(nombre, formatear_conjunto(a._ordenar(s))) for nombre, s in conversion.subconjuntos.items()]


def lineas_de_particiones(resultado):
    """Una línea por ronda de la minimización."""
    lineas = []
    for i, ronda in enumerate(resultado.rondas):
        clases = "  ".join("{" + ", ".join(c) + "}" for c in ronda)
        lineas.append(f"Partición {i}: {clases}")
    if resultado.trampa:
        lineas.append(f"(El AFD es parcial: se agregó temporalmente el estado trampa {resultado.trampa}.)")
    return lineas
