import pygame
import sys
import Jugador
import menu

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

menu.mostrar_menu(screen, background_image, SCREEN_WIDTH, SCREEN_HEIGHT)
jugador = Jugador.Jugador("Gatito")

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Dibujar fondo primero
    screen.blit(background_image, (0, 0))

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    dx = dy = 0
    velocidad = jugador.velocidad

    if keys[pygame.K_LEFT]:
        dx -= 1
    if keys[pygame.K_RIGHT]:
        dx += 1
    if keys[pygame.K_UP]:
        dy -= 1
    if keys[pygame.K_DOWN]:
        dy += 1

    if dx != 0 or dy != 0:
        magnitud = (dx**2 + dy**2) ** 0.5
        dx = dx / magnitud * velocidad
        dy = dy / magnitud * velocidad

    jugador.mover(dx, dy)

    # Verificar si el jugador está dentro del área circular
    centro_area = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    jugador_centro = jugador.rect.center
    distancia = ((jugador_centro[0] - centro_area[0]) ** 2 + (jugador_centro[1] - centro_area[1]) ** 2) ** 0.5

    if distancia > radius:
        jugador.vida -= 1
        if jugador.vida < 0:
            jugador.vida = 0

    # Mostrar vida del jugador
    font = pygame.font.SysFont(None, 36)
    vida_texto = font.render(f"Vida: {jugador.vida}", True, (255, 0, 0))
    screen.blit(vida_texto, (20, 20))

    # Achicar el área cada 10 segundos
    if current_time - last_shrink_time >= shrink_interval and radius > 0:
        radius -= 20
        if radius < 0:
            radius = 0
        last_shrink_time = current_time

    # Dibujar área si el radio es mayor a 0
    if radius > 0:
        scaled_area = pygame.transform.scale(area_image, (int(radius * 2), int(radius * 2)))
        x = SCREEN_WIDTH // 2 - int(radius)
        y = SCREEN_HEIGHT // 2 - int(radius)
        screen.blit(scaled_area, (x, y))

    # Dibujar el personaje
    jugador.mostrar(screen)

    # Verificar si el jugador murió
    if jugador.vida <= 0:
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()