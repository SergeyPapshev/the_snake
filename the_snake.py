from random import randint
from typing import Optional

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Начальная позиция змейки
INIT_POSITION = (320, 240)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    position: tuple[int, int]
    body_color: tuple[int, int, int]

    def __init__(self, position=None, color=None):
        self.position = position
        self.body_color = color

    def draw(self):
        """Функция отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс объекта Яблоко."""

    def __init__(self, color=APPLE_COLOR):
        self.body_color = color
        self.position = Apple.randomize_position()

    @staticmethod
    def randomize_position():
        """Функция определения случайных координат в игровом поле."""
        coord1 = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        coord2 = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return coord1, coord2

    def draw(self):
        """Отрисовка Яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_coords(self):
        """Взять коордиинаты яблока."""
        return self.position


class Snake(GameObject):
    """Класс объекта Змейка."""

    positions: list[tuple[int, int]]
    direction = tuple[int, int]
    next_direction: Optional[tuple[int, int]]
    body_color: tuple[int, int, int]
    init_position: tuple[int, int]
    last: Optional[tuple[int, int]]

    def __init__(self, init_position=INIT_POSITION):
        self.position = init_position
        self.positions = [self.position]
        self.direction = RIGHT
        self.body_color = (0, 255, 0)
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Функция обновления направлениядыижения Змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """Функция обновляет позицию змейки (координаты каждой секции)."""
        head_pos = self.get_head_position()
        headpos_grid = (head_pos[0] // GRID_SIZE,
                        head_pos[1] // GRID_SIZE)
        new_headpos_grid = ((headpos_grid[0] + self.direction[0])
                            % GRID_WIDTH,
                            (headpos_grid[1] + self.direction[1])
                            % GRID_HEIGHT)
        new_headpos = (new_headpos_grid[0] * GRID_SIZE,
                       new_headpos_grid[1] * GRID_SIZE)

        # Если произошло стокновение с яблоком.
        if new_headpos == apple.get_coords():
            self.positions = [new_headpos] + self.positions
            apple.position = apple.randomize_position()
            while apple.position in self.positions:
                apple.position = apple.randomize_position()
            apple.draw()
            self.last = None

        #  Если произошло стокновение со своим хвостом.
        elif new_headpos in self.positions[1:]:
            self.clean_snake()
            self.direction = RIGHT
            self.next_direction = None
            self.last = None
            self.reset()

        # Нет стокновения с яблоком и своим хвостом.
        else:
            self.last = self.positions[-1]
            self.positions = [new_headpos] + self.positions[:-1]

    def clean_snake(self):
        """Стирание змейки с экрана."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)

    def draw(self):
        """Отрисовка Змейки."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента хвоста.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN


def main():
    """Функция реализации логики игры"""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов.
    snake = Snake(INIT_POSITION)
    apple = Apple(APPLE_COLOR)

    # Прорисовка объектов.
    snake.draw()
    apple.draw()

    # Отображение объектов на игровом поле.
    pygame.display.update()

    # Цикл обработки событий игры.
    while True:
        clock.tick(SPEED)

        # Основная логика игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
