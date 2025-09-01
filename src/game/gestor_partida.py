"""Módulo que contiene la clase GestorPartida para gestionar la lógica de la partida de Dudo."""

from enum import Enum

from src.game.dado import Dado, NombreDado
from src.game.jugador import Jugador


class DireccionJuego(Enum):
    Derecha = {"Numero_str": "1", "bool": True}
    Izquierda = {"Numero_str": "-1", "bool": False}

    def __str__(self):
        direcciones = {DireccionJuego.Derecha: "Derecha", DireccionJuego.Izquierda: "Izquierda"}
        return direcciones[self]


class GestorPartida:
    """Clase que gestiona la partida, jugadores y turnos."""

    _jugadores: list[Jugador]
    _direccion_juego: DireccionJuego | None
    _turno_actual: int
    _apuesta_anterior: str
    _apuesta_actual: str
    _cantidad_pintas: dict[str, int]

    def __init__(self, cantidad_jugadores):
        """Inicializa el gestor de partida con la cantidad de jugadores indicada."""
        self._jugadores = []
        self._direccion_juego = None
        self._turno_actual = -1
        self._apuesta_anterior = ""
        self._apuesta_actual = ""
        self._cantidad_pintas = {
            str(NombreDado.AS).lower(): 0,
            str(NombreDado.TONTO).lower(): 0,
            str(NombreDado.TREN).lower(): 0,
            str(NombreDado.CUADRA).lower(): 0,
            str(NombreDado.QUINA).lower(): 0,
            str(NombreDado.SEXTO).lower(): 0,
        }

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
        while (
            direccion.lower() != DireccionJuego.Derecha.value["Numero_str"]
            and direccion.lower() != DireccionJuego.Izquierda.value["Numero_str"]
        ):
            mensaje = (
                f"Jugador {self._turno_actual + 1}:\n"
                f"Ingresa (1) si quieres que la dirección sea hacia la derecha del jugador "
                f"{(self._turno_actual + 1) % len(self._jugadores) + 1}.\n"
                f"Ingresa (-1) si quieres que la dirección sea hacia la izquierda del jugador "
                f"{5 if self._turno_actual == 0 else self._turno_actual}"
            )
            direccion = input(mensaje)

        if direccion == DireccionJuego.Derecha.value["Numero_str"]:
            self._direccion_juego = DireccionJuego.Derecha
        else:
            self._direccion_juego = DireccionJuego.Izquierda

    def solicitar_apuesta_a_jugador(self) -> str:
        """Solicita al Jugador actual que realize su apuesta."""
        apuesta: str = self._jugadores[self._turno_actual].realizar_apuesta(
            self._apuesta_anterior, self._apuesta_actual
        )
        return apuesta

    def eliminar_jugador(self, indice_jugador: int):
        """Elimina a un Jugador de los Jugadores en Juego."""
        if self._jugadores[indice_jugador].get_cantidad_dados() == 0:
            self._jugadores.pop(indice_jugador)

    def procesar_apuesta(self, apuesta):
        """Procesa una apuesta durante la ronda."""
        apuesta_tokenizada = apuesta.split(" ")
        if apuesta_tokenizada[0] == "subir":
            self._apuesta_anterior = self._apuesta_actual
            self._apuesta_actual = apuesta
            return False
        if apuesta == "dudar":
            for jugador in self._jugadores:
                dados_jugador = jugador.ver_cacho()

                if dados_jugador is None:
                    raise ValueError("Error en dados de jugador")

                for dado in dados_jugador:
                    self._cantidad_pintas[dado.lower()] += 1

            cantidad_pinta_apuesta = 0
            apuesta_tokenizada = self._apuesta_actual.split(" ")
            self._apuesta_anterior = self._apuesta_actual
            self._apuesta_actual = apuesta

            if apuesta_tokenizada[0] == "subir":
                cantidad_pinta_apuesta += self._cantidad_pintas[str(NombreDado.AS).lower()]
                if apuesta_tokenizada[2] != str(NombreDado.AS).lower():
                    cantidad_pinta_apuesta += self._cantidad_pintas[apuesta_tokenizada[2]]
                if cantidad_pinta_apuesta >= int(apuesta_tokenizada[1]):
                    self._jugadores[self._turno_actual].perder_dado()
                    return False
                else:
                    if self._direccion_juego is None:
                        raise ValueError("Error en la direccion de Juego")

                    self._jugadores[
                        self.calcular_turno(not self._direccion_juego.value["bool"])
                    ].perder_dado()
                    return True
        if apuesta == "calzar":
            if not self._apuesta_actual.startswith("subir"):
                raise ValueError("No hay apuesta válida para calzar")

            from src.game.validador_apuesta import ValidadorApuesta

            validador = ValidadorApuesta()
            dados_maximos = 5 * len(self._jugadores)
            dados_en_juego = sum(j.get_cantidad_dados() for j in self._jugadores)
            dados_del_jugador = self._jugadores[self._turno_actual].get_cantidad_dados()
            if not validador.puede_calzar(dados_en_juego, dados_maximos, dados_del_jugador):
                raise ValueError("No se cumplen las condiciones para calzar")

    def calcular_turno(self, direccion_derecha: bool):
        """Calcula el turno del jugador actual."""
        if direccion_derecha:
            return (self._turno_actual + 1) % len(self._jugadores)
        else:
            siguiente_turno = self._turno_actual - 1
            if siguiente_turno < 0:
                siguiente_turno = len(self._jugadores) - 1
            return siguiente_turno
