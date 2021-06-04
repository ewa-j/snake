import pygame, sys, random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(WIN, BLUE, block_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]


class FRUIT:
    def __init__(self):
        self.position_fruit()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(WIN, RED, fruit_rect)

    def position_fruit(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.checking_collision()
        self.checking_fail()

    def draw(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def checking_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.position_fruit()
            self.snake.add_block()

    def checking_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_score(self):
        score = 'Score: ' + str(len(self.snake.body) - 3)
        score_text = SCORE_FONT.render(score, True, RED)
        score_x = int(cell_size * cell_number - 50)
        score_y = int(cell_size * cell_number - 50)
        score_rect = score_text.get_rect(center = (score_x, score_y))
        WIN.blit(score_text, score_rect)

    def draw_grass(self):
        grass_color = (0, 128, 43)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(WIN, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(WIN, grass_color, grass_rect)


pygame.init()

cell_size = 40
cell_number = 20
WIDTH, HEIGHT = cell_size * cell_number, cell_size * cell_number
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE")
clock = pygame.time.Clock()
SCORE_FONT = pygame.font.SysFont('ComicSans', 25)

FPS = 60
GREEN = (51, 153, 51)
BLUE = (0, 102, 153)
RED = (153, 0, 0)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            # GOING UP
            if event.key == pygame.K_UP:
                #if going down I can't change direction to up
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            #GOING DOWN
            if event.key == pygame.K_DOWN:
                # if going up I can't change direction to down
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            #GOING LEFT
            if event.key == pygame.K_LEFT:
                # if going right I can't change direction to left
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            #GOING RIGHT
            if event.key == pygame.K_RIGHT:
                # if going left I can't change direction to right
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    WIN.fill(GREEN)
    main_game.draw()
    pygame.display.update()
    clock.tick(FPS)