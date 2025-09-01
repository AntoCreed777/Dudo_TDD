"""Módulo que contiene la clase GestorPartida para gestionar la lógica de la partida de Dudo."""

from enum import Enum

from src.game.dado import Dado, NombreDado
from src.game.jugador import Jugador, TipoApuesta
from src.game.validador_apuesta import ValidadorApuesta


class DireccionJuego(Enum):
    Derecha = {"Numero_str": "1", "bool": True}
    Izquierda = {"Numero_str": "-1", "bool": False}

    def __str__(self):
        direcciones = {DireccionJuego.Derecha: "Derecha", DireccionJuego.Izquierda: "Izquierda"}
        return direcciones[self]


class TipoRondaEspecial(Enum):
    Abierta = "Abierta"
    Cerrada = "Cerrada"

    def __str__(self):
        return self.value


class GestorPartida:
    """Clase que gestiona la partida, jugadores y turnos."""

    _jugadores: list[Jugador]
    _direccion_juego: DireccionJuego | None
    _turno_actual: int
    _apuesta_anterior: str
    _apuesta_actual: str
    _cantidad_pintas: dict[str, int]
    _ronda_especial: bool
    _obligar_usado: dict[str, bool]
    _pinta_fijada_especial: str | None
    _modo_especial: TipoRondaEspecial | None
    _ver_propios: set
    _ver_ajenos: set
    _obligador_nombre: str | None

    def __init__(self, cantidad_jugadores):
        """Inicializa el gestor de partida con la cantidad de jugadores indicada."""
        self._jugadores = []
        self._direccion_juego = None
        self._turno_actual = -1
        self._apuesta_anterior = ""
        self._apuesta_actual = ""
        self._cantidad_pintas = {
            str(NombreDado.AS).lower(): 0,
            str(NombreDado.TONTO).lower(): 0,
            str(NombreDado.TREN).lower(): 0,
            str(NombreDado.CUADRA).lower(): 0,
            str(NombreDado.QUINA).lower(): 0,
            str(NombreDado.SEXTO).lower(): 0,
        }
        self._ronda_especial = False
        self._obligar_usado = {j._nombre: False for j in self._jugadores}
        self._pinta_fijada_especial = None
        self._modo_especial = None
        self._ver_propios = set()
        self._ver_ajenos = set()
        self._obligador_nombre = None

        for _ in range(cantidad_jugadores):
            nombre = input(f"\nIngrese el nombre del jugador {_}: ")
            self._jugadores.append(Jugador(nombre))

    def definir_primer_jugador(self):
        """Define el primer jugador que inicia la partida lanzando el dado."""
        dado = Dado()
        numeros = []
        for i in range(len(self._jugadores)):
            dado.generar_numero()
            numeros.append([i, dado.get_valor_numerico()])

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

            numeros_aux = []
            for num in numeros:
                if num[1] == numero_mayor:
                    dado.generar_numero()
                    numeros_aux.append([num[0], dado.get_valor_numerico()])

            numeros = numeros_aux

        self._turno_actual = indice_numero_mayor

    def definir_direccion_juego(self):
        """Permite al jugador actual elegir la dirección del juego."""
        direccion = ""
        while (
            direccion.lower() != DireccionJuego.Derecha.value["Numero_str"]
            and direccion.lower() != DireccionJuego.Izquierda.value["Numero_str"]
        ):
            mensaje = (
                f"Jugador {self._turno_actual + 1}:\n"
                f"Ingresa (1) si quieres que la dirección sea hacia la derecha del jugador "
                f"{(self._turno_actual + 1) % len(self._jugadores) + 1}.\n"
                f"Ingresa (-1) si quieres que la dirección sea hacia la izquierda del jugador "
                f"{5 if self._turno_actual == 0 else self._turno_actual}"
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

    def eliminar_jugador(self, indice_jugador: int):
        """Elimina a un Jugador de los Jugadores en Juego."""
        if self._jugadores[indice_jugador].get_cantidad_dados() == 0:
            self._jugadores.pop(indice_jugador)

    def procesar_apuesta(self, apuesta):
        """Procesa una apuesta durante la ronda."""
        apuesta_tokenizada = apuesta.split(" ")
        if apuesta_tokenizada[0] == str(TipoApuesta.SUBIR):
            if self._ronda_especial and self._pinta_fijada_especial:
                pinta_nueva = apuesta_tokenizada[2]
                if pinta_nueva != self._pinta_fijada_especial:
                    jugador = self._jugadores[self._turno_actual]
                    cant_nueva = int(apuesta_tokenizada[1])

                    cant_anterior = None
                    if self._apuesta_actual and self._apuesta_actual.startswith(
                        str(TipoApuesta.SUBIR)
                    ):
                        prev = self._apuesta_actual.split(" ")
                        cant_anterior = int(prev[1])

                    puede_cambiar = (
                        jugador.get_cantidad_dados() == 1
                        and self._obligador_nombre is not None
                        and jugador._nombre != self._obligador_nombre
                        and cant_anterior is not None
                        and cant_nueva > cant_anterior
                    )
                    if not puede_cambiar:
                        raise ValueError("Pinta fija en ronda especial")
                    self._pinta_fijada_especial = pinta_nueva

            self._apuesta_anterior = self._apuesta_actual
            self._apuesta_actual = apuesta
            return False

        if apuesta == str(TipoApuesta.DUDAR):
            for jugador in self._jugadores:
                dados_jugador = jugador.ver_cacho()

                if dados_jugador is None:
                    raise ValueError("Error en dados de jugador")

                for dado in dados_jugador:
                    self._cantidad_pintas[dado.lower()] += 1

            cantidad_pinta_apuesta = 0
            apuesta_tokenizada = self._apuesta_actual.split(" ")
            self._apuesta_anterior = self._apuesta_actual
            self._apuesta_actual = apuesta

            if apuesta_tokenizada[0] == str(TipoApuesta.SUBIR):
                cantidad_pinta_apuesta += self._cantidad_pintas[str(NombreDado.AS).lower()]
                if apuesta_tokenizada[2] != str(NombreDado.AS).lower():
                    cantidad_pinta_apuesta += self._cantidad_pintas[apuesta_tokenizada[2]]
                if cantidad_pinta_apuesta >= int(apuesta_tokenizada[1]):
                    self._jugadores[self._turno_actual].perder_dado()
                    self._ronda_especial = False
                    self._pinta_fijada_especial = None
                    self._obligador_nombre = None
                    self._modo_especial = None
                    self._ver_propios.clear()
                    self._ver_ajenos.clear()
                    return False
                else:
                    if self._direccion_juego is None:
                        raise ValueError("Error en la direccion de Juego")

                    self._jugadores[
                        self.calcular_turno(not self._direccion_juego.value["bool"])
                    ].perder_dado()
                    self._ronda_especial = False
                    self._pinta_fijada_especial = None
                    self._obligador_nombre = None
                    self._modo_especial = None
                    self._ver_propios.clear()
                    self._ver_ajenos.clear()
                    return True
        if apuesta == str(TipoApuesta.CALZAR):
            if not self._apuesta_actual.startswith(str(TipoApuesta.SUBIR)):
                raise ValueError("No hay apuesta válida para calzar")

            validador = ValidadorApuesta()
            dados_maximos = 5 * len(self._jugadores)
            dados_en_juego = sum(j.get_cantidad_dados() for j in self._jugadores)
            dados_del_jugador = self._jugadores[self._turno_actual].get_cantidad_dados()
            if not validador.puede_calzar(dados_en_juego, dados_maximos, dados_del_jugador):
                raise ValueError("No se cumplen las condiciones para calzar")

        conteo = {
            str(NombreDado.AS).lower(): 0,
            str(NombreDado.TONTO).lower(): 0,
            str(NombreDado.TREN).lower(): 0,
            str(NombreDado.CUADRA).lower(): 0,
            str(NombreDado.QUINA).lower(): 0,
            str(NombreDado.SEXTO).lower(): 0,
        }
        for jugador in self._jugadores:
            dados_jugador = jugador.ver_cacho()
            if dados_jugador is None:
                raise ValueError("Error en dados de jugador")
            for nombre in dados_jugador:
                conteo[nombre.lower()] += 1
        prev = self._apuesta_actual.split(" ")

        if prev[0] != str(TipoApuesta.SUBIR):
            raise ValueError("No hay apuesta válida para calzar")
        cantidad_objetivo = int(prev[1])
        pinta_objetivo = prev[2]

        if getattr(self, "_ronda_especial", False):
            cantidad = conteo[pinta_objetivo]
        else:
            cantidad = conteo[str(NombreDado.AS).lower()]
            if pinta_objetivo != str(NombreDado.AS).lower():
                cantidad += conteo[pinta_objetivo]

        self._apuesta_anterior = self._apuesta_actual
        self._apuesta_actual = apuesta

        if cantidad == cantidad_objetivo:
            self._jugadores[self._turno_actual]._dados_en_posecion += 1
            self._ronda_especial = False
            self._pinta_fijada_especial = None
            self._obligador_nombre = None
            self._modo_especial = None
            self._ver_propios.clear()
            self._ver_ajenos.clear()
            return True
        self._jugadores[self._turno_actual].perder_dado()
        self._ronda_especial = False
        self._pinta_fijada_especial = None
        self._obligador_nombre = None
        self._modo_especial = None
        self._ver_propios.clear()
        self._ver_ajenos.clear()
        return False

    def calcular_turno(self, direccion_derecha: bool):
        """Calcula el turno del jugador actual."""
        if direccion_derecha:
            return (self._turno_actual + 1) % len(self._jugadores)
        else:
            siguiente_turno = self._turno_actual - 1
            if siguiente_turno < 0:
                siguiente_turno = len(self._jugadores) - 1
            return siguiente_turno

    def jugar_ronda(self):
        """Juega una ronda, termina al dudar o calzar"""
        if self._direccion_juego is None:
            raise ValueError("Debe definirse la direccion de Juego")

        hay_uno = any(j.get_cantidad_dados() == 1 for j in self._jugadores)
        if hay_uno:
            obligador = None
            for j in self._jugadores:
                if j.get_cantidad_dados() == 1 and not getattr(self, "_obligar_usado", {}).get(
                    j._nombre, False
                ):
                    obligador = j
                    break

            if obligador:
                eleccion = input(
                    f"{obligador._nombre}, (5) obligar cerrada: / (6) obligar abierta: "
                )
                if eleccion not in ("5", "6"):
                    raise ValueError("Opción de obligar inválida")
                self._pinta_fijada_especial = (
                    input("Indica la pinta fija (as/tonto/tren/cuadra/quina/sexto): ")
                    .strip()
                    .lower()
                )
                self._ronda_especial = True
                if not hasattr(self, "_obligar_usado"):
                    self._obligar_usado = {}
                self._obligar_usado[obligador._nombre] = True
                self._obligador_nombre = obligador._nombre

                if eleccion == "5":
                    self._modo_especial = TipoRondaEspecial.Cerrada
                    self._ver_propios = {obligador._nombre}
                    self._ver_ajenos = set()
                else:
                    self._modo_especial = TipoRondaEspecial.Abierta
                    self._ver_propios = set()
                    self._ver_ajenos = {j._nombre for j in self._jugadores}

        while True:
            apuesta = self.solicitar_apuesta_a_jugador()

            if apuesta.startswith("subir"):
                self.procesar_apuesta(apuesta)
                self._turno_actual = self.calcular_turno(self._direccion_juego.value["bool"])
                continue

            if apuesta == "dudar":
                resultado = self.procesar_apuesta(apuesta)
                return {"accion": "dudar", "termino": True, "resultado": resultado}

            if apuesta == "calzar":
                resultado = self.procesar_apuesta(apuesta)
                return {"accion": "calzar", "termino": True, "resultado": resultado}

            if apuesta == "pasar":
                self._turno_actual = self.calcular_turno(self._direccion_juego.value["bool"])
                continue

            raise ValueError("Apuesta no reconocida durante la ronda")

    def ver_cacho_para(self, observador, objetivo):
        """Qué ve 'observador' del cacho de 'objetivo'."""
        base = objetivo.ver_cacho()
        modo = getattr(self, "_modo_especial", None)

        if modo is None:
            return base

        if modo == TipoRondaEspecial.Cerrada:
            if observador._nombre == objetivo._nombre:
                return base if observador._nombre in self._ver_propios else None
            return None

        if modo == TipoRondaEspecial.Abierta:
            if observador._nombre == objetivo._nombre:
                return None
            return base if observador._nombre in self._ver_ajenos else None

        raise ValueError("Modo especial desconocido")
