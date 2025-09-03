"""Tests para la clase ValidadorApuesta del juego Dudo."""

import pytest

from src.game.dado import NombreDado
from src.game.validador_apuesta import Apuesta, ValidadorApuesta


@pytest.fixture
def validador():
    """Fixture que retorna un ValidadorApuesta."""
    return ValidadorApuesta()


class TestValidadorApuesta:
    """Tests para la gestión de ValidadorApuesta en Dudo."""

    def test_subir_por_cantidad_o_pinta_superior(self, validador):
        """Verifica la regla de subir por cantidad o pinta superior."""
        base = Apuesta(2, NombreDado.TREN)
        assert validador.puede_subir(base, Apuesta(3, NombreDado.TREN))
        assert validador.puede_subir(base, Apuesta(2, NombreDado.CUADRA))
        assert not validador.puede_subir(base, Apuesta(2, NombreDado.TONTO))
        assert not validador.puede_subir(base, Apuesta(2, NombreDado.TREN))
        assert not validador.puede_subir(base, Apuesta(1, NombreDado.CUADRA))

    def test_regla_cambiar_a_ases(self, validador):
        """Verifica la regla de cambiar a ases."""
        base = Apuesta(7, NombreDado.TREN)
        assert validador.puede_subir(base, Apuesta(4, NombreDado.AS))
        base = Apuesta(8, NombreDado.TREN)
        assert validador.puede_subir(base, Apuesta(5, NombreDado.AS))
        assert not validador.puede_subir(
            Apuesta(7, NombreDado.QUINA),
            Apuesta(3, NombreDado.AS),
        )

    def test_regla_desde_ases(self, validador):
        """Verifica la regla de bajar desde ases."""
        base = Apuesta(2, NombreDado.AS)
        assert validador.puede_subir(base, Apuesta(5, NombreDado.TREN))
        assert not validador.puede_subir(base, Apuesta(4, NombreDado.TREN))
        base = Apuesta(4, NombreDado.AS)
        assert validador.puede_subir(base, Apuesta(9, NombreDado.SEXTO))
        assert not validador.puede_subir(base, Apuesta(8, NombreDado.SEXTO))

    def test_puede_partir_con_ases_solo_primera_vez_por_jugador(self, validador):
        """Verifica la regla de partir con ases solo la primera vez por jugador."""
        assert validador.puede_partir_con_ases(dados_en_mano=1, ya_usado=False)
        assert not validador.puede_partir_con_ases(dados_en_mano=1, ya_usado=True)
        assert not validador.puede_partir_con_ases(dados_en_mano=2, ya_usado=False)
        assert validador.puede_partir_con_ases(dados_en_mano=1, ya_usado=False)

    def test_puede_calzar(self, validador):
        """
        Test que valida si se puede calzar o no.

        Se puede calzar si hay la mitad o más de los dados máximos en juego,
        o el jugador que calza tiene 1 dado.
        """
        assert validador.puede_calzar(dados_en_juego=12, dados_maximos=20, dados_del_jugador=3)
        assert validador.puede_calzar(dados_en_juego=10, dados_maximos=20, dados_del_jugador=5)
        assert not validador.puede_calzar(dados_en_juego=9, dados_maximos=20, dados_del_jugador=2)
        assert validador.puede_calzar(dados_en_juego=9, dados_maximos=20, dados_del_jugador=1)

    def test_puede_subir_sube_cantidad_errado(self, validador):
        assert (
            validador.puede_subir(
                actual=Apuesta(3, NombreDado.QUINA),
                nueva=Apuesta(4, NombreDado.SEXTO),
                ronda_especial=True,
            )
            is False
        )
