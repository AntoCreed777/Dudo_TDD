# Simulador del Juego Dudo Chileno

Implementación de un simulador del juego chileno llamado "Dudo" que maneje la lógica central del juego usando TDD.

## 👥 Integrantes del Equipo

| Nombre | GitHub | Matrícula |
|--------|--------|-----------|
| Antonio Jesus Benavides Puentes | [@AntoCreed777](https://github.com/AntoCreed777) | 2023455954 |
| Ricardo Andres Charris Jimenez | [@RicardoCharris14](https://github.com/RicardoCharris14) | 2022452901 |
| Martin Nicolas Fuentealba Bizama | [@martin777pro](https://github.com/martin777pro) | 2023434272 |

## 📋 Tabla de Contenidos

- [Simulador del Juego Dudo Chileno](#simulador-del-juego-dudo-chileno)
  - [👥 Integrantes del Equipo](#-integrantes-del-equipo)
  - [📋 Tabla de Contenidos](#-tabla-de-contenidos)
  - [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
    - [Lenguaje de programación](#lenguaje-de-programación)
    - [Herramientas de desarrollo y control de versiones](#herramientas-de-desarrollo-y-control-de-versiones)
    - [Testing, Linting y Tipado](#testing-linting-y-tipado)
    - [Integración continua](#integración-continua)
  - [📋 Requisitos Previos](#-requisitos-previos)
  - [⚙️ Instalación](#️-instalación)
  - [🗂️ Estructura del Proyecto](#️-estructura-del-proyecto)
  - [🧪 Metodología de Desarrollo](#-metodología-de-desarrollo)
  - [📚 Documentación del Código](#-documentación-del-código)
  - [📝 Convenciones](#-convenciones)
  - [🤝 Contribuir](#-contribuir)


## 🛠️ Tecnologías Utilizadas

<div align="center">

### Lenguaje de programación
<img src="https://skillicons.dev/icons?i=python&perline=8" />

### Herramientas de desarrollo y control de versiones
<img src="https://skillicons.dev/icons?i=git,github,vscode&perline=5" />

### Testing, Linting y Tipado
<img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
<img src="https://img.shields.io/badge/flake8-4B8BBE?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/mypy-2A6DB2?style=for-the-badge&logo=python&logoColor=white" />

### Integración continua
<img src="https://skillicons.dev/icons?i=githubactions&perline=8" />

</div>


## 📋 Requisitos Previos

- **Sistema operativo:** Linux, macOS, o Windows con WSL
- **Python 3.8+**
- **pdm** para gestión de dependencias y entornos

## ⚙️ Instalación

```bash
git clone https://github.com/AntoCreed777/Dudo_TDD
cd Dudo_TDD
pdm install
```

## 🗂️ Estructura del Proyecto

```
Dudo_TDD/
├── conventions.md
├── pyproject.toml
├── README
├── src/
│   ├── __init__.py
│   ├── game/
│   │   ├── __init__.py
│   │   ├── arbitro_ronda.py
│   │   ├── cacho.py
│   │   ├── contador_pintas.py
│   │   ├── dado.py
│   │   ├── gestor_partida.py
│   │   └── validador_apuesta.py
│   └── services/
│       ├── __init__.py
│       └── generador_aleatorio.py
└── tests/
    ├── test_arbitro_ronda.py
    ├── test_cacho.py
    ├── test_contador_pintas.py
    ├── test_dado.py
    ├── test_gestor_partida.py
    └── test_validador_apuesta.py
```


## 🧪 Metodología de Desarrollo

Este proyecto sigue la metodología **TDD (Test Driven Development)**:
1. Se escribe primero el test (commit RED).
2. Se implementa el código mínimo para pasar el test (commit GREEN).
3. Se refactoriza el código si es necesario (commit REFACTOR).

## 📚 Documentación del Código

La documentación se encuentra en los docstrings de las clases y funciones principales. Para explorar la lógica, revisa los archivos en `src/` y los tests en `tests/`.

## 📝 Convenciones

- Consulta [`conventions.md`](./conventions.md) para las reglas de estilo y buenas prácticas del proyecto.

## 🤝 Contribuir

Si vas a aportar a este repositorio, instala pre-commit para asegurar la calidad del código antes de cada commit:

```bash
pdm add --dev pre-commit
pre-commit install
```
Esto ejecutará automáticamente los hooks configurados en `.pre-commit-config.yaml`.

---

<div align="center">

**Desarrollado con ❤️ por aprender a trabajar con TDD**

📚 **Universidad:** Universidad de Concepción

🎓 **Curso:**  TESTING Y ASEGURAMIENTO DE LA CALIDAD DE SOFTWARE

📋 **Código curso:** 501405-1

📅 **Semestre:** 2025-2

</div>
