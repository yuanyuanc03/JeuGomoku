from PIL import Image

import pygame
import numpy as np

# define global variable of pieces' color
EMPTY = 0
BLACK = 1
WHITE = 2

class Button:
    def __init__(self, text, x, y):
        """
        initialisation of class button
        :param text: string of the button name
        :param x: position x of button
        :param y: position y of button
        """
        self.font = pygame.font.SysFont("Arial", 30)
        self.font.set_bold(True)
        self.font.set_italic(True)
        self.x = x
        self.y = y
        if(isinstance(text, str)):
            self.surface = self.font.render(text, True, pygame.Color("goldenrod"))
        else:
            self.surface = text
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

    def check_click(self, position):
        """
        judge if user click the button
        :param position: the mouseclick position
        :return: if click the button return True; else return False
        """
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False

class Chess(object):
    def __init__(self):
        """
        initialisation of class Chess
        """
        ### initialisation of pygame
        pygame.init()
        ### initialisation of chessboard
        # the size of the edge
        self.space = 80
        # the size of each cell
        self.cell_size = 40
        # the number of all cells
        self.cell_num = 15
        # the size of the whole chessboard
        self.grid_size = self.cell_size * (self.cell_num - 1) + self.space * 2
        # the name of window
        self.title = pygame.display.set_caption('Gomoku')
        # the settings of screen
        self.screen = pygame.display.set_mode((self.grid_size, self.grid_size))
        # the font of screen
        self.font = pygame.font.SysFont("Arial", 20)
        ### chess grid position
        self.position= np.zeros((self.cell_num, self.cell_num, 2))
        self.board = np.zeros((self.cell_num, self.cell_num))
        # the initial chess color is black
        self.chess_color = "black"
        # a binary variable indicate the chess color is black or not
        self.is_black = True
        # background image
        self.bg_path = "../img/background.jpg"
        # create buttons
        self.btn_start = Button("Start", x = 200, y = 80)
        self.btn_startWithTimer = Button("Start with Timer", x = 320, y = 80)
        self.btn_exit = Button("Exit", x = 580, y = 80)
        self.btn_restart = Button("Restart", x = 420, y = 15)
        self.btn_back = Button("Back", x = 560, y = 15)
        # im = Image.open("../img/music2.png")
        # imgpro  = im.resize((40, 40))
        # imgpro.save("../img/music2_resized.png", 'PNG')
        self.imageMusic = pygame.image.load("../img/music2_resized.png").convert_alpha()
        self.btn_music = Button(self.imageMusic, x = 90, y = 15)

        ### set timer
        self.counts = 300
        self.COUNT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.COUNT, 1000)
        self.text = "Timer"

        self.music_path = "../music/music.mp3"
        # initialise the mixer module
        pygame.mixer.init()
        # load music file
        pygame.mixer.music.load(self.music_path)
        # play music
        pygame.mixer.music.play()
        self.is_playMusic = True

        # if gameover
        self.is_gameOver = False

    def btnStart_click(self, event):
        """
        start the game when users click the button Start
        :param event: if users click the button Start then event occurs
        """
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.btn_start.check_click([x, y]):
                    self.draw()

    def btnStartWithTimer_click(self, event):
        """
        start the game with timer when users click the button StartWithTimer
        :param event: if users click the button StartWithTimer then event occurs
        """
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.btn_startWithTimer.check_click([x, y]):
                    self.draw(True)

    def btnExit_click(self, event):
        """
        exit the game when users click the button Exit
        :param event: if users click the button Exit then event occurs
        """
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.btn_exit.check_click([x, y]):
                   exit()

    def btnRestart_click(self, event, timer):
        """
        restart the game
        :param event: if users click the button Restart then event occurs
        """
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.btn_restart.check_click([x, y]):
                    self.position = np.zeros((self.cell_num, self.cell_num, 2))
                    self.board = np.zeros((self.cell_num, self.cell_num))
                    self.chess_color = "black"
                    self.is_black = True
                    self.is_gameOver = False
                    if not self.is_playMusic:
                        self.is_playMusic = True
                    if (timer):
                        self.counts = 300
                    self.draw(timer)

    def btnBack_click(self, event):
        """
        back to the main page
        :param event: if users click the button Back then event occurs
        """
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.btn_back.check_click([x, y]):
                    self.position = np.zeros((self.cell_num, self.cell_num, 2))
                    self.board = np.zeros((self.cell_num, self.cell_num))
                    self.chess_color = "black"
                    self.is_black = True
                    self.is_gameOver = False
                    self.load_bg()

    def btnMusic_click(self, event):
        """
        play music
        :param event: if users click the button Music then event occurs
        """
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.btn_music.check_click([x, y]):
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        self.is_playMusic = False
                    else:
                        pygame.mixer.music.play()
                        self.is_playMusic = True

    def showText(self, text, x, y):
        """
        show text in the screen
        :param text: string of content of text
        :param x: the position x
        :param y: the position y
        """
        text_font = pygame.font.SysFont("Arial", 25)
        text_font.set_bold(True)
        text_font.set_italic(True)
        self.text = text_font.render("                 ", True, "goldenrod", "peachpuff")
        self.screen.blit(self.text, (x, y))
        self.text = text_font.render(text, True, "goldenrod", "peachpuff")
        self.screen.blit(self.text, (x, y))
        pygame.display.update()

    def load_bg(self):
        """
        load the background picture
        """
        while True:
            bg_img = pygame.transform.scale(pygame.image.load(self.bg_path), (self.grid_size, self.grid_size))
            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(self.btn_start.surface, (self.btn_start.x, self.btn_start.y))
            self.screen.blit(self.btn_startWithTimer.surface, (self.btn_startWithTimer.x, self.btn_startWithTimer.y))
            self.screen.blit(self.btn_exit.surface, (self.btn_exit.x, self.btn_exit.y))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                self.btnStart_click(event)
                self.btnStartWithTimer_click(event)
                self.btnExit_click(event)

    def draw(self, timer=False):
        """
        create the chessboard and draw the chess
        """
        # background color
        self.screen.fill("peachpuff")
        self.screen.blit(self.btn_restart.surface, (self.btn_restart.x, self.btn_restart.y))
        self.screen.blit(self.btn_back.surface, (self.btn_back.x, self.btn_back.y))
        self.screen.blit(self.btn_music.surface, (self.btn_music.x, self.btn_music.y))

        for row in range(0, self.cell_num):
            for col in range(0, self.cell_num):
                self.position[row][col][0] = self.cell_size * row + self.space
                self.position[row][col][1] = self.cell_size * col + self.space

        # draw chessboard
        for x in range(0, self.cell_size * self.cell_num, self.cell_size):
            pygame.draw.line(self.screen, "black", (x + self.space, 0 + self.space),
                             (x + self.space, self.cell_size * (self.cell_num - 1) + self.space), 1)
        for y in range(0, self.cell_size * self.cell_num, self.cell_size):
            pygame.draw.line(self.screen, "black", (0 + self.space, y + self.space),
                             (self.cell_size * (self.cell_num - 1) + self.space, y + self.space), 1)

        # draw intersection point in the chessboard
        pygame.draw.circle(self.screen, "black", (self.cell_size * 3 + self.space, self.cell_size * 3 + self.space),
                           5)
        pygame.draw.circle(self.screen, "black",
                           (self.cell_size * 3 + self.space, self.cell_size * 11 + self.space), 5)
        pygame.draw.circle(self.screen, "black",
                           (self.cell_size * 11 + self.space, self.cell_size * 3 + self.space), 5)
        pygame.draw.circle(self.screen, "black",
                           (self.cell_size * 11 + self.space, self.cell_size * 11 + self.space), 5)
        pygame.draw.circle(self.screen, "black", (self.cell_size * 7 + self.space, self.cell_size * 7 + self.space),
                           5)
        pygame.display.update()

        # listen to the pygame's event
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.K_q:
                    exit()
                elif timer and event.type == self.COUNT and not self.is_gameOver:
                    self.counts = self.counts - 1
                    counts_text = str(self.counts)
                    self.showText("Time: " + counts_text, 260, 20)
                    if self.counts == 0:
                        self.gameOver("Time is out!")

                elif event.type == pygame.MOUSEBUTTONDOWN and not self.is_gameOver:
                    x, y = event.pos
                    if(x >= 70 and x <= 650 and y >= 70 and y <= 650):
                        row = round((x - chess.space) / chess.cell_size)
                        col = round((y - chess.space) / chess.cell_size)
                        if (self.board[row][col] == EMPTY):
                            pygame.draw.circle(self.screen, self.chess_color,
                                               (self.position[row][col][0], self.position[row][col][1]), 18)
                            self.play(row, col)
                            self.screen.blit(self.screen, (0, 0))
                            pygame.display.update()

                self.btnMusic_click(event)
                self.btnRestart_click(event, timer)
                self.btnBack_click(event)

                if not pygame.mixer.music.get_busy():
                    if self.is_playMusic:
                        pygame.mixer.music.play()

    def gameOver(self, text):
        """
        if game over, show the text in the screen
        :param text: string of text
        """
        gameover_font = pygame.font.SysFont("Arial", 60)
        gameover_font.set_italic(True)
        gameover_text = gameover_font.render("Game Over, " + text, True, "sandybrown")
        self.screen.blit(gameover_text, (
            round(self.grid_size / 2 - gameover_text.get_width() / 2),
            round(self.grid_size / 2 - gameover_text.get_height() / 2)))
        # if game over, is_gameOver = True
        self.is_gameOver = True

    def play(self, row, col):
        """
        change the color of chess and judge if user is win
        :param row: the number of row
        :param col: the number of column
        """
        if self.is_black:
            self.is_black = False
            self.chess_color = "white"
            self.board[row][col] = BLACK
        else:
            self.is_black = True
            self.chess_color = "black"
            self.board[row][col] = WHITE
        if not self.is_win():
            pass
        else:
            self.gameOver(self.is_win())

    def is_win(self):
        """
        judge each color of user wins
        """
        for c in range(self.cell_num):
            for r in range(self.cell_num):
                if r < self.cell_num - 4 and self.board[r][c] ==  self.board[r + 1][c] ==  self.board[r + 2][c] == \
                        self.board[r + 3][c] == self.board[r + 4][c] == BLACK:
                    return "Black win!"
                elif r < self.cell_num - 4 and self.board[r][c] ==  self.board[r + 1][c] ==  self.board[r + 2][c] == \
                        self.board[r + 3][c] == self.board[r + 4][c] == WHITE:
                    return "White win!"
                elif c < self.cell_num - 4 and self.board[r][c] == self.board[r][c + 1] == self.board[r][c + 2] == \
                        self.board[r][c + 3] == self.board[r][c + 4] == BLACK:
                    return "Black win!"
                elif c < self.cell_num - 4 and self.board[r][c] == self.board[r][c + 1] == self.board[r][c + 2] == \
                        self.board[r][c + 3] == self.board[r][c + 4] == WHITE:
                    return "White win!"
                elif r < self.cell_num - 4 and c < self.cell_num - 4 and self.board[r][c] == self.board[r + 1][c + 1] == \
                        self.board[r + 2][c + 2] == self.board[r + 3][c + 3] == self.board[r + 4][c + 4] == BLACK:
                    return "Black win!"
                elif r < self.cell_num - 4 and c < self.cell_num - 4 and self.board[r][c] == self.board[r + 1][c + 1] == \
                        self.board[r + 2][c + 2] == self.board[r + 3][c + 3] == self.board[r + 4][c + 4] == WHITE:
                    return "White win!"
                elif r > 3 and c < self.cell_num - 4 and self.board[r][c] == self.board[r - 1][c + 1] == \
                        self.board[r - 2][c + 2] == self.board[r - 3][c + 3] == self.board[r - 4][c + 4] == BLACK:
                    return "Black win!"
                elif r > 3 and c < self.cell_num - 4 and self.board[r][c] == self.board[r - 1][c + 1] == \
                        self.board[r - 2][c + 2] == self.board[r - 3][c + 3] == self.board[r - 4][c + 4] == WHITE:
                    return "White win!"
        # if the game doesn't finish, return False
        return False

if __name__ == '__main__':
    chess = Chess()
    chess.load_bg()
