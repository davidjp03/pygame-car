import pygame
import math
import random

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)

# Configurar pantalla
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 400
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Carro con rotación, disparos y vidas")

# Definir variables del carro
ancho_carro = 60
alto_carro = 120
x_carro = ANCHO_PANTALLA // 2
y_carro = ALTO_PANTALLA // 2
angulo_carro = 0
velocidad_carro = 5
velocidad_rotacion = 5

# Variables para el proyectil
ancho_proyectil = 5
alto_proyectil = 10
proyectil_activo = False
velocidad_proyectil = 7
x_proyectil = 0
y_proyectil = 0
angulo_proyectil = 0

# Variables de los bloques
bloques = []
for _ in range(5):
    bloques.append([random.randint(0, ANCHO_PANTALLA - 50), random.randint(0, ALTO_PANTALLA - 50), 50, 20, random.choice([-1, 1]), random.choice([-1, 1])])

# Contador de bloques destruidos
bloques_destruidos = 0

# Vidas del carro
vidas = 3

# Definir fuente para el texto
fuente = pygame.font.SysFont("Arial", 24)

# Definir función para dibujar el carro
def dibujar_carro(pantalla, x, y, angulo):
    # Crear una superficie para el carro (añadir transparencia)
    carro_surface = pygame.Surface((ancho_carro + 20, alto_carro + 20), pygame.SRCALPHA)
    
    # Carrocería
    pygame.draw.rect(carro_surface, AZUL, (10, 10, ancho_carro, alto_carro))
    
    # Ruedas
    pygame.draw.rect(carro_surface, NEGRO, (0, 20, 10, 30))  # Rueda superior izquierda
    pygame.draw.rect(carro_surface, NEGRO, (0, alto_carro - 40, 10, 30))  # Rueda inferior izquierda
    pygame.draw.rect(carro_surface, NEGRO, (ancho_carro + 10, 20, 10, 30))  # Rueda superior derecha
    pygame.draw.rect(carro_surface, NEGRO, (ancho_carro + 10, alto_carro - 40, 10, 30))  # Rueda inferior derecha

    # Luces
    pygame.draw.polygon(carro_surface, AMARILLO, [(30, 10), (10, 0), (50, 0)])  # Luz frontal izquierda
    pygame.draw.polygon(carro_surface, AMARILLO, [(ancho_carro - 30 + 10, 10), (ancho_carro + 10, 0), (ancho_carro - 10, 0)])  # Luz frontal derecha

    # Rotar el carro
    carro_rotado = pygame.transform.rotate(carro_surface, -angulo)
    rect_rotado = carro_rotado.get_rect(center=(x, y))

    # Dibujar el carro rotado
    pantalla.blit(carro_rotado, rect_rotado.topleft)

# Función para dibujar el proyectil
def dibujar_proyectil(pantalla, x, y):
    pygame.draw.rect(pantalla, VERDE, (x, y, ancho_proyectil, alto_proyectil))

# Función para dibujar los bloques
def dibujar_bloques(pantalla, bloques):
    for bloque in bloques:
        pygame.draw.rect(pantalla, ROJO, (bloque[0], bloque[1], bloque[2], bloque[3]))

# Función para mover los bloques
def mover_bloques(bloques):
    for bloque in bloques:
        bloque[0] += bloque[4]  # Movimiento en X
        bloque[1] += bloque[5]  # Movimiento en Y
        if bloque[0] <= 0 or bloque[0] >= ANCHO_PANTALLA - bloque[2]:
            bloque[4] *= -1  # Rebotar en los bordes de la pantalla
        if bloque[1] <= 0 or bloque[1] >= ALTO_PANTALLA - bloque[3]:
            bloque[5] *= -1

# Función para detectar colisión entre el carro y los bloques
def detectar_colision_carro(bloques, x_carro, y_carro):
    for bloque in bloques:
        if bloque[0] < x_carro < bloque[0] + bloque[2] and bloque[1] < y_carro < bloque[1] + bloque[3]:
            return True
    return False

# Función para regenerar un bloque cuando uno es destruido
def regenerar_bloque(bloques):
    bloques.append([random.randint(0, ANCHO_PANTALLA - 50), random.randint(0, ALTO_PANTALLA - 50), 50, 20, random.choice([-1, 1]), random.choice([-1, 1])])

# Bucle principal
ejecutando = True
reloj = pygame.time.Clock()

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()

    # Rotación del carro (invirtiendo las teclas izquierda y derecha)
    if teclas[pygame.K_LEFT]:
        angulo_carro -= velocidad_rotacion
    if teclas[pygame.K_RIGHT]:
        angulo_carro += velocidad_rotacion

    # Traslación del carro (hacia adelante)
    if teclas[pygame.K_UP]:
        x_carro += velocidad_carro * math.sin(math.radians(angulo_carro))
        y_carro -= velocidad_carro * math.cos(math.radians(angulo_carro))
    
    # Traslación del carro (hacia atrás)
    if teclas[pygame.K_DOWN]:
        x_carro -= velocidad_carro * math.sin(math.radians(angulo_carro))
        y_carro += velocidad_carro * math.cos(math.radians(angulo_carro))

    # Disparar proyectil con la barra espaciadora
    if teclas[pygame.K_SPACE] and not proyectil_activo:
        proyectil_activo = True
        angulo_proyectil = angulo_carro
        x_proyectil = x_carro
        y_proyectil = y_carro

    # Movimiento del proyectil
    if proyectil_activo:
        x_proyectil += velocidad_proyectil * math.sin(math.radians(angulo_proyectil))
        y_proyectil -= velocidad_proyectil * math.cos(math.radians(angulo_proyectil))
        if x_proyectil < 0 or x_proyectil > ANCHO_PANTALLA or y_proyectil < 0 or y_proyectil > ALTO_PANTALLA:
            proyectil_activo = False

    # Detección de colisiones entre el proyectil y los bloques
    for bloque in bloques[:]:
        if bloque[0] < x_proyectil < bloque[0] + bloque[2] and bloque[1] < y_proyectil < bloque[1] + bloque[3]:
            bloques.remove(bloque)
            bloques_destruidos += 1
            regenerar_bloque(bloques)
            proyectil_activo = False

    # Detectar colisión entre el carro y los bloques
    if detectar_colision_carro(bloques, x_carro, y_carro):
        vidas -= 1
        if vidas == 0:
            ejecutando = False

    # Mover los bloques
    mover_bloques(bloques)

    # Rellenar la pantalla con un color de fondo
    pantalla.fill(GRIS)

    # Dibujar el carro
    dibujar_carro(pantalla, x_carro, y_carro, angulo_carro)

    # Dibujar el proyectil si está activo
    if proyectil_activo:
        dibujar_proyectil(pantalla, x_proyectil, y_proyectil)

    # Dibujar los bloques
    dibujar_bloques(pantalla, bloques)

    # Mostrar el contador de bloques destruidos
    texto_bloques = fuente.render(f"Bloques destruidos: {bloques_destruidos}", True, BLANCO)
    pantalla.blit(texto_bloques, (10, 10))

    # Mostrar el contador de vidas
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 40))

    # Actualizar la pantalla
    pygame.display.flip()
    
    # Controlar la velocidad de actualización
    reloj.tick(60)

# Cerrar Pygame
pygame.quit()
