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
        self.largeImage = 'largeimage'

        #  Information Panel


    def run(self):
        while self.RUN == True:
            self.update()
            self.draw()

    def input(self):
        for row in self.CELLS:
            for item in row:
                if item['rectangle'].collidepoint(pygame.mouse.get_pos()):
                    if item['active']:
                        item['focus'] = True
                        focusAdjacentTiles(self.CELLS, item)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, row in enumerate(self.CELLS):
                        for j, col in enumerate(row):
                            if col['rectangle'].collidepoint(pygame.mouse.get_pos()):
                                if checkValidSelection(self.CELLS, col, i, j):
                                    clearAdjacentCells(self.CELLS, col, i, j)


    def update(self):
        self.input()

    def draw(self):
        self.gameScreen.fill((0, 0, 0))
        for row in self.CELLS:
            for item in row:
                if item['active']:
                    if item['focus']:
                        self.gameScreen.blit(item[self.largeImage], item['rectangle'].inflate(4, 4))
                    else:
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

def focusAdjacentTiles(grid, currentCell):
    focusCells = [currentCell]

    for cell in focusCells:
        xPos = cell['rectangle'][0] // 40
        yPos = (cell['rectangle'][1]) // 40
        if xPos != 0:
            if grid[xPos - 1][yPos]['value'] == cell['value'] and grid[xPos - 1][yPos] not in focusCells\
                and grid[xPos - 1][yPos]['active'] == cell['active']:
                focusCells.append(grid[xPos - 1][yPos])
        if xPos < len(grid) - 1:
            if grid[xPos + 1][yPos]['value'] == cell['value'] and grid[xPos + 1][yPos] not in focusCells\
                and grid[xPos + 1][yPos]['active'] == cell['active']:
                focusCells.append(grid[xPos + 1][yPos])
        if yPos != 0:
            if grid[xPos][yPos - 1]['value'] == cell['value'] and grid[xPos][yPos - 1] not in focusCells\
                and grid[xPos][yPos - 1]['active'] == cell['active']:
                focusCells.append(grid[xPos][yPos - 1])
        if yPos < len(grid[0]) - 1:
            if grid[xPos][yPos + 1]['value'] == cell['value'] and grid[xPos][yPos + 1] not in focusCells\
                and grid[xPos][yPos + 1]['active'] == cell['active']:
                focusCells.append(grid[xPos][yPos + 1])

    for row in grid:
        for item in row:
            if item in focusCells and len(focusCells) > 1:
                item['focus'] = True
            else:
                item['focus'] = False

    return focusCells

def clearAdjacentCells(grid, cell, x, y):
    cell['active'] = False
    current = grid[x][y]
    if x > 0:
        north = grid[x - 1][y]
        if current['value'] == north['value'] and north['active'] == True:
            north['active'] = False
            clearAdjacentCells(grid, north, x-1, y)
    if x <len(grid) - 1:
        south = grid[x + 1][y]
        if current['value'] == south['value'] and south['active'] == True:
            south['active'] = False
            clearAdjacentCells(grid, south, x + 1, y)
    if y > 0:
        west = grid[x][y - 1]
        if current['value'] == west['value'] and west['active'] == True:
            west['active'] = False
            clearAdjacentCells(grid, west, x, y - 1)
    if y <len(grid[0]) - 1:
        east = grid[x][y + 1]
        if current['value'] == east['value'] and east['active'] == True:
            east['active'] = False
            clearAdjacentCells(grid, east, x, y + 1)

def checkValidSelection(grid, cell, i, j):
    if i > 0:
        if grid[i - 1][j]['value'] == cell['value'] and grid[i - 1][j]['active'] == cell['active'] and cell['active']:
            return True
    if i < len(grid) - 1:
        if grid[i + 1][j]['value'] == cell['value'] and grid[i + 1][j]['active'] == cell['active'] and cell['active']:
            return True
    if j > 0:
        if grid[i][j - 1]['value'] == cell['value'] and grid[i][j - 1]['active'] == cell['active'] and cell['active']:
            return True
    if j < len(grid[0]) - 1:
        if grid[i][j + 1]['value'] == cell['value'] and grid[i][j + 1]['active'] == cell['active'] and cell['active']:
            return True
    return False


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