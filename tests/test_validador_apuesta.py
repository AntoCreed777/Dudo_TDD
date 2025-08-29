import pytest
from src.game.validador_apuesta import ValidadorApuesta, Apuesta
from src.game.dado import NombreDado


@pytest.fixture
def validador():
    return ValidadorApuesta()


class TestValidadorApuesta:
    def test_subir_por_cantidad_o_pinta_superior(self, validador):
        base = Apuesta(2, NombreDado.TREN)

        assert validador.es_valida(base, Apuesta(3, NombreDado.TREN))
        assert validador.es_valida(base, Apuesta(2, NombreDado.CUADRA))

        assert not validador.es_valida(base, Apuesta(2, NombreDado.TONTO))
        assert not validador.es_valida(base, Apuesta(2, NombreDado.TREN))
        assert not validador.es_valida(base, Apuesta(1, NombreDado.CUADRA))

    def test_regla_cambiar_a_ases(self, validador):
        base = Apuesta(7, NombreDado.TREN)
        assert validador.es_valida(base, Apuesta(4, NombreDado.AS))

        base = Apuesta(8, NombreDado.TREN)
        assert validador.es_valida(base, Apuesta(5, NombreDado.AS))

        assert not validador.es_valida(
            Apuesta(7, NombreDado.QUINA),
            Apuesta(3, NombreDado.AS),
        )

    def test_regla_desde_ases(self, validador):
        base = Apuesta(2, NombreDado.AS)
        assert validador.es_valida(base, Apuesta(5, NombreDado.TREN))
        assert not validador.es_valida(base, Apuesta(4, NombreDado.TREN))

        base = Apuesta(4, NombreDado.AS)
        assert validador.es_valida(base, Apuesta(9, NombreDado.SEXTO))
        assert not validador.es_valida(base, Apuesta(8, NombreDado.SEXTO))

    def test_puede_partir_con_ases_solo_primera_vez_por_jugador(self, validador):
        assert validador.puede_partir_con_ases(dados_en_mano=1, ya_usado=False)
        assert not validador.puede_partir_con_ases(dados_en_mano=1, ya_usado=True)
        assert not validador.puede_partir_con_ases(dados_en_mano=2, ya_usado=False)
        assert validador.puede_partir_con_ases(dados_en_mano=1, ya_usado=False)
