import pygame

pygame.init()

win_width = 800
win_height = 550
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Flappy Bird")  # set window name "Flappy Bird"
fb = pygame.image.load('25x25.png')
bg = pygame.image.load("bg.png")
score_font = pygame.font.SysFont('comicsans', 30, True)
endscreen_font = pygame.font.SysFont('comicsans', 100, True)


# bird data
jump_count = 0
bird_x = 50
bird_y = 275
score = 0


# pipe data
pip_width = 100
pip_gap = 150

pip_x_1 = 400
pip_y_1 = 0
pip_length_top1 = 100
pip_passed_1 = False

pip_x_2 = 700
pip_y_2 = 0
pip_length_top2 = 240
pip_passed_2 = False

pip_x_3 = 1000
pip_y_3 = 0
pip_length_top3 = 160
pip_passed_3 = False

# anything that needs to be output on the screen is here
def redrawGameWindow():
    win.blit(bg, (0, 0))
    win.blit(fb, (bird_x, bird_y))
    pygame.draw.rect(win, (81, 240, 37), (pip_x_1, pip_y_1, pip_width, pip_length_top1))
    pygame.draw.rect(win, (81, 240, 37), (pip_x_1, pip_y_1 + pip_length_top1 + pip_gap, pip_width, win_height - pip_length_top1 - pip_gap))
    pygame.draw.rect(win, (81, 240, 37), (pip_x_2, pip_y_2, pip_width, pip_length_top2))
    pygame.draw.rect(win, (81, 240, 37), (pip_x_2, pip_y_2 + pip_length_top2 + pip_gap, pip_width, win_height - pip_length_top2 - pip_gap))
    pygame.draw.rect(win, (81, 240, 37), (pip_x_3, pip_y_3, pip_width, pip_length_top3))
    pygame.draw.rect(win, (81, 240, 37), (pip_x_3, pip_y_3 + pip_length_top3 + pip_gap, pip_width, win_height - pip_length_top3 - pip_gap))
    score_text = score_font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(score_text, (10, 10))
    pygame.display.update()


# main loop
run = True
while run:
    pygame.time.delay(25)

    # if exit the window the code stops
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # input detect
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        jump_count = 13
    if keys[pygame.K_ESCAPE]:
        run = False

    redrawGameWindow()

    bird_y = bird_y - jump_count
    if jump_count != -17:
        jump_count = jump_count - 2

    # move pip
    pip_x_1 = pip_x_1 - 7
    pip_x_2 = pip_x_2 - 7
    pip_x_3 = pip_x_3 - 7

    if pip_x_1 < -100:
        pip_x_1 = pip_x_3 + 300
        pip_length_top1 = ((pip_length_top1 * 367) + 1) % 381 + 10
        pip_passed_1 = False
    if pip_x_2 < -100:
        pip_x_2 = pip_x_1 + 300
        pip_length_top2 = ((pip_length_top2 * 536) + 1) % 381 + 10
        pip_passed_2 = False
    if pip_x_3 < -100:
        pip_x_3 = pip_x_2 + 300
        pip_length_top3 = ((pip_length_top3 * 737) + 1) % 381 + 10
        pip_passed_3 = False

    # score increase
    if pip_x_1 < 50 and pip_passed_1 is False:
        pip_passed_1 = True
        score = score + 1
    if pip_x_2 < 50 and pip_passed_2 is False:
        pip_passed_2 = True
        score = score + 1
    if pip_x_3 < 50 and pip_passed_3 is False:
        pip_passed_3 = True
        score = score + 1

    # touch floor
    if bird_y >= 520:
        score_text = score_font.render('You lose', 1, (0, 0, 0))
        win.blit(score_text, (300, 225))
        pygame.display.update()

        run2 = True
        while run2:
            pygame.time.delay(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    run2 = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
                run2 = False

    # touch pip
    #
    if ((pip_x_1 < bird_x and bird_x < pip_x_1 + pip_width) and (bird_y < pip_length_top1 or pip_length_top1 + pip_gap < bird_y)) or ((pip_x_2 < bird_x and bird_x < pip_x_2 + pip_width) and (bird_y < pip_length_top2 or pip_length_top2 + pip_gap < bird_y)) or ((pip_x_3 < bird_x and bird_x < pip_x_3 + pip_width) and (bird_y < pip_length_top3 or pip_length_top3 + pip_gap < bird_y)):
        score_text = score_font.render('You lose', 1, (0, 0, 0))
        win.blit(score_text, (300, 225))
        pygame.display.update()

        run2 = True
        while run2:
            pygame.time.delay(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    run2 = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
                run2 = False
