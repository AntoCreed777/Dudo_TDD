# Convenciones de Código para Dudo_TDD (Python + TDD)

## Nombres de archivos
- Usar `snake_case` para archivos Python.
- Los módulos van en la carpeta `src/`, los tests en `tests/`.
- Los archivos de test deben comenzar con `test_` (ej: `test_dado.py`).

## Variables
- Usar nombres descriptivos en `snake_case`.
- Constantes en `UPPER_SNAKE_CASE`.

## Clases
- Usar `PascalCase` para clases (ej: `GestorPartida`).
- Nombres sustantivos que representen entidades del juego.

## Métodos y funciones
- Usar `snake_case` para funciones y métodos.
- Nombres descriptivos, verbos al inicio si es una acción (ej: `calcular_pintas`).
- Métodos privados con prefijo `_`.

## Comentarios
- Usar `#` para comentarios de línea.
- Documentar funciones y clases con docstrings (triple comillas).
- Evitar comentarios innecesarios.

## Commits en GitHub (TDD)
- `RED:` Solo el test, sin implementación. El test debe fallar.
- `GREEN:` Implementación mínima para que el test pase.
- `REFACTOR:` Mejoras internas sin cambiar funcionalidad.

## Commits Generales
- `feat`: Nueva funcionalidad.
- `build`: Cambios en dependencias.
- `ci`: Cambios en integración continua.
- `docs`: Documentación.
- `chore`: Tareas menores.
- `perf`: Mejoras de rendimiento.
- `refactor`: Mejoras internas.
- `style`: Formato/código.
- `test`: Pruebas nuevas o corregidas.