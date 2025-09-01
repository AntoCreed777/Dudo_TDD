"""Tests para la clase GestorPartida del juego Dudo."""

import pytest

from src.game.gestor_partida import DireccionJuego, GestorPartida


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

    @pytest.mark.parametrize(
        "direccion,valor",
        [
            (DireccionJuego.Derecha.value["Numero_str"], DireccionJuego.Derecha),
            (DireccionJuego.Izquierda.value["Numero_str"], DireccionJuego.Izquierda),
        ],
    )
    def test_definir_direccion_juego(self, mocker, gestor_4_jugadores, direccion, valor):
        """Verifica la eleccion de ambas direcciones del juego."""
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
        gestor_4_jugadores._jugadores[0]._dados_en_posecion = 0
        assert gestor_4_jugadores._jugadores[0].get_cantidad_dados() == 0
        gestor_4_jugadores.eliminar_jugador(0)
        assert len(gestor_4_jugadores._jugadores) == cantidad_previa_jugadores - 1

    def test_subir_apuesta(self, mocker, gestor_4_jugadores):
        """Test que verifica que el movimiento de subir apuesta funcione correctamente"""
        mocker.patch("builtins.input", side_effect=["1", "3 quina"])
        gestor_4_jugadores._turno_actual = 0
        apuesta = gestor_4_jugadores.solicitar_apuesta_a_jugador()
        gestor_4_jugadores.procesar_apuesta(apuesta)
        assert gestor_4_jugadores._apuesta_actual == "subir 3 quina"

    @pytest.mark.parametrize(
        "dado1,dado2,resultado,dados_jugador", [(3, 3, True, 4), (3, 2, False, 5), (2, 2, False, 5)]
    )
    def test_resultado_dudar(
        self, mocker, gestor_4_jugadores, dado1, dado2, resultado, dados_jugador
    ):
        """Test para probar los casos de haber dudado exitosamente o incorrectamente"""
        gestor_4_jugadores._direccion_juego = DireccionJuego.Derecha
        gestor_4_jugadores._turno_actual = 1
        gestor_4_jugadores._apuesta_actual = "subir 4 tonto"
        mocker.patch(
            "src.game.dado.random.randint",
            side_effect=[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, dado1, dado2],
        )
        for jugador in gestor_4_jugadores._jugadores:
            jugador.agitar_cacho()
        resultado_dudar = gestor_4_jugadores.procesar_apuesta("dudar")
        assert gestor_4_jugadores._apuesta_anterior == "subir 4 tonto"
        assert gestor_4_jugadores._apuesta_actual == "dudar"
        assert resultado_dudar == resultado
        assert gestor_4_jugadores._jugadores[0]._dados_en_posecion == dados_jugador

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_jugar_ronda(self, mocker, gestor_4_jugadores):
        """Test pendiente para jugar una ronda."""
        mocker.patch("builtins.input", side_effect=["1", "3 cuadra"])
        pass

    @pytest.mark.skip(reason="Test aun no implementado")
    def test_verificar_fin_partida(self):
        """Test pendiente para verificar el fin de la partida."""
        pass

    def test_calzar_no_permitido_levanta_error(self, mocker, gestor_4_jugadores):
        """Si no se cumplen las condiciones para calzar, se lanza ValueError."""
        gestor = gestor_4_jugadores
        gestor._turno_actual = 2
        gestor._apuesta_actual = "subir 3 as"
        gestor._jugadores[0]._dados_en_posecion = 2
        gestor._jugadores[1]._dados_en_posecion = 2
        gestor._jugadores[2]._dados_en_posecion = 3
        gestor._jugadores[3]._dados_en_posecion = 2

        side_effect = [1, 2, 3, 4, 1, 6, 6, 5, 5]
        mocker.patch("src.game.dado.random.randint", side_effect=side_effect)
        for j in gestor._jugadores:
            j.agitar_cacho()
        with pytest.raises(ValueError, match="No se cumplen las condiciones para calzar"):
            gestor.procesar_apuesta("calzar")

    def test_calzar_exacto_gana_un_dado(self, mocker, gestor_4_jugadores):
        """Si el conteo coincide exactamente con la apuesta, el calzador gana 1 dado."""
        gestor = gestor_4_jugadores
        gestor._turno_actual = 0
        gestor._apuesta_actual = "subir 6 tren"

        side_effect = [3, 1, 6, 6, 6, 3, 3, 6, 6, 6, 1, 6, 6, 6, 6, 3, 6, 6, 6, 6]
        mocker.patch("src.game.dado.random.randint", side_effect=side_effect)
        for j in gestor._jugadores:
            j.agitar_cacho()
        antes = gestor._jugadores[0].get_cantidad_dados()
        resultado = gestor.procesar_apuesta("calzar")
        despues = gestor._jugadores[0].get_cantidad_dados()
        assert resultado is True
        assert despues == antes + 1

    def test_calzar_falla_pierde_un_dado(self, mocker, gestor_4_jugadores):
        """Si el conteo no coincide exactamente, el calzador pierde 1 dado."""
        gestor = gestor_4_jugadores
        gestor._turno_actual = 1
        gestor._apuesta_actual = "subir 5 tonto"

        side_effect = [1, 3, 4, 5, 6, 2, 2, 1, 6, 6, 1, 1, 4, 5, 6, 1, 1, 4, 5, 6]
        mocker.patch("src.game.dado.random.randint", side_effect=side_effect)
        for j in gestor._jugadores:
            j.agitar_cacho()
        antes = gestor._jugadores[1].get_cantidad_dados()
        resultado = gestor.procesar_apuesta("calzar")
        despues = gestor._jugadores[1].get_cantidad_dados()
        assert resultado is False
        assert despues == antes - 1
