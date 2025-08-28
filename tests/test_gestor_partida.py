import pytest
from src.game.gestor_partida import GestorPartida

class TestGestorPartida:
    @pytest.fixture
    def cuatro_jugadores():
        return 4

    def test_crear_jugadores(cuatro_jugadores):
        gestor = GestorPartida(cuatro_jugadores)
        assert len(gestor.jugadores) == 4

    def test_asignar_turnos():
        pass

    def test_jugar_ronda():
        pass

    def test_procesar_movimiento():
        pass

    def test_verificar_fin_partida():
        pass