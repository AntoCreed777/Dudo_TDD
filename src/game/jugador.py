"""Módulo que contiene la clase Jugador para el juego Dudo."""

from src.game.cacho import Cacho


class Jugador:
    """Clase que representa un jugador en el juego Dudo."""

    _cacho: Cacho
    _dados_en_posecion: int

    def __init__(self):
        """Inicializa el jugador con un cacho y sin dados en posesión."""
        self._cacho = Cacho()
        self._dados_en_posecion = 0

    def agitar_cacho(self):
        """Agita el cacho del jugador con la cantidad de dados en posesión."""
        self._cacho.agitar(cantidad=self._dados_en_posecion)
        print("Cacho Agitado")

    def ver_cacho(self):
        """Muestra los resultados de los dados en el cacho del jugador."""
        print("Tu cacho:")

        resultados = self._cacho.get_resultados()
        if resultados is None:
            print("\tNo tienes dados para ver, tu cacho esta vacio")
            return

        for i, resultado in enumerate(resultados):
            print(f"\tDado {i + 1}: {resultado}")
