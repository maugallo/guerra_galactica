# Crear un juego:
from pygame import mixer
import pygame
import random
import math

# Inicializar pygame:
pygame.init()

# Crear la pantalla:
pantalla = pygame.display.set_mode((900, 700))

# Título, icono y fondo:
pygame.display.set_caption("Guerra Galáctica")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("background.jpg")

# Puntaje:
puntaje = 0
fuente = pygame.font.Font("Minecraft.ttf", 32)
texto_x = 10
texto_y = 10

# Game Over:
fuente_game_over = pygame.font.Font("Minecraft.ttf", 80)

# Música de fondo:
mixer.music.load("ost.mp3")
mixer.music.set_volume(0.1)
mixer.music.play(-1)
sonido_laser = mixer.Sound("laser.mp3")
sonido_laser.set_volume(0.5)
sonido_explosion = mixer.Sound("explosion.mp3")
sonido_explosion.set_volume(0.5)

# Clases:
class Personaje:
    def __init__(self, icono, x, y, movimientox, movimientoy):
        self.icono = icono
        self.x = x
        self.y = y
        self.movimientox = movimientox
        self.movimientoy = movimientoy

    def mostrarse(self):
        # Mostrarse en pantalla:
        pantalla.blit(self.icono, (self.x, self.y))


class Protagonista(Personaje):
    def __init__(self, icono, x, y, movimientox, movimientoy):
        super().__init__(icono, x, y, movimientox, movimientoy)

    def movimiento(self):
        # Movimiento del jugador:
        self.x += self.movimientox
        # Bordes del juego del jugador:
        if self.x <= 0:
            self.x = 0
        elif self.x >= 836:
            self.x = 836


class Enemigo(Personaje):
    def __init__(self, icono, x, y, movimientox, movimientoy):
        super().__init__(icono, x, y, movimientox, movimientoy)

    def terminarsiono(self):
        # Verificar si el juego terminó:
        if self.y > 530:
            mixer.music.stop()
            sonido_explosion.play()
            for self in lista_enemigos:
                self.y = 1000
            game_over()

    def movimiento(self):
        # Movimiento del enemigo:
        self.x += self.movimientox
        # Bordes del juego del enemigo:
        if self.x <= 0:
            self.movimientox = 1
            self.y += self.movimientoy
        elif self.x >= 836:
            self.movimientox = -1
            self.y += self.movimientoy

    def revisar_colision(self, puntaje):
        hay_colision = colision(self.x, laser.x, self.y, laser.y)
        if hay_colision:
            sonido_explosion.play()
            laser.y = 626
            laser.visibilidad = False
            puntaje += random.randint(0, 51)
            self.x = random.randint(0, 800)
            self.y = random.randint(0, 100)
        return puntaje


class Proyectil(Personaje):
    def __init__(self, icono, x, y, movimientox, movimientoy, visibilidad):
        super().__init__(icono, x, y, movimientox, movimientoy)
        self.visibilidad = visibilidad

    def movimiento(self):
        # Definir qué pasa si el laser llega al final de la ventana:
        if self.y <= -64:
            self.y = 626
            self.visibilidad = False
        # Si el laser ya está visible, se moverá verticalmente hasta llegar al final de la ventana:
        if self.visibilidad:
            self.disparar()
            self.y -= self.movimientoy

    def disparar(self):
        pantalla.blit(self.icono, (self.x + 16, self.y - 35))
        self.visibilidad = True


# Funciones complementarias:
def colision(x1, x2, y1, y2):
    distancia = math.sqrt((math.pow(x2 - x1, 2)) + (math.pow(y2 - y1, 2)))
    if distancia < 27:
        return True
    else:
        return False


def mostrar_puntaje():
    texto = fuente.render(f"Score: {puntaje}", True, (182, 225, 255))
    pantalla.blit(texto, (texto_x, texto_y))


def game_over():
    texto_final = fuente_game_over.render(f"GAME OVER", True, (182, 225, 255))
    pantalla.blit(texto_final, (200, 250))


# Objetos de clases:
jugador = Protagonista(pygame.image.load("protagonista.png"), 418, 626, 0, 0)

lista_enemigos = []
for e in range(8):
    enemigo_nuevo = Enemigo(
        pygame.image.load("enemigo.png"),
        random.randint(0, 800),
        random.randint(0, 100),
        1,
        25,
    )
    lista_enemigos.append(enemigo_nuevo)

laser = Proyectil(pygame.image.load("proyectil.png"), 0, 626, 0, 1.5, False)

# Loop del juego:
ejecucion = True
while ejecucion:
    pantalla.blit(fondo, (0, 0))
    for evento in pygame.event.get():
        match evento.type:
            # Caso en que el jugador presione cerrar ventana:
            case pygame.QUIT:
                ejecucion = False
            case pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    jugador.movimientox = 0.7
                if evento.key == pygame.K_LEFT:
                    jugador.movimientox = -0.7
                if evento.key == pygame.K_e and not laser.visibilidad:
                    laser.x = jugador.x
                    sonido_laser.play()
                    laser.disparar()
            case pygame.KEYUP:
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT:
                    jugador.movimientox = 0

    # Movimiento y posición de personajes:
    jugador.movimiento()
    for enemigos in lista_enemigos:
        enemigos.movimiento()
    laser.movimiento()
    # Verificar si el juego terminó:
    for enemigos in lista_enemigos:
        enemigos.terminarsiono()
    # Detectar colision:
    for enemigos in lista_enemigos:
        puntaje = enemigos.revisar_colision(puntaje)
    # Mostrar personajes:
    jugador.mostrarse()
    for enemigos in lista_enemigos:
        enemigos.mostrarse()
    # Mostramos el puntaje:
    mostrar_puntaje()
    # Actualizar el juego (Importante siempre que vaya al final):
    pygame.display.update()
