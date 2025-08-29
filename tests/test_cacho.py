"""Tests para la clase Cacho del juego Dudo."""

import pytest

from src.game.cacho import Cacho


class TestCacho:
    """Tests para la gestión de Cacho en Dudo."""

    @pytest.fixture
    def cacho(self):
        """Fixture que retorna un Cacho."""
        return Cacho()

    def test_agitar(self):
        """Verifica que se agiten los dados correctamente."""
        for cantidad in range(6):  # Pruebo desde 0 hasta 5 dados
            cacho = Cacho()
            cacho.agitar(cantidad=cantidad)
            contador = sum(1 for dado in cacho._dados if dado._valor is not None)
            assert cantidad == contador, f"Deben de haber{cantidad} dados con valores asignados"

    def test_agitar_cantidad_superior_a_5(self, cacho):
        """Verifica que no se agiten más de 5 dados."""
        cacho.agitar(cantidad=6)
        contador = sum(1 for dado in cacho._dados if dado._valor is not None)
        assert 5 == contador, "Solo deben agitarse 5 dados como máximo"

    def test_agitar_cantidad_invalida(self, cacho):
        """Verifica que lanzar una cantidad inválida de dados lanza excepción."""
        with pytest.raises(ValueError, match="Cantidad a agitar invalida"):
            cacho.agitar(cantidad=-1)

    def test_get_resultados(self, cacho):
        """Verifica que los resultados sean correctos tras agitar."""
        cantidad = 5
        cacho.agitar(cantidad=cantidad)
        resultados = cacho.get_resultados()
        assert len(resultados) == cantidad
        for resultado in resultados:
            assert isinstance(resultado, str)

    def test_ocualtar(self, cacho):
        """Verifica que ocultar el cacho retorna None en resultados."""
        cacho.agitar(cantidad=1)
        assert cacho.get_resultados() is not None
        cacho.ocultar()
        assert cacho.get_resultados() is None, "Si el cacho está oculto, debe retornar None"

    def test_mostrar(self, cacho):
        """Verifica que mostrar el cacho lo haga visible nuevamente."""
        cacho.agitar(cantidad=1)
        cacho.ocultar()
        assert cacho.get_resultados() is None
        cacho.mostrar()
        assert cacho.get_resultados() is not None
        assert len(cacho.get_resultados()) == 1

    def test_get_resultados_sin_agitar(self, cacho):
        """Verifica que sin agitar el cacho los resultados sean None."""
        assert cacho.get_resultados() is None
        assert cacho.get_resultados() is None
