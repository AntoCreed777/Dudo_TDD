"""Tests para la clase GestorPartida del juego Dudo."""

import pytest

from src.game.dado import NombreDado
from src.game.gestor_partida import DireccionJuego, GestorPartida, TipoApuesta, TipoRondaEspecial


@pytest.fixture(scope="function")
def gestor_4_jugadores(mocker):
    """Fixture que retorna un GestorPartida con 4 jugadores."""
    mocker.patch("builtins.input", side_effect=["Ricardo", "Antonio", "Martin", "Angel"])
    return GestorPartida(4)


@pytest.fixture(scope="function")
def gestor_2_jugadores(mocker):
    """Fixture que retorna un GestorPartida con 2 jugadores"""
    mocker.patch("builtins.input", side_effect=["Pepa", "Pepe"])
    return GestorPartida(2)


class TestGestorPartida:
    """Tests para la gestión de partida en Dudo."""

    def test_crear_jugadores(self, gestor_4_jugadores):
        """Verifica que se creen 4 jugadores correctamente."""
        assert len(gestor_4_jugadores._jugadores) == 4

    def test_definir_primer_jugador(self, mocker, gestor_4_jugadores):
        """Verifica que se defina el primer jugador correctamente."""
        mocker.patch("src.game.dado.random.randint", side_effect=[2, 2, 5, 2])
        mocker.patch("builtins.input", side_effect=["", "", "", ""])
        gestor_4_jugadores.definir_primer_jugador()
        assert gestor_4_jugadores._turno_actual == 2

    def test_definir_primer_jugador_con_empate(self, mocker, gestor_4_jugadores):
        """Verifica la definición del primer jugador en caso de empate."""
        mocker.patch("src.game.dado.random.randint", side_effect=[1, 2, 5, 5, 3, 6])
        mocker.patch("builtins.input", side_effect=["", "", "", "", "", ""])
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
        mocker.patch(
            "builtins.input",
            side_effect=[TipoApuesta.SUBIR.value, f"3 {str(NombreDado.CUADRA).lower()}"],
        )
        assert (
            gestor_4_jugadores.solicitar_apuesta_a_jugador()
            == f"{str(TipoApuesta.SUBIR)} 3 {str(NombreDado.CUADRA).lower()}"
        )
        gestor_4_jugadores._apuesta_actual = "subir 3 tren"
        mocker.patch("builtins.input", return_value=TipoApuesta.PASAR.value)
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == str(TipoApuesta.PASAR)
        mocker.patch("builtins.input", return_value=TipoApuesta.DUDAR.value)
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == str(TipoApuesta.DUDAR)
        mocker.patch("builtins.input", return_value=TipoApuesta.CALZAR.value)
        assert gestor_4_jugadores.solicitar_apuesta_a_jugador() == str(TipoApuesta.CALZAR)

    def test_eliminar_jugador(self, gestor_4_jugadores):
        """Verifica que se elimine un jugador cuando se queda sin dados."""
        cantidad_previa_jugadores = len(gestor_4_jugadores._jugadores)
        gestor_4_jugadores._jugadores[0]._dados_en_posecion = 0
        assert gestor_4_jugadores._jugadores[0].get_cantidad_dados() == 0
        gestor_4_jugadores.eliminar_jugador(0)
        assert len(gestor_4_jugadores._jugadores) == cantidad_previa_jugadores - 1

    # def test_subir_apuesta(self, mocker, gestor_4_jugadores):
    #     """Test que verifica que el movimiento de subir apuesta funcione correctamente."""
    #     mocker.patch(
    #         "builtins.input",
    #         side_effect=[TipoApuesta.SUBIR.value, f"3 {str(NombreDado.QUINA).lower()}"],
    #     )
    #     gestor_4_jugadores._turno_actual = 0
    #     apuesta = gestor_4_jugadores.solicitar_apuesta_a_jugador()
    #     gestor_4_jugadores.procesar_apuesta(apuesta)
    #     assert (
    #         gestor_4_jugadores._apuesta_actual
    #         == f"{str(TipoApuesta.SUBIR)} 3 {str(NombreDado.QUINA).lower()}"
    #     )

    # @pytest.mark.parametrize(
    #     "dado1,dado2,resultado,dados_jugador", [(3, 3, True, 4), (3, 2, False, 5), (2, 2, False, 5)]
    # )
    # def test_resultado_dudar(
    #     self, mocker, gestor_4_jugadores, dado1, dado2, resultado, dados_jugador
    # ):
    #     """Test para probar los casos de haber dudado exitosamente o incorrectamente."""
    #     gestor_4_jugadores._direccion_juego = DireccionJuego.Derecha
    #     gestor_4_jugadores._turno_actual = 1
    #     gestor_4_jugadores._apuesta_actual = (
    #         f"{str(TipoApuesta.SUBIR)} 4 {str(NombreDado.TONTO).lower()}"
    #     )
    #     mocker.patch(
    #         "src.game.dado.random.randint",
    #         side_effect=[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, dado1, dado2],
    #     )
    #     for jugador in gestor_4_jugadores._jugadores:
    #         jugador.agitar_cacho()
    #     resultado_dudar = gestor_4_jugadores.procesar_apuesta(str(TipoApuesta.DUDAR))
    #     assert (
    #         gestor_4_jugadores._apuesta_anterior
    #         == f"{str(TipoApuesta.SUBIR)} 4 {str(NombreDado.TONTO).lower()}"
    #     )
    #     assert gestor_4_jugadores._apuesta_actual == str(TipoApuesta.DUDAR)
    #     assert resultado_dudar == resultado
    #     assert gestor_4_jugadores._jugadores[0]._dados_en_posecion == dados_jugador

    # def test_calzar_exacto_gana_un_dado(self, mocker, gestor_4_jugadores):
    #     """Si el conteo coincide exactamente con la apuesta, el calzador gana 1 dado."""
    #     gestor = gestor_4_jugadores
    #     gestor._turno_actual = 0
    #     gestor._apuesta_actual = f"{str(TipoApuesta.SUBIR)} 6 {str(NombreDado.TREN).lower()}"

    #     side_effect = [3, 1, 6, 6, 6, 3, 3, 6, 6, 6, 1, 6, 6, 6, 6, 3, 6, 6, 6, 6]
    #     mocker.patch("src.game.dado.random.randint", side_effect=side_effect)
    #     for j in gestor._jugadores:
    #         j.agitar_cacho()
    #     antes = gestor._jugadores[0].get_cantidad_dados()
    #     resultado = gestor.procesar_apuesta(str(TipoApuesta.CALZAR))
    #     despues = gestor._jugadores[0].get_cantidad_dados()
    #     assert resultado is True
    #     assert despues == antes + 1

    # def test_calzar_falla_pierde_un_dado(self, mocker, gestor_4_jugadores):
    #     """Si el conteo no coincide exactamente, el calzador pierde 1 dado."""
    #     gestor = gestor_4_jugadores
    #     gestor._turno_actual = 1
    #     gestor._apuesta_actual = f"{str(TipoApuesta.SUBIR)} 5 {str(NombreDado.TONTO).lower()}"

    #     side_effect = [1, 3, 4, 5, 6, 2, 2, 1, 6, 6, 1, 1, 4, 5, 6, 1, 1, 4, 5, 6]
    #     mocker.patch("src.game.dado.random.randint", side_effect=side_effect)
    #     for j in gestor._jugadores:
    #         j.agitar_cacho()
    #     antes = gestor._jugadores[1].get_cantidad_dados()
    #     resultado = gestor.procesar_apuesta(str(TipoApuesta.CALZAR))
    #     despues = gestor._jugadores[1].get_cantidad_dados()
    #     assert resultado is False
    #     assert despues == antes - 1

    def test_jugar_ronda_termina_con_calzar(self, mocker, gestor_4_jugadores):
        """Ronda normal: termina con 'calzar'."""
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 0
        gestor._apuesta_actual = f"{str(TipoApuesta.SUBIR)} 6 {str(NombreDado.TREN).lower()}"

        mocker.patch(
            "src.game.dado.random.randint",
            side_effect=[3, 1, 6, 6, 6, 3, 3, 6, 6, 6, 1, 6, 6, 6, 6, 3, 6, 6, 6, 6],
        )
        mocker.patch("builtins.input", side_effect=["1", f"6 {str(NombreDado.TREN).lower()}", "4"])

        resultado = gestor.jugar_ronda()
        assert resultado["accion"] == str(TipoApuesta.CALZAR)
        assert resultado["termino"] is True
        assert resultado["resultado"] is True

    def test_jugar_ronda_termina_con_dudar(self, mocker, gestor_4_jugadores):
        """Una ronda termina cuando se ejecuta 'dudar' y se resuelve la apuesta."""
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 1
        gestor._apuesta_actual = f"{str(TipoApuesta.SUBIR)} 4 {str(NombreDado.TONTO).lower()}"

        mocker.patch(
            "src.game.dado.random.randint",
            side_effect=[1, 3, 4, 5, 6, 2, 2, 1, 6, 6, 1, 1, 4, 5, 6, 1, 1, 4, 5, 6],
        )
        mocker.patch("builtins.input", side_effect=["1", f"4 {str(NombreDado.TONTO).lower()}", "3"])

        resultado = gestor.jugar_ronda()
        assert resultado["accion"] == str(TipoApuesta.DUDAR)
        assert resultado["termino"] is True

    def test_jugar_ronda_especial_termina_con_dudar_y_obligar_cerrada(
        self, mocker, gestor_4_jugadores
    ):
        """Ronda especial: obligar 'cerrada', termina con 'dudar'."""
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 1
        gestor._jugadores[1]._dados_en_posecion = 1
        gestor._apuesta_actual = f"{str(TipoApuesta.SUBIR)} 4 {str(NombreDado.TONTO).lower()}"

        mocker.patch(
            "src.game.dado.random.randint",
            side_effect=[1, 2, 2, 6, 6, 1, 2, 1, 6, 6, 6, 1, 6, 6, 6, 6],
        )
        mocker.patch("builtins.input", side_effect=["5", str(NombreDado.TREN).lower(), "3"])

        resultado = gestor.jugar_ronda()
        assert resultado["accion"] == str(TipoApuesta.DUDAR)
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
        gestor._apuesta_actual = f"{str(TipoApuesta.SUBIR)} 3 {str(NombreDado.TREN).lower()}"

        mocker.patch(
            "src.game.dado.random.randint",
            side_effect=[3, 3, 6, 6, 6, 6, 1, 6, 6, 6, 6, 3, 6, 6, 6, 6],
        )
        mocker.patch("builtins.input", side_effect=["6", str(NombreDado.TREN).lower(), "4"])

        resultado = gestor.jugar_ronda()
        assert resultado["accion"] == str(TipoApuesta.CALZAR)
        assert resultado["termino"] is True
        assert resultado["resultado"] in (True, False)

    def test_especial_no_puede_cambiar_pinta_fijada(self, gestor_4_jugadores):
        """Test que valida que no se pueda subir la pinta en la ronda especial."""
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._jugadores[0]._dados_en_posecion = 1
        gestor._apuesta_actual = f"pasar 3 {str(NombreDado.TONTO).lower()}"
        gestor._ronda_especial = True
        assert (
            gestor.validar_apuesta_subir(False, f"1 3 {str(NombreDado.TREN).lower()}".split(" "))
            == "continue"
        )

    def test_especial_otro_con_un_dado_puede_cambiar_pinta_si_sube(
        self, mocker, gestor_4_jugadores
    ):
        """
        Test que valida durante la partida especial.

        Si hay otro jugador ademas del que invoco la partida especial con un solo dado,
        este puede cambiar la pinta fija solo si es que la sube.
        """
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._jugadores[0]._dados_en_posecion = 1
        gestor._jugadores[2]._dados_en_posecion = 1
        gestor._turno_actual = 1
        mocker.patch(
            "builtins.input",
            side_effect=[
                "5",
                str(NombreDado.TREN).lower(),
                "1",
                f"2 {str(NombreDado.TREN).lower()}",
                "1",
                f"3 {str(NombreDado.TONTO).lower()}",
                "4",
            ],
        )
        mocker.patch("src.game.dado.random.randint", side_effect=[3] * 20)

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
        gestor._pinta_fijada_especial = str(NombreDado.TREN).lower()
        gestor._obligador_nombre = obligador._nombre
        gestor._modo_especial = TipoRondaEspecial.CERRADA
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
        gestor._pinta_fijada_especial = str(NombreDado.TREN).lower()
        gestor._obligador_nombre = gestor._jugadores[0]._nombre
        gestor._modo_especial = TipoRondaEspecial.ABIERTA
        gestor._ver_propios = set()
        gestor._ver_ajenos = {j._nombre for j in gestor._jugadores}

        for x in gestor._jugadores:
            assert gestor.ver_cacho_para(x, x) is None
        for obs in gestor._jugadores:
            for obj in gestor._jugadores:
                if obs is obj:
                    continue
                assert gestor.ver_cacho_para(obs, obj) is not None

    def test_reset_visibilidad_al_terminar_ronda(self, mocker, gestor_4_jugadores):
        """Obligar configura visibilidad; al terminar (dudar) se resetea todo."""
        gestor = gestor_4_jugadores
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 0
        gestor._jugadores[0]._dados_en_posecion = 1
        gestor._apuesta_actual = f"{str(TipoApuesta.SUBIR)} 2 {str(NombreDado.TREN).lower()}"

        mocker.patch("src.game.dado.random.randint", side_effect=[3, 3, 3, 3, 3] * 4)
        mocker.patch("builtins.input", side_effect=["5"])
        with pytest.raises(StopIteration):
            _ = gestor.jugar_ronda()

        assert gestor._ronda_especial is True
        assert gestor._modo_especial == TipoRondaEspecial.CERRADA
        assert gestor._ver_propios == {gestor._jugadores[0]._nombre}
        assert gestor._ver_ajenos == set()

        mocker.patch("src.game.dado.random.randint", side_effect=[3, 3, 3, 3, 3] * 4)
        mocker.patch("builtins.input", side_effect=["3"])
        _ = gestor.jugar_ronda()

        assert gestor._ronda_especial is False
        assert gestor._modo_especial is None
        assert len(gestor._ver_propios) == 0
        assert len(gestor._ver_ajenos) == 0

    def test_calcular_dados_en_juego(self, gestor_4_jugadores):
        """Test para validar que se cuentan bien la cantidad de Dados en juego."""
        assert gestor_4_jugadores.dados_en_juego() == 20
        gestor_4_jugadores._jugadores[0].perder_dado()
        assert gestor_4_jugadores.dados_en_juego() == 19
        gestor_4_jugadores._jugadores[1].perder_dado()
        gestor_4_jugadores._jugadores[2].perder_dado()
        assert gestor_4_jugadores.dados_en_juego() == 17

    def test_terminar_partida_al_dudar_bien(self, mocker):
        """Test que prueba la finalizacion de una partida despues de dudar bien."""
        mocker.patch("builtins.input", side_effect=["Ricardo", "Martin"])
        gestor = GestorPartida(2)
        gestor._jugadores[1]._dados_en_posecion = 1
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 1
        gestor._obligar_usado["Martin"] = True
        side_effect = [2, 2, 2, 2, 2, 2]
        mocker.patch("src.game.dado.random.randint", side_effect=side_effect)
        mocker.patch(
            "builtins.input",
            side_effect=[
                TipoApuesta.SUBIR.value,
                f"3 {str(NombreDado.CUADRA).lower()}",
                TipoApuesta.DUDAR.value,
            ],
        )
        mocker.patch.object(GestorPartida, "definir_primer_jugador", return_value=None)
        mocker.patch.object(GestorPartida, "definir_direccion_juego", return_value=None)
        gestor.juego()
        assert len(gestor._jugadores) == 1
        assert gestor._jugadores[0]._nombre == "Ricardo"

    def test_terminar_partida_al_dudar_mal(self, mocker):
        """Test que prueba la finalizacion de una partida despues de dudar erroneamente."""
        mocker.patch("builtins.input", side_effect=["Ricardo", "Martin"])
        gestor = GestorPartida(2)
        gestor._jugadores[0]._dados_en_posecion = 1
        gestor._direccion_juego = DireccionJuego.Derecha
        gestor._turno_actual = 1
        gestor._obligar_usado["Ricardo"] = True
        side_effect = [4, 4, 4, 2, 2, 2]
        mocker.patch("src.game.dado.random.randint", side_effect=side_effect)
        mocker.patch(
            "builtins.input",
            side_effect=[
                TipoApuesta.SUBIR.value,
                f"3 {str(NombreDado.CUADRA).lower()}",
                TipoApuesta.DUDAR.value,
            ],
        )
        mocker.patch.object(GestorPartida, "definir_primer_jugador", return_value=None)
        mocker.patch.object(GestorPartida, "definir_direccion_juego", return_value=None)
        gestor.juego()
        assert len(gestor._jugadores) == 1
        assert gestor._jugadores[0]._nombre == "Martin"

    # @pytest.mark.parametrize(
    #     "numeros,resultado",
    #     [
    #         ([1, 1, 1, 2, 2], False),
    #         ([1, 1, 1, 1, 1], False),
    #         ([1, 2, 3, 4, 5], False),
    #         ([1, 2, 2, 3, 4], True),
    #     ],
    # )
    # def test_dudar_despues_de_pasar(self, mocker, gestor_4_jugadores, numeros, resultado):
    #     """Test que prueba dudar despues de pasar."""
    #     gestor = gestor_4_jugadores
    #     gestor._direccion_juego = DireccionJuego.Derecha
    #     gestor._turno_actual = 0
    #     gestor._apuesta_anterior = "subir 4 tonto"
    #     gestor._apuesta_actual = "pasar"
    #     mocker.patch(
    #         "src.game.dado.random.randint",
    #         side_effect=numeros * 4,
    #     )
    #     for j in gestor._jugadores:
    #         j.agitar_cacho()

    #     resultado = gestor.procesar_apuesta("dudar")

    #     assert resultado is resultado
    #     assert gestor._apuesta_actual == "dudar"

    def test_juego_completo(self, mocker, gestor_2_jugadores):
        gestor = gestor_2_jugadores

        mocker.patch.object(gestor, "definir_primer_jugador", return_value=None)
        mocker.patch.object(gestor, "definir_direccion_juego", return_value=None)
        gestor._turno_actual = 0
        gestor._direccion_juego = DireccionJuego.Derecha
        side_effect = [
            3,
            6,
            2,
            4,
            1,
            3,
            5,
            1,
            2,
            2,
            3,
            6,
            2,
            4,
            1,
            3,
            5,
            1,
            2,
            3,
            6,
            2,
            4,
            1,
            3,
            5,
            1,
            3,
            6,
            2,
            4,
            1,
            3,
            5,
            1,
            3,
            6,
            2,
            4,
            1,
            3,
            5,
            3,
            6,
            2,
            4,
            1,
            3,
            3,
            6,
            2,
            4,
            1,
            3,
            5,
            3,
            6,
            2,
            4,
            1,
            3,
        ]
        mocker.patch("src.game.dado.random.randint", side_effect=side_effect)
        side_effect2 = [
            TipoApuesta.SUBIR.value,
            "3 tonto",
            TipoApuesta.PASAR.value,
            TipoApuesta.DUDAR.value,
            # Pepa pierde 1 dado
            TipoApuesta.SUBIR.value,
            "2 tren",
            TipoApuesta.SUBIR.value,
            "2 cuadra",
            TipoApuesta.SUBIR.value,
            "4 cuadra",
            TipoApuesta.DUDAR.value,
            # Pepa pierde 1 dado
            TipoApuesta.SUBIR.value,
            "3 cuadra",
            TipoApuesta.CALZAR.value,
            # Pepe gana 1 dado
            TipoApuesta.SUBIR.value,
            "3 sexto",
            TipoApuesta.DUDAR.value,
            # Pepa pierde 1 dado
            TipoApuesta.SUBIR.value,
            "1 quina",
            TipoApuesta.SUBIR.value,
            "3 quina",
            TipoApuesta.CALZAR.value,
            # Pepa pierde 1 dado
            TipoRondaEspecial.CERRADA.value,
            TipoApuesta.SUBIR.value,
            "2 tren",
            TipoApuesta.SUBIR.value,
            "3 tren",
            TipoApuesta.CALZAR.value,
            # Pepa gana 1 dado
            TipoApuesta.SUBIR.value,
            "4 sexto",
            TipoApuesta.DUDAR.value,
            # Pepa pierde 1 dado
            TipoApuesta.SUBIR.value,
            "4 tonto",
            TipoApuesta.DUDAR.value,
            # Pepa pierde su ultimo dado
        ]
        mocker.patch("builtins.input", side_effect=side_effect2)
        gestor.juego()
        assert len(gestor._jugadores) == 1
        assert gestor._jugadores[0]._nombre == "Pepa"
        assert gestor._jugadores[0]._dados_en_posecion == 6
