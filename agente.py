import pygame
import random

# Configuración de la pantalla
ANCHO, ALTO = 500, 500
COLOR_FONDO = (30, 30, 30)

# Configuración del agente
TAMAÑO_AGENTE = 20
COLOR_AGENTE = (0, 255, 0)
VELOCIDAD_AGENTE = 2

# Configuración de los obstáculos
COLOR_OBSTACULO = (255, 0, 0)
NUMERO_OBSTACULOS = 5
TAMAÑO_OBSTACULO = 40

# Inicialización de Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Agente Reactivo")

# Posición inicial del agente
agente_x = random.randint(0, ANCHO - TAMAÑO_AGENTE)
agente_y = random.randint(0, ALTO - TAMAÑO_AGENTE)
direccion = random.choice(["ARRIBA","ABAJO","IZQUIERDA","DERECHA"])

# Generar obstáculos en posiciones aleatorias
obstaculos = []
for _ in range(NUMERO_OBSTACULOS):
    obs_x = random.randint(0, ANCHO - TAMAÑO_OBSTACULO)
    obs_y = random.randint(0, ALTO - TAMAÑO_OBSTACULO)
    obstaculos.append(pygame.Rect(obs_x, obs_y, TAMAÑO_OBSTACULO, TAMAÑO_OBSTACULO))

# Función para mover el agente
def mover_agente(x, y, direccion):
    if direccion == "ARRIBA":
        y -= VELOCIDAD_AGENTE

    elif direccion == "ABAJO":
        y += VELOCIDAD_AGENTE

    elif direccion == "IZQUIERDA":
        x -= VELOCIDAD_AGENTE

    elif direccion == "DERECHA":
        x += VELOCIDAD_AGENTE

    return x, y

# Función para verificar colisión
def verificar_colision(x, y):
    rectangulo_agente = pygame.Rect(x, y, TAMAÑO_AGENTE, TAMAÑO_AGENTE)

    if x < 0 or x > ANCHO - TAMAÑO_AGENTE or y < 0 or y > ALTO - TAMAÑO_AGENTE:
        return True # Colisión con los bordes

    for obs in obstaculos:
        if rectangulo_agente.colliderect(obs):
            return True # Colisión con un obstáculo
    return False

# Bucle principal
ejecutando = True
while ejecutando:
    pygame.time.delay(20)

# Verificar eventos (cierre de ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT :
            ejecutando = False

# Mover el agente
    nuevo_x, nuevo_y = mover_agente(agente_x, agente_y, direccion)

# Si hay colisión, cambiar dirección aleatoria
    if verificar_colision(nuevo_x, nuevo_y):
        direccion = random.choice(["ARRIBA","ABAJO","IZQUIERDA","DERECHA"])
    else:
        agente_x, agente_y = nuevo_x, nuevo_y

# Dibujar el entorno
    pantalla.fill(COLOR_FONDO)

    pygame.draw.rect(pantalla, COLOR_AGENTE, (agente_x, agente_y, TAMAÑO_AGENTE, TAMAÑO_AGENTE))

    for obs in obstaculos:
        pygame.draw.rect(pantalla, COLOR_OBSTACULO, obs)
    pygame.display.update()

# Cerrar Pygame
pygame.quit()