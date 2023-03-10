#  Import Modules
import pygame
import sys
from random import randint

#  Game Objects
class Game:
    def __init__(self, sw, sh, cS, tS):

        #  Game Settings
        self.S_Width = sw
        self.S_Height = sh
        self.cellSize = cS
        self.topBar = 40
        self.gameOver = True
        self.buttons = []

        #  Setup
        pygame.init()
        self.gameScreen = pygame.display.set_mode((self.S_Width, self.S_Height))
        pygame.display.set_caption("Collapse")
        self.font = pygame.font.SysFont(' Arial', 22, True)
        self.CELLIMAGES = [createImage(num, self.cellSize) for num in range(1, 6)]
        self.CELLIMAGESNUMBERS = [createColorBlindImage(surf, num + 1, self.font) for num, surf in enumerate(self.CELLIMAGES)]
        self.newGameIconImage = infoPanel('New Game', 'Grey', 'Black', (100, 40))
        self.colorBlindButton = infoPanel('Color', 'Grey', 'Black', (60, 40))

        #  Buttons Setup
        self.newGameIconRect = self.newGameIconImage.get_rect(topleft=(1095, 0))
        self.buttons.append(self.newGameIconRect)
        self.colorBlindButtonRect = self.colorBlindButton.get_rect(topleft=(1200, 0))
        self.buttons.append(self.colorBlindButtonRect)

        #  Game Groups
        self.numRows = (self.S_Width)//self.cellSize
        self.numCols = (self.S_Height - self.topBar)//self.cellSize
        self.CELLS = createCellGrid(self.numRows, self.numCols, self.cellSize, self)

        #  Game loop
        self.RUN = True
        self.colorBlind = False
        self.image = 'image' if self.colorBlind == False else 'colorBlindImage'
        self.largeImage = 'largeimage' if self.colorBlind == False else 'largeColorBlindImage'

        #  Information Panel
        self.topScore = tS
        self.score = 0
        self.currentScore = 0
        self.possibleScore = 0
        self.colors = countColors(self.CELLS)
        self.colorScore = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    def run(self):
        while self.RUN == True:
            self.update()
            self.draw()

    def moveCells(self):
        for i, row in enumerate(self.CELLS):
            for j, col in enumerate(row):

                if j < len(self.CELLS[0]) - 1:
                    if self.CELLS[i][j + 1]['active'] == False:
                        self.CELLS[i][j + 1]['rectangle'], self.CELLS[i][j]['rectangle'] = \
                            self.CELLS[i][j]['rectangle'], self.CELLS[i][j + 1]['rectangle']
                        self.CELLS[i][j + 1], self.CELLS[i][j] = self.CELLS[i][j], self.CELLS[i][j + 1]

                if j == len(self.CELLS[0]) - 1 and self.CELLS[i][j]['active'] == False:
                    for r, row in enumerate(self.CELLS):
                        for c, cols in enumerate(row):
                            if r > i:
                                self.CELLS[r - 1][c]['rectangle'], self.CELLS[r][c]['rectangle'] = \
                                    self.CELLS[r][c]['rectangle'], self.CELLS[r - 1][c]['rectangle']
                                self.CELLS[r - 1][c], self.CELLS[r][c] = self.CELLS[r][c], self.CELLS[r - 1][c]

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
                    if not self.gameOver:
                        for i, row in enumerate(self.CELLS):
                            for j, col in enumerate(row):
                                if col['rectangle'].collidepoint(pygame.mouse.get_pos()):
                                    if checkValidSelection(self.CELLS, col, i, j):
                                        clearAdjacentCells(self.CELLS, col, i, j)
                                        self.score += self.currentScore
                                        self.colorScore[col['value']] += self.currentScore
                                        self.currentScore = 0
                                        self.colors = countColors(self.CELLS)
                        if self.buttons[0].collidepoint(pygame.mouse.get_pos()):
                            self.newGame()
                        if self.buttons[1].collidepoint(pygame.mouse.get_pos()):
                            if self.colorBlind:
                                self.colorBlind = False
                            else:
                                self.colorBlind = True
                    else:
                        if self.buttons[0].collidepoint(pygame.mouse.get_pos()):
                            self.newGame()

    def newGame(self):
        writeNewTopScore(self.topScore, self.score)
        self.score = 0
        self.colorScore = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.CELLS = createCellGrid(self.numRows, self.numCols, self.cellSize, self)
        self.colors = countColors(self.CELLS)
        self.infoPanels()
        self.update()
        self.gameOver = False
        self.draw()

    def update(self):
        self.input()
        self.moveCells()
        for row in self.CELLS:
            for item in row:
                if item['active'] == False:
                    item['value'] = 0
        if self.score > self.topScore:
            self.topScore = self.score
        self.gameOver = checkForGameOver(self.CELLS)
        self.image = 'image' if self.colorBlind == False else 'colorBlindImage'
        self.largeImage = 'largeimage' if self.colorBlind == False else 'largeColorBlindImage'

    def infoPanels(self):
        self.scoreImage = infoPanel(f'Score : {self.score}', 'Black', 'White')
        self.gameScreen.blit(self.scoreImage, (0, 0))
        self.topScoreImage = infoPanel(f'Best : {self.topScore}', 'Black', 'White')
        self.gameScreen.blit(self.topScoreImage, (155, 0))
        self.possibleScoreImage = infoPanel(f'Selection : {self.possibleScore}', 'Black', 'White')
        self.gameScreen.blit(self.possibleScoreImage, (310, 0))
        self.scoreImage = infoPanel(f'Score : {self.score}', 'Black', 'White')

        self.greenCellsImage = infoPanel(f'Green : {self.colors[0]}', 'Black', 'Green', (120, 40))
        self.gameScreen.blit(self.greenCellsImage, (465, 0))
        self.redCellsImage = infoPanel(f'Red : {self.colors[1]}', 'Black', 'Red', (120, 40))
        self.gameScreen.blit(self.redCellsImage, (590, 0))
        self.blueCellsImage = infoPanel(f'Blue : {self.colors[2]}', 'Black', 'Blue', (120, 40))
        self.gameScreen.blit(self.blueCellsImage, (715, 0))
        self.yellowCellsImage = infoPanel(f'Yellow : {self.colors[3]}', 'Black', 'Yellow', (120, 40))
        self.gameScreen.blit(self.yellowCellsImage, (840, 0))
        self.purpleCellsImage = infoPanel(f'Purple : {self.colors[4]}', 'Black', 'Purple', (120, 40))
        self.gameScreen.blit(self.purpleCellsImage, (975, 0))

        self.gameScreen.blit(self.newGameIconImage, self.newGameIconRect)
        self.gameScreen.blit(self.colorBlindButton, self.colorBlindButtonRect)

    def draw(self):
        self.gameScreen.fill((0, 0, 0))
        for row in self.CELLS:
            for item in row:
                if item['active']:
                    if item['focus']:
                        self.gameScreen.blit(item[self.largeImage], item['rectangle'].inflate(4, 4))
                    else:
                        self.gameScreen.blit(item[self.image], item['rectangle'])
        self.infoPanels()

        if self.gameOver:
            self.gameScreen.fill((0, 0, 0))
            endScreen = endGameScreen(self.gameScreen, self.colorScore)
            self.gameScreen.blit(endScreen, (self.gameScreen.get_width()//2 - endScreen.get_width()//2,
                                             self.gameScreen.get_height()//2 - endScreen.get_height()//2))
            self.gameScreen.blit(self.newGameIconImage, self.newGameIconRect)

        pygame.display.update()


#  Game utility Functions
def createImage(num, cellsize):
    colors = {1: 'Green', 2: 'Red', 3: 'Blue', 4: 'Yellow', 5: 'Purple'}
    cell = pygame.Surface((cellsize, cellsize))
    cell.fill(colors[num])
    pygame.draw.rect(cell, 'Black', (0, 0, cellsize, cellsize), 1)
    return cell

def createColorBlindImage(surf, num, font):
    newSurf = surf.copy()
    text = font.render(str(num), False, (0, 0, 0))
    textRect = text.get_rect(center=(newSurf.get_width()//2, newSurf.get_height()//2))
    newSurf.blit(text, textRect)
    return newSurf

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
                 'colorBlindImage': mainGame.CELLIMAGESNUMBERS[value - 1],
                 'largeColorBlindImage': pygame.transform.scale(mainGame.CELLIMAGESNUMBERS[value - 1], (45, 45)),
                 'rectangle': pygame.Rect(row * cellSize,40 + (col * cellSize), cellSize, cellSize),
                 'focus': False,
                 'active': True}
            )
        grid.append(line)
    return grid

def focusAdjacentTiles(grid, currentCell):
    focusCells = [currentCell]

    for cell in focusCells:
        xPos = cell['rectangle'][0] // 40
        yPos = (cell['rectangle'][1] - 40) // 40
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
    game.possibleScore = 0
    for num in range(len(focusCells)-1):
        game.possibleScore += calculateScore(game.possibleScore)

    return focusCells

def clearAdjacentCells(grid, cell, x, y):
    cell['active'] = False
    current = grid[x][y]
    if x > 0:
        north = grid[x - 1][y]
        if current['value'] == north['value'] and north['active'] == True:
            north['active'] = False
            game.currentScore += (calculateScore(game.currentScore))
            clearAdjacentCells(grid, north, x-1, y)
    if x <len(grid) - 1:
        south = grid[x + 1][y]
        if current['value'] == south['value'] and south['active'] == True:
            south['active'] = False
            game.currentScore += (calculateScore(game.currentScore))
            clearAdjacentCells(grid, south, x + 1, y)
    if y > 0:
        west = grid[x][y - 1]
        if current['value'] == west['value'] and west['active'] == True:
            west['active'] = False
            game.currentScore += (calculateScore(game.currentScore))
            clearAdjacentCells(grid, west, x, y - 1)
    if y <len(grid[0]) - 1:
        east = grid[x][y + 1]
        if current['value'] == east['value'] and east['active'] == True:
            east['active'] = False
            game.currentScore += (calculateScore(game.currentScore))
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

def infoPanel(message, bgColor, txtColor, size=(150, 40)):
    surf = pygame.Surface(size)
    surf.fill(bgColor)

    font = pygame.font.SysFont('Arial', 22, True)
    text = font.render(message, False, txtColor)
    textRect = text.get_rect(midleft=(5, surf.get_height()//2))
    surf.blit(text, textRect)
    return surf

def calculateScore(score):
    if score < 3: return 1
    elif score <= 6: return 2
    elif score <= 9: return 4
    elif score <= 12: return 8
    elif score <= 15: return 16
    elif score <= 18: return 32
    else: return 64

def countColors(grid):
    colorCount = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for row in grid:
        for item in row:
            if item['active']:
                colorCount[item['value']] += 1
    return [colorCount[1], colorCount[2], colorCount[3], colorCount[4], colorCount[5]]

def readTopScore():
    try:
        with open('TopScore.txt', 'r+') as file:
            a = file.read().split(' ')
            return int(a[2])
    except:
        return 0

def writeNewTopScore(TOPSCORE, TOTALSCORE):
    if TOTALSCORE >= TOPSCORE:
        with open('TopScore.txt', 'w') as file:
            file.write(f'Topscore = {str(TOTALSCORE)}')

def checkForGameOver(grid):
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if i != 0:
                if grid[i - 1][j]['value'] == grid[i][j]['value'] and grid[i - 1][j]['active'] == grid[i][j]['active'] and grid[i][j]['active']:
                    return False
            if i < len(grid) - 1:
                if grid[i + 1][j]['value'] == grid[i][j]['value'] and grid[i + 1][j]['active'] == grid[i][j]['active'] and grid[i][j]['active']:
                    return False
            if j != 0:
                if grid[i][j - 1]['value'] == grid[i][j]['value'] and grid[i][j - 1]['active'] == grid[i][j]['active'] and grid[i][j]['active']:
                    return False
            if j < len(grid[0]) - 1:
                if grid[i][j + 1]['value'] == grid[i][j]['value'] and grid[i][j + 1]['active'] == grid[i][j]['active'] and grid[i][j]['active']:
                    return False
    return True

def endGameScreen(gamescreen, cellColorScores):
    surf = pygame.Surface((400, 800))
    surf.fill('Grey')

    bestScore = infoPanel(f'Best Score: '.ljust(15, ' ') + f'{game.topScore}'.ljust(10, ' '), 'White', 'Black', (300, 50))
    bestScoreRect = bestScore.get_rect(topleft=(50, 50 + (surf.get_height() // 8) * 0))
    surf.blit(bestScore, bestScoreRect)

    Score = infoPanel(f'Score: '.ljust(15, ' ') + f'{game.score}'.ljust(10, ' '), 'Black', 'White', (300, 50))
    ScoreRect = Score.get_rect(topleft=(50, 50 + (surf.get_height() // 8) * 1))
    surf.blit(Score, ScoreRect)

    greenScore = infoPanel(f'Green Score: '.ljust(15, ' ') + f'{cellColorScores[1]}'.ljust(10, ' '), 'Green', 'Black', (300, 50))
    greenScoreRect = greenScore.get_rect(topleft=(50, 50 + (surf.get_height() // 8) * 2))
    surf.blit(greenScore, greenScoreRect)

    redScore = infoPanel(f'Red Score: '.ljust(15, ' ') + f'{cellColorScores[2]}'.ljust(10, ' '), 'Red', 'Black', (300, 50))
    redScoreRect = redScore.get_rect(topleft=(50, 50 + (surf.get_height() // 8) * 3))
    surf.blit(redScore, redScoreRect)

    blueScore = infoPanel(f'Blue Score: '.ljust(15, ' ') + f'{cellColorScores[3]}'.ljust(10, ' '), 'Blue', 'Black', (300, 50))
    blueScoreRect = blueScore.get_rect(topleft=(50, 50 + (surf.get_height() // 8) * 4))
    surf.blit(blueScore, blueScoreRect)

    yellowScore = infoPanel(f'Yellow Score: '.ljust(15, ' ') + f'{cellColorScores[4]}'.ljust(10, ' '), 'Yellow', 'Black', (300, 50))
    yellowScoreRect = yellowScore.get_rect(topleft=(50, 50 + (surf.get_height() // 8) * 5))
    surf.blit(yellowScore, yellowScoreRect)

    purpleScore = infoPanel(f'Purple Score: '.ljust(15, ' ') + f'{cellColorScores[5]}'.ljust(10, ' '), 'Purple', 'Black', (300, 50))
    purpleScoreRect = purpleScore.get_rect(topleft=(50, 50 + (surf.get_height() // 8) * 6))
    surf.blit(purpleScore, purpleScoreRect)
    return surf

#  Game Variables / Settings
screenWidth = 1280
screenHeight = 960
cellSize = 40

#   Main Game
if __name__ == '__main__':
    topScore = readTopScore()
    game = Game(screenWidth, screenHeight, cellSize, topScore)
    game.run()
    pygame.quit()
    sys.exit()