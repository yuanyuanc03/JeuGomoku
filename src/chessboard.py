import pygame
import numpy as np

# define global variable of pieces' color
EMPTY = 0
BLACK = 1
WHITE = 2

class Chess(object):
    def __init__(self):
        pygame.init()
        self.space = 60
        self.cell_size = 40
        self.cell_num = 15
        self.grid_size = self.cell_size * (self.cell_num - 1) + self.space * 2
        self.title = pygame.display.set_caption('Gomoku')
        self.screen = pygame.display.set_mode((self.grid_size, self.grid_size))
        # chess grid position
        self.position= np.zeros((self.cell_num, self.cell_num, 2))
        self.board = np.zeros((self.cell_num, self.cell_num))
        self.chess_color = "black"
        self.is_black = True

        self.bg_path = "../img/background.jpg"

    def load_bg(self):
        while True:
            bg_img = pygame.transform.scale(pygame.image.load(self.bg_path), (self.grid_size, self.grid_size))
            self.screen.blit(bg_img, (0, 0))
            pygame.display.update()

    def draw(self):
        # background color
        self.screen.fill("peachpuff")

        for row in range(0, self.cell_num):
            for col in range(0, self.cell_num):
                self.position[row][col][0] = self.cell_size * row + self.space
                self.position[row][col][1] = self.cell_size * col + self.space

        for x in range(0, self.cell_size * self.cell_num, self.cell_size):
            pygame.draw.line(self.screen, "black", (x + self.space, 0 + self.space),
                             (x + self.space, self.cell_size * (self.cell_num - 1) + self.space), 1)
        for y in range(0, self.cell_size * self.cell_num, self.cell_size):
            pygame.draw.line(self.screen, "black", (0 + self.space, y + self.space),
                             (self.cell_size * (self.cell_num - 1) + self.space, y + self.space), 1)

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
        pygame.display.update()  # 刷新窗口显示

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    row = round((x - chess.space) / chess.cell_size)
                    col = round((y - chess.space) / chess.cell_size)
                    if(self.board[row][col] == EMPTY):
                        pygame.draw.circle(self.screen, self.chess_color, (self.position[row][col][0], self.position[row][col][1]), 18)
                        self.play(row, col)
                        self.screen.blit(self.screen, (0, 0))
                        pygame.display.update()

    def play(self, row, col):
        if self.is_black:
            self.is_black = False
            self.chess_color = "white"
            self.board[row][col] = BLACK
        else:
            self.is_black = True
            self.chess_color = "black"
            self.board[row][col] = WHITE

    def is_win(self):
        return True

if __name__ == '__main__':
    chess = Chess()
    # chess.load_bg()
    chess.draw()
