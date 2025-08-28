from src.game.jugador import Jugador

class GestorPartida:
    def __init__(self, cantidad_jugadores):
        self.jugadores = []
        for jugador in range(cantidad_jugadores):
            self.jugadores.append(Jugador())