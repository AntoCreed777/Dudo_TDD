import pytest
from src.game.gestor_partida import GestorPartida

@pytest.fixture(scope="class")
def gestor_4_jugadores():
    return GestorPartida(4)

class TestGestorPartida:
    

    def test_crear_jugadores(self, gestor_4_jugadores):
        assert len(gestor_4_jugadores.jugadores) == 4


    def test_definir_primer_jugador(self, mocker, gestor_4_jugadores):
        mocker.patch("src.game.dado.random.randint", side_effect=[2, 2, 5, 2])
        gestor_4_jugadores.definir_primer_jugador()
        assert gestor_4_jugadores.turno_actual == 2
    
    @pytest.mark.skip(reason="Test aun no implementado")
    def test_jugar_ronda(self):
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_procesar_movimiento(self):
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_verificar_fin_partida(self):
        pass