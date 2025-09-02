"""Módulo que contiene la clase Jugador para el juego Dudo."""

from enum import Enum

from src.game.cacho import Cacho
from src.game.dado import NombreDado


class TipoApuesta(Enum):
    SUBIR = "1"
    PASAR = "2"
    DUDAR = "3"
    CALZAR = "4"

    def __str__(self):
        traduccion = {
            TipoApuesta.SUBIR: "subir",
            TipoApuesta.PASAR: "pasar",
            TipoApuesta.DUDAR: "dudar",
            TipoApuesta.CALZAR: "calzar",
        }
        return traduccion[self]


class Jugador:
    """Clase que representa un jugador en el juego Dudo."""

    _cacho: Cacho
    _dados_en_posecion: int
    _nombre: str

    def __init__(self, nombre):
        """Inicializa el jugador con un cacho y 5 dados en posesión."""
        self._nombre = nombre
        self._cacho = Cacho()
        self._dados_en_posecion = 5

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

        return resultados

    def realizar_apuesta(self, apuesta_anterior: str, apuesta_actual: str) -> str:
        """Permite al Jugador realizar una apuesta."""
        hay_apuesta_anterior: bool = apuesta_anterior != ""
        hay_apuesta_actual: bool = apuesta_actual != ""
        indicaciones = "\n"
        numeros_validos = ["1"]

        if hay_apuesta_anterior:
            indicaciones += (
                f"Apuesta anterior: {apuesta_anterior}\nApuesta actual: {apuesta_actual}\n"
            )
        elif hay_apuesta_actual:
            indicaciones += f"Apuesta actual: {apuesta_actual}\n"

        indicaciones += (
            f"{self._nombre}, "
            "Ingrese el número correspondiente a la apuesta que quiere realizar:\n1: Subir\n"
        )
        if hay_apuesta_actual:
            if apuesta_actual != str(TipoApuesta.PASAR):
                indicaciones += "2: Pasar\n"
                numeros_validos.append("2")

            indicaciones += "3: Dudar\n"
            numeros_validos.append("3")
            indicaciones += "4: Calzar\n"
            numeros_validos.append("4")

        indicaciones += "\nR: "

        apuesta = input(indicaciones)
        while apuesta not in numeros_validos:
            print("\nLa jugada ingresada no es valida, ingrese una nueva jugada.")
            apuesta = input(indicaciones)

        if apuesta == TipoApuesta.SUBIR.value:
            pintas = [str(pinta).lower() for pinta in NombreDado]
            apuesta = ""
            while (
                len(apuesta.split(" ")) != 2
                or not apuesta.split(" ")[0].isdigit()
                or apuesta.split(" ")[1].lower() not in pintas
            ):
                apuesta = input(
                    "\nIngrese la cantidad de dados seguido de la pinta a estimar "
                    "separados por un espacio (Ej: 5 tren):\n\nR: "
                )
            return f"{TipoApuesta.SUBIR} " + apuesta
        elif apuesta == TipoApuesta.PASAR.value:
            return str(TipoApuesta.PASAR)
        elif apuesta == TipoApuesta.DUDAR.value:
            return str(TipoApuesta.DUDAR)
        else:
            return str(TipoApuesta.CALZAR)

    def get_cantidad_dados(self) -> int:
        """Retorna la cantidad de dados en posecion."""
        return self._dados_en_posecion

    def perder_dado(self):
        """Resta un dado al jugador."""
        self._dados_en_posecion -= 1

    def ganar_dado(self):
        """Suma un dado al jugador"""
        self._dados_en_posecion += 1
