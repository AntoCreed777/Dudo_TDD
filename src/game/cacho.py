"""Módulo que contiene la clase Cacho para gestionar los dados del jugador en Dudo."""

from src.game.dado import Dado


class Cacho:
    """Clase que representa el cacho de un jugador en Dudo."""

    _dados: list[Dado]
    _cantidad_agitada: int
    _oculto: bool

    """Módulo que contiene la clase Cacho para gestionar los dados del jugador en Dudo."""

    def __init__(self):
        """Inicializa el cacho con 5 dados y lo deja visible."""
        self._oculto = False
        self._cantidad_agitada = 0
        self._dados = []
        for i in range(5):  # Se crean la cantidad maxima de dados que pueden haber dentro del cacho
            self._dados.append(Dado())

    def agitar(self, cantidad: int):
        """Agita el cacho con la cantidad de dados indicada."""
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
        """Devuelve los resultados de los dados agitados si el cacho está visible."""
        if self._oculto or self._cantidad_agitada == 0:
            return None

        resultados = []
        for i in range(self._cantidad_agitada):
            resultados.append(self._dados[i].get_valor())
        return resultados

    def ocultar(self):
        """Oculta el cacho del jugador."""
        self._oculto = True

    def mostrar(self):
        """Muestra el cacho del jugador."""
        self._oculto = False
