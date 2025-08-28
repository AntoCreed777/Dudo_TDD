import pytest
from src.game.jugador import Jugador


class TestJugador:

    @pytest.fixture
    def jugador(self):
        return Jugador()

    def test_agitar_cacho(self, capsys, jugador):
        jugador.agitar_cacho()

        captura = capsys.readouterr()

        assert captura.out == "Cacho Agitado"
