import pygame
import proyectil
from direccion import Direccion

class Jugador:
    def __init__(self, nombre):
        imagen_original = pygame.image.load("player.png")
        self.imagen = pygame.transform.scale(imagen_original, (64, 64))
        self.nombre = nombre     
        self.vida = 100 #vida inicial
        self.velocidad = 2
        self.posicion = [100, 100]  # Posición inicial
        self.direccion = Direccion.E  # usar enum de direcciones

        self.rect=self.imagen.get_rect()
        self.rect.topleft = self.posicion

    def mover(self, dx, dy):
        # Actualiza dirección según movimiento horizontal/vertical usando el enum
        if dx != 0 or dy != 0:
            # Normalizar a signos (-1, 0, 1)
            sx = 0 if abs(dx) < 1e-6 else (1 if dx > 0 else -1)
            sy = 0 if abs(dy) < 1e-6 else (1 if dy > 0 else -1)

            mapping = {
                (0, -1): Direccion.N,
                (1, -1): Direccion.NE,
                (1, 0): Direccion.E,
                (1, 1): Direccion.SE,
                (0, 1): Direccion.S,
                (-1, 1): Direccion.SW,
                (-1, 0): Direccion.W,
                (-1, -1): Direccion.NW,
            }

            self.direccion = mapping.get((sx, sy), self.direccion)

        self.rect.x += dx
        self.rect.y += dy
        # Mantener posicion sincronizada (por si otros usan self.posicion)
        self.posicion = [self.rect.x, self.rect.y]

    def mostrar(self, screen):
        screen.blit(self.imagen, self.rect)

    def lanzar_proyectil(self):
        # Crea un proyectil desde el centro del jugador, pasando la enum Direccion
        x = self.rect.centerx
        y = self.rect.centery
        return proyectil.Proyectil(x, y, self.direccion)


