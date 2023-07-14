import pygame
from random import choice
from math import sqrt

FPS = 30
WIDTH, HEIGHT = 400, 550

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

class Game:
    def __init__(self, score):
        self.matrix = [[None]*3 for _ in range(3)]
        self.turn = choice(['x', 'o'])
        self.over = False
        self.winner = None
        self.score = score
        self.buttons = [pygame.Rect(50, 475, 125, 50), pygame.Rect(225, 475, 125, 50)]
        self.gameOverMarkers = [False]*4
        self.loadText()
        self.loadImages()
    
    def loadImages(self):
        self.cross = pygame.transform.scale(pygame.image.load('x.png'), (80, 80))
        self.o = pygame.transform.scale(pygame.image.load('o.png'), (80, 80))
        self.redline_hor = pygame.image.load('red-line.png')
        self.redline_ver = pygame.transform.rotate(self.redline_hor, 90)
        self.redline_dia2 = pygame.transform.rotate(pygame.transform.scale(self.redline_hor, (sqrt(2)*300, 30)), 45)
        self.redline_dia1 = pygame.transform.rotate(self.redline_dia2, 90)
        self.lines = [self.redline_hor, self.redline_ver, self.redline_dia1, self.redline_dia2]
        self.images = [self.cross, self.o]
    
    def loadText(self):
        self.fontEngine = pygame.font.SysFont('Komika Axis', 15)
        self.playAgainText = self.fontEngine.render('Play Again', True, 'white')
        self.resetScoreText = self.fontEngine.render('Reset Score', True, 'white')
        self.drawText = pygame.transform.scale2x(self.fontEngine.render('DRAW', True, 'white'))
        self.text = [self.playAgainText, self.resetScoreText, self.drawText]
    
    def handleClick(self, clicks):
        if self.matrix[clicks[0]-1][clicks[1]-1] != None or self.over:
            return
        self.matrix[clicks[0]-1][clicks[1]-1] = self.turn
        self.turn = 'x' if self.turn == 'o' else 'o'
        self.checkGameOver()
    
    def checkGameOver(self):
        # Checking rows
        board = self.matrix
        for row in range(3):
            if (board[row][0] == board[row][1] == board[row][2]) and board[row][0]:
                self.over, self.winner = True, board[row][0]
                self.gameOverMarkers[0] = row + 1
        
        # Checking column
        for col in range(3):
            if (board[0][col] == board[1][col] == board[2][col]) and board[0][col]:
                self.over, self.winner = True, board[0][col]
                self.gameOverMarkers[1] = col + 1
        
        # Checking diagonal one \
        if (board[0][0] == board[1][1] == board[2][2]) and board[0][0]:
            self.over, self.winner = True, board[0][0]
            self.gameOverMarkers[2] = True
        
        # Checking Diagonal two /
        if (board[0][2] == board[1][1] == board[2][0]) and board[0][2]:
            self.over, self.winner = True, board[0][2]
            self.gameOverMarkers[3] = True
        
        # Adding the score
        if self.over and self.winner == 'o':
            self.score[0] += 1
        if self.over and self.winner == 'x':
            self.score[1] += 1
        if any(None in row for row in self.matrix):
            return
        elif not self.over:
            self.over, self.winner = True, 'draw'
    
    def handleButtonClick(self, buttonNo):
        if buttonNo == 1:
            self.__init__(self.score)
        if buttonNo == 2:
            self.score = [0,0]

def draw(window: pygame.Surface, images, turn, matrix, over, winner, buttons, score, lines, text, gameOverMarkers):
    # Background and rectangles
    window.fill((91, 192, 222))
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(55+100*j, 155+100*i, 90, 90)
            pygame.draw.rect(window, 'white', rect, border_radius=10)
            if matrix[i][j] == 'x':
                window.blit(images[0], (60+100*j, 160+100*i))
            if matrix[i][j] == 'o':
                window.blit(images[1], (60+100*j, 160+100*i))
    
    # Turn Displayer
    x_surface = images[0].copy()
    o_surface = images[1].copy()
    if turn == 'o':
        o_surface.set_alpha(255)
        x_surface.set_alpha(120)
    if turn == 'x':
        x_surface.set_alpha(255)
        o_surface.set_alpha(120)
    window.blit(o_surface, (60, 60))
    window.blit(x_surface, (260, 60))

    # Buttons and text
    pygame.draw.rect(window, 'red', buttons[0], border_radius=10)
    pygame.draw.rect(window, 'blue', buttons[1], border_radius=10)
    playAgainRect = text[0].get_rect()
    playAgainRect.center = buttons[0].center
    window.blit(text[0], playAgainRect)
    resetScoreRect = text[1].get_rect()
    resetScoreRect.center = buttons[1].center
    window.blit(text[1], resetScoreRect)

    # Score
    scoreSurface = pygame.font.SysFont('Komika Axis', 60).render(f'{score[0]}:{score[1]}', True, 'white')
    scoreRect = scoreSurface.get_rect()
    scoreRect.center = (200, 100)
    window.blit(scoreSurface, scoreRect)

    # Game Over
    if over:
        if gameOverMarkers[0]:
            redRect = lines[0].get_rect()
            redRect.center = (200, 100*(gameOverMarkers[0]+1))
            window.blit(lines[0], redRect)
        if gameOverMarkers[1]:
            redRect = lines[1].get_rect()
            redRect.center = (100*gameOverMarkers[1], 300)
            window.blit(lines[1], redRect)
        if gameOverMarkers[2]:
            redRect = lines[2].get_rect()
            redRect.center = (200, 300)
            window.blit(lines[2], redRect)
        if gameOverMarkers[3]:
            redRect = lines[3].get_rect()
            redRect.center = (200, 300)
            window.blit(lines[3], redRect)
        if winner == 'draw':
            drawRect = text[2].get_rect()
            drawRect.center = (200, 300)
            window.blit(text[2], drawRect)

    pygame.display.update()

def userClick():
    x, y = pygame.mouse.get_pos()

    # Checking x
    if x in range(50, 350):
        if x in range(50, 150):
            col = 1
        elif x in range(150, 250):
            col = 2
        else:
            col = 3
    else:
        col = None
    
    # Checking y
    if y in range(150, 450):
        if y in range(150, 250):
            row = 1
        elif y in range(250, 350):
            row = 2
        else:
            row = 3
    else:
        row = None
    
    # Checking Button Clicks
    if x in range(50, 175) and y in range(475, 525):
        return [1]
    if x in range(225, 350) and y in range(475, 525):
        return [2]
    
    if row and col:
        return [row, col]
    
    return None

def main():
    clock = pygame.time.Clock()
    running = True
    game = Game([0,0])

    while running:
        clock.tick(FPS)

        draw(window, game.images, game.turn, game.matrix, game.over, game.winner, game.buttons, game.score, game.lines, game.text, game.gameOverMarkers)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicks = userClick()
                if len(clicks) == 2:
                    game.handleClick(clicks)
                elif clicks and len(clicks) == 1:
                    game.handleButtonClick(clicks[0])

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
