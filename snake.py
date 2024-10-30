import pygame
import sys
import random

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width // 2), (screen_height // 2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (0, 255, 0)  # Bright green for all segments
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + (x * gridsize), cur[1] + (y * gridsize))

        # Check for collision with the edges
        if new[0] < 0 or new[0] >= screen_width or new[1] < 0 or new[1] >= screen_height:
            self.reset()
        elif len(self.positions) > 2 and new in self.positions[2:]:  # Check for collision with itself
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width // 2), (screen_height // 2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.circle(surface, self.color, (int(p[0] + gridsize // 2), int(p[1] + gridsize // 2)), gridsize // 2)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.position[0] + gridsize // 2, self.position[1] + gridsize // 2), gridsize // 2)

def drawGrid(surface):
    surface.fill((0, 0, 0))  # Set background to black

screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width // gridsize
grid_height = screen_height // gridsize

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace", 16)

    while True:
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(snake.score), 1, (255, 255, 255))
        screen.blit(text, (5, 10))
        pygame.display.update()

main()
