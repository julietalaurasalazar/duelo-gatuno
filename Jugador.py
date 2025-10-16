import pygame
import proyectil
from direccion import Direccion
import math

class Jugador:
    def __init__(self, nombre):
        imagen_original = pygame.image.load("player.png")
        # Guardar imagen base orientada hacia la derecha (ESTE)
        self.base_image = pygame.transform.scale(imagen_original, (64, 64))
        self.imagen = self.base_image

        self.nombre = nombre     
        self.vida = 100 #vida inicial
        self.velocidad = 2
        self.posicion = [100, 100]  # Posición inicial
        self.direccion = Direccion.E  # usar enum de direcciones

        self.rect = self.imagen.get_rect()
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

            new_dir = mapping.get((sx, sy), self.direccion)
            if new_dir != self.direccion:
                # actualizar direccion y rotar/transformar imagen según la nueva dirección
                # NOTA: Norte y Sur deben conservar la última transformación visual.
                center = self.rect.center
                self.direccion = new_dir

                if self.direccion in (Direccion.N, Direccion.S):
                    # mantener self.imagen tal como estaba (conservar última rotación)
                    pass
                elif self.direccion == Direccion.W:
                    # Oeste: flip horizontal de la base
                    self.imagen = pygame.transform.flip(self.base_image, True, False)
                elif self.direccion in (Direccion.NW, Direccion.SW):
                    # Noroeste / Suroeste: primero flip horizontal la base (para mirar oeste),
                    # luego rotar esa imagen para inclinarla hacia la diagonal correcta.
                    vx, vy = self.direccion.vector
                    angle_deg = math.degrees(math.atan2(-vy, vx))
                    flipped_base = pygame.transform.flip(self.base_image, True, False)
                    # restar 180° de la rotación calculada (porque partimos de la imagen volteada)
                    self.imagen = pygame.transform.rotate(flipped_base, angle_deg - 180)
                else:
                    # Este, NE y SE: rotación igual que en proyectil (atan2 con -vy)
                    vx, vy = self.direccion.vector
                    angle_deg = math.degrees(math.atan2(-vy, vx))
                    self.imagen = pygame.transform.rotate(self.base_image, angle_deg)

                # reconstruir rect y restaurar centro para evitar "saltos"
                self.rect = self.imagen.get_rect()
                self.rect.center = center

        self.rect.x += dx
        self.rect.y += dy
        # Mantener posicion sincronizada (por si otros usan self.posicion)
        self.posicion = [self.rect.x, self.rect.y]

    def mostrar(self, screen):
        screen.blit(self.imagen, self.rect)

    def aplicar_impulso(self, vector, fuerza):
        # vector puede ser tupla (vx, vy) con valores -1,0,1 (o cualquier otro)
        try:
            vx, vy = vector
        except Exception:
            vx, vy = (0, 0)
        # aplicar desplazamiento instantáneo (knockback)
        self.rect.x += int(vx * fuerza)
        self.rect.y += int(vy * fuerza)
        # sincronizar posicion
        self.posicion = [self.rect.x, self.rect.y]

    def lanzar_proyectil(self):
        # Crea un proyectil desde el centro del jugador, pasando la enum Direccion y el owner (self)
        x = self.rect.centerx
        y = self.rect.centery
        return proyectil.Proyectil(x, y, self.direccion, owner=self)


