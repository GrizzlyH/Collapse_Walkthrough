#  Import Modules
import pygame
import sys
from random import randint

#  Game Objects
class Game:
    def __init__(self, sw, sh, cS):

        #  Game Settings
        self.S_Width = sw
        self.S_Height = sh
        self.cellSize = cS

        #  Setup
        pygame.init()
        self.gameScreen = pygame.display.set_mode((self.S_Width, self.S_Height))
        pygame.display.set_caption("Collapse")
        self.CELLIMAGES = [createImage(num, self.cellSize) for num in range(1, 6)]

        #  Buttons Setup

        #  Game Groups
        self.numRows = (self.S_Width)//self.cellSize
        self.numCols = (self.S_Height)//self.cellSize
        self.CELLS = createCellGrid(self.numRows, self.numCols, self.cellSize, self)

        #  Game loop
        self.RUN = True
        self.image = 'image'

        #  Information Panel


    def run(self):
        while self.RUN == True:
            self.update()
            self.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False


    def update(self):
        self.input()

    def draw(self):
        self.gameScreen.fill((0, 0, 0))
        for row in self.CELLS:
            for item in row:
                self.gameScreen.blit(item[self.image], item['rectangle'])
        pygame.display.update()


#  Game utility Functions
def createImage(num, cellsize):
    colors = {1: 'Green', 2: 'Red', 3: 'Blue', 4: 'Yellow', 5: 'Purple'}
    cell = pygame.Surface((cellsize, cellsize))
    cell.fill(colors[num])
    pygame.draw.rect(cell, 'Black', (0, 0, cellsize, cellsize), 1)
    return cell

def createCellGrid(rows, cols, cellSize, mainGame):
    """Generates a list of lists, which contains all of the cell information per cell"""
    grid = []
    for row in range(rows):
        line = []
        for col in range(cols):
            value = randint(1, 5)
            line.append(
                {'value': value,
                 'image': mainGame.CELLIMAGES[value-1],
                 'largeimage': pygame.transform.scale(mainGame.CELLIMAGES[value-1], (45, 45)),
                 'rectangle': pygame.Rect(row * cellSize, (col * cellSize), cellSize, cellSize),
                 'focus': False,
                 'active': True}
            )
        grid.append(line)
    return grid

#  Game Variables / Settings
screenWidth = 1280
screenHeight = 960
cellSize = 40

#   Main Game
if __name__ == '__main__':
    game = Game(screenWidth, screenHeight, cellSize)
    game.run()
    pygame.quit()
    sys.exit()