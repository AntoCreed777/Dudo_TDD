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

    def test_jugar_ronda_termina_con_calzar(self, mocker, gestor_4_jugadores):
        """Ronda normal: termina con 'calzar'."""
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 0
        gestor._apuesta_actual = "subir 6 tren"

        mocker.patch(
            "src.game.dado.random.randint",
            side_effect=[3, 1, 6, 6, 6, 3, 3, 6, 6, 6, 1, 6, 6, 6, 6, 3, 6, 6, 6, 6],
        )
        mocker.patch("builtins.input", side_effect=["1", "6 tren", "4"])
        for j in gestor._jugadores:
            j.agitar_cacho()

        resultado = gestor.jugar_ronda()
        assert resultado["accion"] == "calzar"
        assert resultado["termino"] is True
        assert resultado["resultado"] is True

    def test_jugar_ronda_termina_con_dudar(self, mocker, gestor_4_jugadores):
        """Una ronda termina cuando se ejecuta 'dudar' y se resuelve la apuesta."""
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 1
        gestor._apuesta_actual = "subir 4 tonto"

        mocker.patch(
            "src.game.dado.random.randint",
            side_effect=[1, 3, 4, 5, 6, 2, 2, 1, 6, 6, 1, 1, 4, 5, 6, 1, 1, 4, 5, 6],
        )
        mocker.patch("builtins.input", side_effect=["1", "4 tonto", "3"])
        for j in gestor._jugadores:
            j.agitar_cacho()

        resultado = gestor.jugar_ronda()
        assert resultado["accion"] == "dudar"
        assert resultado["termino"] is True

    def test_jugar_ronda_especial_termina_con_dudar_y_obligar_cerrada(
        self, mocker, gestor_4_jugadores
    ):
        """Ronda especial: obligar 'cerrada', termina con 'dudar'."""
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 1
        gestor._jugadores[1]._dados_en_posecion = 1
        gestor._apuesta_actual = "subir 4 tonto"

        mocker.patch(
            "src.game.dado.random.randint",
            side_effect=[1, 2, 2, 6, 6, 1, 2, 1, 6, 6, 6, 1, 6, 6, 6, 6],
        )
        mocker.patch("builtins.input", side_effect=["5", "tren", "3"])
        for j in gestor._jugadores:
            j.agitar_cacho()

        resultado = gestor.jugar_ronda()
        assert resultado["accion"] == "dudar"
        assert resultado["termino"] is True
        assert isinstance(resultado["resultado"], bool)

    def test_jugar_ronda_especial_termina_con_calzar_y_obligar_abierta(
        self, mocker, gestor_4_jugadores
    ):
        """Ronda especial 'abierta', termina con 'calzar'."""
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 0
        gestor._jugadores[0]._dados_en_posecion = 1
        gestor._apuesta_actual = "subir 3 tren"

        mocker.patch(
            "src.game.dado.random.randint",
            side_effect=[3, 3, 6, 6, 6, 6, 1, 6, 6, 6, 6, 3, 6, 6, 6, 6],
        )
        mocker.patch("builtins.input", side_effect=["6", "tren", "4"])
        for j in gestor._jugadores:
            j.agitar_cacho()

        resultado = gestor.jugar_ronda()
        assert resultado["accion"] == "calzar"
        assert resultado["termino"] is True
        assert resultado["resultado"] in (True, False)

    def test_especial_no_puede_cambiar_pinta_fijada(self, mocker, gestor_4_jugadores):
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._jugadores[0]._dados_en_posecion = 1
        mocker.patch("builtins.input", side_effect=["5", "tren", "1", "3 tonto"])
        mocker.patch("src.game.dado.random.randint", side_effect=[3, 3, 3, 3, 3] * 4)
        for j in gestor._jugadores:
            j.agitar_cacho()

        with pytest.raises(ValueError, match="Pinta fija en ronda especial"):
            gestor.jugar_ronda()

    def test_especial_otro_con_un_dado_puede_cambiar_pinta_si_sube(
        self, mocker, gestor_4_jugadores
    ):
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._jugadores[0]._dados_en_posecion = 1
        gestor._jugadores[2]._dados_en_posecion = 1
        gestor._turno_actual = 1
        mocker.patch(
            "builtins.input", side_effect=["5", "tren", "1", "2 tren", "1", "3 tonto", "4"]
        )
        mocker.patch("src.game.dado.random.randint", side_effect=[3] * 20)
        for j in gestor._jugadores:
            j.agitar_cacho()

        resultado = gestor.jugar_ronda()
        assert resultado["termino"] is True

    def test_visibilidad_cerrada(self, gestor_4_jugadores):
        """En 'cerrada': solo el obligador ve su propio cacho; nadie ve ajenos."""
        gestor = gestor_4_jugadores
        for j in gestor._jugadores:
            j.agitar_cacho()
            j._cacho.mostrar()

        obligador = gestor._jugadores[0]
        gestor._ronda_especial = True
        gestor._pinta_fijada_especial = "tren"
        gestor._obligador_nombre = obligador._nombre
        gestor._modo_especial = "cerrada"
        gestor._ver_propios = {obligador._nombre}
        gestor._ver_ajenos = set()

        assert gestor.ver_cacho_para(obligador, obligador) is not None
        for otro in gestor._jugadores[1:]:
            assert gestor.ver_cacho_para(otro, otro) is None
        for obs in gestor._jugadores:
            for obj in gestor._jugadores:
                if obs is obj:
                    continue
                assert gestor.ver_cacho_para(obs, obj) is None

    def test_visibilidad_abierta(self, gestor_4_jugadores):
        """En 'abierta': nadie ve su propio cacho; todos ven los ajenos."""
        gestor = gestor_4_jugadores
        for j in gestor._jugadores:
            j.agitar_cacho()
            j._cacho.mostrar()

        gestor._ronda_especial = True
        gestor._pinta_fijada_especial = "tren"
        gestor._obligador_nombre = gestor._jugadores[0]._nombre
        gestor._modo_especial = "abierta"
        gestor._ver_propios = set()
        gestor._ver_ajenos = {j._nombre for j in gestor._jugadores}

        for x in gestor._jugadores:
            assert gestor.ver_cacho_para(x, x) is None
        for obs in gestor._jugadores:
            for obj in gestor._jugadores:
                if obs is obj:
                    continue
                assert gestor.ver_cacho_para(obs, obj) is not None
