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

    def test_contar_pintas(self, mocker, contador_pintas):
        jugador = Jugador("Test")
        mocker.patch.object(jugador, "ver_cacho", return_value=None)

        with pytest.raises(ValueError, match="Error en dados de jugador"):
            contador_pintas.contar_pintas([jugador])
