"""Módulo que contiene la clase ArbitroRonda para gestionar la ronda del juego Dudo."""

from src.game.contador_pintas import ContadorPintas
from src.game.dado import NombreDado
from src.game.jugador import Jugador, TipoApuesta


class ArbitroRonda:
    @staticmethod
    def procesar_apuesta(
        apuesta_anterior: str,
        apuesta_actual: str,
        apuesta_nueva: str,
        jugadores: list[Jugador],
        es_ronda_especial: bool,
        turno_anterior: int,
    ) -> bool:
        """Procesa una apuesta durante la ronda."""
        if apuesta_nueva == str(TipoApuesta.DUDAR):
            return ArbitroRonda.procesar_apuesta_dudar(
                apuesta_actual, jugadores, es_ronda_especial, turno_anterior
            )
        else:
            return ArbitroRonda.procesar_apuesta_calzar(
                apuesta_anterior, apuesta_actual, jugadores, es_ronda_especial
            )

    @staticmethod
    def procesar_apuesta_dudar(
        apuesta_actual: str, jugadores: list[Jugador], es_ronda_especial: bool, turno_anterior: int
    ) -> bool:
        contador_pintas = ContadorPintas()
        cantidad_pintas: dict[str, int] = contador_pintas.contar_pintas(jugadores=jugadores)

        cantidad_pinta_apuesta = 0

        apuesta_tokenizada = apuesta_actual.split(" ")

        if apuesta_tokenizada[0] == str(TipoApuesta.SUBIR):
            pinta_objetivo = apuesta_tokenizada[2]
            if es_ronda_especial:
                cantidad_pinta_apuesta = cantidad_pintas[pinta_objetivo]
            else:
                cantidad_pinta_apuesta = cantidad_pintas[str(NombreDado.AS).lower()]
                if pinta_objetivo != str(NombreDado.AS).lower():
                    cantidad_pinta_apuesta += cantidad_pintas[pinta_objetivo]

            if cantidad_pinta_apuesta >= int(apuesta_tokenizada[1]):
                return False
            else:
                return True
        else:
            conteo_de_pintas = contador_pintas.contar_pintas([jugadores[turno_anterior]])

            cantidad_2 = 0
            cantidad_3 = 0
            cantidad_5 = 0
            todos_diferentes = True
            for pinta in conteo_de_pintas:
                if conteo_de_pintas[pinta] == 2:
                    cantidad_2 += 1
                    todos_diferentes = False
                elif conteo_de_pintas[pinta] == 3:
                    cantidad_3 += 1
                    todos_diferentes = False
                elif conteo_de_pintas[pinta] == 4:
                    todos_diferentes = False
                elif conteo_de_pintas[pinta] == 5:
                    cantidad_5 += 1
                    todos_diferentes = False

            # Exite una pinta que tiene 3 apariciones y otra con 2, existe una pinta con 5 apariciones o todas las pintas son diferentes
            if (cantidad_3 == 1 and cantidad_2 == 1) or cantidad_5 == 1 or todos_diferentes:
                return False
            else:
                return True

    @staticmethod
    def procesar_apuesta_calzar(
        apuesta_anterior: str,
        apuesta_actual: str,
        jugadores: list[Jugador],
        es_ronda_especial: bool,
    ) -> bool:
        contador_pintas = ContadorPintas()
        cantidad_pintas: dict[str, int] = contador_pintas.contar_pintas(jugadores=jugadores)
        prev = apuesta_actual.split(" ")

        # Elige la apuesta actual o la anterior dependiendo si la actual es pasar
        if prev[0] == str(TipoApuesta.SUBIR):
            cantidad_objetivo = int(prev[1])
            pinta_objetivo = prev[2]
        else:
            prev = apuesta_anterior.split(" ")
            cantidad_objetivo = int(prev[1])
            pinta_objetivo = prev[2]

        cantidad = 0
        if es_ronda_especial:
            cantidad = cantidad_pintas[pinta_objetivo]
        else:
            cantidad = cantidad_pintas[str(NombreDado.AS).lower()]
            if pinta_objetivo != str(NombreDado.AS).lower():
                cantidad += cantidad_pintas[pinta_objetivo]

        if cantidad == cantidad_objetivo:
            return True
        else:
            return False
