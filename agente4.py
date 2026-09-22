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
COLOR_TEXTO = (255, 255, 255)

# Configuración de la simulación
NUM_ASPIRADORES = 3

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sistema Multi-Agente de Limpieza")

try:
    pygame.font.init()
    fuente = pygame.font.Font(None, 36)
except:
    pass

# Generar el entorno y contar la suciedad inicial
entorno = [[random.choice([0, 1]) for _ in range(COLUMNAS)] for _ in range(FILAS)]
celdas_sucias_restantes = sum(sum(fila) for fila in entorno)

# Inicializar múltiples aspiradores evitando que aparezcan en la misma celda
aspiradores = []
while len(aspiradores) < NUM_ASPIRADORES:
    nuevo_x, nuevo_y = random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1)
    if [nuevo_x, nuevo_y] not in aspiradores:
        aspiradores.append([nuevo_x, nuevo_y])

# Variables para Estadísticas
movimientos_totales = 0
tiempo_inicio = pygame.time.get_ticks()
tiempo_final = 0
simulacion_terminada = False

# Función para mover un aspirador usando Visión Local
def mover_aspirador_vision_local(x, y, lista_aspiradores):
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(movimientos)
    
    opciones_sucias = []
    opciones_limpias = []
    
    # Evaluar las 4 casillas adyacentes
    for dx, dy in movimientos:
        nuevo_x, nuevo_y = x + dx, y + dy
        
        # Verificar que esté dentro de los límites
        if 0 <= nuevo_x < FILAS and 0 <= nuevo_y < COLUMNAS:
            # Verificar colisión: que la casilla no esté ocupada por otro aspirador
            if [nuevo_x, nuevo_y] not in lista_aspiradores:
                if entorno[nuevo_x][nuevo_y] == 1:
                    opciones_sucias.append((nuevo_x, nuevo_y))
                else:
                    opciones_limpias.append((nuevo_x, nuevo_y))
                    
    # Prioridad 1: Moverse a una casilla sucia
    if opciones_sucias:
        return random.choice(opciones_sucias)
    # Prioridad 2: Si todo alrededor está limpio, moverse a una casilla limpia al azar
    elif opciones_limpias:
        return random.choice(opciones_limpias)
        
    # Si está acorralado (por bordes y otros aspiradores), se queda en su lugar
    return x, y

# Bucle principal
ejecutando = True
while ejecutando:
    pygame.time.delay(200) # Velocidad acelerada a 200ms para compensar múltiples agentes

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Lógica de limpieza y movimiento (solo si queda suciedad)
    if celdas_sucias_restantes > 0:
        for i in range(NUM_ASPIRADORES):
            x, y = aspiradores[i]
            
            # Regla 1: Si está sucio, limpia
            if entorno[x][y] == 1:
                entorno[x][y] = 0
                celdas_sucias_restantes -= 1
            # Regla 2: Si está limpio, busca a dónde moverse
            else:
                nuevo_x, nuevo_y = mover_aspirador_vision_local(x, y, aspiradores)
                if nuevo_x != x or nuevo_y != y:
                    aspiradores[i] = [nuevo_x, nuevo_y]
                    movimientos_totales += 1
                    
        # Registrar el tiempo exacto en que se limpió la última celda
        if celdas_sucias_restantes == 0 and not simulacion_terminada:
            tiempo_final = (pygame.time.get_ticks() - tiempo_inicio) / 1000.0
            simulacion_terminada = True

    # --- DIBUJO ---
    pantalla.fill(COLOR_FONDO)
    
    # Dibujar celdas
    for i in range(FILAS):
        for j in range(COLUMNAS):
            color = COLOR_SUCIO if entorno[i][j] == 1 else COLOR_LIMPIO
            pygame.draw.rect(pantalla, color, (j * TAMAÑO_CELDA, i * TAMAÑO_CELDA, TAMAÑO_CELDA, TAMAÑO_CELDA))

    # Dibujar todos los aspiradores
    for asp in aspiradores:
        pygame.draw.rect(pantalla, COLOR_ASPIRADOR, (asp[1] * TAMAÑO_CELDA, asp[0] * TAMAÑO_CELDA, TAMAÑO_CELDA, TAMAÑO_CELDA))

    # Dibujar estadísticas finales si ya terminó
    if simulacion_terminada:
        # Fondo semi-transparente para el texto
        panel_superpuesto = pygame.Surface((ANCHO, ALTO))
        panel_superpuesto.set_alpha(180) # Transparencia (0-255)
        panel_superpuesto.fill((0, 0, 0))
        pantalla.blit(panel_superpuesto, (0, 0))
        
        texto_fin = fuente.render("¡Limpieza Completada!", True, COLOR_ASPIRADOR)
        texto_tiempo = fuente.render(f"Tiempo: {tiempo_final:.1f} s", True, COLOR_TEXTO)
        texto_movs = fuente.render(f"Mov. Totales: {movimientos_totales}", True, COLOR_TEXTO)
        
        pantalla.blit(texto_fin, (ANCHO//2 - texto_fin.get_width()//2, 130))
        pantalla.blit(texto_tiempo, (ANCHO//2 - texto_tiempo.get_width()//2, 180))
        pantalla.blit(texto_movs, (ANCHO//2 - texto_movs.get_width()//2, 220))

    pygame.display.update()

pygame.quit()