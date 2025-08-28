from src.game.cacho import Cacho


class Jugador:
    _cacho: Cacho
    _dados_en_posecion: int

    def __init__(self):
        self._cacho = Cacho()
        self._dados_en_posecion = 0

    def agitar_cacho(self):
        self._cacho.agitar(cantidad=self._dados_en_posecion)
        print("Cacho Agitado")
