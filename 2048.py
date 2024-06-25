import pygame
import random

H = 600
W = H
GRIDSIZE = 4
SQSIZE = H / GRIDSIZE
SQOFFSET = 3

COLORLIST = {
    2: (238, 230, 219),
    4: (236, 224, 200),
    8: (239, 178, 124),
    16: (243, 151, 104),
    32: (242, 125, 98),
    64: (244, 96, 66),
    128: (234, 207, 118),
    256: (237, 203, 103),
    512: (236, 200, 90),
    1024: (231, 194, 87),
    2048: (232, 190, 78)
}

pygame.init()

running = True
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Cooper Black', 48)

class Tile:
    def __init__(self, value, x, y):
        self.x = (x * SQSIZE) + SQOFFSET
        self.y = (y * SQSIZE) + SQOFFSET
        self.h = SQSIZE - (2*SQOFFSET)
        self.w = self.h
        self.value = value
        self.rect = pygame.Rect(self.x, self.y, SQSIZE, SQSIZE)
        self.color = COLORLIST.get(self.value, COLORLIST[2048])
        self.alreadyMerged = False
    
    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, self.color, self.rect, 0, 5)
        self.color = COLORLIST.get(self.value, COLORLIST[2048])
        self.text = font.render(str(self.value), 1, "black" if self.value < 8 else "white")
        self.textw, self.texth = font.size(str(self.value))
        self.xoffset, self.yoffset = (self.w-self.textw) // 2, (self.h-self.texth) // 2
        screen.blit(self.text, [self.x + self.xoffset, self.y + self.yoffset])
    
    def move(self, row, col):
        self.x = (row * SQSIZE) + SQOFFSET
        self.y = (col * SQSIZE) + SQOFFSET

    def double(self):
        self.value *= 2
        self.alreadyMerged = True

def startGame():     
    tiles = [[None for _ in range(GRIDSIZE)] for _ in range(GRIDSIZE)]
    randx = random.randint(0, GRIDSIZE-1)
    randy = random.randint(0, GRIDSIZE-1)
    randval = random.choice([2, 2, 2, 2, 2, 2, 2, 4])
    tiles[randy][randx] = Tile(randval, randx, randy)
    return tiles

def move(dir, tiles):
    boardChanged = False
    if dir == "up":
        # For each column
        for col in range(GRIDSIZE):
            # For each cell except the topmost cell
            for cell in range(1, GRIDSIZE):
                if tiles[cell][col] is not None:
                    foundTileAt = None
                    # For each cell between the top row and the cell
                    for nextSpace in range(cell - 1, -1, -1):
                        if tiles[nextSpace][col] is not None and tiles[cell][col] is not None and foundTileAt == None:
                            foundTileAt = nextSpace
                            if tiles[nextSpace][col].value == tiles[cell][col].value and not tiles[nextSpace][col].alreadyMerged:
                                tiles[nextSpace][col].double()
                                tiles[cell][col] = None
                                boardChanged = True
                                break
                            elif nextSpace + 1 != cell:
                                tiles[cell][col].move(col, nextSpace+1) 
                                tiles[nextSpace+1][col] = tiles[cell][col]
                                tiles[cell][col] = None
                                boardChanged = True

                    if foundTileAt == None and tiles[0][col] == None:
                        tiles[cell][col].move(col, 0)
                        tiles[0][col] = tiles[cell][col]
                        tiles[cell][col] = None
                        boardChanged = True
    
    if dir == "down":
        # For each column
        for col in range(GRIDSIZE):
            # For each cell except the bottom most cell
            for cell in range(GRIDSIZE - 2, -1, -1):
                if tiles[cell][col] is not None:
                    foundTileAt = None
                    # For each cell between the bottom row and the cell
                    for nextSpace in range(cell + 1, GRIDSIZE):
                        if tiles[nextSpace][col] is not None and tiles[cell][col] is not None and foundTileAt == None:
                            foundTileAt = nextSpace
                            if tiles[nextSpace][col].value == tiles[cell][col].value and not tiles[nextSpace][col].alreadyMerged:
                                tiles[nextSpace][col].double()
                                tiles[cell][col] = None
                                boardChanged = True
                                break
                            elif nextSpace - 1 != cell:
                                tiles[cell][col].move(col, nextSpace-1) 
                                tiles[nextSpace-1][col] = tiles[cell][col]
                                tiles[cell][col] = None
                                boardChanged = True

                    if foundTileAt == None and tiles[GRIDSIZE-1][col] == None:
                        tiles[cell][col].move(col, GRIDSIZE-1)
                        tiles[-1][col] = tiles[cell][col]
                        tiles[cell][col] = None
                        boardChanged = True

    if dir == "left":
        # For each row
        for row in range(GRIDSIZE):
            # For each cell except the leftmost cell
            for cell in range(1, GRIDSIZE):
                if tiles[row][cell] is not None:
                    foundTileAt = None
                    # For each cell between the left column and the cell
                    for nextSpace in range(cell - 1, -1, -1):
                        if tiles[row][nextSpace] is not None and tiles[row][cell] is not None and foundTileAt == None:
                            foundTileAt = nextSpace
                            if tiles[row][nextSpace].value == tiles[row][cell].value and not tiles[row][nextSpace].alreadyMerged:
                                tiles[row][nextSpace].double()
                                tiles[row][cell] = None
                                boardChanged = True
                                break
                            elif nextSpace + 1 != cell:
                                tiles[row][cell].move(nextSpace+1, row) 
                                tiles[row][nextSpace+1] = tiles[row][cell]
                                tiles[row][cell] = None
                                boardChanged = True

                    if foundTileAt == None and tiles[row][0] == None:
                        tiles[row][cell].move(0, row)
                        tiles[row][0] = tiles[row][cell]
                        tiles[row][cell] = None
                        boardChanged = True

    if dir == "right":
        # For each row
        for row in range(GRIDSIZE):
            # For each cell except the rightmost cell
            for cell in range(GRIDSIZE - 2, -1, -1):
                if tiles[row][cell] is not None:
                    foundTileAt = None
                    # For each cell between the right column and the cell
                    for nextSpace in range(cell + 1, GRIDSIZE):
                        if tiles[row][nextSpace] is not None and tiles[row][cell] is not None and foundTileAt == None:
                            foundTileAt = nextSpace
                            if tiles[row][nextSpace].value == tiles[row][cell].value and not tiles[row][nextSpace].alreadyMerged:
                                tiles[row][nextSpace].double()
                                tiles[row][cell] = None
                                boardChanged = True
                                break
                            elif nextSpace - 1 != cell:
                                tiles[row][cell].move(nextSpace-1, row) 
                                tiles[row][nextSpace-1] = tiles[row][cell]
                                tiles[row][cell] = None
                                boardChanged = True

                    if foundTileAt == None and tiles[row][-1] == None:
                        tiles[row][cell].move(GRIDSIZE-1, row)
                        tiles[row][-1] = tiles[row][cell]
                        tiles[row][cell] = None
                        boardChanged = True

    if boardChanged:
        createRandom()
    
    for row in tiles:
        for cell in row:
            try:
                cell.alreadyMerged = False
            except AttributeError:
                continue


def createRandom():
    while True:
        randx = random.randint(0, GRIDSIZE-1)
        randy = random.randint(0, GRIDSIZE-1)
        randval = random.choice([2, 2, 2, 4])
        if tiles[randy][randx] == None:
            tiles[randy][randx] = Tile(randval, randx, randy)
            break

backgroundGrid = []
for i in range(GRIDSIZE):
    row = []
    for j in range(GRIDSIZE):
        x = (j * SQSIZE) + SQOFFSET # Make the squares slight smaller than the SQSIZE
        y = (i * SQSIZE) + SQOFFSET
        rect = pygame.Rect(x, y, SQSIZE - (2*SQOFFSET), SQSIZE - (2*SQOFFSET))
        row.append(rect)
    backgroundGrid.append(row)


tiles = startGame()

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                move("up", tiles)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                move("down", tiles)
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                move("left", tiles)
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                move("right", tiles)
            if event.key == pygame.K_r:
                tiles = startGame()
                
    screen.fill(("gray90"))
    for row in backgroundGrid:
        for cell in row:
            pygame.draw.rect(screen, "gray75", cell, 0, 5)
    
    for row in tiles:
        for cell in row:
            if cell != None:
                cell.draw()

    pygame.display.flip()