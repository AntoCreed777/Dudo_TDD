"""Tests para la clase Jugador del juego Dudo."""

import pytest

from src.game.dado import NombreDado
from src.game.jugador import Jugador


class TestJugador:
    """Tests para la gestión de Jugador en Dudo."""

    @pytest.fixture
    def jugador(self):
        """Fixture que retorna un Jugador."""
        return Jugador("Antonio")

    def test_agitar_cacho(self, capsys, jugador):
        """Verifica que se agite el cacho correctamente."""
        jugador.agitar_cacho()
        captura = capsys.readouterr()
        assert captura.out == "Cacho Agitado\n"

    @pytest.mark.parametrize(
        "parametros_input, impresion_esperada",
        [
            ([str(NombreDado.AS)], "Cacho Agitado\nTu cacho:\n\tDado 1: As\n"),
            (
                [str(NombreDado.QUINA), str(NombreDado.TONTO)],
                "Cacho Agitado\nTu cacho:\n\tDado 1: Quina\n\tDado 2: Tonto\n",
            ),
            ([], "Cacho Agitado\nTu cacho:\n\tNo tienes dados para ver, tu cacho esta vacio\n"),
            (None, "Cacho Agitado\nTu cacho:\n\tEsta Oculto, no puedes ver el contenido\n"),
        ],
    )
    def test_ver_cacho(self, mocker, capsys, jugador, parametros_input, impresion_esperada):
        """Verifica la visualización de los resultados del cacho."""
        mocker.patch.object(jugador._cacho, "get_resultados", return_value=parametros_input)
        jugador.agitar_cacho()
        jugador.ver_cacho()
        captura = capsys.readouterr()
        assert captura.out == impresion_esperada
