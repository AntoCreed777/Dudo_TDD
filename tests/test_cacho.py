import pytest
from src.game.cacho import Cacho


class TestCacho:

    @pytest.fixture
    def cacho(self):
        return Cacho()

    def test_agitar(self):
        for cantidad in range(6):   # Pruebo desde 0 hasta 5 dados
            cacho = Cacho()
            cacho.agitar(cantidad=cantidad)
            contador = 0
            for dado in cacho._dados:
                if dado._valor is not None:
                    contador += 1
            assert cantidad == contador, f"Deben de haber{cantidad} dados con valores asignados"

    def test_agitar_cantidad_superior_a_5(self, cacho):
        cantidad_ingresada = 6
        cantidad_esperada = 5

        cacho.agitar(cantidad=cantidad_ingresada)
        contador = 0

        for dado in cacho._dados:
            if dado._valor is not None:
                contador += 1
        assert cantidad_esperada == contador, f"Deben de haber{cantidad_esperada} dados con valores asignados"

    def test_agitar_cantidad_invalida(self, cacho):
        with pytest.raises(ValueError, match="Cantidad a agitar invalida"):
            cacho.agitar(cantidad=-1)

    def test_get_resultados(self, cacho):
        cantidad = 5

        cacho.agitar(cantidad=cantidad)
        resultados = cacho.get_resultados()

        assert len(resultados) == cantidad
        for resultado in resultados:
            assert isinstance(resultado, str)
