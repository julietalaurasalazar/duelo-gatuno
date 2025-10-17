import pygame
import sys

def mostrar_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    menu_activo = True
    font_titulo = pygame.font.SysFont(None, 72)
    font_opcion = pygame.font.SysFont(None, 48)
    opcion_seleccionada = 0  # 0 = Jugar, 1 = Jugar (Frenetico), 2 = Salir

    while menu_activo:
        screen.fill((0, 0, 0))

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