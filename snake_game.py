import pygame
import enum
import collections
import random

BLOCK_SIZE = 20
SPEED = 10
blue1 = (0, 0, 255)
blue2 = (0, 100, 255)
red = (255, 0, 0)

Point = collections.namedtuple("Point", ["x", "y"])

class Direction(enum.Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Snake_Game():
    def __init__(self, w = 640, h = 400):
        pygame.init() #initialize pygame
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h)) #This creates game window
        self.Direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.w/2 - BLOCK_SIZE, self.h/2), Point(self.w/2 - 2 *BLOCK_SIZE, self.h/2)]
        self.score = 0
        self.food = None
        self.place_food()

    def place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE))
        y = random.randint(0, (self.h - BLOCK_SIZE))
        self.food = Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT :
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        self.head = Point(x, y)
    
    def draw(self):
        self.display.fill((0, 0, 0))
        for i in self.snake:
            pygame.draw.rect(self.display, blue1, (i.x, i.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, blue2, (i.x + 4 , i.y + 4 , 12, 12))
        pygame.draw.rect(self.display, red, (self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        font = pygame.font.Font(None, 36)
        score = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.display.blit(score, (10, 10))
        pygame.display.update() 
    
    def update_snake(self):
        if abs(self.head.x - self.food.x) < BLOCK_SIZE and abs(self.head.y - self.food.y) < BLOCK_SIZE:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

    def is_collision(self):
        if (self.head.x >= self.w or self.head.x < 0 or self.head.y >= self.h or self.head.y < 0):
            return True
        elif self.head in self.snake[1:]:
            return True
        return False
    
    def run_game(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    running = False
                elif i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_LEFT and self.Direction != Direction.RIGHT:
                        self.Direction = Direction.LEFT
                    elif i.key == pygame.K_RIGHT and self.Direction != Direction.LEFT:
                        self.Direction = Direction.RIGHT
                    elif i.key == pygame.K_UP and self.Direction != Direction.DOWN:
                        self.Direction = Direction.UP
                    elif i.key == pygame.K_DOWN and self.Direction != Direction.UP:
                        self.Direction = Direction.DOWN

            self.move(self.Direction)
            self.snake.insert(0, self.head)
            self.update_snake()
            self.draw()

            if self.is_collision() == True:
                break
            clock.tick(SPEED)

if __name__ == "__main__":
    object = Snake_Game()
    object.run_game()
