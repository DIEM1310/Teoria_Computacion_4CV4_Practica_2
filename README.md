# Práctica 2: Autómatas finitos no deterministas (AFND) y simulación de AFD con interfaz gráfica

Instituto Politécnico Nacional · Escuela Superior de Cómputo

| Dato | Valor |
|---|---|
| Alumno | Diego Polo Santoscoy |
| Boleta | 2025630828 |
| Grupo | 4CV4 |
| Carrera | Ingeniería en Sistemas Computacionales |
| Unidad de aprendizaje | Teoría de la Computación |
| Profesor | Gabriel Hurtado Avilés |
| Fecha de entrega | 6 de octubre de 2026 |

## Objetivo

Profundizar en los autómatas finitos no deterministas y sus conversiones mediante JFLAP, desarrollar una aplicación con interfaz gráfica capaz de definir, importar y simular autómatas en varios formatos, y trasladar a un modelo formal propio una aplicación descrita en la literatura revisada.

## Índice de la práctica

| Ejercicio | Documento |
|---|---|
| 1. Entorno de trabajo y flujo de ramas | [docs/01-entorno.md](docs/01-entorno.md) |
| 2. AFND y AFND-λ en JFLAP | [docs/02-jflap.md](docs/02-jflap.md) |
| 3. Simulador de autómatas con interfaz gráfica | [docs/03-simulador.md](docs/03-simulador.md) |
| 4. Investigación y estado del arte | [docs/04-investigacion.md](docs/04-investigacion.md) |
| 5. Del artículo al autómata | [docs/05-del-articulo-al-automata.md](docs/05-del-articulo-al-automata.md) |
| Propuesta de trabajo | [docs/propuesta.md](docs/propuesta.md) |
| Bibliografía | [docs/bibliografia.md](docs/bibliografia.md) |

Los autómatas están en [automatas/](automatas/), organizados en `lista2-afd/`, `lista3-afnd/`, `lista3-afnd-lambda/`, `conversiones/` y `aplicacion/`. Cada uno se entrega en `.jff` (formato principal) y también en `.json` y `.xml`. Las capturas están en [evidencias/](evidencias/).

## Código reutilizado de la Práctica 1

El entorno de contenedores (`entorno/`, `requirements.txt`, `pytest.ini`) y el módulo [src/lenguajes.py](src/lenguajes.py) con sus pruebas ([tests/test_lenguajes.py](tests/test_lenguajes.py)) proceden de la Práctica 1 y se copiaron sin reescribirlos: prefijos, sufijos, subcadenas, cerradura de Kleene y cerradura positiva. Los `.jff` de los AFD de la Práctica 1 también se conservan.

Repositorio de la Práctica 1: <https://github.com/DIEM1310/Teoria_Computacion_4CV4_Practica_1>

## Cómo levantar el entorno y ejecutar las pruebas

Hace falta tener **Docker Desktop** instalado y encendido (se usó Docker Desktop con Docker 29.8.1 y Docker Compose v5.5.1). La interfaz usa **Flet 0.86.5**, versión fijada en [requirements.txt](requirements.txt). Hay tres contenedores, uno por versión de Python (3.11, 3.12 y 3.13).

Los comandos se ejecutan desde la carpeta `entorno/`:

| Para... | Comando |
|---|---|
| Construir las tres imágenes | `docker compose build` |
| Ver la versión de Python de cada contenedor | `docker compose run --rm py311 python --version`, y lo mismo con `py312` y `py313` |
| Ejecutar las pruebas en cada contenedor | `docker compose run --rm py311 pytest -q`, y lo mismo con `py312` y `py313` |
| Abrir el simulador | `docker compose up py312` y abrir http://localhost:8550 en el navegador |
| Apagar y limpiar | `docker compose down` |

Las mismas pruebas se ejecutan en GitHub Actions con las tres versiones de Python en cada confirmación y en cada Pull Request ([.github/workflows/pruebas.yml](.github/workflows/pruebas.yml)).

## Estructura del repositorio

| Carpeta o archivo | Contenido |
|---|---|
| `src/lenguajes.py` | Operaciones sobre cadenas y lenguajes (Práctica 1) |
| `src/automata.py` | Núcleo del autómata: definición, simulación, λ-clausura y conversión (no depende de Flet) |
| `src/formatos.py` | Lectura y escritura de `.jff`, `.json` y `.xml` (no depende de Flet) |
| `src/app.py` | Interfaz gráfica con Flet |
| `tests/` | Pruebas con pytest |
| `automatas/` | Autómatas de los ejercicios, en los tres formatos |
| `docs/` | Documentos de cada ejercicio, en Markdown |
| `evidencias/` | Capturas de git, de la integración continua, de JFLAP y de la aplicación |

## Formatos de archivo y convención para λ

El simulador lee y escribe tres formatos. Los tres representan los cinco componentes de la quíntupla (alfabeto, estados, estado inicial, estados de aceptación y función de transición) y la exportación y la importación son operaciones inversas.

| Formato | Uso |
|---|---|
| `.jff` | Formato nativo de JFLAP; es el principal. Las coordenadas `x` e `y` solo sirven para dibujar y el lector las tolera sin depender de ellas. |
| `.json` | Campos `tipo`, `alfabeto`, `estados`, `inicial`, `aceptacion` y `transiciones` (cada una con `desde`, `lee` y `hacia`). |
| `.xml` | Elemento `automata` con `alfabeto`, `estados` y `transiciones`, con los mismos datos que el `.json`. |

**La transición λ se escribe con la cadena vacía como símbolo leído** en los tres formatos: `<read/>` en `.jff`, `"lee": ""` en `.json` y `lee=""` en `.xml`. Es la convención habitual para λ, pero es la decisión que más problemas causa al leer archivos de otras herramientas: un lector que no la respete tomará la transición vacía como un símbolo más. En pantalla y en la documentación, la cadena vacía y la transición λ se muestran con el símbolo `λ`, como en la Práctica 1. Por eso `λ` no puede ser un símbolo del alfabeto.

El campo `tipo` del `.json` y del `.xml` toma los valores `AFD`, `AFND` o `AFND-lambda`.
