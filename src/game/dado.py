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

    @staticmethod
    def a_enum(pinta: str) -> "NombreDado":
        """Convierte una cadena en minúsculas al enum correspondiente.
        Lanza ValueError si no existe."""
        traduccion = {
            str(NombreDado.AS).lower(): NombreDado.AS,
            str(NombreDado.TONTO).lower(): NombreDado.TONTO,
            str(NombreDado.TREN).lower(): NombreDado.TREN,
            str(NombreDado.CUADRA).lower(): NombreDado.CUADRA,
            str(NombreDado.QUINA).lower(): NombreDado.QUINA,
            str(NombreDado.SEXTO).lower(): NombreDado.SEXTO,
        }
        pinta_normalizada = pinta.strip().lower()
        try:
            return traduccion[pinta_normalizada]
        except KeyError:
            raise ValueError(f"Pinta inválida: {pinta}")


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
