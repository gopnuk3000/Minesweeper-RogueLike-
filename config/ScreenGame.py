import random
import sys
import pygame
import json
from config.GameBoard import load_image


def startGame():
    intro_text = ["Сапер рогалик", "",
                  "Открывайте клетки, и не попадитесь на мины",
                  "с каждым уровнем все сложнее и сложнее,",
                  "Удачи!"]

    screen = pygame.display.set_mode((500, 400))
    fon = pygame.transform.scale(load_image('fon.png'), (500, 400))
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


def endGame(SCOREGAME, LEVEL, WIN):
    if not WIN:
        intro_text = ["Конец игры", "",
                      "Вы проиграли!", "",
                      f"Ваши очки: {SCOREGAME}", f"Уровень комнаты: {LEVEL}"]
    else:
        intro_text = ["Конец игры", "",
                      "Ты выйграл!", "",
                      f"Ваши очки: {SCOREGAME}", f"Уровень комнаты: {LEVEL}"]

    screen = pygame.display.set_mode((300, 300))
    fon = pygame.transform.scale(load_image('fon.png'), (300, 300))
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

def quizScreen(lvl: str):
    with open('data/quiz.json', 'r', encoding='utf-8') as F:
        QUIZ: dict = json.load(F)

    # id = random.randint(0, len(QUIZ[lvl].items()))
    data_quiz = QUIZ[lvl]
    data_quest_random = [t for t in data_quiz.values()]
    data_quiz_correct = [r for r in random.choice(data_quest_random).values()]
    quiz_question_answer = data_quiz_correct[0], data_quiz_correct[1], data_quiz_correct[2]

    intro_text = [f"{quiz_question_answer[0]}",""," - ".join(quiz_question_answer[1]), "Выберите правильный ответ"]

    screen = pygame.display.set_mode((350, 350))
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