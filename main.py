from src.game.gestor_partida import GestorPartida


def ingresar_cantidad_jugadores() -> int:
    while True:
        try:
            respuesta = int(
                input("Ingrese la cantidad de Jugadores (Si desea salir ingrese -1):\t")
            )
            while respuesta < 2:
                print("\nLa cantidad mínima de jugadores es 2\n")
                respuesta = int(
                    input("Ingrese la cantidad de Jugadores (Si desea salir ingrese -1):\t")
                )
        except ValueError:
            continue

        if respuesta == -1:
            exit(0)

        return respuesta


def main():
    gestor_partida = GestorPartida(cantidad_jugadores=ingresar_cantidad_jugadores())
    gestor_partida.juego()


if __name__ == "__main__":
    main()
