import os
import random
import pygame
pygame.font.init()
pygame.mixer.init()


class Ball(pygame.sprite.Sprite):
    def __init__(self, group, radius, x, y):
        # конструктор родительского класса Sprite
        super().__init__(group)
        self.add(balls)
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.x = x
        self.y = y
        # скорость шарика
        self.vx = random.randint(7, 10)
        self.vy = random.randint(7, 10)
        self.radius = radius
        self.revival = 3  # количество возрождений

    def update(self):
        global start
        if start:
            self.rect = self.rect.move(self.vx, self.vy)
        # Проверка на столкновение
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, blocks):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, platforms):
            self.vy = -self.vy
        if self.rect.bottom > height:
            start = not start
            self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
            self.revival -= 1
            if self.revival <= 0:
                global gameover
                gameover = True
        for i in range(self.revival):
            pygame.draw.circle(screen, (255,255,255), (i * 12 + 20, 850), 5)
 

class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders) 
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


blocks_colors = {
    'red': (220, 20, 60),
    'orange': (255, 69, 0),
    'yellow': (50, 205, 50),
    'green': (218, 165, 32)
}


class Block(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, color):
        # конструктор родительского класса Sprite
        super().__init__(all_sprites)
        self.add(blocks)
        self.image = pygame.Surface((x2, y2),
                                    pygame.SRCALPHA, 32)
        self.image.fill(blocks_colors[color])
        self.rect = pygame.Rect(x1, y1, x2, y2)
        self.color = blocks_colors[color]
        

    def update(self):
        # Проверка на столкновение
        if pygame.sprite.spritecollideany(self, balls):
            global score, block_count
            if self.color == (220,20,60):
                score += 40
            if self.color == (255,69,0):
                score += 30
            if self.color == (50,205,50):
                score += 20
            if self.color == (218,165,32):
                score += 10
            block_count -= 1
            self.kill()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        # конструктор родительского класса Sprite
        super().__init__(all_sprites)
        self.add(platforms)
        self.image = pygame.Surface((x2, y2),
                                    pygame.SRCALPHA, 32)
        self.image.fill(pygame.Color('white'))
        self.rect = pygame.Rect(x1, y1, x2, y2)
        self.speed = 0
    
    def update(self):
        self.speed = 0
        key = pygame.key.get_pressed()
        # Проверка на нажатие клавиш-стрелок
        if key[pygame.K_LEFT]:
            self.speed -= 10
        if key[pygame.K_RIGHT]:
            self.speed += 10
        self.rect.x += self.speed
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0


class Gameover(pygame.sprite.Sprite):
    def __init__(self, group, image):
        # конструктор родительского класса Sprite
        super().__init__(group)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = -900

    def update(self):
        if gameover:
            if self.rect.left < 0:
                self.rect.left += 30


def start_screen():
	fon = pygame.image.load('images/bg.png')
	screen.blit(fon, (0, 0))
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			elif event.type == pygame.KEYDOWN or \
    				event.type == pygame.MOUSEBUTTONDOWN:
				return  # начинаем игру
		pygame.display.flip()
		clock.tick(60)


def gameWin():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if chr(event.key) == 'y':
                    return
                if event.key == pygame.K_ESCAPE:  # Выход при нажатии клавиши Esc
                    pygame.quit()
                    quit()
        fon = pygame.image.load('images/game_win.png') 
        screen.blit(fon, (0, 0))
        drawGameWin()			
        pygame.display.update()
        clock.tick(60)
    return


def drawGameWin(color=(0, 0, 0)):
    bg = pygame.image.load('images/game_win.png')
    screen.blit(bg, (0, 0))
    updateScore(score, 50, 50, (255, 208, 215))
    updateLevel(level_num, 50, 100, (255, 208, 215))


def gameOver():
    # Добавление спрайта конца игры
    all_sprites = pygame.sprite.Group()
    Gameover(all_sprites, "images/gameover.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if chr(event.key) == 'y':  # Новая игра при нажатии  клавиши Н
                    return
                if event.key == pygame.K_ESCAPE:  # Выход при нажатии клавиши Esc
                    pygame.quit()
                    quit()
        screen.fill((0, 0, 0))	
        all_sprites.update()
        all_sprites.draw(screen)	
        pygame.display.update()
        clock.tick(60)
    return


def updateScore(score, x=10, y=800, color=(255, 255, 255)):
    font = pygame.font.Font('fonts/Segoe Script.ttf', 25) 
    score_msg = font.render('Счёт: {}'.format(score), 2, color)
    screen.blit(score_msg, (x, y))


def updateLevel(level, x=780, y=800, color=(255, 255, 255)):
    font = pygame.font.Font('fonts/Segoe Script.ttf', 25) 
    score_msg = font.render('Уровень: {}'.format(level + 1), 2, color)
    screen.blit(score_msg, (x, y))


# Получение мвссива с расположением блоков из файла
def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


# Инициализация сетки блоков
def generate_level(level):
    global block_count
    for j in range(len(level)):
        for i in range(len(level[j])):
            if level[j][i] == '-':
                Block(i * 102 + 10, j * 34 + 10, 100, 30, 'red')
            elif level[j][i] == '/':
                Block(i * 102 + 10, j * 34 + 10, 100, 30, 'orange')
            elif level[j][i] == '*':
                Block(i * 102 + 10, j * 34 + 10, 100, 30, 'yellow')
            elif level[j][i] == '#':
                Block(i * 102 + 10, j * 34 + 10, 100, 30, 'green')
            elif level[j][i] == '.':
                pass
            block_count += 1 

size = width, height = 935, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()
start_screen()
pygame.mixer.music.load('sounds/bg.mp3')  # загрузить музыку 
pygame.mixer.music.play(-1)               # включить музыку на повтор
score = 0
level_num = 0

if __name__ == '__main__': 
    while True: 
        backgroung = pygame.image.load('images/game_bg.png')                                                                    
        screen.blit(backgroung, (0, 0))
        balls = pygame.sprite.Group()
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()
        blocks = pygame.sprite.Group()
        platforms = pygame.sprite.Group()

        Colors = [(220,20,60), (255,69,0), (50,205,50), (218,165,32)]
        # все спрайты
        all_sprites = pygame.sprite.Group()

        Border(5, 5, width - 5, 5)
        Border(5, 5, 5, height - 5)
        Border(width - 5, 5, width - 5, height - 5)
        block_count = 0
        level_name = 'maps/Level_' + str(level_num % 5) + '.map'  # Получение имени уровня
        level_map = load_level(level_name) 
        generate_level(level_map)           # Загрузка уровня
        Ball(all_sprites, 20, 450, 450)
        Platform(400, 870, 200, 10)

        win = False
        start = False
        gameover = False

        while not gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_1:
                        pygame.mixer.music.pause() # Поставить музыку на паузу при нажатии клавиши 1
                    elif event.key == pygame.K_2:
                        pygame.mixer.music.unpause() # Включить музыку при нажатии клавиши 2
                if event.type == pygame.KEYDOWN:  # Проверка на нажатие калавиши
                    if event.key == pygame.K_ESCAPE:  # Выход при нажатии клавиши Esc
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_SPACE:  # Начало игры и пауза
                        start = not start
            screen.blit(backgroung, (0, 0))
            if start:
                all_sprites.update()
            all_sprites.draw(screen)
            updateScore(score)
            updateLevel(level_num)
            pygame.display.flip()
            clock.tick(50)
            if block_count <= 0:
                gameover = True
                win = True
        if win:
            gameWin()
            level_num += 1
        else:
            gameOver()
            score = 0
            level_num = 0
        