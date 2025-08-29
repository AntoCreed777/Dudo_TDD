from src.game.jugador import Jugador
from src.game.dado import Dado


class GestorPartida:
    def __init__(self, cantidad_jugadores):
        self._jugadores = []
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
                    repeticiones=1
                elif num[1] == numero_mayor:
                    repeticiones+=1

            if repeticiones==1:
                break

            numeros_aux = []
            for num in numeros:
                if num[1] == numero_mayor:
                    dado.generar_numero()
                    numeros_aux.append([num[0], dado.get_valor_numerico()])

            numeros = numeros_aux

        self._turno_actual = indice_numero_mayor
