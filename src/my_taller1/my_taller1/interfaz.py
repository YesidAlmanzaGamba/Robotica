import pygame
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

button1 = pygame.Rect(50, 50, 100, 50)
button2 = pygame.Rect(50, 150, 100, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
current_color1 = color_inactive
current_color2 = color_inactive

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.collidepoint(event.pos):
                print('Button 1 was pressed')
            elif button2.collidepoint(event.pos):
                print('Button 2 was pressed')
        if event.type == pygame.MOUSEMOTION:
            if button1.collidepoint(event.pos):
                current_color1 = color_active
            else:
                current_color1 = color_inactive
            if button2.collidepoint(event.pos):
                current_color2 = color_active
            else:
                current_color2 = color_inactive

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, current_color1, button1)
    pygame.draw.rect(screen, current_color2, button2)
    pygame.display.update()