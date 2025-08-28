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

    def ver_cacho(self):
        print("Tu cacho:")

        resultados = self._cacho.get_resultados()
        if resultados is None:
            print("\tNo tienes dados para ver, tu cacho esta vacio")
            return

        for i, resultado in enumerate(resultados):
            print(f"\tDado {i + 1}: {resultado}")
