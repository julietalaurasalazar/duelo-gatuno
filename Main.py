import pygame

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inicio del juego")

# Cargar imagen de fondo
background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar imagen del área
area_image = pygame.image.load("area.png").convert_alpha()

# Radio inicial del área
max_radius = min(SCREEN_WIDTH, SCREEN_HEIGHT)
radius = float(max_radius/1.5)

# Tiempo de achicamiento
shrink_interval = 5000  # 10 segundos en milisegundos
last_shrink_time = pygame.time.get_ticks()

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Dibujar fondo
    screen.blit(background_image, (0, 0))

    # Achicar el área cada 10 segundos
    if current_time - last_shrink_time >= shrink_interval and radius > 0:
        radius -= 20  # Cantidad que se achica cada vez
        if radius < 0:
            radius = 0
        last_shrink_time = current_time

    # Dibujar área si el radio es mayor a 0
    if radius > 0:
        scaled_area = pygame.transform.scale(area_image, (int(radius * 2), int(radius * 2)))
        x = SCREEN_WIDTH // 2 - int(radius)
        y = SCREEN_HEIGHT // 2 - int(radius)
        screen.blit(scaled_area, (x, y))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()