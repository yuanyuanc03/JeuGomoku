import pygame
import numpy as np

# define global variable of pieces' color
EMPTY = 0
BLACK = 1
WHITE = 2

class Button:
    def __init__(self, text, x, y, bg):
        self.font = pygame.font.SysFont("Arial", 40)
        self.x = x
        self.y = y
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, 1, pygame.Color("white"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface((self.size[0] + 130, self.size[1] + 10))
        self.surface.fill(bg)
        self.surface.blit(self.text, (65, 5))
        self.rect = pygame.Rect(self.x, self.y, self.size[0] + 130, self.size[1] + 130)

class Chess(object):
    def __init__(self):
        pygame.init()
        self.space = 60
        self.cell_size = 40
        self.cell_num = 15
        self.grid_size = self.cell_size * (self.cell_num - 1) + self.space * 2
        self.title = pygame.display.set_caption('Gomoku')
        self.screen = pygame.display.set_mode((self.grid_size, self.grid_size))
        self.font = pygame.font.SysFont("Arial", 20)
        # chess grid position
        self.position= np.zeros((self.cell_num, self.cell_num, 2))
        self.board = np.zeros((self.cell_num, self.cell_num))
        self.chess_color = "black"
        self.is_black = True
        # background image
        self.bg_path = "../img/background.jpg"
        # create buttons
        self.btn_start = Button("Start", x = 200, y = 80, bg="sandybrown")
        self.btn_exit = Button("Exit", x = 450, y = 80, bg="sandybrown")

    def btnStart_click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.btn_start.rect.collidepoint(x, y):
                    self.draw()

    def btnExit_click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.btn_exit.rect.collidepoint(x, y):
                    pygame.quit()

    def load_bg(self):
        while True:
            bg_img = pygame.transform.scale(pygame.image.load(self.bg_path), (self.grid_size, self.grid_size))
            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(self.btn_start.surface, (self.btn_start.x, self.btn_start.y))
            self.screen.blit(self.btn_exit.surface, (self.btn_exit.x, self.btn_exit.y))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.btnStart_click(event)
                self.btnExit_click(event)

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
        pygame.display.update()

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
        if not self.is_win():
            pass
        else:
            print(self.is_win())
            # running = False

    def is_win(self):
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
        return False

if __name__ == '__main__':
    chess = Chess()
    chess.load_bg()
