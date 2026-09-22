import pygame
import random
import sys

# Configuración de la pantalla
ANCHO, ALTO = 500, 500
COLOR_FONDO = (30, 30, 30)

# Configuración de los agentes
TAMAÑO_AGENTE = 20
COLOR_AGENTE1 = (0, 255, 0)      
COLOR_AGENTE2_AUTO = (0, 0, 150)  
COLOR_AGENTE2_MANUAL = (0, 200, 255) 
VELOCIDAD_AGENTE = 2

# Configuración de los obstáculos
COLOR_OBSTACULO = (255, 0, 0)
NUMERO_OBSTACULOS = 15 # Aumentado a 15 obstáculos
TAMAÑO_OBSTACULO = 40

# Configuración del Botón
COLOR_BOTON_AUTO = (100, 100, 100)
COLOR_BOTON_MANUAL = (0, 100, 200)
COLOR_TEXTO_BOTON = (255, 255, 255)
RECT_BOTON = pygame.Rect(10, 10, 180, 30)

# DICCIONARIO DE OPUESTOS
OPUESTOS = {
    "ARRIBA": "ABAJO",
    "ABAJO": "ARRIBA",
    "IZQUIERDA": "DERECHA",
    "DERECHA": "IZQUIERDA"
}

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Agente Reactivo - Memoria Corto Plazo (Sin solapamiento)")

try:
    pygame.font.init()
    fuente = pygame.font.Font(None, 24)
    usar_texto = True
except (RuntimeError, Exception):
    usar_texto = False

# Posiciones iniciales
agente1_x = random.randint(0, ANCHO - TAMAÑO_AGENTE)
agente1_y = random.randint(0, ALTO - TAMAÑO_AGENTE)
direccion1 = random.choice(list(OPUESTOS.keys()))
rectangulo_agente1 = pygame.Rect(agente1_x, agente1_y, TAMAÑO_AGENTE, TAMAÑO_AGENTE)

agente2_x = random.randint(0, ANCHO - TAMAÑO_AGENTE)
agente2_y = random.randint(0, ALTO - TAMAÑO_AGENTE)
direccion2_auto = random.choice(list(OPUESTOS.keys())) 
modo_manual_agente2 = False 
rectangulo_agente2 = pygame.Rect(agente2_x, agente2_y, TAMAÑO_AGENTE, TAMAÑO_AGENTE)

# GENERACIÓN DE OBSTÁCULOS SIN SOLAPAMIENTO
obstaculos = []
for _ in range(NUMERO_OBSTACULOS):
    while True:
        obs_x = random.randint(0, ANCHO - TAMAÑO_OBSTACULO)
        obs_y = random.randint(0, ALTO - TAMAÑO_OBSTACULO)
        nuevo_obs = pygame.Rect(obs_x, obs_y, TAMAÑO_OBSTACULO, TAMAÑO_OBSTACULO)
        
        # 1. Verificar que no pise a los agentes o al botón
        colision_entidades = nuevo_obs.colliderect(rectangulo_agente1) or \
                             nuevo_obs.colliderect(rectangulo_agente2) or \
                             nuevo_obs.colliderect(RECT_BOTON)
                             
        # 2. Verificar que no se solape con otros obstáculos ya creados
        colision_obstaculos = any(nuevo_obs.colliderect(obs_existente) for obs_existente in obstaculos)
        
        # Solo se agrega si hay espacio completamente libre
        if not colision_entidades and not colision_obstaculos:
            obstaculos.append(nuevo_obs)
            break

def mover_agente_auto(x, y, direccion):
    if direccion == "ARRIBA": y -= VELOCIDAD_AGENTE
    elif direccion == "ABAJO": y += VELOCIDAD_AGENTE
    elif direccion == "IZQUIERDA": x -= VELOCIDAD_AGENTE
    elif direccion == "DERECHA": x += VELOCIDAD_AGENTE
    return x, y

# HEURÍSTICA: MEMORIA A CORTO PLAZO (ANTI-REBOTE) ¿
def obtener_nueva_direccion(direccion_actual):
    direccion_prohibida = OPUESTOS[direccion_actual]
    opciones_validas = ["ARRIBA", "ABAJO", "IZQUIERDA", "DERECHA"]
    
    # Se elimina la opción de regresar por donde venía
    opciones_validas.remove(direccion_prohibida)
    
    return random.choice(opciones_validas)

def verificar_colision(x, y, rect_otro_agente):
    rect = pygame.Rect(x, y, TAMAÑO_AGENTE, TAMAÑO_AGENTE)
    if x < 0 or x > ANCHO - TAMAÑO_AGENTE or y < 0 or y > ALTO - TAMAÑO_AGENTE:
        return True
    for obs in obstaculos:
        if rect.colliderect(obs): return True
    if rect.colliderect(rect_otro_agente): return True
    return False

# Bucle principal
ejecutando = True
while ejecutando:
    pygame.time.delay(20)

    rectangulo_agente1.x, rectangulo_agente1.y = agente1_x, agente1_y
    rectangulo_agente2.x, rectangulo_agente2.y = agente2_x, agente2_y

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if RECT_BOTON.collidepoint(evento.pos):
                modo_manual_agente2 = not modo_manual_agente2

    # --- LÓGICA AGENTE 1 ---
    nuevo_x1, nuevo_y1 = mover_agente_auto(agente1_x, agente1_y, direccion1)
    if verificar_colision(nuevo_x1, nuevo_y1, rectangulo_agente2):
        direccion1 = obtener_nueva_direccion(direccion1)
    else:
        agente1_x, agente1_y = nuevo_x1, nuevo_y1

    # --- LÓGICA AGENTE 2 ---
    if not modo_manual_agente2:
        nuevo_x2, nuevo_y2 = mover_agente_auto(agente2_x, agente2_y, direccion2_auto)
        if verificar_colision(nuevo_x2, nuevo_y2, rectangulo_agente1):
            direccion2_auto = obtener_nueva_direccion(direccion2_auto)
        else:
            agente2_x, agente2_y = nuevo_x2, nuevo_y2
    else:
        teclas = pygame.key.get_pressed()
        nuevo_x2, nuevo_y2 = agente2_x, agente2_y
        if teclas[pygame.K_w]: nuevo_y2 -= VELOCIDAD_AGENTE
        elif teclas[pygame.K_s]: nuevo_y2 += VELOCIDAD_AGENTE
        elif teclas[pygame.K_a]: nuevo_x2 -= VELOCIDAD_AGENTE
        elif teclas[pygame.K_d]: nuevo_x2 += VELOCIDAD_AGENTE

        if not verificar_colision(nuevo_x2, agente2_y, rectangulo_agente1):
            agente2_x = nuevo_x2
        if not verificar_colision(agente2_x, nuevo_y2, rectangulo_agente1):
            agente2_y = nuevo_y2

    pantalla.fill(COLOR_FONDO)
    
    # Dibujar obstáculos
    for obs in obstaculos:
        pygame.draw.rect(pantalla, COLOR_OBSTACULO, obs)

    # Dibujar botón
    color_boton = COLOR_BOTON_MANUAL if modo_manual_agente2 else COLOR_BOTON_AUTO
    pygame.draw.rect(pantalla, color_boton, RECT_BOTON, border_radius=5)
    
    if usar_texto:
        texto_boton = "Control: Manual" if modo_manual_agente2 else "Control: Automático"
        sup_texto = fuente.render(texto_boton, True, COLOR_TEXTO_BOTON)
        pantalla.blit(sup_texto, sup_texto.get_rect(center=RECT_BOTON.center))

    # Dibujar agentes
    pygame.draw.rect(pantalla, COLOR_AGENTE1, (agente1_x, agente1_y, TAMAÑO_AGENTE, TAMAÑO_AGENTE))
    
    color_agente2 = COLOR_AGENTE2_MANUAL if modo_manual_agente2 else COLOR_AGENTE2_AUTO
    pygame.draw.rect(pantalla, color_agente2, (agente2_x, agente2_y, TAMAÑO_AGENTE, TAMAÑO_AGENTE))

    pygame.display.update()

pygame.quit()