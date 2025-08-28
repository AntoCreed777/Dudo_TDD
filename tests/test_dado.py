import pytest
from src.game.dado import Dado, NombreDado


class TestDado:

    @pytest.fixture
    def dado(self):
        return Dado()

    def test_generar_numero_del_1_al_6(self, dado):
        resultado = dado.generar_numero()
        assert 1 <= resultado <= 6, "El número debe estar entre 1 y 6"

    def test_generar_numeros_multiples(self, dado):
        resultados = [dado.generar_numero() for _ in range(1000)]

        # Verificar que todos están en rango
        assert all(1 <= num <= 6 for num in resultados), \
            "Todos los números deberían estar entre 1 y 6"

        # Verificar que aparezcan todos los números al menos una vez
        for i in range(1, 7):
            assert i in resultados, f"El número {i} debería aparecer al menos una vez"

    def test_numero_a_nombre(self, dado):
        for enum_val in NombreDado:
            assert dado.numero_a_nombre(enum_val.value) == str(enum_val)

    def test_numero_a_nombre_invalido(self, dado):
        with pytest.raises(ValueError, match="Número inválido"):
            dado.numero_a_nombre(0)

        with pytest.raises(ValueError, match="Número inválido"):
            dado.numero_a_nombre(7)
