from enum import Enum


class NombreDado(Enum):
    AS = 1
    TONTO = 2
    TREN = 3
    CUADRA = 4
    QUINA = 5
    SEXTO = 6

    def __str__(self):
        nombres = {
            NombreDado.AS: "As",
            NombreDado.TONTO: "Tonto",
            NombreDado.TREN: "Tren",
            NombreDado.CUADRA: "Cuadra",
            NombreDado.QUINA: "Quina",
            NombreDado.SEXTO: "Sexto"
        }
        return nombres[self]


class Dado:
    _valor: int | None

    def __init__(self):
        self._valor = None

    def generar_numero(self):
        import random
        self._valor = random.randint(1, 6)

    def numero_a_nombre(self, numero: int) -> str:
        try:
            nombre_enum = NombreDado(numero)
            return str(nombre_enum)
        except ValueError:
            raise ValueError("Número inválido")

    def get_valor(self) -> str:
        if self._valor is None:
            raise ValueError("No se ha generado ningún valor todavía")
        return self.numero_a_nombre(self._valor)
