import pygame
import proyectil
from direccion import Direccion
import math

class Jugador:
    def __init__(self, nombre, screen_width, screen_height, posicion=(100, 100),invertido=False):
        imagen_original = pygame.image.load("player.png")
        # Guardar imagen base orientada hacia la derecha (ESTE)
        self.base_image = pygame.transform.scale(imagen_original, (64, 64))
        # imagen actualmente mostrada (se ajusta según invertido)
        self.imagen = self.base_image

        # imágenes que guardan la última diagonal para N y S y su dirección origen
        # Inicializar por defecto como si las últimas orientaciones hubieran sido NE y SE
        vx, vy = Direccion.NE.vector
        angle_ne = math.degrees(math.atan2(-vy, vx))
        img_ne = pygame.transform.rotate(self.base_image, angle_ne)

        vx, vy = Direccion.SE.vector
        angle_se = math.degrees(math.atan2(-vy, vx))
        img_se = pygame.transform.rotate(self.base_image, angle_se)

        # Si está invertido, flippear las imágenes iniciales para que apunten hacia el oeste
        if invertido:
            img_ne = pygame.transform.flip(img_ne, True, False)
            img_se = pygame.transform.flip(img_se, True, False)
            # la imagen inicial debe mostrarse hacia el oeste
            self.imagen = pygame.transform.flip(self.base_image, True, False)
        else:
            self.imagen = self.base_image

        # Guardar imágenes diagonales y direcciones origen coherentes con invertido
        self.last_diag_north_img = img_ne.copy()
        self.last_diag_north_dir = Direccion.NE if not invertido else Direccion.NW
        self.last_diag_south_img = img_se.copy()
        self.last_diag_south_dir = Direccion.SE if not invertido else Direccion.SW

        # última orientación horizontal conocida (Direccion.E o Direccion.W)
        self.last_horizontal_dir = Direccion.E if not invertido else Direccion.W

        self.nombre = nombre     
        self.vida = 100 #vida inicial
        self.velocidad = 2
        self.screen_width = screen_width     
        self.screen_height = screen_height
        # usar la posición pasada al constructor (convertir a lista para mutabilidad)
        self.posicion = [int(posicion[0]), int(posicion[1])]
        # Dirección inicial según invertido
        self.direccion = Direccion.W if invertido else Direccion.E

        self.rect = self.imagen.get_rect()
        self.rect.topleft = self.posicion

    def _diag_is_east(self, d):
        return d in (Direccion.NE, Direccion.SE)

    def _diag_is_west(self, d):
        return d in (Direccion.NW, Direccion.SW)

    def mover(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        # Limitar dentro de la ventana usando los atributos
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

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
                center = self.rect.center
                self.direccion = new_dir

                # Si la nueva dirección es horizontal pura, actualizar last_horizontal_dir
                if self.direccion == Direccion.E:
                    self.last_horizontal_dir = Direccion.E
                    # Este: imagen base rotada 0°
                    self.imagen = self.base_image
                elif self.direccion == Direccion.W:
                    self.last_horizontal_dir = Direccion.W
                    # Oeste: flip horizontal de la base
                    self.imagen = pygame.transform.flip(self.base_image, True, False)
                elif self.direccion in (Direccion.NE, Direccion.SE):
                    # NE / SE: rotación igual que en proyectil (imagen orientada a ESTE)
                    vx, vy = self.direccion.vector
                    angle_deg = math.degrees(math.atan2(-vy, vx))
                    img = pygame.transform.rotate(self.base_image, angle_deg)
                    self.imagen = img
                    # guardar como última diagonal correspondiente y su dirección
                    if self.direccion == Direccion.NE:
                        self.last_diag_north_img = img.copy()
                        self.last_diag_north_dir = Direccion.NE
                    else:
                        self.last_diag_south_img = img.copy()
                        self.last_diag_south_dir = Direccion.SE
                    # diagonales NE/SE implican orientación horizontal ESTE
                    self.last_horizontal_dir = Direccion.E
                elif self.direccion in (Direccion.NW, Direccion.SW):
                    # Noroeste / Suroeste: flip + rotación para inclinar hacia la diagonal oeste
                    vx, vy = self.direccion.vector
                    angle_deg = math.degrees(math.atan2(-vy, vx))
                    flipped_base = pygame.transform.flip(self.base_image, True, False)
                    img = pygame.transform.rotate(flipped_base, angle_deg - 180)
                    self.imagen = img
                    # guardar como última diagonal correspondiente y su dirección
                    if self.direccion == Direccion.NW:
                        self.last_diag_north_img = img.copy()
                        self.last_diag_north_dir = Direccion.NW
                    else:
                        self.last_diag_south_img = img.copy()
                        self.last_diag_south_dir = Direccion.SW
                    # diagonales NW/SW implican orientación horizontal OESTE
                    self.last_horizontal_dir = Direccion.W
                elif self.direccion == Direccion.N:
                    # Norte: tomar la última diagonal norte almacenada y ajustar +/−45°
                    img = self.last_diag_north_img.copy()
                    if self.last_diag_north_dir == Direccion.NW:
                        img = pygame.transform.rotate(img, -45)
                    elif self.last_diag_north_dir == Direccion.NE:
                        img = pygame.transform.rotate(img, 45)
                    # además tener en cuenta la última orientación horizontal (E/W)
                    if self.last_diag_north_dir is not None:
                        # Si la última horizontal conocida difiere de la horizontal del origen diagonal, flipear
                        if self.last_horizontal_dir == Direccion.W and self._diag_is_east(self.last_diag_north_dir):
                            img = pygame.transform.flip(img, True, False)
                        if self.last_horizontal_dir == Direccion.E and self._diag_is_west(self.last_diag_north_dir):
                            img = pygame.transform.flip(img, True, False)
                    else:
                        # si no hay diagonal conocida, aplicar flip según last_horizontal_dir sobre base
                        if self.last_horizontal_dir == Direccion.W:
                            img = pygame.transform.flip(img, True, False)
                    self.imagen = img
                elif self.direccion == Direccion.S:
                    # Sur: tomar la última diagonal sur almacenada y ajustar +/−45°
                    img = self.last_diag_south_img.copy()
                    # CORRECCIÓN: SW -> +45°, SE -> -45°
                    if self.last_diag_south_dir == Direccion.SW:
                        img = pygame.transform.rotate(img, 45)
                    elif self.last_diag_south_dir == Direccion.SE:
                        img = pygame.transform.rotate(img, -45)
                    # tener en cuenta la última orientación horizontal (E/W)
                    if self.last_diag_south_dir is not None:
                        if self.last_horizontal_dir == Direccion.W and self._diag_is_east(self.last_diag_south_dir):
                            img = pygame.transform.flip(img, True, False)
                        if self.last_horizontal_dir == Direccion.E and self._diag_is_west(self.last_diag_south_dir):
                            img = pygame.transform.flip(img, True, False)
                    else:
                        if self.last_horizontal_dir == Direccion.W:
                            img = pygame.transform.flip(img, True, False)
                    self.imagen = img
                else:
                    # Por seguridad: dejar base
                    self.imagen = self.base_image

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


