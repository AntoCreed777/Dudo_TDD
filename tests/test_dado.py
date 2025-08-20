from src.game.dado import Dado

class TestDado:
    def test_generar_numero_del_1_al_6(self):
        dado = Dado()
        assert 1 <= dado.generar_numero() <= 6
