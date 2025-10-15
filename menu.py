import pygame
import sys

def mostrar_menu(screen, background_image, SCREEN_WIDTH, SCREEN_HEIGHT):
    menu_activo = True
    font_titulo = pygame.font.SysFont(None, 72)
    font_opcion = pygame.font.SysFont(None, 48)

    opcion_seleccionada = 0  # 0 = Un jugador

    while menu_activo:
        screen.fill((0, 0, 0))  # Fondo negro

        # Título
        titulo = font_titulo.render("Menú Principal", True, (255, 255, 255))
        screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, 100))

        # Opción: Un jugador (amarillo si seleccionada)
        color_opcion1 = (255, 255, 0) if opcion_seleccionada == 0 else (255, 255, 255)
        opcion1 = font_opcion.render("1. Un jugador", True, color_opcion1)
        screen.blit(opcion1, (SCREEN_WIDTH // 2 - opcion1.get_width() // 2, 250))

        # Instrucción
        instruccion = font_opcion.render("Presiona ENTER para comenzar", True, (200, 200, 200))
        screen.blit(instruccion, (SCREEN_WIDTH // 2 - instruccion.get_width() // 2, 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_activo = False