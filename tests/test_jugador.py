import pytest
from src.game.jugador import Jugador
from src.game.dado import NombreDado


class TestJugador:

    @pytest.fixture
    def jugador(self):
        return Jugador()

    def test_agitar_cacho(self, capsys, jugador):
        jugador.agitar_cacho()

        captura = capsys.readouterr()

        assert captura.out == "Cacho Agitado\n"

    @pytest.mark.parametrize("parametros_input, impresion_esperada", [
            (
                [str(NombreDado.AS)],
                "Cacho Agitado\nTu cacho:\n\tDado 1: As\n"
            ),
            (
                [str(NombreDado.QUINA), str(NombreDado.TONTO)],
                "Cacho Agitado\nTu cacho:\n\tDado 1: Quina\n\tDado 2: Tonto\n"
            ),
            (
                None,
                "Cacho Agitado\nTu cacho:\n\tNo tienes dados para ver, tu cacho esta vacio\n"
            )
        ]
    )
    def test_ver_cacho(self, mocker, capsys, jugador, parametros_input, impresion_esperada):
        mocker.patch.object(jugador._cacho, "get_resultados", return_value=parametros_input)

        jugador.agitar_cacho()
        jugador.ver_cacho()

        captura = capsys.readouterr()

        assert captura.out == impresion_esperada
