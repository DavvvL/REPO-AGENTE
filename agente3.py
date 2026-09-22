import pygame 
import random

# Configuración de la pantalla
ANCHO, ALTO = 400, 400
TAMAÑO_CELDA = 40

FILAS = ANCHO // TAMAÑO_CELDA
COLUMNAS = ALTO // TAMAÑO_CELDA

# Colores
COLOR_FONDO = (30, 30, 30)
COLOR_SUCIO = (139, 69, 19) # Marrón
COLOR_LIMPIO = (255, 255, 255) # Blanco
COLOR_ASPIRADOR = (0, 255, 0) # Verde

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Aspirador Autónomo")

# Generar el entorno con suciedad aleatoria (1 = sucio, 0 = limpio)
entorno = [[random.choice([0, 1]) for _ in range(COLUMNAS)] for _ in range(FILAS)]

# Posición inicial del aspirador
aspirador_x, aspirador_y = random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)

# Función para mover el aspirador a una celda vecina aleatoria
def mover_aspirador(x, y):
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(movimientos) # Aleatorizar movimientos
    for dx, dy in movimientos:
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < FILAS and 0 <= nuevo_y < COLUMNAS:
            return nuevo_x, nuevo_y
            
    # El retorno por defecto va fuera del bucle para asegurar que evalúe todas las opciones
    return x, y 

# Bucle principal
ejecutando = True
while ejecutando:
    pygame.time.delay(500) # Pausa para visualizar mejor el movimiento

    # Verificar eventos (cierre de ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Regla 1: Si la casilla actual está sucia, la limpia
    if entorno[aspirador_x][aspirador_y] == 1:
        entorno[aspirador_x][aspirador_y] = 0 
    # Regla 2: Si la casilla está limpia, se mueve aleatoriamente a una casilla vecina
    else:
        aspirador_x, aspirador_y = mover_aspirador(aspirador_x, aspirador_y)

    # Dibujar el entorno
    pantalla.fill(COLOR_FONDO)
    for i in range(FILAS):
        for j in range(COLUMNAS):
            color = COLOR_SUCIO if entorno[i][j] == 1 else COLOR_LIMPIO
            pygame.draw.rect(pantalla, color, (j * TAMAÑO_CELDA, i * TAMAÑO_CELDA, TAMAÑO_CELDA, TAMAÑO_CELDA))

    # Dibujar el aspirador
    pygame.draw.rect(pantalla, COLOR_ASPIRADOR, (aspirador_y * TAMAÑO_CELDA, aspirador_x * TAMAÑO_CELDA, TAMAÑO_CELDA, TAMAÑO_CELDA))

    pygame.display.update()

# Cerrar Pygame
pygame.quit()