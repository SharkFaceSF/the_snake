from random import choice, randint

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

# Цвета:
BOARD_BACKGROUND_COLOR = (190, 202, 14)
BORDER_COLOR = (133, 141, 4)
APPLE_COLOR = (235, 51, 36)
SNAKE_COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс для всех объектов игры."""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Рисует объект на экране."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Задает случайное положение яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Рисует яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(
            screen, self.body_color, rect, border_radius=GRID_SIZE // 5
        )
        pygame.draw.rect(
            screen, BORDER_COLOR, rect, 1, border_radius=GRID_SIZE // 5
        )


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку, обрабатывает появление с другой стороны."""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.next_direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        # Добавляем новую голову и удаляем последний сегмент
        self.positions = [new_head] + self.positions[:-1]
        self.direction = self.next_direction

    def grow(self):
        """Добавляет сегмент к змейке."""
        self.positions.append(self.positions[-1])

    def check_collision(self):
        """Проверяет столкновение с телом."""
        # Столкновение с телом
        return self.positions[0] in self.positions[3:]

    def draw(self):
        """Рисует змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(
                screen, self.body_color, rect, border_radius=GRID_SIZE // 5
            )
            pygame.draw.rect(
                screen, BORDER_COLOR, rect, 1, border_radius=GRID_SIZE // 5
            )

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction

    def update_direction(self, new_direction):
        """Обновляет направление змейки"""
        if new_direction != (-self.direction[0], -self.direction[1]):
            self.next_direction = new_direction


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основной игровой цикл."""
    pygame.init()
    apple = Apple()
    snake = Snake()

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

        # Проверка на съедание яблока
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

        # Рисование объектов
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
