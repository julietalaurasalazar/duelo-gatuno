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
sonido_maullido = pygame.mixer.Sound("gatito-maulla.ogg")
sonido_ladrido = pygame.mixer.Sound("perrito-ladra.wav")
sonido_splash = pygame.mixer.Sound("splash.wav")

sonido_disparo.set_volume(0.2)
sonido_pierde_vida.set_volume(0.2)
sonido_maullido.set_volume(0.3)
sonido_ladrido.set_volume(0.3)
sonido_splash.set_volume(0.4)

# Cargar imagen de fondo
background_image = pygame.image.load("fondo.jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar imagen del área
area_image = pygame.image.load("area.png").convert_alpha()

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Dibujar vida
def dibujar_barra_vida(x, y, vida_actual, nombre):
    MAX_VIDA = 100
    BAR_WIDTH = 200
    BAR_HEIGHT = 20
    PADDING = 10  # Espacio alrededor del contenido
    TEXT_HEIGHT = 25

    # Calcular dimensiones del recuadro de fondo
    fondo_x = x - PADDING
    fondo_y = y - TEXT_HEIGHT - PADDING
    fondo_ancho = BAR_WIDTH + 2 * PADDING
    fondo_alto = BAR_HEIGHT + TEXT_HEIGHT + 2 * PADDING

    # Dibujar fondo marrón con borde negro grueso
    pygame.draw.rect(screen, (139, 69, 19), (fondo_x, fondo_y, fondo_ancho, fondo_alto))  # Marrón
    pygame.draw.rect(screen, (0, 0, 0), (fondo_x, fondo_y, fondo_ancho, fondo_alto), 4)    # Borde negro grueso

    # Dibujar barra de fondo gris
    pygame.draw.rect(screen, (100, 100, 100), (x, y, BAR_WIDTH, BAR_HEIGHT))

    # Calcular vida proporcional
    vida_proporcional = max(0, min(vida_actual / MAX_VIDA, 1))
    ancho_vida = int(BAR_WIDTH * vida_proporcional)

    # Color dinámico según vida
    if vida_proporcional > 0.6:
        color = (0, 255, 0)
    elif vida_proporcional > 0.3:
        color = (255, 165, 0)
    else:
        color = (255, 0, 0)

    # Dibujar barra de vida
    pygame.draw.rect(screen, color, (x, y, ancho_vida, BAR_HEIGHT))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, BAR_WIDTH, BAR_HEIGHT), 2)

    # Dibujar nombre del jugador
    font = pygame.font.SysFont(None, 28)
    texto = font.render(nombre, True, (255, 255, 255))
    screen.blit(texto, (x, y - TEXT_HEIGHT))        

# Función principal del juego
def jugar(modo_juego):

    pygame.mixer.music.stop()
    pygame.mixer.music.load("musica-juego.wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    
    # Radio inicial del área
    max_radius = min(SCREEN_WIDTH, SCREEN_HEIGHT)
    radius = float(max_radius / 1.5)
    shrink_interval = 5000
    last_shrink_time = pygame.time.get_ticks()

    # Crear jugadores
        # SETEO DE COORDENADAS 
    jugador1_x = SCREEN_WIDTH // 2 - 150  # Izquierda del centro
    jugador2_x = SCREEN_WIDTH // 2 + 150  # Derecha del centro
    jugadores_y = SCREEN_HEIGHT // 2      # Ambos a la misma altura

    if modo_juego == "frenetico":
        # En modo frenético ambos jugadores no tienen cooldown
        jugador1 = Jugador.Jugador("Gatito", SCREEN_WIDTH, SCREEN_HEIGHT, posicion=(jugador1_x, jugadores_y), invertido=False, cooldown=False)
        jugador2 = Jugador.Jugador("Perrito", SCREEN_WIDTH, SCREEN_HEIGHT, posicion=(jugador2_x, jugadores_y), invertido=True, image_path='perrito.png', cooldown=False)
    else:
        jugador1 = Jugador.Jugador("Gatito", SCREEN_WIDTH, SCREEN_HEIGHT, posicion=(jugador1_x, jugadores_y), invertido=False)
        jugador2 = Jugador.Jugador("Perrito", SCREEN_WIDTH, SCREEN_HEIGHT, posicion=(jugador2_x, jugadores_y), invertido=True,image_path='perrito.png') if modo_juego == "dos" else None

    proyectiles = []
    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # Configuracion de CONTROLES en juego
        for event in pygame.event.get():
            #CIERRE FORZADO
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            #DISPARO
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
            #DASH 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                jugador1.usar_dash()
            if jugador2 and event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                jugador2.usar_dash()

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

        # AREA SEGURA EN RELACION CON EL JUGADOR 
        centro_area = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        for j in [jugador1, jugador2] if jugador2 else [jugador1]:
            centro = j.rect.center
            distancia = ((centro[0] - centro_area[0])**2 + (centro[1] - centro_area[1])**2)**0.5
            # PENALIZACION SI ESTA FUERA DEL AREA
            if distancia > radius:
                j.vida -= 1
                sonido_splash.play()
                sonido_maullido.play(loops=3) if j.nombre == "Gatito" else sonido_ladrido.play(loops=3)
                if j.vida < 0:
                    j.vida = 0
        # ACHICAMIENTO DEL AREA X TIEMPO
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

        # FUNCIONAMIENTO DE LA COLISION
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

        dibujar_barra_vida(20, 60, jugador1.vida, "Gatito")
        if jugador2:
            dibujar_barra_vida(SCREEN_WIDTH - 220, 60, jugador2.vida, "Perrito")

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