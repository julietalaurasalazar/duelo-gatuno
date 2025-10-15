import pygame

class Proyectil:
    def __init__(self, x, y, direccion):
        imagen_original = pygame.image.load("proyectil.png")
        self.imagen = pygame.transform.scale(imagen_original, (32, 32))
        self.velocidad = 10
        self.posicion = [float(x), float(y)]
        # direccion debe ser una instancia de Direccion (enum) con .vector -> (vx, vy)
        self.direccion = direccion
        self.vector = direccion.vector

        self.rect = self.imagen.get_rect()
        # centrar el rect en la posición inicial
        self.rect.center = (int(self.posicion[0]), int(self.posicion[1]))

    def mover(self):
        # mover en ambas componentes usando el vector del enum
        self.posicion[0] += self.velocidad * self.vector[0]
        self.posicion[1] += self.velocidad * self.vector[1]
        self.rect.center = (int(self.posicion[0]), int(self.posicion[1]))

    def mostrar(self, screen):
        screen.blit(self.imagen, self.rect)