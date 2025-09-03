"""Tests para la clase ContadorPintas del juego Dudo."""

import pytest

from src.game.contador_pintas import ContadorPintas
from src.game.jugador import Jugador


class TestContadorPintas:
    """Tests para la gestión de partida en Dudo."""

    @pytest.fixture
    def contador_pintas(self):
        """Fixture que retorna ContadorPintas."""
        return ContadorPintas()

    def test_contar_pintas_error_dados_jugador(self, mocker, contador_pintas):
        """Test que valida que se lanze la excepcion cuando ocurre el error."""
        jugador = Jugador("Test")
        mocker.patch.object(jugador, "ver_cacho", return_value=None)

        with pytest.raises(ValueError, match="Error en dados de jugador"):
            contador_pintas.contar_pintas([jugador])
