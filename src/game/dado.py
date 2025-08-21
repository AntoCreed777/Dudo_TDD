class Dado:
    def generar_numero(self) -> int:
        import random
        return random.randint(1, 6)  # [1, 6]

    def numero_a_nombre(self, numero: int) -> str:
        nombres = {
            1: "As",
            2: "Tonto",
            3: "Tren",
            4: "Cuadra",
            5: "Quina",
            6: "Sexto"
        }
        if numero in nombres:
            return nombres[numero]
        raise ValueError("Número inválido")
