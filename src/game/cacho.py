from src.game.dado import Dado


class Cacho:
    _dados: list[Dado]

    def __init__(self):
        self._dados = []
        for i in range(5):  # Se crean la cantidad maxima de dados que pueden haber dentro del cacho
            self._dados.append(Dado())

    def agitar(self, cantidad: int):
        if cantidad < 0:
            raise ValueError("Cantidad a agitar invalida")

        if cantidad > 5:
            cantidad = 5

        resultados = []
        for i in range(cantidad):
            self._dados[i].generar_numero()
            resultados.append(self._dados[i].get_valor())
