import random
import time

import numpy as np


def mostrar_sudoku(sudoku):
    for num_fila in range(9):
        fila = "| "
        # se divide el sudoku en 3 con "-" cada 3 filas
        if num_fila % 3 == 0:
            print("-" * 25)

        # se recorre ahora la columna en del num_fila actual
        for num_columna in range(9):
            if num_columna % 3 == 0 and num_columna != 0:
                fila += "| "
            fila += str(sudoku[num_fila, num_columna]) + " "

        fila += "|"
        print(fila)
    print("-" * 25)


def posicion_valida(sudoku, fila, columna, num) -> bool:
    # verifica  la fila en la que esta el numero
    for x in range(9):
        fila_actual = sudoku[fila, x]
        columna_actual = sudoku[x, columna]
        if num == fila_actual or num == columna_actual:
            return False

    # verifica la columna en la que esta el numero
    for y in range(9):
        columna_actual = sudoku[y, columna]
        if num == columna_actual:
            return False

    # verifica la casilla en la que esta ubicado el numero
    casilla_x = int((fila / 3)) * 3
    casilla_y = int((columna / 3)) * 3
    for x in range(3):
        casilla = sudoku[casilla_x:casilla_x + 3][x][casilla_y:casilla_y + 3]
        if num in casilla:
            return False

    return True


def rellenar_sudoku(sudoku, revision_total=False):
    # False, recorre desde la fila 1, necesario para crear el sudoku de forma aleatoria ya que la linea 1 esta ocupada
    # True, si se necesita que la funcion trabaje con todas las filas del sudoku
    if revision_total == False:
        x = 1
    else:
        x = 0
    # se recorre cada fila y columna del sudoku
    for fila in range(x, 9):
        for columna in range(9):
            if sudoku[fila, columna] == 0:
                for num in range(1, 10):
                    # si no hay ningun emento en esa, verifica si el numero elegido es valido
                    if posicion_valida(sudoku, fila, columna, num):
                        #  añade el numero valido a esa  celda
                        sudoku[fila, columna] = num
                        # se llama recursivamente con el nuevo sudoku
                        if rellenar_sudoku(sudoku, revision_total):
                            return True
                        else:
                            # si no se le puede poner ningun numero en esa celda reemplaza la anterior celda por 0
                            sudoku[fila, columna] = 0
                # esto activa el else de arriba si no deja poner ningun numero del 1 al 9
                return False
    # cuando el sudoku está lleno retorna True
    return True


def crear_sudoku():
    # se crea un boceto del sudoku con solo 0
    sudoku = np.zeros((9, 9), dtype=int)

    # se rellena la priemra fila del sudoku con numeros aleatorios para que de ahi nazca el resto de numero
    for x in range(9):
        while sudoku[0][x] == 0:
            num = random.randint(1, 9)
            if num not in sudoku[0]:
                sudoku[0][x] = num
    rellenar_sudoku(sudoku)
    return sudoku


# se eliminan aleatoriamente celdas para que queden las celdas necesarias para cada dificultad
def eliminar_casillas(sudoku, num):
    for _ in range(num):
        while True:
            fila = random.randint(0, 8)
            columna = random.randint(0, 8)
            if sudoku[fila][columna] != 0:
                sudoku[fila][columna] = 0
                break
    return sudoku


# realiza el mismo procedimiento de la funcion "rellenar_sudoku" pero este se detiene con solo dar un numero
def consejos(sudoku):
    for fila in range(9):
        for columna in range(9):
            if sudoku[fila, columna] == 0:
                for num in range(1, 10):
                    if posicion_valida(sudoku, fila, columna, num):
                        sudoku[fila, columna] = num
                        break
                break
        break
    print("- La pista fue el numero:", num, ", en la fila:", fila + 1, "y la columna:", columna + 1)
    mostrar_sudoku(sudoku)

    print("- Selecciona una opcion:\n")
    print("1. Desea pedir otra pista?\n")
    eleccion = input("Presione cualquier otra tecla para regresar: \n")

    # cada nueva pista se realiza en un sudoku "temporal" asi que no afecta al original y solo tiene un uso visual
    if eleccion == '1':
        consejos(sudoku)


def jugar(sudoku):
    while True:
        print("---MENU PRINCIPAL---")
        print("Tablero de Sudoku:")
        mostrar_sudoku(sudoku)

        print("- Selecciona una opcion:\n")
        print("1. Jugar:\n")
        print("2. Pista:\n")
        print("3. Regresar:\n")

        eleccion = input("Ingrese el número de opción: \n")

        if eleccion == '1':
            fila = int(input("Ingrese la fila (1-9): ")) - 1
            columna = int(input("Ingrese la columna (1-9): ")) - 1
            if (fila < 0 or fila > 8) or (columna < 0 or columna > 8):
                print("Fila o columna fuera de rango. Intente de nuevo.")
                time.sleep(2)
                continue

            if sudoku[fila][columna] != 0:
                print("Esta celda ya está llena. Elija otra.")
                time.sleep(2)
                continue

            num = int(input("Ingrese el número (1-9): "))

            sudoku[fila][columna] = num

        elif eleccion == '2':
            print("- Selecciona una opcion:\n")
            print("1. Pedir una pista:\n")
            print("2. Revisar si mi sudoku es valido:\n")
            eleccion = input("Presione cualquier otra tecla para regresar: \n")
            if eleccion == '1':
                print("- Escriba el estado actual de su sudoku (su estado actual está abajo) : \n")
                # convertimos el sudoku  en una  string
                print(sudoku.tolist(), "\n")

                # ahora en una lista
                estado_actual = eval(input())
                # ahora en una lista de numpy
                estado_actual = np.array(estado_actual)
                consejos(estado_actual)

            elif eleccion == '2':
                temp = np.copy(sudoku)
                if rellenar_sudoku(temp, True):
                    print("- El sudoku es completamente valido y se puede resolver")
                else:
                    print("- Su sudoku no es valido, no hay forma de resolverlo")
                time.sleep(3)

        elif eleccion == '3':
            break

        else:
            print("Ingrese una opcion valida")
            time.sleep(3)

        if 0 not in sudoku:
            print("¡Felicidades! Has resuelto el Sudoku.")
            time.sleep(3)
            break


def main():
    sudoku = crear_sudoku()
    while True:
        print("- Selecciona un nivel de dificultad:")
        print("1. Fácil (40 numeros de ventaja)")
        print("2. Medio (30 numeros de ventaja)")
        print("3. Difícil (15 numeros de ventaja)")
        print("4. Salir")

        eleccion = input("Ingrese el número de opción: \n")

        if eleccion == '1':
            eliminar_casillas(sudoku, 41)  # 40 números para el nivel fácil
        elif eleccion == '2':
            eliminar_casillas(sudoku, 51)  # 30 números para el nivel medio
        elif eleccion == '3':
            eliminar_casillas(sudoku, 66)  # 15 números para el nivel dificil
        elif eleccion == '4':
            break
        else:
            print("Opción no válida. Por favor, elige una opción válida.")

        jugar(sudoku)


main()
