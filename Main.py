import pygame
import sys
import Jugador

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inicio del juego")

# Cargar sonidos
sonido_disparo = pygame.mixer.Sound("sonido-disparo.aif")
sonido_pierde_vida = pygame.mixer.Sound("sonido-baja-vida.wav")
sonido_disparo.set_volume(0.2)
sonido_pierde_vida.set_volume(0.2)

# Cargar imagen de fondo
background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar imagen del área
area_image = pygame.image.load("area.png").convert_alpha()

# Radio inicial del área
max_radius = min(SCREEN_WIDTH, SCREEN_HEIGHT)
radius = float(max_radius / 1.5)

# Tiempo de achicamiento
shrink_interval = 5000
last_shrink_time = pygame.time.get_ticks()

# Reloj para controlar FPS
clock = pygame.time.Clock()

# ----------MOSTRAR MENÚ--------------

# Música menú
pygame.mixer.music.load("musica-menu.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # Loop música menú

try:
    import menu
    modo_juego = menu.mostrar_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
except ImportError:
    modo_juego = "uno"

# Crear jugadores (misma altura para ambos)
shared_y = SCREEN_HEIGHT - 150  # puedes cambiar a SCREEN_HEIGHT//2 u otra constante
jugador1 = Jugador.Jugador("Gatito", SCREEN_WIDTH, SCREEN_HEIGHT, posicion=(100, shared_y), invertido=False)
jugador2 = Jugador.Jugador("Perrito", SCREEN_WIDTH, SCREEN_HEIGHT, posicion=(SCREEN_WIDTH - 150, shared_y), invertido=True) if modo_juego == "dos" else None

# Lista de proyectiles
proyectiles = []

# Bucle principal
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # Disparo jugador 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            proyectiles.append(jugador1.lanzar_proyectil())
            sonido_disparo.play()

        # Disparo jugador 2
        if jugador2 and event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            proyectiles.append(jugador2.lanzar_proyectil())
            sonido_disparo.play()

    # Dibujar fondo
    screen.blit(background_image, (0, 0))

    # Obtener teclas presionadas
    keys = pygame.key.get_pressed()

    # Movimiento jugador 1
    dx1 = dy1 = 0
    if keys[pygame.K_LEFT]: dx1 -= 1
    if keys[pygame.K_RIGHT]: dx1 += 1
    if keys[pygame.K_UP]: dy1 -= 1
    if keys[pygame.K_DOWN]: dy1 += 1
    if dx1 or dy1:
        mag1 = (dx1**2 + dy1**2)**0.5
        dx1 = dx1 / mag1 * jugador1.velocidad
        dy1 = dy1 / mag1 * jugador1.velocidad
    jugador1.mover(dx1, dy1)

    # Movimiento jugador 2
    if jugador2:
        dx2 = dy2 = 0
        if keys[pygame.K_a]: dx2 -= 1
        if keys[pygame.K_d]: dx2 += 1
        if keys[pygame.K_w]: dy2 -= 1
        if keys[pygame.K_s]: dy2 += 1
        if dx2 or dy2:
            mag2 = (dx2**2 + dy2**2)**0.5
            dx2 = dx2 / mag2 * jugador2.velocidad
            dy2 = dy2 / mag2 * jugador2.velocidad
        jugador2.mover(dx2, dy2)

    # Verificar si los jugadores están dentro del área
    centro_area = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    for j in [jugador1, jugador2] if jugador2 else [jugador1]:
        centro = j.rect.center
        distancia = ((centro[0] - centro_area[0])**2 + (centro[1] - centro_area[1])**2)**0.5
        if distancia > radius:
            j.vida -= 1
            if j.vida < 0:
                j.vida = 0

    # Achicar el área
    if current_time - last_shrink_time >= shrink_interval and radius > 0:
        radius -= 20
        radius = max(radius, 0)
        last_shrink_time = current_time

    # Dibujar área
    if radius > 0:
        scaled_area = pygame.transform.scale(area_image, (int(radius * 2), int(radius * 2)))
        x = SCREEN_WIDTH // 2 - int(radius)
        y = SCREEN_HEIGHT // 2 - int(radius)
        screen.blit(scaled_area, (x, y))

    # Dibujar jugadores
    jugador1.mostrar(screen)
    if jugador2:
        jugador2.mostrar(screen)

    # Mover y mostrar proyectiles
    for p in proyectiles[:]:
        p.mover()
        p.mostrar(screen)

        # Colisiones con jugadores (no golpear al owner)
        targets = [jugador1] + ([jugador2] if jugador2 else [])
        collided = False
        for t in targets:
            if t is None:
                continue
            if getattr(p, "owner", None) is t:
                continue
            if p.rect.colliderect(t.rect):
                # aplicar knockback y daño
                knockback_force = 30  # ajustar según convenga
                t.aplicar_impulso(p.vector, knockback_force)
                t.vida -= 10
                if t.vida < 0:
                    t.vida = 0
                # eliminar proyectil después del impacto
                if p in proyectiles:
                    proyectiles.remove(p)
                collided = True
                break

        if collided:
            continue

        # Eliminar proyectil fuera de pantalla
        if p.rect.right < 0 or p.rect.left > SCREEN_WIDTH or p.rect.bottom < 0 or p.rect.top > SCREEN_HEIGHT:
            if p in proyectiles:
                proyectiles.remove(p)

# ----------FINAL PARTIDA--------------      

    # Verificar si algún jugador murió
    for j in [jugador1, jugador2] if jugador2 else [jugador1]:
        if j.vida <= 0:
            
            pygame.mixer.music.stop()  # Detener música de partida
            pygame.mixer.music.load("musica-gameover.wav")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()  # Música de game over (una vez)

            game_over_font = pygame.font.SysFont(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
            break

    # Mostrar vidas
    font = pygame.font.SysFont(None, 36)
    vida1 = font.render(f"Vida Gatito: {jugador1.vida}", True, (255, 0, 0))
    screen.blit(vida1, (20, 20))
    if jugador2:
        vida2 = font.render(f"Vida Perrito: {jugador2.vida}", True, (0, 0, 255))
        screen.blit(vida2, (SCREEN_WIDTH - vida2.get_width() - 20, 20))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()