import pytest
from src.game.cacho import Cacho


class TestCacho:

    @pytest.fixture
    def cacho(self):
        return Cacho()

    def test_agitar(self, cacho):
        for cantidad in range(6):   # Pruebo desde 0 hasta 5 dados
            resultados = cacho.agitar(cantidad=cantidad)
            assert len(resultados) == cantidad
