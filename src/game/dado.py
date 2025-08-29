"""Módulo que contiene la clase Dado y NombreDado para el juego Dudo."""

import random
from enum import Enum


class NombreDado(Enum):
    """Enumeración de los nombres posibles de los dados en Dudo."""

    AS = 1
    TONTO = 2
    TREN = 3
    CUADRA = 4
    QUINA = 5
    SEXTO = 6

    def __str__(self) -> str:
        """Devuelve el nombre del dado como cadena."""
        nombres = {
            NombreDado.AS: "As",
            NombreDado.TONTO: "Tonto",
            NombreDado.TREN: "Tren",
            NombreDado.CUADRA: "Cuadra",
            NombreDado.QUINA: "Quina",
            NombreDado.SEXTO: "Sexto",
        }
        return nombres[self]


class Dado:
    """Clase que representa un dado en el juego Dudo."""

    _valor: int | None

    def __init__(self):
        """Inicializa el dado sin valor asignado."""
        self._valor = None

    def generar_numero(self):
        """Genera un número aleatorio entre 1 y 6 para el dado."""
        self._valor = random.randint(1, 6)

    def numero_a_nombre(self, numero: int) -> str:
        """Convierte un número en el nombre correspondiente del dado."""
        try:
            nombre_enum = NombreDado(numero)
            return str(nombre_enum)
        except ValueError as exc:
            raise ValueError("Número inválido") from exc

    def get_valor(self) -> str:
        """Devuelve el nombre del valor actual del dado."""
        if self._valor is None:
            raise ValueError("No se ha generado ningún valor todavía")
        return self.numero_a_nombre(self._valor)

    def get_valor_numerico(self):
        """Devuelve el valor numérico actual del dado."""
        return self._valor
