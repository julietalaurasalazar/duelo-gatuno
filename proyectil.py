import pygame
import math
from direccion import Direccion

class Proyectil:
    def __init__(self, x, y, direccion):
        imagen_original = pygame.image.load("proyectil.png")
        # imagen base orientada hacia el ESTE (x positivo)
        self.base_image = pygame.transform.scale(imagen_original, (32, 32))
        self.velocidad = 10
        self.posicion = [float(x), float(y)]

        # direccion preferiblemente es una instancia de Direccion
        if isinstance(direccion, Direccion):
            self.direccion = direccion
            self.vector = direccion.vector
        else:
            # aceptar también una tupla/lista (vx, vy) o valores numéricos
            try:
                vx, vy = direccion
                self.vector = (int(vx), int(vy))
                self.direccion = None
            except Exception:
                # fallback: mover a la derecha
                self.vector = (1, 0)
                self.direccion = None

        # Calcular ángulo en grados para rotar la imagen base.
        # Usamos atan2 con -vy porque en pantalla Y crece hacia abajo.
        vx, vy = self.vector
        angle_deg = math.degrees(math.atan2(-vy, vx))
        # rotar la imagen base para que apunte en la dirección deseada
        self.imagen = pygame.transform.rotate(self.base_image, angle_deg)

        self.rect = self.imagen.get_rect()
        self.rect.center = (int(self.posicion[0]), int(self.posicion[1]))

    def mover(self):
        # mover usando el vector (puede venir del enum Direccion)
        self.posicion[0] += self.velocidad * self.vector[0]
        self.posicion[1] += self.velocidad * self.vector[1]
        self.rect.center = (int(self.posicion[0]), int(self.posicion[1]))

    def mostrar(self, screen):
        screen.blit(self.imagen, self.rect)