from src.game.jugador import Jugador
from src.game.dado import Dado


class GestorPartida:
    def __init__(self, cantidad_jugadores):
        self._jugadores = []
        self.cantidad_jugadores = cantidad_jugadores
        self.direccion_juego = 0
        self._turno_actual = 0
        for i in range(cantidad_jugadores):
            self._jugadores.append(Jugador())

    def definir_primer_jugador(self):
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
        direccion = ""
        while direccion.lower() != "1" and direccion.lower() != "-1":
            direccion = input(f"Jugador {self._turno_actual + 1}:\nIngresa (1) si quieres que la"
            f" dirección sea hacia el jugador {(self._turno_actual + 1) % self.cantidad_jugadores + 1}.\nIngresa (-1) si quieres que la"
            f" dirección sea hacia el jugador {5 if self._turno_actual == 0 else self._turno_actual}")

        if direccion == "1":
            self.direccion_juego = 1
        else:
            self.direccion_juego = -1
