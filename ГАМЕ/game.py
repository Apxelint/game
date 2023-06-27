# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading

import pygame

#Импортируем библиотеку pygame и инициализируем ее модуль
pygame.init()

#Global Constants. Задаем глобальные константы

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
#Создаем объект экрана соответствующего заданным размерам
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Устанавливаем название окна
pygame.display.set_caption("Chrome DinoSAURUS Runner")

#Загружаем иконку окна
Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

#Создаем набор изображений для каждого состояния игрока
RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]

#Создаем наборы изображений для каждого вида кактуса
SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
]

#Создаем набор изображений для каждого вида птицы
BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

#Загружаем облако заднего фона
CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

#Загружаем картинку трассы заднего фона
BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

#Задаем цвет для текстовых надписей
FONT_COLOR=(0,0,0)

#Создаем класс игрока
class Dinosaur:
    #Задаем параметры для позиции игрока, для прыжка и прочее
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    #Создаем конструктор класса
    def __init__(self):
        # Загружаем наборы изображений игрока
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        # Задаем начальные состояния игрока
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        # Задаем начальный индекс изображения в наборе
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        # Задаем начальную позицию игрока на экране
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    # Определяем метод для обновления состояния игрока
    def update(self, userInput):
        # Если игрок опускается, то выполняем метод duck
        if self.dino_duck:
            self.duck()
        # Если игрок бежит, то выполняем метод run
        if self.dino_run:
            self.run()
        # Если игрок прыгает, то выполняем метод jump
        if self.dino_jump:
            self.jump()

        # Если индекс текущего изображения больше 10, то обнуляем его
        if self.step_index >= 10:
            self.step_index = 0

        # Определяем действия при различных нажатиях клавиш
        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    # Определяем метод обработки способности игрока опускаться
    def duck(self):
        # С помощью индекса определяем, какое изображение необходимо показывать
        self.image = self.duck_img[self.step_index // 5]
        # Задаем координаты изображения в пространстве экрана
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        # Увеличиваем индекс
        self.step_index += 1

    # Определяем метод обработки способности игрока бежать
    def run(self):
        # С помощью индекса определяем, какое изображение необходимо показывать
        self.image = self.run_img[self.step_index // 5]
        # Задаем координаты изображения в пространстве экрана
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        # Увеличиваем индекс
        self.step_index += 1

    # Определяем метод для прыжка игрока
    def jump(self):
        # Показываем изображение прыжка
        self.image = self.jump_img
        # Если игрок прыгает, то уменьшаем его координату y
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            # Уменьшаем скорость прыжка
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

#Определяем класс для облаков со случайными позициями x и y, изображением облака и шириной
class Cloud:

    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    # Обновляем положение облака и случайным образом генерируем новое положение, если оно исчезнет с экрана
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    # Добавляем облако на экран
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

#Определяем класс препятствий с изображением и типом, а также прямоугольник для обнаружения столкновений
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    # Обновляем положение препятствия и удаляем его из списка, если оно исчезнет с экрана
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    # Добавляем препятствие на экране
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

#Определяем подкласс для небольших препятствий из кактусов со случайным типом и заданным положением y.
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

#Определяем подкласс для препятствий из больших кактусов со случайным типом и заданным положением y.
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

#Определяем подкласс для препятствий для птиц с заданным типом и случайным положением y с анимацией
class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    # Добавление птицы на экран с анимацией
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

#Определяем основной игровой цикл и все необходимые переменные
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False

    # Функция для увеличения очков и скорости игры, а также отображения высокого балла и текущего результата
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    # Функция для рисования(добавления) и перемещения повторяющегося фонового изображения
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Функция для отмены приостановки игры
    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    # Функция для приостановки игры и отображения сообщения и элементов управления для отмены паузы
    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    # Основной игровой цикл, который обрабатывает события, обновляет состояния игрока и препятствий, а также проверяет наличие столкновений
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        # Установка цвета фона экрана в зависимости от времени суток и получение информации о перемещении игрока
        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0))
        userInput = pygame.key.get_pressed()

        # Рисуем и обновлем игрока, а также случайным образом генерируем новые препятствия
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            # Проверяем, нет ли столкновения с игроком, и задерживаем отображением меню на две секунды
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)
        # Рисуем и обновляем фон и облако, а также увеличиваем количество очков
        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

#Определите функцию под названием "menu", которая принимает параметр "death_count".
def menu(death_count):
    # Объявляем глобальные переменные 'points' и 'FONT_COLOR'
    global points
    global FONT_COLOR
    # Установливаем логической переменной с именем 'run' значение True
    run = True
    # Запускаем цикл while и продолжаем его, пока значение 'run' равно True
    while run:
        # Получаем текущее время
        current_time = datetime.datetime.now().hour
        # Если сейчас день (между 7 утра и 7 вечера), устанавливаем цвет шрифта на черный и заливаем экран белым
        if 7 < current_time < 19:
            FONT_COLOR=(0,0,0)
            SCREEN.fill((255, 255, 255))
        # В противном случае сейчас ночь, поэтому установливаем цвет шрифта на белый и заливаем экран серым
        else:
            FONT_COLOR=(255,255,255)
            SCREEN.fill((128, 128, 128))
        # Создайте новый объект шрифта под названием "font" размером 30
        font = pygame.font.Font("freesansbold.ttf", 30)

        # Если игрок еще не умер (количество смертей равно 0), отобразите текст "Нажмите любую клавишу для запуска".
        # В противном случае игрок уже умирал раньше, поэтому отобразите текст "Нажмите любую клавишу для перезапуска".
        if death_count == 0:
            text = font.render("Press any Key to Start", True, FONT_COLOR)
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            # Отображаем результат игрока на экране
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            # Открываем 'score.txt ' сохраняем файл и прикладываем к нему счёт игрока
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
            f.close()
            # Открываем 'score.txt " сохраняем и прочитываем сохраненные баллы
            with open("score.txt", "r") as f:
                score = (
                    f.read()
                )
                # Преобразуем баллы из строк в целые числа и находим самый высокий балл
                score_ints = [int(x) for x in score.split()]  # Преобразовываем строки в целые числа
            highscore = max(score_ints)  # Суммируем все элементы списка
            # Отображаем наивысший балл на экране
            hs_score_text = font.render(
                "High Score : " + str(highscore), True, FONT_COLOR
            )
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)
        # Отцентрируем объект "текст" на экране, а затем отрисовываем его
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        # Отображаем спрайт игрока на экране
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        # Обновляем отображение
        pygame.display.update()
        # Перебор всех событий в очереди событий Pygame
        for event in pygame.event.get():
            # Если пользователь нажмет кнопку закрыть, то выйдем из игры
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            # Если пользователь нажмет какую-либо клавишу, снова запустим основной игровой цикл
            if event.type == pygame.KEYDOWN:
                main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
