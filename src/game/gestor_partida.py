"""Módulo que contiene la clase GestorPartida para gestionar la lógica de la partida de Dudo."""

from src.game.dado import Dado
from src.game.jugador import Jugador


class GestorPartida:
    """Clase que gestiona la partida, jugadores y turnos."""

    def __init__(self, cantidad_jugadores):
        """Inicializa el gestor de partida con la cantidad de jugadores indicada."""
        self._jugadores = []
        self._direccion_juego = 0
        self._turno_actual = 0
        self._apuesta_anterior = ""
        self._apuesta_actual = ""

        for _ in range(cantidad_jugadores):
            nombre = input(f"\nIngrese el nombre del jugador {_}: ")
            self._jugadores.append(Jugador(nombre))

    def definir_primer_jugador(self):
        """Define el primer jugador que inicia la partida lanzando el dado."""
        dado = Dado()
        numeros = []
        for i in range(len(self._jugadores)):
            dado.generar_numero()
            numeros.append([i, dado.get_valor_numerico()])

        while True:
            repeticiones = 1
            indice_numero_mayor = -1
            numero_mayor = -1
            for num in numeros:
                if num[1] > numero_mayor:
                    indice_numero_mayor = num[0]
                    numero_mayor = num[1]
                    repeticiones = 1
                elif num[1] == numero_mayor:
                    repeticiones += 1

            if repeticiones == 1:
                break

            numeros_aux = []
            for num in numeros:
                if num[1] == numero_mayor:
                    dado.generar_numero()
                    numeros_aux.append([num[0], dado.get_valor_numerico()])

            numeros = numeros_aux

        self._turno_actual = indice_numero_mayor

    def definir_direccion_juego(self):
        """Permite al jugador actual elegir la dirección del juego."""
        direccion = ""
        while direccion.lower() != "1" and direccion.lower() != "-1":
            mensaje = (
                f"Jugador {self._turno_actual + 1}:\n"
                f"Ingresa (1) si quieres que la dirección sea hacia el jugador "
                f"{(self._turno_actual + 1) % len(self._jugadores) + 1}.\n"
                f"Ingresa (-1) si quieres que la dirección sea hacia el jugador "
                f"{5 if self._turno_actual == 0 else self._turno_actual}"
            )
            direccion = input(mensaje)

        if direccion == "1":
            self._direccion_juego = 1
        else:
            self._direccion_juego = -1

    def solicitar_apuesta_a_jugador(self) -> str:
        apuesta: str = self._jugadores[self._turno_actual].realizar_apuesta(self._apuesta_anterior,
                                                                            self._apuesta_actual)
        return apuesta
