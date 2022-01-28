import random
import sys
import pygame
import os

pygame.init()
width = 500
height = 500
FPS = 70
Grom_speed = 0


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Майор Гром. Летающая шаверма")
bg = pygame.image.load("фон.jpg")
clock = pygame.time.Clock()
score = 0
lives = 3


def terminate():
    pygame.quit()
    sys.exit()


def draw_score(surf, text, size, x, y):
    font = pygame.font.SysFont('arial', size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def draw_lives(surf, x, y, live):
    for i in range(live):
        live_img = load_image("кепка.png", -1)
        img = pygame.transform.scale(live_img, (35, 35))
        img_rect = img.get_rect()
        img_rect.x = x + 35 * i
        img_rect.y = y
        surf.blit(img, img_rect)


class Grom(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        player_img = load_image("гром.png")
        self.image = pygame.transform.scale(player_img, (90, 180))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.movie_right = False
        self.movie_left = False

    def update(self):
        self.speedx = Grom_speed
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0


class Shaverma(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        shava_img = load_image("шава.png", -1)
        self.image = pygame.transform.scale(shava_img, (45, 45))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height - 50:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)


class Plague(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        mask_img = load_image("маска.png", -1)
        self.image = pygame.transform.scale(mask_img, (35, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height + 10:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)


def end_screen():
    intro_text = ["                      Ты сгорел, почернел...(", "", "",
                  "", "", "", "", "", "", "", "", "", "", "",
                  "*для перезапуска тыкните куда-нибудь на клавиатуре*"]
    fon = pygame.transform.scale(load_image('gameover.jpg'), (width, height))
    show_screen(intro_text, fon)


def start_screen():
    intro_text = ["Майор Гром. Летающая Шаверма.", "",
                  "Предыстория:",
                  "Чумной доктор решил покуситься на самое святое - ",
                  "на любимый прилавок с шавермой ",
                  "молодого майора полиции Санкт Петербурга, Игоря Грома",
                  "Ваша задача помочь Игорю поймать всю разлетевшуюся шаверму",
                  "и не дать Чумному Доктору навредить вам", "",
                  "Правила игры:",
                  "Движение - стрелки влево, вправо",
                  "Поймал шаверму +50 баллов",
                  "Поймал маску ЧД -1 жизнь", "",
                  "P.s. Для начала игры нажмите на пробел"]
    fon = pygame.transform.scale(load_image('start.jpg'), (width, height))
    show_screen(intro_text, fon)


def show_screen(intro_text, fon):
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 21)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bad_mobs = pygame.sprite.Group()
player = Grom()
all_sprites.add(player)
start_screen()
for i in range(5):
    m = Shaverma()
    all_sprites.add(m)
    mobs.add(m)
for i in range(1):
    p = Plague()
    all_sprites.add(p)
    bad_mobs.add(p)

game_over = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.movie_right = True
                Grom_speed += 9
            if event.key == pygame.K_LEFT:
                player.movie_left = True
                Grom_speed -= 9
        elif not game_over and event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.movie_right = False
                Grom_speed = 0
            if event.key == pygame.K_LEFT:
                Grom_speed = 0
                player.movie_left = False

    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        score += 50
        m = Shaverma()
        all_sprites.add(m)
        mobs.add(m)
    hits = pygame.sprite.spritecollide(player, bad_mobs, True)
    if hits:
        m = Plague()
        all_sprites.add(m)
        bad_mobs.add(m)
        if lives > 0:
            lives -= 1
            print(lives)
        else:
            game_over = True
            mobs.empty()
            bad_mobs.empty()
            all_sprites.empty()
    if not game_over:
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        draw_score(screen, str(score), 24, width - 450, 10)
        draw_lives(screen, width - 120, 10, lives)
    else:
        screen.blit(load_image('фон.jpg'), screen.get_rect())
        end_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Grom()
        all_sprites.add(player)
        lives = 3
        score = 0
        for i in range(5):
            m = Shaverma()
            all_sprites.add(m)
            mobs.add(m)
        for i in range(1):
            p = Plague()
            all_sprites.add(p)
            bad_mobs.add(p)

    pygame.display.flip()
    clock.tick(FPS)
