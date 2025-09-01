"""Módulo que contiene las clases Apuesta y ValidadorApuesta para el juego Dudo."""

from src.game.dado import NombreDado


class Apuesta:
    """Clase que representa una apuesta en el juego Dudo."""

    # Luego hay que eliminar estos comentarios
    # pylint: disable=too-few-public-methods

    def __init__(self, cantidad: int, pinta: NombreDado):
        """Inicializa una apuesta con cantidad y pinta."""
        self.cantidad = cantidad
        self.pinta = pinta


class ValidadorApuesta:
    """Clase que valida las apuestas en el juego Dudo."""

    def puede_partir_con_ases(self, dados_en_mano: int, ya_usado: bool = False) -> bool:
        """Verifica si se puede partir con ases según los dados en mano y si ya se usó."""
        return dados_en_mano == 1 and not ya_usado

    def es_valida(self, actual: Apuesta, nueva: Apuesta) -> bool:
        """Valida si una nueva apuesta es válida respecto a la actual."""
        if actual.pinta != NombreDado.AS and nueva.pinta == NombreDado.AS:
            return self._validar_cambio_a_ases(actual.cantidad, nueva.cantidad)

        if actual.pinta == NombreDado.AS and nueva.pinta != NombreDado.AS:
            return self._validar_desde_ases(actual.cantidad, nueva.cantidad)

        if nueva.pinta.value < actual.pinta.value:
            return False

        if nueva.pinta == actual.pinta:
            return nueva.cantidad > actual.cantidad

        return nueva.cantidad >= actual.cantidad

    def _validar_cambio_a_ases(self, cantidad_actual: int, cantidad_nueva: int) -> bool:
        """Valida el cambio de una apuesta normal a Ases."""
        if cantidad_actual % 2 == 0:
            minimo = (cantidad_actual // 2) + 1
        else:
            minimo = (cantidad_actual + 1) // 2
        return cantidad_nueva >= minimo

    def _validar_desde_ases(self, cantidad_actual: int, cantidad_nueva: int) -> bool:
        """Valida el cambio desde Ases hacia otra pinta."""
        minimo = (cantidad_actual * 2) + 1
        return cantidad_nueva >= minimo

    def puede_calzar(self, dados_en_juego: int, dados_maximos: int, dados_del_jugador: int) -> bool:
        """Indica si se puede calzar con los dados actuales y del jugador."""
        mitad = (dados_maximos + 1) // 2
        return dados_del_jugador == 1 or dados_en_juego >= mitad
