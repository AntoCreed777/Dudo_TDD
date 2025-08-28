from src.game.dado import Dado


class Cacho:
    _dados: list[Dado]
    _cantidad_agitada: int
    _oculto: bool

    def __init__(self):
        self._oculto = False
        self._cantidad_agitada = 0
        self._dados = []
        for i in range(5):  # Se crean la cantidad maxima de dados que pueden haber dentro del cacho
            self._dados.append(Dado())

    def agitar(self, cantidad: int):
        if cantidad < 0:
            raise ValueError("Cantidad a agitar invalida")

        if cantidad > 5:
            cantidad = 5

        self._cantidad_agitada = cantidad

        resultados = []
        for i in range(cantidad):
            self._dados[i].generar_numero()
            resultados.append(self._dados[i].get_valor())

    def get_resultados(self) -> list[str] | None:
        if self._oculto:
            return None

        resultados = []
        for i in range(self._cantidad_agitada):
            resultados.append(self._dados[i].get_valor())
        return resultados

    def ocultar(self):
        self._oculto = True

    def mostrar(self):
        self._oculto = False
