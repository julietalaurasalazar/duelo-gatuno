import pygame
import proyectil

class Jugador:
    def __init__(self, nombre):
        imagen_original = pygame.image.load("player.png")
        self.imagen = pygame.transform.scale(imagen_original, (64, 64))
        self.nombre = nombre     
        self.vida = 100 #vida inicial
        self.velocidad = 2
        self.posicion = [100, 100]  # Posición inicial
        self.direccion = 1  # 1 para derecha, -1 para izquierda

        self.rect=self.imagen.get_rect()
        self.rect.topleft = self.posicion

    def mover(self, dx, dy):
        # Actualiza dirección según movimiento horizontal
        if dx > 0:
            self.direccion = 1
        elif dx < 0:
            self.direccion = -1

        self.rect.x += dx
        self.rect.y += dy
        # Mantener posicion sincronizada (por si otros usan self.posicion)
        self.posicion = [self.rect.x, self.rect.y]

    def mostrar(self, screen):
        screen.blit(self.imagen, self.rect)

    def lanzar_proyectil(self):
        # Crea un proyectil desde el centro vertical del jugador hacia su dirección
        x = self.rect.centerx
        y = self.rect.centery
        return proyectil.Proyectil(x, y, self.direccion)


