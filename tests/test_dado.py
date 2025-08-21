import pytest
from src.game.dado import Dado

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
        assert all(1 <= num <= 6 for num in resultados), "Todos los números deberían estar entre 1 y 6"
        
        # Verificar que aparezcan todos los números al menos una vez
        for i in range(1, 7):
            assert i in resultados, f"El número {i} debería aparecer al menos una vez"
    
    def test_numero_a_nombre(self, dado):
        assert dado.numero_a_nombre(1) == "As"
        assert dado.numero_a_nombre(2) == "Dos"
        assert dado.numero_a_nombre(3) == "Tres"
        assert dado.numero_a_nombre(4) == "Cuatro"
        assert dado.numero_a_nombre(5) == "Cinco"
        assert dado.numero_a_nombre(6) == "Seis"
