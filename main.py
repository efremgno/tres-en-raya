import random

def jugar(icono_jugador1, icono_jugador2):
    dificultad = seleccionarDificultad()
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
        tablero = jugarTurno(turno, tablero, icono_jugador1, icono_jugador2, dificultad)
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

def jugarTurno(jugador, tablero, icono_jugador1, icono_jugador2, dificultad):
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
        nuevo_tablero = dificultad(tablero, icono_jugador2, icono_jugador1)
    return nuevo_tablero

# icono = o
# devuelve el nuevo tablero
def jugarMaquinaFacil(tablero, icono, icono_usuario):
    jugado = False
    while(not jugado) :
        posicion = [random.randint(0,2), random.randint(0,2)]
        if tablero[posicion[0]][posicion[1]] == "-":
            tablero[posicion[0]][posicion[1]] = icono
            jugado = True
    return tablero

def jugarMaquinaNormal(tablero, icono_maquina, icono_usuario):
    casilla = comprobarPosibleVictoria(tablero,icono_maquina)
    if(not casilla):
        casilla = comprobarPosibleVictoria(tablero,icono_usuario)
        if(not casilla):
            return jugarMaquinaFacil(tablero, icono_maquina, icono_usuario)
    print(f"Casilla: {casilla}")
    tablero[casilla[0]][casilla[1]] = icono_maquina
    return tablero

def jugarMaquinaDificil(tablero, icono_maquina, icono_usuario):
    n_icono_maquina = 0
    n_icono_usuario = 0
    esquinas = [(0,0), (0,2), (2,0), (2,2)]
    laterales = [(0,1), (1,0), (1,2), (2,1)]
    centro = (1,1)
    movimientos_usuario = []
    movimientos_maquina = []
    for indiceFila, fila in enumerate(tablero):
        for indiceColumna, celda in enumerate(fila):
            if celda == icono_maquina:
                n_icono_maquina +=1
                movimientos_maquina.append((indiceFila, indiceColumna))
            if celda == icono_usuario:
                n_icono_usuario +=1
                movimientos_usuario.append((indiceFila, indiceColumna))
    # juega la máquina primero
    if n_icono_maquina == n_icono_usuario:
        if n_icono_maquina == 0: # Primer movimiento
            movimiento = random.randint(0,len(esquinas)-1)
            movimiento = esquinas[movimiento]
        elif n_icono_maquina == 1: #segundo movimiento
            movimiento_usuario = movimientos_usuario[0]
            movimiento_maquina = movimientos_maquina[0]
            if movimiento_usuario == centro:
                #muevo a la esquina contraria
                movimiento = esquina_contraria(movimiento_maquina)
            elif movimiento_usuario in esquinas:
                if movimiento_usuario == esquina_contraria(movimiento_maquina):
                    movimiento = centro
                else:
                    movimiento = esquina_contraria(movimiento_maquina)
            else:
                movimiento = centro
        elif n_icono_maquina == 2: # tercer movimiento
            if comprobarPosibleVictoria(tablero, icono_maquina) != None:
                movimiento = comprobarPosibleVictoria(tablero, icono_maquina)
            elif comprobarPosibleVictoria(tablero, icono_usuario) != None:
                movimiento = comprobarPosibleVictoria(tablero, icono_usuario)
            else:
                if any(movimiento in laterales for movimiento in movimientos_usuario):
                    # Detectar el movimiento lateral del usuario
                    movimiento_usuario_lateral = next(
                        movimiento for movimiento in movimientos_usuario if movimiento in laterales
                    )
                    # Calcular la posición contraria y paralela
                    x, y = movimiento_usuario_lateral
                    if x == 0 or x == 2:  # Lateral en una columna
                        movimiento = (2 - x, y)
                    elif y == 0 or y == 2:  # Lateral en una fila
                        movimiento = (x, 2 - y)
                    # Elegir la esquina adyacente que esté libre
                    esquinas_libres = [
                        esquina for esquina in esquinas
                        if tablero[esquina[0]][esquina[1]] == '' and esquina not in [
                            (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)
                        ]
                    ]
                    movimiento = esquinas_libres[0] #siempre va a haber una esquina libre
                else:
                    movimiento = jugarMaquinaFacil(tablero, icono_maquina, icono_usuario)
        else:
            movimiento = jugarMaquinaFacil(tablero, icono_maquina, icono_usuario)
    # juega el usuario primero
    else:
        if n_icono_maquina == 0: # Primer movimiento
            if centro in movimientos_usuario:
                movimiento = random.randint(0,len(esquinas)-1)
                movimiento = esquinas[movimiento]
            else:
                movimiento = centro
        elif n_icono_maquina == 1: #segundo movimiento
            if hay_esquinas_contrarias(movimientos_usuario):
                movimiento = random.randint(0,len(laterales)-1)
                movimiento = laterales[movimiento]
            else:
                movimiento = jugarMaquinaNormal(tablero, icono_maquina, icono_usuario)
        else:
            movimiento = jugarMaquinaNormal(tablero, icono_maquina, icono_usuario)
    tablero[movimiento[0]][movimiento[1]] = icono_maquina
    return tablero

def esquina_contraria(esquina):
    return (2 - esquina[0], 2 - esquina[1])

def hay_esquinas_contrarias(movimientos):
    # Esquinas contrarias
    esquinas_opuestas = [((0, 0), (2, 2)), ((0, 2), (2, 0))]
    
    # Verificar si algún par de esquinas opuestas está en los movimientos
    for esquina1, esquina2 in esquinas_opuestas:
        if esquina1 in movimientos and esquina2 in movimientos:
            return True
    
    return False

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
        fila = int(posicion[0])-1
        columna = int(posicion[1])-1   

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

def comprobarPosibleVictoria(tablero, icono):
    # Comprobar filas
    for i, fila in enumerate(tablero):
        contador = 0
        casillaLibre = None
        for j, celda in enumerate(fila):
            if tablero[i][j] == icono:
                contador += 1
            elif tablero[i][j] == "-":
                casillaLibre = (i, j)
        if contador == 2 and casillaLibre is not None:
            return casillaLibre

    # Comprobar columnas
    for columna in range(len(tablero[0])):
        contador = 0
        casillaLibre = None
        for fila in range(len(tablero)):
            if tablero[fila][columna] == icono:
                contador += 1
            elif tablero[fila][columna] == "-":
                casillaLibre = (fila, columna)
        if contador == 2 and casillaLibre is not None:
            return casillaLibre

    # Comprobar diagonal principal
    contador = 0
    casillaLibre = None
    for i in range(len(tablero)):
        if tablero[i][i] == icono:
            contador += 1
        elif tablero[i][i] == "-":
            casillaLibre = (i, i)
    if contador == 2 and casillaLibre is not None:
        return casillaLibre

    # Comprobar diagonal secundaria
    contador = 0
    casillaLibre = None
    for i in range(len(tablero)):
        if tablero[i][len(tablero) - 1 - i] == icono:
            contador += 1
        elif tablero[i][len(tablero) - 1 - i] == "-":
            casillaLibre = (i, len(tablero) - 1 - i)
    if contador == 2 and casillaLibre is not None:
        return casillaLibre

    return False

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

def seleccionarDificultad():
    dificultadSeleccionada = False
    while(not dificultadSeleccionada):
        try:
            dificultad = int(input("Selecciona la dificultad:\n    1 - Fácil\n    2 - Normal\n    3 - Díficil\n"))
            if (dificultad == 1):
                dificultadMaquina = jugarMaquinaFacil
            elif (dificultad == 2):
                dificultadMaquina = jugarMaquinaNormal
            elif (dificultad == 3):
                dificultadMaquina = jugarMaquinaDificil
            else:
                raise ValueError("Opción inválida")
            dificultadSeleccionada = True
        except Exception:
            print("Por favor, escoja una dificultad válida\n")
    return dificultadMaquina
        
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