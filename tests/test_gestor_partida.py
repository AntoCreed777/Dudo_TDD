import pytest
from src.game.gestor_partida import GestorPartida


@pytest.fixture(scope="class")
def gestor_4_jugadores():
    return GestorPartida(4)


class TestGestorPartida:

    def test_crear_jugadores(self, gestor_4_jugadores):
        assert len(gestor_4_jugadores._jugadores) == 4

    def test_definir_primer_jugador(self, mocker, gestor_4_jugadores):
        mocker.patch("src.game.dado.random.randint", side_effect=[2, 2, 5, 2])
        gestor_4_jugadores.definir_primer_jugador()
        assert gestor_4_jugadores._turno_actual == 2

    def test_definir_primer_jugador_con_empate(self, mocker, gestor_4_jugadores):
        mocker.patch("src.game.dado.random.randint", side_effect=[1, 2, 5, 5, 3, 6])
        gestor_4_jugadores.definir_primer_jugador()
        assert gestor_4_jugadores._turno_actual == 3

    def test_definir_direccion_antihoraria_juego(self, mocker, gestor_4_jugadores):
        mocker.patch("src.game.gestor_partida.builtins.input", return_value="-1")
        gestor_4_jugadores.definir_direccion_juego()
        assert gestor_4_jugadores.direccion_juego == -1

    def test_definir_direccion_horaria_juego(self, mocker, gestor_4_jugadores):
        mocker.patch("src.game.gestor_partida.builtins.input", return_value="1")
        gestor_4_jugadores.definir_direccion_juego()
        assert gestor_4_jugadores.direccion_juego == 1

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_jugar_ronda(self):
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_procesar_movimiento(self):
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_verificar_fin_partida(self):
        pass
