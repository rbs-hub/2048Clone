__author__ = 'Toni Ribas'

'''
A game clone based on the infamous 2048 game created by Gabriele Cirulli.
The official game: http://git.io/2048
'''

import pygame, sys, random, pickle
from pygame.locals import *

pygame.font.init()


# Global variables
fps         = 60
screen_size = (screen_width, screen_height) = (600, 700)
tile_number = 4
tile_size   = 100
pad_size    = 10

board_size  = (tile_number + 1)*pad_size + tile_number*tile_size
assert board_size < screen_width, 'Invalid dimension'

x_margin    = int((screen_width - board_size)/2)
y_margin    = int((screen_height - board_size)/2)

default_fontname    = 'ubuntu'
default_fgcolor     = (121,110,101)
default_bgcolor     = (251,248,239)
default_fontsize    = 20

board_bgcolor = (191,172,160)

tilebgcolor   = {
    0    : (208,191,180),
    2    : (241,228,218),
    4    : (241,223,200),
    8    : (255,174,117),
    16   : (255,144,92),
    32   : (255,116,85),
    64   : (255,81,35),
    128  : (245,206,114),
    256  : (246,203,96),
    512  : (255,196,73),
    1024 : (247,195,61),
    2048 : (255,190,39),
    4098 : (255,44,0),
    81992: (0,179,167),
    16384: (0,179,167),
    32768: (0,179,167),
    65536: (0,179,167)
    }

tilefontsize = {
    2    : 55,
    4    : 55,
    8    : 55,
    16   : 50,
    32   : 50,
    64   : 50,
    128  : 45,
    256  : 45,
    512  : 45,
    1024 : 35,
    2048 : 35,
    4098 : 35,
    81992: 30,
    16384: 30,
    32768: 30,
    65536: 30
    }

tilefontcolor = {
    2    : (121,110,101),
    4    : (121,110,101),
    8    : (250,246,242),
    16   : (250,246,242),
    32   : (250,246,242),
    64   : (250,246,242),
    128  : (250,246,242),
    256  : (250,246,242),
    512  : (250,246,242),
    1024 : (250,246,242),
    2048 : (250,246,242),
    4098 : (250,246,242),
    81992: (250,246,242),
    16384: (250,246,242),
    32768: (250,246,242),
    65536: (250,246,242)
    }

''' Direction '''
UP    = 'up'
DOWN  = 'down'
LEFT  = 'left'
RIGHT = 'right'


def main():
    global screen, score, hscore
    pygame.init()
    pygame.display.set_caption('2048')
    screen  = pygame.display.set_mode(screen_size)
    
    # load savegame file if existed
    try:
        with open('savegame', 'rb') as f:
            score, hscore, board = pickle.load(f)

    # create new savegame file if not existed
    except FileNotFoundError:
        score = 0
        hscore = 0
        board = [[0 for _ in range(tile_number)] for _ in range(tile_number)]
        board = getNewNumber(board, True)
        with open('savegame', 'wb') as f:
            pickle.dump([score, hscore, board], f)
    
    message  = 'Press (left, right, up, or down) arrow keys to slide'
    drawScreen(board, score, message)
    
    # main game loop
    while True:
        direction   = None
        # event handling loop for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                if score > hscore: hscore = score
                with open('savegame', 'wb') as f:
                    pickle.dump([score, hscore, board], f)
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button ==1:
                    if newgame_rect.collidepoint(event.pos):
                        if score > hscore: hscore = score
                        board   = [[0 for _ in range(tile_number)] for _ in range(tile_number)]
                        board   = getNewNumber(board, True)
                        score   = 0
                        message = 'New game created...'
                        drawScreen(board, score, message)

            elif event.type == KEYUP:
                if event.key == K_UP:
                    if checkIfMoveValid(board, UP):
                        direction = UP
                        message = f'last move: {direction}'

                elif event.key == K_DOWN:
                    if checkIfMoveValid(board, DOWN):
                        direction = DOWN
                        message = f'last move: {direction}'

                elif event.key == K_LEFT:
                    if checkIfMoveValid(board, LEFT):
                        direction = LEFT
                        message = f'last move: {direction}'

                elif event.key == K_RIGHT:
                    if checkIfMoveValid(board, RIGHT):
                        direction = RIGHT
                        message = f'last move: {direction}'

        # if the event handling produce
        if direction:
            board,temp = moveTiles(board, direction)
            getNewNumber(board, False)
            score+=temp
            drawScreen(board, score, message)

        # checking if the game is over
        if gameOver(board):
            game_over = createTextObject('Game over!', default_fontname, 80, default_fgcolor)
            game_over_rect = game_over.get_rect(center = (int(screen_width/2), int(screen_height/2)))
            screen.blit(game_over, game_over_rect)
            message = 'Click a new game to start a new game...'

        pygame.display.update()
        pygame.time.Clock().tick(fps) 


def createTextObject(text, fontname, fontsize, fgcolor, bgcolor=None, **option):
    font    = pygame.font.SysFont(fontname, fontsize, bold=True)
    img     = font.render(str(text), 2, fgcolor, bgcolor)

    return img.convert_alpha()


def gameOver(board):
    return not any(0 in _ for _ in board) and not \
        checkIfMoveValid(board, LEFT) and not \
            checkIfMoveValid(board, RIGHT) and not \
                checkIfMoveValid(board, UP) and not \
                    checkIfMoveValid(board, DOWN)


def gameWin(board):
    return 2048 in board


def getNewNumber(board, newGame):
    """ Generate two new numbers with value 2 or 4 """
    if newGame:
        newNumbers = random.choices([2,4],[15,1],k=2)
        temp    = []
        for x in range(tile_number):
            for y in range(tile_number):
                temp.append((x,y))
        a,b = (0,0)
        while a == b:
            a,b = random.choices(temp, k=2)
        board[a[0]][a[1]] = newNumbers[0]
        board[b[0]][b[1]] = newNumbers[1]
    else:
        if any(0 in _ for _ in board):
            newNumber = random.choices([2,4], [15,1], k=1)
            temp = []
            for row in range(tile_number):
                for col in range(tile_number):
                    if board[row][col] == 0:
                        temp.append((row, col))
            genPos = random.choice(temp)
            board[genPos[0]][genPos[1]] = newNumber[0]
        else:
            pass
    return board


def drawScreen(board, score, message):
    '''
        Updating and drawing the screen
    '''
    global newgame_rect

    screen.fill(default_bgcolor)
    newgame = createTextObject('New game', default_fontname, 20, default_fgcolor, default_bgcolor)
    newgame_rect = newgame.get_rect(bottomright=(screen_width-x_margin, y_margin-10))    

    screen.blit(newgame, newgame_rect)

    title       = createTextObject('2048', 'ubuntu', 100, default_fgcolor, None)
    titlerect   = title.get_rect(bottomleft=(x_margin, y_margin+10))
    screen.blit(title, titlerect)
       
    if message:
        messageimg = createTextObject(message, default_fontname, 12, (0,179,167), bgcolor=None)
        messagerect = messageimg.get_rect(midleft = (x_margin, y_margin+board_size+80))
        screen.blit(messageimg, messagerect)

    pygame.draw.rect(screen, board_bgcolor, (x_margin, y_margin, board_size, board_size))     
    for row in range(tile_number):
        center_y = y_margin + pad_size*(row + 1) + tile_size*row+50
        for col in range(tile_number):
            center_x = x_margin + pad_size*(col + 1) + tile_size*col+50
            tile_value = board[row][col]
            drawTile(row, col, center_x, center_y, tile_value)
    
    pygame.draw.rect(screen, (191,172,160), (screen_width-x_margin-100, y_margin-95, 100, 50))
    best = createTextObject('BEST', default_fontname, 16, (238,228,218))
    bestrect = best.get_rect(center=(screen_width-x_margin-50,y_margin-85))
    screen.blit(best, bestrect)
    
    hscorelabel = createTextObject(hscore, default_fontname, 20, (238,228,218))
    hscorelabelrect = hscorelabel.get_rect(center=(screen_width-x_margin-50,y_margin-63))
    screen.blit(hscorelabel, hscorelabelrect)


    pygame.draw.rect(screen, (191,172,160), (screen_width-x_margin-210, y_margin-95, 100, 50))
    scoreimg = createTextObject('SCORE', default_fontname, 16, (238,228,218))
    scorerect = scoreimg.get_rect(center=(screen_width-x_margin-160,y_margin-85))
    screen.blit(scoreimg, scorerect)

    scorelabel = createTextObject(score, default_fontname, 20, (238,228,218))
    scorelabelrect = scorelabel.get_rect(center=(screen_width-x_margin-160,y_margin-63))
    screen.blit(scorelabel, scorelabelrect)

    label1 = createTextObject('HOW TO PLAY: Use your arrow keys to move the tiles.', default_fontname, 14, default_fgcolor)
    label1_rect = label1.get_rect(topleft=(x_margin, y_margin + board_size + pad_size))
    screen.blit(label1, label1_rect)

    label2 = createTextObject('When two tiles with the same number touch, they merge into one!', default_fontname, 14, default_fgcolor)
    label2_rect = label2.get_rect(topleft=(x_margin, y_margin + board_size + pad_size+15))
    screen.blit(label2, label2_rect)

    label3 = createTextObject('Created by Toni based on 2048 by Gabriele Cirulli.', default_fontname, 19, default_fgcolor)
    label3_rect = label3.get_rect(topleft=(x_margin, y_margin + board_size + pad_size+30))
    screen.blit(label3, label3_rect)


def drawTile(x, y, center_x, center_y, number):
    pygame.draw.rect(screen, tilebgcolor[number], (center_x-50, center_y-50, tile_size, tile_size))
    if number != 0:
        tile    = createTextObject(str(number), default_fontname, tilefontsize[number], tilefontcolor[number], bgcolor=None)
        tilerect= tile.get_rect(center=(center_x, center_y))
        screen.blit(tile, tilerect)


def checkIfMoveValid(board, direction):
    ''' Checking if the the move direction is valid '''
    if board == moveTiles(board, direction)[0]:
        return False
    else:
        return True
  

def rowMoveLeft(row):
    ''' 
        Slide given row from right to left, ex: [2, 0, 0, 2] --> [4, 0, 0, 0].
        These method return new row and score for the action
    '''
    score=[]
    previous = -1
    counter  = 0
    tempRow  = [0 for _ in range(tile_number)]
    for element in row:
        if element != 0:
            if previous == -1:
                previous = element
                tempRow[counter] = element
                counter += 1
            
            elif previous == element:
                previous -= 1
                tempRow[counter-1] = 2*element
                score.append(2*element)
            
            else:
                previous = element
                tempRow[counter] = element
                counter += 1
    score=sum(_ for _ in score)
    return tempRow, score


def moveTiles(board, direction):
    """
        Slide the given board based on given direction (LEFT, RIGHT, UP, DOWN).\n
        These method return a new board and score.
    """
    score = []
    tempBoard = [[0 for _ in range(tile_number)] for _ in range(tile_number)]
    
    if direction == UP:
        for i in range(tile_number):
            row = []
            for j in range(tile_number):
                row.append(board[j][i])
            row,temp = rowMoveLeft(row)
            for j in range(tile_number):
                tempBoard[j][i]=row[j]
            score.append(temp)
        score=sum(_ for _ in score)

    elif direction == DOWN:
        for i in range(tile_number):
            row = []
            for j in reversed(range(tile_number)):
                row.append(board[j][i])

            row,temp = rowMoveLeft(row)
            for j in reversed(range(tile_number)):
                tempBoard[j][i]=row[tile_number - j - 1]
            score.append(temp)
        score=sum(_ for _ in score)

    elif direction == LEFT:
        for i in range(tile_number):
            tempBoard[i], temp = rowMoveLeft(board[i])
            score.append(temp)
        score=sum(_ for _ in score)

    elif direction == RIGHT:
        for i in range(tile_number):
            row = []
            for j in reversed(range(tile_number)):
                row.append(board[i][j])
            row,temp = rowMoveLeft(row)
            score.append(temp)

            for j in reversed(range(tile_number)):
                tempBoard[i][j] = row[tile_number - j -1]
        score=sum(_ for _ in score)

    return tempBoard, score   

if __name__ == "__main__":
=======
__author__ = 'Toni Ribas'

'''
A game clone based on the infamous 2048 game created by Gabriele Cirulli.
The official game: http://git.io/2048
'''

import pygame, sys, random, pickle
from pygame.locals import *


# Global variables
fps         = 60
screen_size = (screen_width, screen_height) = (600, 700)
tile_number = 4
tile_size   = 100
pad_size    = 10

board_size  = (tile_number + 1)*pad_size + tile_number*tile_size
assert board_size < screen_width, 'Invalid dimension'

x_margin    = int((screen_width - board_size)/2)
y_margin    = int((screen_height - board_size)/2)

default_fontname    = 'ubuntu'
default_fgcolor     = (121,110,101)
default_bgcolor     = (251,248,239)
default_fontsize    = 20

board_bgcolor = (191,172,160)

tilebgcolor   = {
    0    : (208,191,180),
    2    : (241,228,218),
    4    : (241,223,200),
    8    : (255,174,117),
    16   : (255,144,92),
    32   : (255,116,85),
    64   : (255,81,35),
    128  : (245,206,114),
    256  : (246,203,96),
    512  : (255,196,73),
    1024 : (247,195,61),
    2048 : (255,190,39),
    4098 : (255,44,0),
    81992: (0,179,167),
    16384: (0,179,167),
    32768: (0,179,167),
    65536: (0,179,167)
    }

tilefontsize = {
    2    : 55,
    4    : 55,
    8    : 55,
    16   : 50,
    32   : 50,
    64   : 50,
    128  : 45,
    256  : 45,
    512  : 45,
    1024 : 35,
    2048 : 35,
    4098 : 35,
    81992: 30,
    16384: 30,
    32768: 30,
    65536: 30
    }

tilefontcolor = {
    2    : (121,110,101),
    4    : (121,110,101),
    8    : (250,246,242),
    16   : (250,246,242),
    32   : (250,246,242),
    64   : (250,246,242),
    128  : (250,246,242),
    256  : (250,246,242),
    512  : (250,246,242),
    1024 : (250,246,242),
    2048 : (250,246,242),
    4098 : (250,246,242),
    81992: (250,246,242),
    16384: (250,246,242),
    32768: (250,246,242),
    65536: (250,246,242)
    }

''' Direction '''
UP    = 'up'
DOWN  = 'down'
LEFT  = 'left'
RIGHT = 'right'


def main():
    global screen, score, hscore
    pygame.font.init()

    pygame.init()
    pygame.display.set_caption('2048')
    screen  = pygame.display.set_mode(screen_size)
    
    ''' Initializing the game '''
    message  = 'Press (left, right, up, or down) arrow keys to slide'
    with open('savegame', 'rb') as f:
        score, hscore, board = pickle.load(f)
    drawScreen(board, score, message)
    
    ''' Game main loop '''
    while True:
        direction   = None
        ''' Event handling loop'''
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                if score > hscore: hscore = score
                with open('savegame', 'wb') as f:
                    pickle.dump([score, hscore, board], f)
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button ==1:
                    if newgame_rect.collidepoint(event.pos):
                        if score > hscore: hscore = score
                        board   = [[0 for _ in range(tile_number)] for _ in range(tile_number)]
                        board   = getNewNumber(board, True)
                        score   = 0
                        message = 'New game created...'
                        drawScreen(board, score, message)

            elif event.type == KEYUP:
                if event.key == K_UP:
                    if checkIfMoveValid(board, UP):
                        direction = UP
                        message = f'last move: {direction}'

                elif event.key == K_DOWN:
                    if checkIfMoveValid(board, DOWN):
                        direction = DOWN
                        message = f'last move: {direction}'

                elif event.key == K_LEFT:
                    if checkIfMoveValid(board, LEFT):
                        direction = LEFT
                        message = f'last move: {direction}'

                elif event.key == K_RIGHT:
                    if checkIfMoveValid(board, RIGHT):
                        direction = RIGHT
                        message = f'last move: {direction}'

        if direction:
            board,temp = moveTiles(board, direction)
            getNewNumber(board, False)
            score+=temp
            drawScreen(board, score, message)
    
        if gameOver(board):
            game_over = createTextObject('Game over!', default_fontname, 80, default_fgcolor)
            game_over_rect = game_over.get_rect(center = (int(screen_width/2), int(screen_height/2)))
            screen.blit(game_over, game_over_rect)
            message = 'Click a new game to start a new game...'

        pygame.display.update()
        pygame.time.Clock().tick(fps) 


def createTextObject(text, fontname, fontsize, fgcolor, bgcolor=None, **option):
    font    = pygame.font.SysFont(fontname, fontsize, bold=True)
    img     = font.render(str(text), 2, fgcolor, bgcolor)

    return img.convert_alpha()


def getCenterPos(x,y):
    center_x= x_margin + pad_size*(x + 1) + tile_size*x + 50
    center_y= y_margin + pad_size*(y + 1) + tile_size*y + 50
    
    return center_x, center_y


def gameOver(board):
    return not any(0 in _ for _ in board) and not \
        checkIfMoveValid(board, LEFT) and not \
            checkIfMoveValid(board, RIGHT) and not \
                checkIfMoveValid(board, UP) and not \
                    checkIfMoveValid(board, DOWN)


def gameWin(board):
    return 2048 in board


def getNewNumber(board, newGame):
    """ Generate two new numbers with value 2 or 4 """
    if newGame:
        newNumbers = random.choices([2,4],[15,1],k=2)
        temp    = []
        for x in range(tile_number):
            for y in range(tile_number):
                temp.append((x,y))
        a,b = (0,0)
        while a == b:
            a,b = random.choices(temp, k=2)
        board[a[0]][a[1]] = newNumbers[0]
        board[b[0]][b[1]] = newNumbers[1]
    else:
        if any(0 in _ for _ in board):
            newNumber = random.choices([2,4], [15,1], k=1)
            temp = []
            for row in range(tile_number):
                for col in range(tile_number):
                    if board[row][col] == 0:
                        temp.append((row, col))
            genPos = random.choice(temp)
            board[genPos[0]][genPos[1]] = newNumber[0]
        else:
            pass
    return board


def drawScreen(board, score, message):
    '''
        Updating and drawing the screen
    '''
    global newgame_rect

    screen.fill(default_bgcolor)
    newgame = createTextObject('New game', default_fontname, 20, default_fgcolor, default_bgcolor)
    newgame_rect = newgame.get_rect(bottomright=(screen_width-x_margin, y_margin-10))    

    screen.blit(newgame, newgame_rect)

    title       = createTextObject('2048', 'ubuntu', 100, default_fgcolor, None)
    titlerect   = title.get_rect(bottomleft=(x_margin, y_margin+10))
    screen.blit(title, titlerect)
       
    if message:
        messageimg = createTextObject(message, default_fontname, 12, (0,179,167), bgcolor=None)
        messagerect = messageimg.get_rect(midleft = (x_margin, y_margin+board_size+80))
        screen.blit(messageimg, messagerect)

    pygame.draw.rect(screen, board_bgcolor, (x_margin, y_margin, board_size, board_size))     
    for row in range(tile_number):
        center_y = y_margin + pad_size*(row + 1) + tile_size*row+50
        for col in range(tile_number):
            center_x = x_margin + pad_size*(col + 1) + tile_size*col+50
            tile_value = board[row][col]
            drawTile(row, col, center_x, center_y, tile_value)
    
    pygame.draw.rect(screen, (191,172,160), (screen_width-x_margin-100, y_margin-95, 100, 50))
    best = createTextObject('BEST', default_fontname, 16, (238,228,218))
    bestrect = best.get_rect(center=(screen_width-x_margin-50,y_margin-85))
    screen.blit(best, bestrect)
    
    hscorelabel = createTextObject(hscore, default_fontname, 20, (238,228,218))
    hscorelabelrect = hscorelabel.get_rect(center=(screen_width-x_margin-50,y_margin-63))
    screen.blit(hscorelabel, hscorelabelrect)


    pygame.draw.rect(screen, (191,172,160), (screen_width-x_margin-210, y_margin-95, 100, 50))
    scoreimg = createTextObject('SCORE', default_fontname, 16, (238,228,218))
    scorerect = scoreimg.get_rect(center=(screen_width-x_margin-160,y_margin-85))
    screen.blit(scoreimg, scorerect)

    scorelabel = createTextObject(score, default_fontname, 20, (238,228,218))
    scorelabelrect = scorelabel.get_rect(center=(screen_width-x_margin-160,y_margin-63))
    screen.blit(scorelabel, scorelabelrect)

    label1 = createTextObject('HOW TO PLAY: Use your arrow keys to move the tiles.', default_fontname, 14, default_fgcolor)
    label1_rect = label1.get_rect(topleft=(x_margin, y_margin + board_size + pad_size))
    screen.blit(label1, label1_rect)

    label2 = createTextObject('When two tiles with the same number touch, they merge into one!', default_fontname, 14, default_fgcolor)
    label2_rect = label2.get_rect(topleft=(x_margin, y_margin + board_size + pad_size+15))
    screen.blit(label2, label2_rect)

    label3 = createTextObject('Created by Toni based on 2048 by Gabriele Cirulli.', default_fontname, 19, default_fgcolor)
    label3_rect = label3.get_rect(topleft=(x_margin, y_margin + board_size + pad_size+30))
    screen.blit(label3, label3_rect)


def drawTile(x, y, center_x, center_y, number):
    pygame.draw.rect(screen, tilebgcolor[number], (center_x-50, center_y-50, tile_size, tile_size))
    if number != 0:
        tile    = createTextObject(str(number), default_fontname, tilefontsize[number], tilefontcolor[number], bgcolor=None)
        tilerect= tile.get_rect(center=(center_x, center_y))
        screen.blit(tile, tilerect)


def checkIfMoveValid(board, direction):
    ''' Checking if the the move direction is valid '''
    if board == moveTiles(board, direction)[0]:
        return False
    else:
        return True
  

def rowMoveLeft(row):
    ''' 
        Slide given row from right to left, ex: [2, 0, 0, 2] --> [4, 0, 0, 0].
        These method return new row and score for the action
    '''
    score=[]
    previous = -1
    counter  = 0
    tempRow  = [0 for _ in range(tile_number)]
    for element in row:
        if element != 0:
            if previous == -1:
                previous = element
                tempRow[counter] = element
                counter += 1
            
            elif previous == element:
                previous -= 1
                tempRow[counter-1] = 2*element
                score.append(2*element)
            
            else:
                previous = element
                tempRow[counter] = element
                counter += 1
    score=sum(_ for _ in score)
    return tempRow, score


def moveTiles(board, direction):
    """
        Slide the given board based on given direction (LEFT, RIGHT, UP, DOWN).\n
        These method return a new board and score.
    """
    score = []
    tempBoard = [[0 for _ in range(tile_number)] for _ in range(tile_number)]
    
    if direction == UP:
        for i in range(tile_number):
            row = []
            for j in range(tile_number):
                row.append(board[j][i])
            row,temp = rowMoveLeft(row)
            for j in range(tile_number):
                tempBoard[j][i]=row[j]
            score.append(temp)
        score=sum(_ for _ in score)

    elif direction == DOWN:
        for i in range(tile_number):
            row = []
            for j in reversed(range(tile_number)):
                row.append(board[j][i])

            row,temp = rowMoveLeft(row)
            for j in reversed(range(tile_number)):
                tempBoard[j][i]=row[tile_number - j - 1]
            score.append(temp)
        score=sum(_ for _ in score)

    elif direction == LEFT:
        for i in range(tile_number):
            tempBoard[i], temp = rowMoveLeft(board[i])
            score.append(temp)
        score=sum(_ for _ in score)

    elif direction == RIGHT:
        for i in range(tile_number):
            row = []
            for j in reversed(range(tile_number)):
                row.append(board[i][j])
            row,temp = rowMoveLeft(row)
            score.append(temp)

            for j in reversed(range(tile_number)):
                tempBoard[i][j] = row[tile_number - j -1]
        score=sum(_ for _ in score)

    return tempBoard, score   

if __name__ == "__main__":
>>>>>>> 324e23854a9035d7a89762b3704cceff6f938553
    main()