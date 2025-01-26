from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
ROUNDING = GRID_SIZE // 5

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (190, 202, 14)
BORDER_COLOR = (133, 141, 4)
APPLE_COLOR = (235, 51, 36)
SNAKE_COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс для всех объектов игры."""

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Рисует объект на экране."""
        raise NotImplementedError('метод draw не реализован')


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(
        self, position=SCREEN_CENTER,
        body_color=APPLE_COLOR,
        occupied_positions=None
    ):
        super().__init__(position, body_color)
        if occupied_positions is None:
            occupied_positions = []
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Задает случайное положение яблока, избегая занятых позиций."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Рисует яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(
            screen, self.body_color, rect, border_radius=ROUNDING
        )
        pg.draw.rect(
            screen, BORDER_COLOR, rect, 1, border_radius=ROUNDING
        )


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку, обрабатывает появление с другой стороны."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        # Добавляем новую голову и удаляем последний сегмент
        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

    def grow(self):
        """Добавляет сегмент к змейке."""
        self.positions.append(self.last)

    def check_collision(self):
        """Проверяет столкновение с телом."""
        # Столкновение с телом
        return self.get_head_position() in self.positions[3:]

    def draw(self):
        """Рисует змейку на экране."""
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(
                screen, self.body_color, rect, border_radius=ROUNDING
            )
            pg.draw.rect(
                screen, BORDER_COLOR, rect, 1, border_radius=ROUNDING
            )

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.direction = self.direction

    def update_direction(self, new_direction):
        """Обновляет направление змейки"""
        if new_direction != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основной игровой цикл."""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Обработка ввода
        handle_keys(snake)

        # Движение змейки
        snake.move()

        # Проверка столкновений
        if snake.check_collision():
            snake.reset()
            apple.randomize_position(snake.positions)

        # Проверка на съедание яблока
        elif snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        # Рисование объектов
        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
