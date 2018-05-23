import pygame
import pygame.locals
import numpy as np

class Board(object):
    def __init__(self, width, height):
        """
        Initiate main board of the game
        """
        self.surface = pygame.display.set_mode((width,height), pygame.NOFRAME)
        pygame.display.set_caption("Conway's Game of Life")

    def draw(self, *args):
        """
        Draw all arguments to the board
        """
        background = (0, 0, 0)
        self.surface.fill(background)
        for drawable in args:
            drawable.draw_on(self.surface)
        pygame.display.update()

class Game(object):
    """
    Game handling function, it initiates the main surface, clock and the population
    It contains the main game loop and handles events
    """
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.board = Board(width, height)
        self.fps_clock = pygame.time.Clock()
        self.population = Population(8, width, height)

    def run(self):
        """
        At the start it generates 2 blink puffers and a bi-gun,
        next it starts a main game loop and let it live by itself
        """
        self.population.draw_blinkpuffer1(10,10,0)
        self.population.draw_blinkpuffer1(100,190,1)
        self.population.draw_bi_gun(50, 75)
        while not self.handle_events():
            self.population.next_gen()
            self.board.draw(self.population)
            self.fps_clock.tick(60)

    def handle_events(self):
        """
        Available events are:
        window close,
        space to generate random population,
        f10 for fullscreen
        """
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True
            elif event.type is pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.population.ppl = self.population.rand_gen(0.1)
            elif event.type is pygame.KEYDOWN and event.key == pygame.K_F10:
                if self.board.surface.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode((self.width, self.height))
                else:
                    pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

class Population:
    def __init__(self, size, width, height):
        """
        Initiates a population with all cells dead
        """
        self.size = size
        self.cols = width // size
        self.rows = height // size
        self.ppl = [ [False for x in range(self.cols)] for y in range(self.rows)]

    def gen_alive(self):
        """
        Simple generator which yields alive cells
        """
        for y in range(self.cols):
            for x in range(self.rows):
                if  self.ppl[x][y] == True:
                    yield (x, y)

    def neighbourhood(self, x, y):
        """
        returns amount of living neighbours of given cell
        """
        amount = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i > 0 and i < self.rows and j > 0 and j < self.cols:
                    if (i != x or j != y) and self.ppl[i][j]:
                        amount += 1
        return amount
                
    def next_gen(self):
        """
        Creates next generation based on previous one
        """
        next_ppl = self.empty_gen()
        for y in range(self.cols):
            for x in range(self.rows):
                if self.ppl[x][y] == False and self.neighbourhood(x, y) == 3 :
                    next_ppl[x][y] = True
                elif self.ppl[x][y] == True and (self.neighbourhood(x, y) == 2 or self.neighbourhood(x, y) == 3):
                    next_ppl[x][y] = True
        self.ppl = next_ppl
    
    def empty_gen(self):
        """
        Create an empty gen
        """
        gen = [ [False for x in range(self.cols)] for y in range(self.rows)]
        return gen
    
    def rand_gen(self, n):
        """
        Creates a random generation with a given chance of a cell being alive, it takes 0 to 1 values, higher doesnt affect
        something like 0.05 would be optimal as a parameter
        """
        gen = [[np.random.rand() < n for x in range(self.cols)]for y in range(self.rows)]
        return gen
    
    """
    Some predefined structures
    """
    def draw_blinkpuffer1(self, x, y, rot):
        i = [2,3,4,9 ,1,4,8,9,10, 4,8,10,11,15,16,17, 0,4,9,10,11,14,17, 4,9,10,17, 1,3,9,13,17, 13,17, 17, 14,16 ]
        j = [0,0,0,0, 1,1,1,1,1, 2,2,2,2,2,2,2, 3,3,3,3,3,3,3, 4,4,4,4, 5,5,5,5,5, 6,6, 7, 8,8 ]
        if rot == 0:
            for n, m in zip(i, j):
                self.ppl[x+n][y-m] = True
        elif rot == 1:
            for n, m in zip(i, j):
                self.ppl[x-n][y+m] = True
    
    def draw_timebomb(self, x, y, rot = 0):
        i = [1, 0, 1,3,4, 4,5, 3, 1,2, 3, 4, 2,3, 0, 0,1]
        j = [0, 1, 2,2,2, 3,3, 5, 7,7, 9, 10, 12,12, 13, 14,14]

        if rot == 0:
            for n, m in zip(i, j):
                self.ppl[x+n][y+m] = True
        elif rot == 1:
            for n, m in zip(i, j):
                self.ppl[x-n][y+m] = True

    def draw_bi_gun(self, x, y):
        i = [8,9, 8,9, 2,8, 1,2,3,7,8,9, 0,1,3,7,9,10, 3,7, 3,7, 7,11, 7,11, 4,5,7,11,13,14, 5,6,7,11,12,13, 6,12, 5,6, 5,6]
        j = [0,0, 1,1, 9,9, 10,10,10,10,10,10, 11,11,11,11,11,11, 14,14, 15,15, 34,34, 35,35, 38,38,38,38,38,38, 39,39,39,39,39,39, 40,40, 48,48, 49,49]
        for n, m in zip(i, j):
                self.ppl[x+n][y+m] = True

    def draw_queen_bee(self, x, y, rot):
        i = [0,1,5,6, 2,3,4, 1,5, 2,4, 3]
        j = [0,0,0,0, 1,1,1, 2,2, 3,3, 4]
        if rot == 0:
            for n, m in zip(i, j):
                    self.ppl[x-m][y+n] = True
        elif rot == 1:
            for n, m in zip(i, j):
                    self.ppl[x-n][y+m] = True
        elif rot == 2:
            for n, m in zip(i, j):
                    self.ppl[x+m][y+n] = True
        elif rot == 3:
            for n, m in zip(i, j):
                    self.ppl[x+n][y-m] = True
        
    def draw_on(self, surface):
        """
        Draws all living cells to the surfce
        """
        for x, y in self.gen_alive():
            size = (self.size-1, self.size-1)
            position = (y * self.size, x * self.size)
            color = (255, 255, 255)
            pygame.draw.rect(surface, color, (position, size), 1)
    
if __name__ == "__main__":
    game = Game(1600, 850)
    game.run()
