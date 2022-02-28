import pygame
from pygame.locals import *
import random

# Projeto feito por : Carlos Eduardo, André, Leonardo Vinicius, Lucas Raimundo

# inicializador de fonte e mixer de musica
pygame.mixer.init()
pygame.font.init()

# variaveis de texto/cores/etc
fonte = pygame.font.SysFont('arial', 20, bold=True, italic=True)  #
fonte2 = pygame.font.SysFont('arial', 15, bold=True, italic=True)
points = 0
red = (255, 0, 0)
blue = (0, 0, 80)
yellow = (200, 200, 10)
purple = (0, 0, 255)
speed = 15
toplay = True
operadores = random.choice(range(1, 5))

# variais de tamanho e setando a janela
pygame.display.set_caption('Snake')
WINDOW_SIZE = (600, 600)
PIXEL_SIZE = 10

# musica de fundo e sons
pygame.mixer.music.load('hxhend3.wav')
pygame.mixer.music.play(-1)
colisao_maca = pygame.mixer.Sound('smw_kick.wav')
colisao_maca_dourada = pygame.mixer.Sound('smw_switch_timer_ending.wav')
colisao_parede = pygame.mixer.Sound('smw_thunder.wav')
mudanca_operador = pygame.mixer.Sound('smb3_nspade_match.wav')

# processamento de imagens
fundo = pygame.image.load('fundosnake.png')
fundo = pygame.transform.scale(fundo, WINDOW_SIZE)

maca_vermelha = pygame.image.load('redapple2.png')
maca_vermelha = pygame.transform.scale(maca_vermelha, (10, 10))

maca_amarela = pygame.image.load('yelolowapple2.png')
maca_amarela = pygame.transform.scale(maca_amarela, (10, 10))

maca_azul = pygame.image.load('blueapple2.png')
maca_azul = pygame.transform.scale(maca_azul, (10, 10))

cobra = pygame.image.load('cobra3.png')
cobra = pygame.transform.scale(cobra, (10, 10))

change_turn = pygame.image.load('spiral.png')
change_turn = pygame.transform.scale(change_turn, (10, 10))

def collision(pos1, pos2):  # função de colisão
    return pos1 == pos2

def off_limits(pos):  # função de bater na parede
    if 0 <= pos[0] < WINDOW_SIZE[0] and 0 <= pos[1] < WINDOW_SIZE[1]:
        return False
    else:
        return True

def random_on_grid():
    x = random.randint(0, WINDOW_SIZE[0])
    y = random.randint(0, WINDOW_SIZE[1])
    return x // PIXEL_SIZE * PIXEL_SIZE, y // PIXEL_SIZE * PIXEL_SIZE

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

snake_pos = [(250, 50), (260, 50), (270, 50)]  # posição da cobra inicialmente
snake_surface = cobra
snake_direction = K_LEFT  # direção que a cobra vai começar

red_apple_surface = maca_vermelha
red_apple_pos = random_on_grid()

blue_apple_surface = maca_azul
blue_apple_pos = random_on_grid()  # posicao aleatória dele

yellow_apple_surface = maca_amarela
yellow_apple_pos = random_on_grid()  # posicao aleatória dele

change_surface = change_turn
change_pos = random_on_grid()

def restart_game():  # reiniciar o jogo
    global snake_pos, yellow_apple_pos, red_apple_pos, blue_apple_pos, snake_direction
    snake_pos = [(250, 50), (260, 50), (270, 50)]
    snake_direction = K_LEFT
    red_apple_pos = random_on_grid()
    blue_apple_pos = random_on_grid()
    yellow_apple_pos = random_on_grid()
    restart_operador()

def restart_operador():
    global operadores
    operadores = random.choice(range(1, 5))

while toplay:  # loop infinito

    pygame.time.Clock().tick(speed)
    screen.blit(fundo, (0, 0))
    pygame.draw.rect(screen, (100, 200, 140), (0, 0, 250, 95))
    pygame.draw.rect(screen, (100, 200, 140), (475, 0, 120, 30))
    texto2 = fonte2.render('Cada maçã tem uma pontuação:', True, (0, 0, 0))
    texto3 = fonte2.render('vermelha 1 ponto', True, red)
    texto4 = fonte2.render('azul 2 pontos', True, blue)
    texto5 = fonte2.render('amarela 5 pontos', True, (250, 250, 30))

    if operadores == 1:
        operadores_escreve = '+'
    elif operadores == 2:
        operadores_escreve = '-'
    elif operadores == 3:
        operadores_escreve = '*'
    else:
        operadores_escreve = '/'

    texto6 = fonte.render(f'operador da vez: {operadores_escreve}', True, (0, 0, 0))
    mensagem = f'Pontos: {points}'
    texto_formatado = fonte.render(mensagem, True, (0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                snake_direction = event.key

    screen.blit(red_apple_surface, red_apple_pos)
    screen.blit(blue_apple_surface, blue_apple_pos)
    screen.blit(yellow_apple_surface, yellow_apple_pos)
    screen.blit(change_surface, change_pos)

    if collision(red_apple_pos, snake_pos[0]):  # colisão da cobra com a maça
        colisao_maca.play()
        snake_pos.append((-10, -10))

        if operadores == 1:
            points = points + 1
        elif operadores == 2:
            points = points - 1
        elif operadores == 3:
            points = points * 1
        else:
            points = points / 1

        red_apple_pos = random_on_grid()  # maça volta a aparecer aleatoriamente
        yellow_apple_pos = random_on_grid()
        blue_apple_pos = random_on_grid()

    if collision(blue_apple_pos, snake_pos[0]):  # cobra colide com o bapple
        colisao_maca.play()

        if operadores == 1:
            points = points + 2
        elif operadores == 2:
            points = points - 2
        elif operadores == 3:
            points = points * 2
        else:
            points = points / 2

        blue_apple_pos = random_on_grid()
        yellow_apple_pos = random_on_grid()
        red_apple_pos = random_on_grid()

    if collision(change_pos, snake_pos[0]):  # colisão da cobra com a maça
        mudanca_operador.play()
        restart_operador()
        change_pos = random_on_grid()

    if collision(yellow_apple_pos, snake_pos[0]):  # colisão da cobra com a maça
        colisao_maca_dourada.play()
        snake_pos.append((-10, -10))

        if operadores == 1:
            points = points + 5
        elif operadores == 2:
            points = points - 5
        elif operadores == 3:
            points = points * 5
        else:
            points = points / 5

        restart_operador()
        yellow_apple_pos = random_on_grid()  # maça volta a aparecer aleatoriamente
        blue_apple_pos = random_on_grid()
        red_apple_pos = random_on_grid()

    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    for i in range(len(snake_pos) - 1, 0, -1):  # cobra bater nela mesma
        if collision(snake_pos[0], snake_pos[i]):
            colisao_parede.play()
            points = 0
            restart_game()
            break
        snake_pos[i] = snake_pos[i - 1]

    if off_limits(snake_pos[0]):  # cobra bater na parede
        colisao_parede.play()
        points = 0
        restart_game()

    if snake_direction == K_UP:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - PIXEL_SIZE)
    elif snake_direction == K_DOWN:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + PIXEL_SIZE)
    elif snake_direction == K_LEFT:
        snake_pos[0] = (snake_pos[0][0] - PIXEL_SIZE, snake_pos[0][1])
    elif snake_direction == K_RIGHT:
        snake_pos[0] = (snake_pos[0][0] + PIXEL_SIZE, snake_pos[0][1])

    screen.blit(texto_formatado, (480, 5))  # para aparecer a pontuação
    screen.blit(texto2, (10, 5))  # para aparecer mensagem sobre cores
    screen.blit(texto3, (10, 25))
    screen.blit(texto4, (10, 40))
    screen.blit(texto5, (10, 55))
    screen.blit(texto6, (10, 70))

    pygame.display.update()
