"""Tests para la clase GestorPartida del juego Dudo."""

import pytest

from src.game.gestor_partida import GestorPartida


@pytest.fixture(scope="function")
def gestor_4_jugadores(mocker):
    """Fixture que retorna un GestorPartida con 4 jugadores."""
    mocker.patch("builtins.input", side_effect=["Ricardo", "Antonio", "Martin", "Angel"])
    return GestorPartida(4)


class TestGestorPartida:
    """Tests para la gestión de partida en Dudo."""

    def test_crear_jugadores(self, gestor_4_jugadores):
        """Verifica que se creen 4 jugadores correctamente."""
        assert len(gestor_4_jugadores._jugadores) == 4

    def test_definir_primer_jugador(self, mocker, gestor_4_jugadores):
        """Verifica que se defina el primer jugador correctamente."""
        mocker.patch("src.game.dado.random.randint", side_effect=[2, 2, 5, 2])
        gestor_4_jugadores.definir_primer_jugador()
        assert gestor_4_jugadores._turno_actual == 2

    def test_definir_primer_jugador_con_empate(self, mocker, gestor_4_jugadores):
        """Verifica la definición del primer jugador en caso de empate."""
        mocker.patch("src.game.dado.random.randint", side_effect=[1, 2, 5, 5, 3, 6])
        gestor_4_jugadores.definir_primer_jugador()
        assert gestor_4_jugadores._turno_actual == 3

    def test_definir_direccion_antihoraria_juego(self, mocker, gestor_4_jugadores):
        """Verifica la dirección antihoraria del juego."""
        mocker.patch("builtins.input", return_value="1")
        gestor_4_jugadores.definir_direccion_juego()
        assert gestor_4_jugadores._direccion_juego == 1

    def test_definir_direccion_horaria_juego(self, mocker, gestor_4_jugadores):
        """Verifica la dirección horaria del juego."""
        mocker.patch("builtins.input", return_value="-1")
        gestor_4_jugadores.definir_direccion_juego()
        assert gestor_4_jugadores._direccion_juego == -1

    def test_solicitar_apuesta(self, mocker, gestor_4_jugadores):
        mocker.patch("builtins.input", side_effect=["1", "3 cuadra"])
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == "subir 3 cuadra"
        mocker.patch("builtins.input", return_value="2")
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == "pasar"
        mocker.patch("builtins.input", return_value="3")
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == "dudar"
        mocker.patch("builtins.input", return_value="4")
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == "calzar"

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_jugar_ronda(self):
        """Test pendiente para jugar una ronda."""
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_procesar_movimiento(self):
        """Test pendiente para procesar un movimiento."""
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_verificar_fin_partida(self):
        """Test pendiente para verificar el fin de la partida."""
        pass
