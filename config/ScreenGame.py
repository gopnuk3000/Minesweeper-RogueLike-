import os.path
import random
import sys
import pygame
import json
from config.GameBoard import load_image

# начало игры
def startGame():
    # текст
    intro_text = ["Сапер рогалик", "",
                  "Открывайте клетки, и не попадитесь на мины",
                  "с каждым уровнем все сложнее и сложнее,",
                  "Удачи!"]

    # рисовка фона, текста
    screen = pygame.display.set_mode((500, 400))
    fon = pygame.transform.scale(load_image('fon.png'), (500, 400))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()

        # отступы
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    clock = pygame.time.Clock()

    # цикл заставки: по нажатию мывши или клавиатуры выходим
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)

# Конец игры: разная в зависимости от выйграша или пройгрыша
def endGame(SCOREGAME, LEVEL, WIN):
    if not WIN:
        intro_text = ["Конец игры", "",
                      "Вы проиграли!", "",
                      f"Ваши очки: {SCOREGAME}", f"Уровень комнаты: {LEVEL}", 'Ваш прогресс сохранен на рабочий стол']
    else:
        intro_text = ["Конец игры", "",
                      "Ты выйграл!", "",
                      f"Ваши очки: {SCOREGAME}", f"Уровень комнаты: {LEVEL}", 'Ваш прогресс сохранен на рабочий стол']

    # аналогично что в заставке начала игры
    screen = pygame.display.set_mode((500, 300))
    fon = pygame.transform.scale(load_image('fon.png'), (500, 300))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    with open(f'{os.path.expanduser("~")}/Desktop/result.txt', 'w', encoding='utf-8') as F:
        text = f"""Статистка игры\n==================\nУровень: {LEVEL};\nОчки: {SCOREGAME};\n==================\nПродолжайте развиваться!"""
        F.write(text)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)

# уровень был пройден
def levelComplite():
    intro_text = ["Уровень пройден!"]

    screen = pygame.display.set_mode((250, 150))
    fon = pygame.transform.scale(load_image('fon.png'), (250, 150))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)

# экран квиза: всплывают ответы на вопрос и сам вопрос
def quizScreen(lvl: str):
    with open('data/quiz.json', 'r', encoding='utf-8') as F:
        QUIZ: dict = json.load(F)

    # рандомный квиз из файла
    data_quiz = QUIZ[lvl]
    data_quest_random = [t for t in data_quiz.values()]
    data_quiz_correct = [r for r in random.choice(data_quest_random).values()]
    quiz_question_answer = data_quiz_correct[0], data_quiz_correct[1], data_quiz_correct[2]

    intro_text = [f"{quiz_question_answer[0]}","",f"{quiz_question_answer[1][0]}", f"{quiz_question_answer[1][1]}", f"{quiz_question_answer[1][2]}", f"{quiz_question_answer[1][3]}", "", "Введите правильный ответ"]

    screen = pygame.display.set_mode((950, 380))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    question_rect = []
    screen.fill((0, 0, 0))
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        if line in quiz_question_answer[1]:
            question_rect.append(line)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()

    clock = pygame.time.Clock()

    # цикл в котором пишем ответ на клавиатуре: правильный ответ - True, иначе False
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Удаление последнего символа
                elif event.key == pygame.K_RETURN:
                    if quiz_question_answer[2].lower() == input_text.lower():
                        return True
                    else:
                        return False
                else:
                    input_text += event.unicode  # Добавление нового символа
        screen.fill((255,255,255), (0, 330, 950, 450))
        text_surface = font.render(input_text, 1, (0,0,0))
        screen.blit(text_surface, (10, 340))
        pygame.display.flip()
        clock.tick(60)