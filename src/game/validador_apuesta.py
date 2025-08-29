from src.game.dado import NombreDado


class Apuesta:
    def __init__(self, cantidad: int, pinta: NombreDado):
        self.cantidad = cantidad
        self.pinta = pinta


class ValidadorApuesta:
    def puede_partir_con_ases(self, dados_en_mano: int, ya_usado: bool = False) -> bool:
        return dados_en_mano == 1 and not ya_usado

    def es_valida(self, actual: Apuesta, nueva: Apuesta) -> bool:
        if actual.pinta != NombreDado.AS and nueva.pinta == NombreDado.AS:
            return self._validar_cambio_a_ases(actual.cantidad, nueva.cantidad)

        if actual.pinta == NombreDado.AS and nueva.pinta != NombreDado.AS:
            return self._validar_desde_ases(actual.cantidad, nueva.cantidad)

        if nueva.pinta.value < actual.pinta.value:
            return False

        if nueva.pinta == actual.pinta:
            return nueva.cantidad > actual.cantidad

        return nueva.cantidad >= actual.cantidad

    def _validar_cambio_a_ases(
        self, cantidad_actual: int, cantidad_nueva: int
    ) -> bool:
        if cantidad_actual % 2 == 0:
            minimo = (cantidad_actual // 2) + 1
        else:
            minimo = (cantidad_actual + 1) // 2
        return cantidad_nueva >= minimo

    def _validar_desde_ases(
        self, cantidad_actual: int, cantidad_nueva: int
    ) -> bool:
        minimo = (cantidad_actual * 2) + 1
        return cantidad_nueva >= minimo