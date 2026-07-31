import sys
import random
from math import sin
from pygame import *

# --- Inicialización ---
init()

# --- Configuración de Pantalla ---
VENTANA_ANCHO, VENTANA_ALTO = 600, 600
ventana = display.set_mode((VENTANA_ANCHO, VENTANA_ALTO))
display.set_caption("Laberintos Extremos")

# --- Paleta de Colores Neón / Modern Arcade ---
COLOR_FONDO_MENU = (18, 18, 28)
COLOR_FONDO_JUEGO = (25, 27, 42)
COLOR_GRID = (35, 38, 58)

COLOR_PARED = (41, 98, 255)
COLOR_PARED_BORDE = (0, 229, 255)

COLOR_META = (255, 215, 0)
COLOR_META_GLOW = (255, 235, 59, 100)

COLOR_BOTON = (38, 166, 154)
COLOR_BOTON_HOVER = (0, 230, 118)
COLOR_BOTON_RED = (229, 57, 53)
COLOR_BOTON_RED_HOVER = (255, 82, 82)
COLOR_TEXTO = (240, 240, 255)
COLOR_TEXTO_SOMBRA = (10, 10, 20)

PLAYER1_IMAG = 'hero.png'
PLAYER2_IMAG = 'cyborg.png'

# --- Fuentes ---
try:
    fuente_titulo = font.SysFont("Verdana", 32, bold=True)
    fuente_subtitulo = font.SysFont("Verdana", 18, bold=True)
    fuente_boton = font.SysFont("Verdana", 13, bold=True)
except (FileNotFoundError, OSError):
    fuente_titulo = font.Font(None, 36)
    fuente_subtitulo = font.Font(None, 22)
    fuente_boton = font.Font(None, 16)

# --- Sistema de Partículas ---
class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radio = random.randint(2, 5)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.vida = 255

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 10

    def dibujar(self, superficie):
        if self.vida > 0:
            s = Surface((self.radio * 2, self.radio * 2), SRCALPHA)
            draw.circle(s, (*self.color, self.vida), (self.radio, self.radio), self.radio)
            superficie.blit(s, (self.x - self.radio, self.y - self.radio))

particulas = []

# --- Clases del Juego ---

class M_c(sprite.Sprite):
    def __init__(self, sprite_img, pos_x, pos_y, speed=0, dir_x=0, dir_y=0, limite_min=0, limite_max=0):
        super().__init__()
        try:
            self.image = transform.scale(image.load(sprite_img), (32, 32))
        except (error, FileNotFoundError):
            self.image = Surface((32, 32))
            self.image.fill((255, 0, 100) if dir_x != 0 or dir_y != 0 else (0, 229, 255))
            
        self.speed = speed
        self.rect = self.image.get_rect()
        
        self.pos_inicial_x = pos_x
        self.pos_inicial_y = pos_y
        self.dir_x_inicial = dir_x
        self.dir_y_inicial = dir_y
        
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.dir_x = dir_x
        self.dir_y = dir_y
        
        self.limite_min = limite_min
        self.limite_max = limite_max

    def reset(self):
        ventana.blit(self.image, (self.rect.x, self.rect.y))

    def reiniciar_posicion(self):
        self.rect.x = self.pos_inicial_x
        self.rect.y = self.pos_inicial_y
        self.dir_x = self.dir_x_inicial
        self.dir_y = self.dir_y_inicial

    def update_jugador(self):
        keys = key.get_pressed()
        movido = False
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            movido = True
        if keys[K_d] and self.rect.x < VENTANA_ANCHO - 32:
            self.rect.x += self.speed
            movido = True
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            movido = True
        if keys[K_s] and self.rect.y < VENTANA_ALTO - 32:
            self.rect.y += self.speed
            movido = True

        if movido and random.random() < 0.4:
            particulas.append(Particula(self.rect.centerx, self.rect.centery, (0, 229, 255)))

    def update_enemigo(self):
        if self.dir_x != 0:
            self.rect.x += self.speed * self.dir_x
            if self.rect.x <= self.limite_min:
                self.rect.x = self.limite_min
                self.dir_x *= -1
            elif self.rect.x >= self.limite_max - 32:
                self.rect.x = self.limite_max - 32
                self.dir_x *= -1

        if self.dir_y != 0:
            self.rect.y += self.speed * self.dir_y
            if self.rect.y <= self.limite_min:
                self.rect.y = self.limite_min
                self.dir_y *= -1
            elif self.rect.y >= self.limite_max - 32:
                self.rect.y = self.limite_max - 32
                self.dir_y *= -1

        if random.random() < 0.3:
            particulas.append(Particula(self.rect.centerx, self.rect.centery, (255, 52, 100)))


class Pared(sprite.Sprite):
    def __init__(self, pos_x, pos_y, ancho, alto, es_meta=False):
        super().__init__()
        self.es_meta = es_meta
        self.rect = Rect(pos_x, pos_y, ancho, alto)

    def dibujar(self, tiempo=0):
        if self.es_meta:
            pulso = int((sin(tiempo * 0.008) + 1) * 6)
            glow_rect = self.rect.inflate(pulso, pulso)
            s = Surface((glow_rect.width, glow_rect.height), SRCALPHA)
            draw.rect(s, COLOR_META_GLOW, s.get_rect())
            ventana.blit(s, glow_rect.topleft)

            draw.rect(ventana, COLOR_META, self.rect)
            draw.rect(ventana, (255, 255, 255), self.rect, 2)
        else:
            draw.rect(ventana, COLOR_PARED, self.rect)
            draw.rect(ventana, COLOR_PARED_BORDE, self.rect, 2)


def dibujar_fondo_grid():
    ventana.fill(COLOR_FONDO_JUEGO)
    tamanio_celda = 40
    for x in range(0, VENTANA_ANCHO, tamanio_celda):
        draw.line(ventana, COLOR_GRID, (x, 0), (x, VENTANA_ALTO))
    for y in range(0, VENTANA_ALTO, tamanio_celda):
        draw.line(ventana, COLOR_GRID, (0, y), (VENTANA_ANCHO, y))


def crear_boton(rectangulo, texto, fuente, color_normal, color_hover):
    pos_raton = mouse.get_pos()
    colision = rectangulo.collidepoint(pos_raton)
    color_actual = color_hover if colision else color_normal
    
    rect_sombra = rectangulo.move(0, 4)
    draw.rect(ventana, (10, 10, 15), rect_sombra)
    
    draw.rect(ventana, color_actual, rectangulo)
    draw.rect(ventana, (255, 255, 255), rectangulo, 2)
    
    sup_texto = fuente.render(texto, True, COLOR_TEXTO)
    rect_texto = sup_texto.get_rect(center=rectangulo.center)
    ventana.blit(sup_texto, rect_texto)
    
    return colision and mouse.get_pressed()[0]


def render_texto_con_sombra(texto, fuente, centro_x, centro_y, color=COLOR_TEXTO):
    sup_sombra = fuente.render(texto, True, COLOR_TEXTO_SOMBRA)
    rect_sombra = sup_sombra.get_rect(center=(centro_x + 2, centro_y + 2))
    ventana.blit(sup_sombra, rect_sombra)
    
    sup_texto = fuente.render(texto, True, color)
    rect_texto = sup_texto.get_rect(center=(centro_x, centro_y))
    ventana.blit(sup_texto, rect_texto)


# --- Carga de Mapas ---

def cargar_mapa(numero_mapa):
    paredes = []
    enemigos = []
    
    GROSOR_PARED = 13
    
    if numero_mapa == 1:
        paredes = [
            Pared(100, 0, GROSOR_PARED, 480),
            Pared(220, 120, GROSOR_PARED, 480),
            Pared(340, 0, GROSOR_PARED, 480),
            Pared(460, 120, GROSOR_PARED, 480),
        ]
        meta = Pared(520, 520, 45, 45, es_meta=True)
        enemigos.append(M_c(PLAYER2_IMAG, 140, 10, speed=6, dir_y=1, limite_min=0, limite_max=580))
        enemigos.append(M_c(PLAYER2_IMAG, 380, 500, speed=7, dir_y=-1, limite_min=0, limite_max=580))

    elif numero_mapa == 2:
        # MAPA 2: ESPIRAL PERFECTA (Entrada ÚNICA por abajo hacia la meta)
        paredes = [
            # 1. ANILLO EXTERIOR
            Pared(50, 50, 500, GROSOR_PARED),           # Techo
            Pared(537, 50, GROSOR_PARED, 500),          # Derecha
            Pared(50, 537, 500, GROSOR_PARED),          # Suelo
            Pared(50, 130, GROSOR_PARED, 420),          # Izquierda (deja paso arriba)

            # 2. ANILLO INTERMEDIO
            Pared(130, 130, 340, GROSOR_PARED),         # Techo intermedio
            Pared(457, 130, GROSOR_PARED, 330),         # Derecha intermedio
            Pared(130, 447, 340, GROSOR_PARED),         # Suelo intermedio
            Pared(130, 210, GROSOR_PARED, 250),         # Izquierda intermedio

            # 3. HABITACIÓN CENTRAL DE LA META
            Pared(210, 210, 180, GROSOR_PARED),         # Techo central
            Pared(210, 210, GROSOR_PARED, 180),         # Pared Izquierda central
            Pared(377, 210, GROSOR_PARED, 180),         # Pared Derecha central
            
            # Suelo central con la ÚNICA ENTRADA
            Pared(210, 377, 45, GROSOR_PARED),          # Lado izquierdo del suelo
            Pared(332, 377, 58, GROSOR_PARED),          # Lado derecho del suelo
        ]
        
        # Meta ubicada en el centro
        meta = Pared(280, 275, 40, 40, es_meta=True)
        
        # --- ENEMIGOS DEL MAPA 2 ---
        # Anillos exterior e intermedio
        enemigos.append(M_c(PLAYER2_IMAG, 70, 70, speed=5, dir_y=1, limite_min=70, limite_max=480))
        enemigos.append(M_c(PLAYER2_IMAG, 150, 80, speed=6, dir_x=1, limite_min=150, limite_max=480))
        enemigos.append(M_c(PLAYER2_IMAG, 480, 150, speed=7, dir_y=1, limite_min=150, limite_max=410))

        # Enemigos en los pasillos izquierdo y derecho junto a la meta
        enemigos.append(M_c(PLAYER2_IMAG, 170, 220, speed=5, dir_y=1, limite_min=220, limite_max=400))  # Izquierda
        enemigos.append(M_c(PLAYER2_IMAG, 410, 220, speed=6, dir_y=1, limite_min=220, limite_max=400))  # Derecha

    elif numero_mapa == 3:
        paredes = [
            Pared(0, 150, 480, GROSOR_PARED),
            Pared(120, 300, 480, GROSOR_PARED),
            Pared(0, 450, 480, GROSOR_PARED),
        ]
        meta = Pared(20, 500, 45, 45, es_meta=True)
        
        enemigos.append(M_c(PLAYER2_IMAG, 20, 80, speed=9, dir_x=1, limite_min=10, limite_max=570))
        enemigos.append(M_c(PLAYER2_IMAG, 530, 220, speed=8, dir_x=-1, limite_min=130, limite_max=570))
        enemigos.append(M_c(PLAYER2_IMAG, 200, 380, speed=10, dir_x=1, limite_min=10, limite_max=570))

    return paredes, meta, enemigos


def reiniciar_juego():
    player_1.reiniciar_posicion()
    particulas.clear()


# --- Configuración Inicial ---
player_1 = M_c(PLAYER1_IMAG, 15, 15, speed=4)

rect_jugar = Rect((VENTANA_ANCHO - 180) // 2, (VENTANA_ALTO - 50) // 2, 180, 50)

ancho_dif, alto_dif = 160, 48
espaciado = (VENTANA_ANCHO - (ancho_dif * 3)) // 4
y_dif = (VENTANA_ALTO - alto_dif) // 2 + 30

rect_mapa1 = Rect(espaciado, y_dif, ancho_dif, alto_dif)
rect_mapa2 = Rect(espaciado * 2 + ancho_dif, y_dif, ancho_dif, alto_dif)
rect_mapa3 = Rect(espaciado * 3 + ancho_dif * 2, y_dif, ancho_dif, alto_dif)

rect_reiniciar = Rect((VENTANA_ANCHO // 2) - 160, 330, 140, 45)
rect_siguiente_nivel = Rect((VENTANA_ANCHO // 2) - 170, 330, 160, 45)
rect_menu_principal = Rect((VENTANA_ANCHO // 2) + 10, 330, 150, 45)

estado = "menu_principal"
num_mapa_actual = 1
lista_paredes = []
meta_actual = None
lista_enemigos = []
run = True
clock = time.Clock()

# --- Bucle Principal ---
while run:
    tiempo_actual = time.get_ticks()
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            run = False

    # 1. MENÚ PRINCIPAL
    if estado == "menu_principal":
        dibujar_fondo_grid()
        render_texto_con_sombra("LABERINTOS EXTREMOS", fuente_titulo, VENTANA_ANCHO // 2, 180)

        if crear_boton(rect_jugar, "JUGAR", fuente_subtitulo, COLOR_BOTON, COLOR_BOTON_HOVER):
            estado = "seleccion_mapa"
            time.wait(150)

    # 2. SELECCIÓN DE MAPA
    elif estado == "seleccion_mapa":
        dibujar_fondo_grid()
        render_texto_con_sombra("SELECCIONA TU DESAFÍO", fuente_subtitulo, VENTANA_ANCHO // 2, 180)

        if crear_boton(rect_mapa1, "MAPA 1: ZIG-ZAG", fuente_boton, COLOR_BOTON, COLOR_BOTON_HOVER):
            num_mapa_actual = 1
            lista_paredes, meta_actual, lista_enemigos = cargar_mapa(num_mapa_actual)
            reiniciar_juego()
            estado = "jugando"

        if crear_boton(rect_mapa2, "MAPA 2: ESPIRAL", fuente_boton, COLOR_BOTON, COLOR_BOTON_HOVER):
            num_mapa_actual = 2
            lista_paredes, meta_actual, lista_enemigos = cargar_mapa(num_mapa_actual)
            reiniciar_juego()
            estado = "jugando"

        if crear_boton(rect_mapa3, "MAPA 3: DESAFÍO", fuente_boton, COLOR_BOTON, COLOR_BOTON_HOVER):
            num_mapa_actual = 3
            lista_paredes, meta_actual, lista_enemigos = cargar_mapa(num_mapa_actual)
            reiniciar_juego()
            estado = "jugando"

    # 3. PANTALLA DE JUEGO
    elif estado == "jugando":
        dibujar_fondo_grid()
        
        for p in particulas[:]:
            p.update()
            p.dibujar(ventana)
            if p.vida <= 0:
                particulas.remove(p)

        player_1.reset()
        player_1.update_jugador()

        for enemigo in lista_enemigos:
            enemigo.reset()
            enemigo.update_enemigo()
            if sprite.collide_rect(player_1, enemigo):
                estado = "derrotado"
                time.wait(150)

        if meta_actual:
            meta_actual.dibujar(tiempo_actual)

        if estado == "jugando":
            for p in lista_paredes:
                p.dibujar()
                if sprite.collide_rect(player_1, p):
                    estado = "derrotado"
                    time.wait(150)
                    break

        if estado == "jugando" and meta_actual and sprite.collide_rect(player_1, meta_actual):
            estado = "victoria"
            time.wait(150)

    # 4. PANTALLA DE DERROTA
    elif estado == "derrotado":
        dibujar_fondo_grid()
        render_texto_con_sombra("¡HAS SIDO ELIMINADO!", fuente_titulo, VENTANA_ANCHO // 2, 220, COLOR_BOTON_RED_HOVER)

        if crear_boton(rect_reiniciar, "REINICIAR", fuente_subtitulo, COLOR_BOTON, COLOR_BOTON_HOVER):
            reiniciar_juego()
            for ene in lista_enemigos:
                ene.reiniciar_posicion()
            estado = "jugando"
            time.wait(150)

        if crear_boton(rect_menu_principal, "MENÚ", fuente_subtitulo, COLOR_BOTON_RED, COLOR_BOTON_RED_HOVER):
            reiniciar_juego()
            estado = "menu_principal"
            time.wait(150)

    # 5. PANTALLA DE VICTORIA
    elif estado == "victoria":
        dibujar_fondo_grid()
        render_texto_con_sombra("¡ESCAPASTE CON ÉXITO!", fuente_titulo, VENTANA_ANCHO // 2, 220, COLOR_BOTON_HOVER)

        texto_sig_nivel = "SIGUIENTE NIVEL" if num_mapa_actual < 3 else "COMPLETADO"
        
        if crear_boton(rect_siguiente_nivel, texto_sig_nivel, fuente_subtitulo, COLOR_BOTON, COLOR_BOTON_HOVER):
            if num_mapa_actual < 3:
                num_mapa_actual += 1
                lista_paredes, meta_actual, lista_enemigos = cargar_mapa(num_mapa_actual)
                reiniciar_juego()
                estado = "jugando"
            else:
                reiniciar_juego()
                estado = "menu_principal"
            time.wait(150)

        if crear_boton(rect_menu_principal, "MENÚ", fuente_subtitulo, COLOR_BOTON_RED, COLOR_BOTON_RED_HOVER):
            reiniciar_juego()
            estado = "menu_principal"
            time.wait(150)

    display.update()
    clock.tick(60)

quit()
sys.exit()