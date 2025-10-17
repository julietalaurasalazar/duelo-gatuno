import pygame
import sys
import Jugador

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
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

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Función principal del juego
def jugar(modo_juego):
    # Radio inicial del área
    max_radius = min(SCREEN_WIDTH, SCREEN_HEIGHT)
    radius = float(max_radius / 1.5)
    shrink_interval = 5000
    last_shrink_time = pygame.time.get_ticks()

    # Crear jugadores
    jugador1_x = SCREEN_WIDTH // 2 - 150  # Izquierda del centro
    jugador2_x = SCREEN_WIDTH // 2 + 150  # Derecha del centro
    jugadores_y = SCREEN_HEIGHT // 2      # Ambos a la misma altura

    jugador1 = Jugador.Jugador("Gatito", SCREEN_WIDTH, SCREEN_HEIGHT, posicion=(jugador1_x, jugadores_y), invertido=False)
    jugador2 = Jugador.Jugador("Perrito", SCREEN_WIDTH, SCREEN_HEIGHT, posicion=(jugador2_x, jugadores_y), invertido=True,image_path='perrito.png') if modo_juego == "dos" else None

    proyectiles = []
    pygame.mixer.music.stop()

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                nuevo_proyectil = jugador1.lanzar_proyectil()
                if nuevo_proyectil: # Sólo añade y reproduce sonido si NO está en cooldown
                    proyectiles.append(nuevo_proyectil)
                    sonido_disparo.play()
            
            if jugador2 and event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                nuevo_proyectil = jugador2.lanzar_proyectil()
                if nuevo_proyectil: # Sólo añade y reproduce sonido si NO está en cooldown
                    proyectiles.append(nuevo_proyectil)
                    sonido_disparo.play()

        screen.blit(background_image, (0, 0))
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

        centro_area = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        for j in [jugador1, jugador2] if jugador2 else [jugador1]:
            centro = j.rect.center
            distancia = ((centro[0] - centro_area[0])**2 + (centro[1] - centro_area[1])**2)**0.5
            if distancia > radius:
                j.vida -= 1
                if j.vida < 0:
                    j.vida = 0

        if current_time - last_shrink_time >= shrink_interval and radius > 0:
            radius -= 20
            radius = max(radius, 0)
            last_shrink_time = current_time

        if radius > 0:
            scaled_area = pygame.transform.scale(area_image, (int(radius * 2), int(radius * 2)))
            x = SCREEN_WIDTH // 2 - int(radius)
            y = SCREEN_HEIGHT // 2 - int(radius)
            screen.blit(scaled_area, (x, y))

        jugador1.mostrar(screen)
        if jugador2:
            jugador2.mostrar(screen)

        for p in proyectiles[:]:
            p.mover()
            p.mostrar(screen)
            targets = [jugador1] + ([jugador2] if jugador2 else [])
            collided = False
            for t in targets:
                if t is None or getattr(p, "owner", None) is t:
                    continue
                if p.rect.colliderect(t.rect):
                    t.aplicar_impulso(p.vector, 150)
                    if p in proyectiles:
                        proyectiles.remove(p)
                    collided = True
                    break
            if collided:
                continue
            if p.rect.right < 0 or p.rect.left > SCREEN_WIDTH or p.rect.bottom < 0 or p.rect.top > SCREEN_HEIGHT:
                if p in proyectiles:
                    proyectiles.remove(p)

        # Verificar si algún jugador murió
        for j in [jugador1, jugador2] if jugador2 else [jugador1]:
            if j.vida <= 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("musica-gameover.wav")
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play()
                game_over_font = pygame.font.SysFont(None, 72)
                game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 80))

                # Determinar ganador
                if jugador2 and jugador1.vida <= 0 and jugador2.vida > 0:
                    ganador = "¡Ganó Perrito!"
                elif jugador2 and jugador2.vida <= 0 and jugador1.vida > 0:
                    ganador = "¡Ganó Gatito!"
                else:
                    ganador = "¡Empate!"

                ganador_font = pygame.font.SysFont(None, 48)
                ganador_text = ganador_font.render(ganador, True, (255, 255, 0))
                screen.blit(ganador_text, (SCREEN_WIDTH // 2 - ganador_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

                pygame.display.flip()
                pygame.time.delay(3000)
                running = False
                break

        font = pygame.font.SysFont(None, 36)
        vida1 = font.render(f"Vida Gatito: {jugador1.vida}", True, (255, 0, 0))
        screen.blit(vida1, (20, 20))
        if jugador2:
            vida2 = font.render(f"Vida Perrito: {jugador2.vida}", True, (0, 0, 255))
            screen.blit(vida2, (SCREEN_WIDTH - vida2.get_width() - 20, 20))

        pygame.display.update()
        clock.tick(60)

# 🔁 Bucle principal del programa
while True:
    pygame.mixer.music.load("musica-menu.wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    try:
        import menu
        modo_juego = menu.mostrar_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    except ImportError:
        modo_juego = "uno"

    jugar(modo_juego)