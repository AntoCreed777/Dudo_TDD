"""Módulo que contiene la clase GestorPartida para gestionar la lógica de la partida de Dudo."""

import os
import platform
from enum import Enum

from src.game.arbitro_ronda import ArbitroRonda
from src.game.contador_pintas import ContadorPintas
from src.game.dado import Dado, NombreDado
from src.game.jugador import Jugador, TipoApuesta
from src.game.validador_apuesta import Apuesta, ValidadorApuesta

# Constantes de retorno
STR_BREAK: str = "break"
STR_CONTINUE: str = "continue"


def limpiar_terminal():
    """Limpia la terminal según el sistema operativo."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


class DireccionJuego(Enum):
    """Dirección de turno en la partida: derecha o izquierda."""

    Derecha = {"Numero_str": "1", "bool": True}
    Izquierda = {"Numero_str": "-1", "bool": False}

    def __str__(self):
        """Devuelve la representación legible de la dirección."""
        direcciones = {DireccionJuego.Derecha: "Derecha", DireccionJuego.Izquierda: "Izquierda"}
        return direcciones[self]


class TipoRondaEspecial(Enum):
    """Tipos de ronda especial: abierta, cerrada o normal."""

    CERRADA = "5"
    ABIERTA = "6"
    NORMAL = "7"

    def __str__(self):
        """Devuelve la representación legible del modo de ronda especial."""
        traduccion = {
            TipoRondaEspecial.ABIERTA: "Abierta",
            TipoRondaEspecial.CERRADA: "Cerrada",
            TipoRondaEspecial.NORMAL: "Normal",
        }
        return traduccion[self]


class GestorPartida:
    """Clase que gestiona la partida, jugadores y turnos."""

    _jugadores: list[Jugador]
    _direccion_juego: DireccionJuego | None
    _turno_actual: int
    _apuesta_anterior: str
    _apuesta_actual: str
    _contador_pintas: ContadorPintas
    _ronda_especial: bool
    _obligar_usado: dict[str, bool]
    _modo_especial: TipoRondaEspecial | None
    _ver_propios: set
    _ver_ajenos: set
    _total_dados_iniciales: int

    def __init__(self, cantidad_jugadores: int):
        """Inicializa el gestor de partida con la cantidad de jugadores indicada."""
        self._jugadores = []
        self._direccion_juego = None
        self._turno_actual = -1
        self._apuesta_anterior = ""
        self._apuesta_actual = ""
        self._ronda_especial = False
        self._obligar_usado = {j._nombre: False for j in self._jugadores}
        self._modo_especial = None
        self._ver_propios = set()
        self._ver_ajenos = set()
        self._total_dados_iniciales = 5 * cantidad_jugadores

        self._contador_pintas = ContadorPintas()

        for _ in range(cantidad_jugadores):
            nombre = input(f"\nIngrese el nombre del jugador {_ + 1}: ")
            self._jugadores.append(Jugador(nombre))

    def juego(self):
        """Ejecuta el bucle principal del juego hasta que exista un ganador."""
        self.definir_primer_jugador()
        self.definir_direccion_juego()

        while True:
            resultado = self.jugar_ronda()
            if resultado["accion"] == str(TipoApuesta.DUDAR):
                if self.accion_dudar(resultado=resultado["resultado"]):
                    break
            else:
                if resultado["resultado"]:
                    jugador_ganador = self._jugadores[self._turno_actual]
                    print(f"¡{jugador_ganador._nombre} calzo exitosamente y gano un dado!\n")
                else:
                    jugador_perdedor = self._jugadores[self._turno_actual]
                    print(f"¡{jugador_perdedor._nombre} calzo erroneamente y pierde un dado!\n")
                    if jugador_perdedor.get_cantidad_dados() == 0:
                        self.eliminar_jugador(self._turno_actual)
                        print(
                            f"{jugador_perdedor._nombre} se ha quedado sin dados ¡Jugador eliminado!\n"
                        )
                        if len(self._jugadores) == 1:
                            print(
                                f"El juego a finalizado ¡{self._jugadores[0]._nombre} es el ganador!\n"
                            )
                            break

    def accion_dudar(self, resultado: bool) -> bool:
        """Resuelve los efectos de 'dudar' y actualiza turnos/estado.

        Args:
            resultado: True si pierde el jugador anterior; False si pierde quien duda.

        Returns:
            True si la partida terminó tras esta resolución, False en caso contrario.
        """
        if resultado:
            direccion_juego = self._direccion_juego
            if direccion_juego is None:
                raise TypeError("No puede ser None al momento de ejecutar esto")

            indice_jugador = self.calcular_turno(not direccion_juego.value["bool"])
            jugador_perdedor = self._jugadores[indice_jugador]
            print(
                f"¡{self._jugadores[self._turno_actual]._nombre} dudo exitosamente!\n"
                f"¡{jugador_perdedor._nombre} pierde un dado!\n"
            )

            if jugador_perdedor.get_cantidad_dados() == 0:
                self.eliminar_jugador(indice_jugador)
                print(f"{jugador_perdedor._nombre} se ha quedado sin dados ¡Jugador eliminado!\n")
                if len(self._jugadores) == 1:
                    print(f"El juego a finalizado ¡{self._jugadores[0]._nombre} es el ganador!\n")
                    return True

            self._turno_actual = indice_jugador
        else:
            jugador_perdedor = self._jugadores[self._turno_actual]
            print(f"¡{jugador_perdedor._nombre} dudo erroneamente y pierde un dado!\n")

            if jugador_perdedor.get_cantidad_dados() == 0:
                self.eliminar_jugador(self._turno_actual)
                print(f"{jugador_perdedor._nombre} se ha quedado sin dados ¡Jugador eliminado!\n")
                if len(self._jugadores) == 1:
                    print(f"El juego a finalizado ¡{self._jugadores[0]._nombre} es el ganador!\n")
                    return True

        return False

    def jugar_ronda(self):
        """Juega una ronda, termina al dudar o calzar."""
        if self._direccion_juego is None:
            raise ValueError("Debe definirse la direccion de Juego")

        for jugador in self._jugadores:
            jugador.agitar_cacho()

        self.hay_un_dado()

        primer_apuesta = True
        while True:
            apuesta = self.solicitar_apuesta_a_jugador()
            apuesta_tokenizada = apuesta.split(" ")
            while True:
                if apuesta_tokenizada[0] == str(TipoApuesta.SUBIR):
                    retorno = self.validar_apuesta_subir(primer_apuesta, apuesta_tokenizada)

                    if retorno == STR_BREAK:
                        break
                    elif retorno == STR_CONTINUE:
                        continue

                elif apuesta_tokenizada[0] == str(TipoApuesta.CALZAR):
                    if ValidadorApuesta.puede_calzar(
                        dados_en_juego=self.dados_en_juego(),
                        dados_maximos=self._total_dados_iniciales,
                        dados_del_jugador=self._jugadores[self._turno_actual].get_cantidad_dados(),
                    ):
                        break
                    continue
                elif apuesta_tokenizada[0] == str(TipoApuesta.PASAR):
                    break
                else:
                    break
                print("\nLa jugada ingresada no es valida, ingrese una nueva jugada.")
                apuesta = self.solicitar_apuesta_a_jugador()
                apuesta_tokenizada = apuesta.split(" ")

            primer_apuesta = False

            resultado = self.procesar_apuesta(apuesta)
            if not resultado:
                continue
            else:
                return resultado

    def procesar_apuesta(self, apuesta: str):
        """Procesa una apuesta y, si corresponde, finaliza la ronda.

        Para 'subir' y 'pasar' avanza el turno y la ronda continúa (retorna False).
        Para 'dudar' y 'calzar' resuelve el resultado y retorna un diccionario con:
        {'accion', 'termino': bool, 'resultado': bool}.
        """
        if apuesta.startswith(str(TipoApuesta.SUBIR)):
            self._apuesta_anterior = self._apuesta_actual
            self._apuesta_actual = apuesta
            if self._direccion_juego is None:
                raise ValueError("Debe definirse la direccion de Juego")
            self._turno_actual = self.calcular_turno(self._direccion_juego.value["bool"])
            return False

        elif apuesta == str(TipoApuesta.DUDAR):
            if self._direccion_juego is None:
                raise ValueError("Debe definirse la direccion de Juego")
            turno_anterior = self.calcular_turno(not self._direccion_juego.value["bool"])
            resultado = ArbitroRonda.procesar_apuesta(
                self._apuesta_anterior,
                self._apuesta_actual,
                apuesta,
                self._jugadores,
                self._ronda_especial,
                turno_anterior,
            )

            if resultado:
                self._jugadores[turno_anterior].perder_dado()
            else:
                self._jugadores[self._turno_actual].perder_dado()

            self.resetear_atributos()

            return {"accion": str(TipoApuesta.DUDAR), "termino": True, "resultado": resultado}

        elif apuesta == str(TipoApuesta.CALZAR):
            resultado = ArbitroRonda.procesar_apuesta(
                self._apuesta_anterior,
                self._apuesta_actual,
                apuesta,
                self._jugadores,
                self._ronda_especial,
                -1,
            )

            if resultado:
                self._jugadores[self._turno_actual].ganar_dado()
            else:
                self._jugadores[self._turno_actual].perder_dado()

            self.resetear_atributos()

            return {"accion": str(TipoApuesta.CALZAR), "termino": True, "resultado": resultado}

        elif apuesta == str(TipoApuesta.PASAR):
            self._apuesta_anterior = self._apuesta_actual
            self._apuesta_actual = apuesta
            if self._direccion_juego is None:
                raise ValueError("Debe definirse la direccion de Juego")
            self._turno_actual = self.calcular_turno(self._direccion_juego.value["bool"])
            return False

    def resetear_atributos(self):
        """Restablece flags y estado temporal al terminar una ronda."""
        self._apuesta_actual = ""
        self._apuesta_anterior = ""
        self._ronda_especial = False
        self._modo_especial = None
        self._ver_propios.clear()
        self._ver_ajenos.clear()

    def hay_un_dado(self):
        """Activa ronda especial (abierta/cerrada) si un jugador puede 'obligar'.

        Configura modo de visibilidad y marca uso de 'obligar' por jugador.
        """
        obligador = None
        for j in self._jugadores:
            if j.get_cantidad_dados() == 1 and not getattr(self, "_obligar_usado", {}).get(
                j._nombre, False
            ):
                obligador = j
                break

        if obligador:
            eleccion = input(
                f"{obligador._nombre}, elige si quieres jugar ronda especial o no:\n"
                "(5) obligar cerrada\n(6) obligar abierta\n(7) Jugar ronda normal\n\nR: "
            )
            while eleccion not in (
                TipoRondaEspecial.CERRADA.value,
                TipoRondaEspecial.ABIERTA.value,
                TipoRondaEspecial.NORMAL.value,
            ):
                limpiar_terminal()
                print("\nOpción incorrecta.\n")
                eleccion = input(
                    f"{obligador._nombre}, elige si quieres jugar ronda especial o no:\n"
                    "(5) obligar cerrada\n(6) obligar abierta\n(7) Jugar ronda normal\n\nR: "
                )

            if not hasattr(self, "_obligar_usado"):
                self._obligar_usado = {}
            self._obligar_usado[obligador._nombre] = True
            if eleccion == TipoRondaEspecial.NORMAL.value:
                return

            self._ronda_especial = True

            if eleccion == TipoRondaEspecial.CERRADA.value:
                self._modo_especial = TipoRondaEspecial.CERRADA
                self._ver_propios = {obligador._nombre}
                self._ver_ajenos = set()
            else:
                self._modo_especial = TipoRondaEspecial.ABIERTA
                self._ver_propios = set()
                self._ver_ajenos = {j._nombre for j in self._jugadores}

    def definir_primer_jugador(self):
        """Define el primer jugador que inicia la partida lanzando el dado."""
        limpiar_terminal()
        print("\nSe definirá el jugador que iniciará la primera ronda.\n")

        dado = Dado()
        numeros = []
        for i, jugador in enumerate(self._jugadores):
            input(f"{jugador._nombre}, presiona enter para lanzar un dado...\n")
            dado.generar_numero()
            numeros.append([i, dado.get_valor_numerico()])
            print(f"Obtuviste un {numeros[i][1]}\n")

        while True:
            repeticiones = 1
            indice_numero_mayor = -1
            numero_mayor = -1
            for num in numeros:
                if num[1] > numero_mayor:
                    indice_numero_mayor = num[0]
                    numero_mayor = num[1]
                    repeticiones = 1
                elif num[1] == numero_mayor:
                    repeticiones += 1

            if repeticiones == 1:
                break

            print("Ocurrio un empate.\n")
            numeros_aux = []
            i = 0
            for num in numeros:
                if num[1] == numero_mayor:
                    input(
                        f"{self._jugadores[num[0]]._nombre}, "
                        "presiona enter para volver a lanzar tu dado...\n"
                    )
                    dado.generar_numero()
                    numeros_aux.append([num[0], dado.get_valor_numerico()])
                    print(f"Obtuviste un {numeros_aux[i][1]}\n")
                    i += 1

            numeros = numeros_aux

        self._turno_actual = indice_numero_mayor
        print(f"{self._jugadores[indice_numero_mayor]._nombre} iniciará la primera ronda.\n")

    def definir_direccion_juego(self):
        """Permite al jugador actual elegir la dirección del juego."""
        direccion = ""
        while (
            direccion.lower() != DireccionJuego.Derecha.value["Numero_str"]
            and direccion.lower() != DireccionJuego.Izquierda.value["Numero_str"]
        ):
            mensaje = (
                f"Jugador {self._turno_actual + 1}:\n\n"
                f"Ingresa (1) si quieres que la dirección sea hacia la derecha (jugador "
                f"{(self._turno_actual + 1) % len(self._jugadores) + 1}).\n"
                f"Ingresa (-1) si quieres que la dirección sea hacia la izquierda (jugador "
                f"{5 if self._turno_actual == 0 else self._turno_actual}): \n\nR: "
            )
            direccion = input(mensaje)

        if direccion == DireccionJuego.Derecha.value["Numero_str"]:
            self._direccion_juego = DireccionJuego.Derecha
        else:
            self._direccion_juego = DireccionJuego.Izquierda

    def solicitar_apuesta_a_jugador(self) -> str:
        """Solicita al Jugador actual que realize su apuesta."""
        apuesta: str = self._jugadores[self._turno_actual].realizar_apuesta(
            self._apuesta_anterior, self._apuesta_actual
        )
        return apuesta

    def validar_apuesta_subir(self, primer_apuesta: bool, apuesta_tokenizada) -> str:
        """Valida 'subir' en el contexto actual y guía el bucle de entrada.

        Devuelve STR_BREAK para aceptar la jugada o STR_CONTINUE para solicitar otra.
        """
        if primer_apuesta:
            if apuesta_tokenizada[2] == str(NombreDado.AS).lower():
                if ValidadorApuesta.puede_partir_con_ases(
                    self._jugadores[self._turno_actual]._dados_en_posecion,
                    self._obligar_usado.get(self._jugadores[self._turno_actual]._nombre, False),
                ):
                    return STR_BREAK
                else:
                    return STR_CONTINUE
            else:
                return STR_BREAK
        elif self._apuesta_actual == str(TipoApuesta.PASAR):
            apuesta_anterior = self._apuesta_anterior.split(" ")
            if ValidadorApuesta.puede_subir(
                Apuesta(int(apuesta_anterior[1]), NombreDado.a_enum(apuesta_anterior[2])),
                Apuesta(int(apuesta_tokenizada[1]), NombreDado.a_enum(apuesta_tokenizada[2])),
                self._ronda_especial,
                self._jugadores[self._turno_actual].get_cantidad_dados() == 1,
            ):
                return STR_BREAK
            return STR_CONTINUE
        else:
            apuesta_actual = self._apuesta_actual.split(" ")
            if ValidadorApuesta.puede_subir(
                Apuesta(int(apuesta_actual[1]), NombreDado.a_enum(apuesta_actual[2])),
                Apuesta(int(apuesta_tokenizada[1]), NombreDado.a_enum(apuesta_tokenizada[2])),
                self._ronda_especial,
                self._jugadores[self._turno_actual].get_cantidad_dados() == 1,
            ):
                return STR_BREAK
            return STR_CONTINUE

    def eliminar_jugador(self, indice_jugador: int):
        """Elimina a un Jugador de los Jugadores en Juego."""
        if self._jugadores[indice_jugador].get_cantidad_dados() == 0:
            self._jugadores.pop(indice_jugador)

    def calcular_turno(self, direccion_derecha: bool):
        """Calcula el turno del jugador actual."""
        if direccion_derecha:
            return (self._turno_actual + 1) % len(self._jugadores)
        else:
            siguiente_turno = self._turno_actual - 1
            if siguiente_turno < 0:
                siguiente_turno = len(self._jugadores) - 1
            return siguiente_turno

    def ver_cacho_para(self, observador, objetivo):
        """Qué ve 'observador' del cacho de 'objetivo'."""
        base = objetivo.ver_cacho()
        modo = getattr(self, "_modo_especial", None)

        if modo is None:
            return base

        if modo == TipoRondaEspecial.CERRADA:
            if observador._nombre == objetivo._nombre:
                return base if observador._nombre in self._ver_propios else None
            return None

        if modo == TipoRondaEspecial.ABIERTA:
            if observador._nombre == objetivo._nombre:
                return None
            return base if observador._nombre in self._ver_ajenos else None

        raise ValueError("Modo especial desconocido")

    def dados_en_juego(self):
        """Devuelve el total de dados actualmente en juego."""
        total = 0
        for jugador in self._jugadores:
            total += jugador._dados_en_posecion

        return total
