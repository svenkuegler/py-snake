import pygame, time
from pygame.locals import *

# ----------------------------------------------------------------

WINDOW_SIZE_WIDTH=1200
WINDOW_SIZE_HEIGTH=800
TILE_SIZE=40
DEFAULT_LENGTH=3

# ----------------------------------------------------------------
class BorderColisionError(Exception):
    def __init__(self) -> None:
        super().__init__(self)

# ----------------------------------------------------------------
class Apple():
    """
    Apple Class
    """
    def __init__(self) -> None:
        pass

# ----------------------------------------------------------------
class Snake():
    """"
    Snake Class
    """
    def __init__(self, window, length) -> None:
        self.window = window
        self.length = length
        self.direction = 'down'
        self.x = [40]*length
        self.y = [40]*length
        self.tile = pygame.image.load("resources/tile.png").convert()

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"
    
    def check_border(self):
        if (self.x[0] + TILE_SIZE) == WINDOW_SIZE_WIDTH or self.x[0] == 0:
            raise BorderColisionError

        if (self.y[0] + TILE_SIZE) == WINDOW_SIZE_HEIGTH or self.y[0] == 0:
            raise BorderColisionError

    def walk(self):
        self.check_border()

        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= TILE_SIZE
        if self.direction == 'right':
            self.x[0] += TILE_SIZE
        if self.direction == 'up':
            self.y[0] -= TILE_SIZE
        if self.direction == 'down':
            self.y[0] += TILE_SIZE

        self.draw()

    def draw(self):
        self.window.fill((110, 110, 5))

        for i in range(self.length):
            self.window.blit(self.tile, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def reset(self):
        self.direction = "down"
        self.length = DEFAULT_LENGTH
        self.x = [40]*self.length
        self.y = [40]*self.length

# ----------------------------------------------------------------
class Game():
    """
    Main Game Class
    """
    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGTH))
        self.snake = Snake(self.window, DEFAULT_LENGTH)
        self.snake.draw()

    def game_over(self):
        text = pygame.font.Font(None, 64)
        m = text.render("Game Over",True,(0,0,0))
        self.window.blit(m, (200, 200))
        pygame.display.flip()
    
    def reset(self):
        self.snake.reset()
        self.play()

    def play(self):
        self.snake.walk()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                    
                    if event.key == K_n:
                        self.reset()

                    if event.key == K_ESCAPE:
                        running=False

                elif event.type == QUIT:
                    running=False
            
            try:
                self.play()
            except BorderColisionError as e:
                self.game_over()
            
            time.sleep(.2)
            

# ----------------------------------------------------------------
if __name__ == '__main__':
    game = Game()
    game.run()