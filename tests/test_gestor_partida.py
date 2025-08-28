import pytest
from src.game.gestor_partida import GestorPartida

@pytest.fixture
def cuatro_jugadores():
    return 4

class TestGestorPartida:
    

    def test_crear_jugadores(self, cuatro_jugadores):
        gestor = GestorPartida(cuatro_jugadores)
        assert len(gestor.jugadores) == 4


    @pytest.mark.skip(reason="Test aun no implementado")
    def test_asignar_turnos(self):
        pass
    
    @pytest.mark.skip(reason="Test aun no implementado")
    def test_jugar_ronda(self):
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_procesar_movimiento(self):
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_verificar_fin_partida(self):
        pass