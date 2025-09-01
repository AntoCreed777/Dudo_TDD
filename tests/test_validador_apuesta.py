"""Tests para la clase ValidadorApuesta del juego Dudo."""

import pytest

from src.game.dado import NombreDado
from src.game.jugador import TipoApuesta
from src.game.validador_apuesta import Apuesta, ValidadorApuesta


@pytest.fixture
def validador():
    """Fixture que retorna un ValidadorApuesta."""
    return ValidadorApuesta()


class TestValidadorApuesta:
    """Tests para la gestión de ValidadorApuesta en Dudo."""

    def test_subir_por_cantidad_o_pinta_superior(self, validador):
        """Verifica la regla de subir por cantidad o pinta superior."""
        base = Apuesta(str(TipoApuesta.SUBIR), 2, NombreDado.TREN)
        assert validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 3, NombreDado.TREN))
        assert validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 2, NombreDado.CUADRA))
        assert not validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 2, NombreDado.TONTO))
        assert not validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 2, NombreDado.TREN))
        assert not validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 1, NombreDado.CUADRA))

    def test_regla_cambiar_a_ases(self, validador):
        """Verifica la regla de cambiar a ases."""
        base = Apuesta(str(TipoApuesta.SUBIR), 7, NombreDado.TREN)
        assert validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 4, NombreDado.AS))
        base = Apuesta(str(TipoApuesta.SUBIR), 8, NombreDado.TREN)
        assert validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 5, NombreDado.AS))
        assert not validador.es_valida(
            Apuesta(str(TipoApuesta.SUBIR), 7, NombreDado.QUINA),
            Apuesta(str(TipoApuesta.SUBIR), 3, NombreDado.AS),
        )

    def test_regla_desde_ases(self, validador):
        """Verifica la regla de bajar desde ases."""
        base = Apuesta(str(TipoApuesta.SUBIR), 2, NombreDado.AS)
        assert validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 5, NombreDado.TREN))
        assert not validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 4, NombreDado.TREN))
        base = Apuesta(str(TipoApuesta.SUBIR), 4, NombreDado.AS)
        assert validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 9, NombreDado.SEXTO))
        assert not validador.es_valida(base, Apuesta(str(TipoApuesta.SUBIR), 8, NombreDado.SEXTO))

    def test_puede_partir_con_ases_solo_primera_vez_por_jugador(self, validador):
        """Verifica la regla de partir con ases solo la primera vez por jugador."""
        assert validador.puede_partir_con_ases(dados_en_mano=1, ya_usado=False)
        assert not validador.puede_partir_con_ases(dados_en_mano=1, ya_usado=True)
        assert not validador.puede_partir_con_ases(dados_en_mano=2, ya_usado=False)
        assert validador.puede_partir_con_ases(dados_en_mano=1, ya_usado=False)

    def test_puede_calzar(self, validador):
        """Se puede calzar si hay la mitad o más de los dados máximos en juego,
        o el jugador que calza tiene 1 dado.
        """
        assert validador.puede_calzar(dados_en_juego=12, dados_maximos=20, dados_del_jugador=3)
        assert validador.puede_calzar(dados_en_juego=10, dados_maximos=20, dados_del_jugador=5)
        assert not validador.puede_calzar(dados_en_juego=9, dados_maximos=20, dados_del_jugador=2)
        assert validador.puede_calzar(dados_en_juego=9, dados_maximos=20, dados_del_jugador=1)
