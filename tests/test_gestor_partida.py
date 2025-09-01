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

    @pytest.mark.parametrize("direccion,valor", [
        ("1", 1),
        ("-1", -1)
    ])
    def test_definir_direccion_juego(self, mocker, gestor_4_jugadores, direccion, valor):
        """Verifica la dirección antihoraria del juego."""
        mocker.patch("builtins.input", return_value=direccion)
        gestor_4_jugadores.definir_direccion_juego()
        assert gestor_4_jugadores._direccion_juego == valor

    def test_solicitar_apuesta(self, mocker, gestor_4_jugadores):
        """Verifica que se puedan solicitar apuestas al siguiente Jugador."""
        mocker.patch("builtins.input", side_effect=["1", "3 cuadra"])
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == "subir 3 cuadra"
        mocker.patch("builtins.input", return_value="2")
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == "pasar"
        mocker.patch("builtins.input", return_value="3")
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == "dudar"
        mocker.patch("builtins.input", return_value="4")
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == "calzar"

    def test_eliminar_jugador(self, gestor_4_jugadores):
        """Verifica que se elimine un jugador cuando se queda sin dados."""
        cantidad_previa_jugadores = len(gestor_4_jugadores._jugadores)
        gestor_4_jugadores._jugadores[0]._dados_en_posicion = 0
        assert gestor_4_jugadores._jugadores[0].get_cantidad_dados() == 0
        gestor_4_jugadores.eliminar_jugador(0)
        assert len(gestor_4_jugadores._jugadores) == cantidad_previa_jugadores - 1

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_subir_apuesta(self, mocker, gestor_4_jugadores):
        """Test que verifica que el movimiento de subir apuesta funcione correctamente"""
        mocker.patch("builtins.input", side_effect=["1", "3 quina"])
        gestor_4_jugadores._turno_actual = 0
        apuesta = gestor_4_jugadores.solicitar_apuesta_a_jugador()
        gestor_4_jugadores.procesar_apuesta(apuesta)
        assert gestor_4_jugadores._apuesta_actual() == "3 quina"

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_resultado_dudar(self):
        """Test pendiente para procesar un movimiento."""
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_jugar_ronda(self, mocker, gestor_4_jugadores):
        """Test pendiente para jugar una ronda."""
        mocker.patch("builtins.input", side_effect=["1", "3 cuadra"])
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_verificar_fin_partida(self):
        """Test pendiente para verificar el fin de la partida."""
        pass
