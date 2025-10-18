import pygame
import sys

def mostrar_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    menu_activo = True
    font_titulo = pygame.font.SysFont(None, 72)
    font_opcion = pygame.font.SysFont(None, 48)
    opcion_seleccionada = 0  # 0 = Jugar, 1 = Jugar (Frenetico), 2 = Salir

    # Variables para animación vertical
    deco_base_y = SCREEN_HEIGHT - 400
    deco_offset = 0
    deco_direction = 1  # 1 = abajo, -1 = arriba
    deco_speed = 2      # velocidad de movimiento

    while menu_activo:
        screen.fill((0, 0, 0))

        # Animación: rebote suave entre -30 y +30 píxeles
        deco_offset += deco_direction * deco_speed
        if deco_offset > 30 or deco_offset < -30:
            deco_direction *= -1

        titulo = font_titulo.render("DUELO ARCOIRIS", True, (255, 141, 161))
        screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, 100))

        menu = font_titulo.render("Menú Principal", True, (40, 114, 51))
        screen.blit(menu, (SCREEN_WIDTH // 2 - menu.get_width() // 2, 250))

        # Colores según selección
        color0 = (255, 255, 0) if opcion_seleccionada == 0 else (255, 255, 255)
        color1 = (255, 255, 0) if opcion_seleccionada == 1 else (255, 255, 255)
        color2 = (255, 255, 0) if opcion_seleccionada == 2 else (255, 255, 255)

        # Opciones (orden: Jugar, Jugar (Frenetico), Salir)
        opcion0 = font_opcion.render("1. Jugar", True, color0)
        opcion1 = font_opcion.render("2. Jugar (Frenetico)", True, color1)
        opcion2 = font_opcion.render("3. Salir", True, color2)

        screen.blit(opcion0, (SCREEN_WIDTH // 2 - opcion0.get_width() // 2, 320))
        screen.blit(opcion1, (SCREEN_WIDTH // 2 - opcion1.get_width() // 2, 390))
        screen.blit(opcion2, (SCREEN_WIDTH // 2 - opcion2.get_width() // 2, 460))

        # Instrucciones
        gato_controles = pygame.image.load("player1-comandos.png").convert_alpha()
        gato_controles = pygame.transform.scale(gato_controles, (100, 100))
        perro_controles = pygame.image.load("player2-comandos.png").convert_alpha()
        perro_controles = pygame.transform.scale(perro_controles, (100, 100))

        screen.blit(gato_controles, (100, SCREEN_HEIGHT - 300))
        screen.blit(perro_controles, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300))

        # Personajes decorativos
        gato_deco = pygame.image.load("player.png").convert_alpha()
        gato_deco = pygame.transform.scale(gato_deco, (100, 100))
        perro_deco = pygame.image.load("perrito.png").convert_alpha()
        perro_deco = pygame.transform.scale(perro_deco, (100, 100))
        perro_deco = pygame.transform.flip(perro_deco, True, False)  # Voltea horizontalmente

        screen.blit(gato_deco, (100, SCREEN_HEIGHT - 400))
        screen.blit(perro_deco, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 400)) 

        pygame.display.update()
        pygame.time.delay(16)  # ~60 FPS

        #instruccion = font_opcion.render("Usa ↑ ↓ y ENTER para elegir", True, (200, 200, 200))
        #screen.blit(instruccion, (SCREEN_WIDTH // 2 - instruccion.get_width() // 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcion_seleccionada = max(0, opcion_seleccionada - 1)
                if event.key == pygame.K_DOWN:
                    opcion_seleccionada = min(2, opcion_seleccionada + 1)
                if event.key == pygame.K_RETURN:
                    # Devolvemos modos: 'dos' -> normal (Jugar), 'frenetico' -> frenético, o salir
                    if opcion_seleccionada == 0:
                        return "dos"
                    elif opcion_seleccionada == 1:
                        return "frenetico"
                    elif opcion_seleccionada == 2:
                        pygame.quit()
                        sys.exit()