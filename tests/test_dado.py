import pytest
from src.game.dado import Dado, NombreDado


class TestDado:

    @pytest.fixture
    def dado(self):
        return Dado()

    def test_generar_numero_del_1_al_6(self, dado, mocker):
        for enum_val in NombreDado:
            mocker.patch("random.randint", return_value=enum_val.value)
            dado.generar_numero()
            assert dado._valor == enum_val.value, f"El número generado debe ser {enum_val.value}"
            assert dado.get_valor() == str(enum_val), f"El nombre debe ser {str(enum_val)}"

    def test_generar_numeros_multiples(self, dado):
        valores = []
        for _ in range(1000):
            dado.generar_numero()
            valores.append(dado._valor)

        # Verificar que todos están en rango
        assert all(1 <= num <= 6 for num in valores), "Todos los números deberían estar entre 1 y 6"

        # Verificar que aparezcan todos los números al menos una vez
        for i in range(1, 7):
            assert i in valores, f"El número {i} debería aparecer al menos una vez"

    def test_numero_a_nombre(self, dado):
        for enum_val in NombreDado:
            assert dado.numero_a_nombre(enum_val.value) == str(enum_val)

    def test_numero_a_nombre_invalido(self, dado):
        with pytest.raises(ValueError, match="Número inválido"):
            dado.numero_a_nombre(0)

        with pytest.raises(ValueError, match="Número inválido"):
            dado.numero_a_nombre(7)

    def test_get_valor_nombre_correcto(self, dado, mocker):
        from src.game.dado import NombreDado
        for enum_val in NombreDado:
            mocker.patch("random.randint", return_value=enum_val.value)
            dado.generar_numero()
            assert dado.get_valor() == str(enum_val)

    def test_get_valor_sin_generar_numero(self, dado):
        dado._valor = None
        with pytest.raises(ValueError, match="No se ha generado ningún valor todavía"):
            dado.get_valor()
