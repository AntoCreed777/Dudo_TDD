"""Módulo que contiene la clase Jugador para el juego Dudo."""

from src.game.cacho import Cacho


class Jugador:
    """Clase que representa un jugador en el juego Dudo."""

    _cacho: Cacho
    _dados_en_posecion: int

    def __init__(self, nombre):
        """Inicializa el jugador con un cacho y sin dados en posesión."""
        self._nombre = nombre
        self._cacho = Cacho()
        self._dados_en_posecion = 0

    def agitar_cacho(self):
        """Agita el cacho del jugador con la cantidad de dados en posesión."""
        self._cacho.agitar(cantidad=self._dados_en_posecion)
        print("Cacho Agitado")

    def ver_cacho(self):
        """Muestra los resultados de los dados en el cacho del jugador."""
        print("Tu cacho:")

        resultados = self._cacho.get_resultados()

        if resultados is None:
            print("\tEsta Oculto, no puedes ver el contenido")
            return

        if len(resultados) == 0:
            print("\tNo tienes dados para ver, tu cacho esta vacio")
            return

        for i, resultado in enumerate(resultados):
            print(f"\tDado {i + 1}: {resultado}")

    def realizar_apuesta(self, apuesta_anterior: str, apuesta_actual: str) -> str:
        hay_apuesta_anterior: bool = apuesta_anterior != ""
        hay_apuesta_actual: bool = apuesta_actual != ""
        indicaciones = "\n"
        numeros_validos = ["1", "2", "3", "4"]

        if hay_apuesta_anterior:
            indicaciones += f"Apuesta anterior: {apuesta_anterior}\nApuesta actual: "
            "{apuesta_actual}\n"
        elif hay_apuesta_actual:
            indicaciones += f"Apuesta actual: {apuesta_actual}\n"

        indicaciones += f"{self._nombre}, Ingrese el número correspondiente a la apuesta"
        "que quiere realizar:\n1: Subir\n2: Pasar\n3: Dudar\n4: Calzar\n\nR: "

        # indicaciones += f"{self._nombre}, Ingrese el número correspondiente a la apuesta"
        # " que quiere realizar:\n"
        # "1: Subir\n"
        # if apuesta_actual != "pasar":
        #     indicaciones += "2: Pasar\n"
        # if hay_apuesta_actual:
        #     indicaciones += "3: Dudar\n"
        # if hay_apuesta_actual and apuesta_actual != "pasar" or hay_apuesta_anterior:
        #     indicaciones += "4: Calzar\n"

        # indicaciones += "\nR: "
        apuesta = None
        while apuesta not in numeros_validos:
            apuesta = input(indicaciones)

        if apuesta == "1":
            pintas = ["as", "tonto", "tren", "cuadra", "quina", "sexto"]
            apuesta = ""
            while (len(apuesta.split(" ")) != 2 or not apuesta.split(" ")[0].isdigit()
                   or apuesta.split(" ")[1].lower() not in pintas):
                apuesta = input("\nIngrese la cantidad de dados seguido de la pinta a estimar "
                                "separados por un espacio (Ej: 5 tren):\nR: ")
            return ("subir " + apuesta).strip()
        elif apuesta == "2":
            return "pasar"
        elif apuesta == "3":
            return "dudar"
        elif apuesta == "4":
            return "calzar"
