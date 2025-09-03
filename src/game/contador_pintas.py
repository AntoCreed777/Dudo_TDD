"""Módulo para contar pintas en el juego Dudo."""

from src.game.dado import NombreDado
from src.game.jugador import Jugador


class ContadorPintas:
    """Clase para contar pintas en el juego Dudo."""

    nombres_dados: list[str]

    def __init__(self):
        """Inicia los nombres de las caras de los Dados a contar."""
        self.nombres_dados = [
            str(NombreDado.AS).lower(),
            str(NombreDado.TONTO).lower(),
            str(NombreDado.TREN).lower(),
            str(NombreDado.CUADRA).lower(),
            str(NombreDado.QUINA).lower(),
            str(NombreDado.SEXTO).lower(),
        ]

    def contar_pintas(self, jugadores: list[Jugador]) -> dict[str, int]:
        """Cuenta la cantidad de pintas de todos los dados de los jugadores."""
        cantidad_pintas = {nombre: 0 for nombre in self.nombres_dados}
        for jugador in jugadores:
            dados_jugador = jugador.ver_cacho()
            if dados_jugador is None:
                raise ValueError("Error en dados de jugador")
            for dado in dados_jugador:
                cantidad_pintas[dado.lower()] += 1
        return cantidad_pintas
