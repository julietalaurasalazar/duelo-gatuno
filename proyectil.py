import pygame

class Proyectil:
    def __init__(self, x, y, direccion):
        imagen_original = pygame.image.load("proyectil.png")
        self.imagen = pygame.transform.scale(imagen_original, (32, 32))
        self.velocidad = 10
        self.posicion = [x, y]
        self.direccion = direccion  # 1 para derecha, -1 para izquierda

        self.rect = self.imagen.get_rect()
        self.rect.topleft = self.posicion

    def mover(self):
        self.posicion[0] += self.velocidad * self.direccion
        self.rect.topleft = self.posicion

    def mostrar(self, screen):
        screen.blit(self.imagen, self.rect)