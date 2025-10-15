import pygame
import sys

def mostrar_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    menu_activo = True
    font_titulo = pygame.font.SysFont(None, 72)
    font_opcion = pygame.font.SysFont(None, 48)
    opcion_seleccionada = 0  # 0 = Un jugador, 1 = Dos jugadores

    while menu_activo:
        screen.fill((0, 0, 0))

        titulo = font_titulo.render("Menú Principal", True, (255, 255, 255))
        screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, 100))

        color1 = (255, 255, 0) if opcion_seleccionada == 0 else (255, 255, 255)
        color2 = (255, 255, 0) if opcion_seleccionada == 1 else (255, 255, 255)

        opcion1 = font_opcion.render("1. Un jugador", True, color1)
        opcion2 = font_opcion.render("2. Dos jugadores", True, color2)

        screen.blit(opcion1, (SCREEN_WIDTH // 2 - opcion1.get_width() // 2, 250))
        screen.blit(opcion2, (SCREEN_WIDTH // 2 - opcion2.get_width() // 2, 320))

        instruccion = font_opcion.render("Usa ↑ ↓ y ENTER para elegir", True, (200, 200, 200))
        screen.blit(instruccion, (SCREEN_WIDTH // 2 - instruccion.get_width() // 2, 450))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcion_seleccionada = max(0, opcion_seleccionada - 1)
                if event.key == pygame.K_DOWN:
                    opcion_seleccionada = min(1, opcion_seleccionada + 1)
                if event.key == pygame.K_RETURN:
                    return "uno" if opcion_seleccionada == 0 else "dos"