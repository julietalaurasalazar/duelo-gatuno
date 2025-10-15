import pygame

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
        self.rect.x += dx
        self.rect.y += dy

    def mostrar(self, screen):
        screen.blit(self.imagen, self.rect) 


 