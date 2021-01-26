import pygame

pygame.init()
title = pygame.display.set_caption('Gomoku')
screen = pygame.display.set_mode((500, 500))

while True:
    image = "../img/bg.jpg"
    backgroud_img = pygame.image.load(image).convert()  # 加载方式2（适用于普通图像，提高渲染速度）
    bg_img = pygame.image.load(image).convert_alpha()
    screen.blit(bg_img, (0, 0))
    pygame.display.update()