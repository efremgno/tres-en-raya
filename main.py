import random

def jugar(icono_jugador1, icono_jugador2):
    # jugador1 = x, jugador2 = o
    tablero = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]
    ganador = False
    turno = turnoInicial()
    mostrar_tablero(tablero)
    while(not ganador):
        tablero = jugarTurno(turno, tablero, icono_jugador1, icono_jugador2)
        mostrar_tablero(tablero)
        resultado = comprobar_resultado(tablero, icono_jugador1, icono_jugador2)
        if(resultado):
            ganador = True
        turno = cambiar_turno(turno)
    return resultado

def mostrarMenuInicio():
    saludo = "Hola, bienvenido al 3 en raya\nPulsa 1 para jugar\nPulsa 2 para ver las normas\nPulsa 3 para finalizar el programa\n"
    return saludo

def turnoInicial():
    return random.randint(0,1)

def jugarTurno(jugador, tablero, icono_jugador1, icono_jugador2):
    if(not jugador):
        jugadaValida = False
        while(not jugadaValida):
            print("Es tu turno")
            posicion = obtenerPosicionUsuario()
            nuevo_tablero = jugarUsuario(posicion, tablero, icono_jugador1)
            if nuevo_tablero != False:
                jugadaValida = True
    else:
        print("Turno de la máquina")
        nuevo_tablero = jugarMaquina(tablero, icono_jugador2)
    return nuevo_tablero

# icono = o
# devuelve el nuevo tablero
def jugarMaquina(tablero, icono):
    jugado = False
    while(not jugado) :
        posicion = [random.randint(0,2), random.randint(0,2)]
        if tablero[posicion[0]][posicion[1]] == "-":
            tablero[posicion[0]][posicion[1]] = icono
            jugado = True
    return tablero

# Devuelve true si se ha jugado correctamente y False si no está vacía la casilla marcada por el usuario
def jugarUsuario(posicion, tablero, icono):
    if tablero[posicion[0]][posicion[1]] == "-":
        tablero[posicion[0]][posicion[1]] = icono
        return tablero
    else:
        return False

def normas():
    return "Normas:\n    - El primer número representa la fila\n    - El segundo número representa la columna\n    - El rango de númeores está entre 1 y 3\n"

def obtenerPosicionUsuario():
    try:
        posicion = input("Fila,Columna\n")
        posicion = posicion.split(',')
        if (len(posicion) != 2):
            raise ValueError("Casilla inválida.")
        fila = int(posicion[0]-1)
        columna = int(posicion[1]-1)   

        if fila < 0 or fila >= 3 or columna < 0 or columna >= 3:
            raise ValueError("Las posiciones deben estar entre 1 y 3.")
  
        return [fila, columna]
    except Exception as e:
        print("Por favor, escoja una casilla válida\n")
        return obtenerPosicionUsuario()
    
def cambiar_turno(turno):
    if turno == 0:
        return 1
    else:
        return 0
    
def comprobar_ganador(tablero, icono):
    # Comprobar filas
    for fila in tablero:
        if all(celda == icono for celda in fila):
            return True

    # Comprobar columnas
    for columna in range(len(tablero[0])):
        if all(tablero[fila][columna] == icono for fila in range(len(tablero))):
            return True

    # Comprobar diagonal principal
    if all(tablero[i][i] == icono for i in range(len(tablero))):
        return True

    # Comprobar diagonal secundaria
    if all(tablero[i][len(tablero) - 1 - i] == icono for i in range(len(tablero))):
        return True

    return False

# devuelve True en caso de empate
def comprobar_empate(tablero):
    for fila in tablero:
        for columna in fila:
            if(columna == '-'):
                return False
    return True

def comprobar_resultado(tablero, icono_jugador1, icono_jugador2):
    if (comprobar_ganador(tablero, icono_jugador1)):
        resultado = icono_jugador1
    elif (comprobar_ganador(tablero, icono_jugador2)):
        resultado = icono_jugador2
    elif comprobar_empate(tablero):
        resultado = "-"
    else:
        resultado = False
    return resultado
        
def mostrar_resultado(icono_jugador1, icono_jugador2):
    if (resultado == icono_jugador1):
        print("¡Enhorabuena! ¡Has ganado!")
    elif(resultado == icono_jugador2):
        print("¡Has perdido! Jajaj")
    elif (resultado == "-"):
        print("¡Empate! No puedes conmigo")

def mostrar_tablero(tablero):
    for fila in tablero:
        print(" | ".join(fila))
        
icono_jugador1 = 'x'
icono_jugador2 = 'o'
finalizar = False
while(not finalizar):
    eleccion_usuario = int(input(mostrarMenuInicio()))
    if (eleccion_usuario == 1):
        resultado = jugar(icono_jugador1, icono_jugador2)
        mostrar_resultado(icono_jugador1, icono_jugador2)
    elif eleccion_usuario == 2:
        print(normas())
    elif eleccion_usuario == 3:
        finalizar = True
    else:
        print("Por favor, escoge una opción válida.\n")