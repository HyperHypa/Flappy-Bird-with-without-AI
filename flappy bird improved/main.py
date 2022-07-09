import pygame

pygame.init()

win_width = 800
win_height = 550
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Flappy Bird")  # set window name "Flappy Bird"
fb = pygame.image.load('25x25.png')
bg = pygame.image.load("bg.png")
top_pipe = pygame.image.load("pipe.png")
bottom_pipe = pygame.transform.flip(top_pipe, False, True)
score_font = pygame.font.SysFont('comicsans', 30, True)
endscreen_font = pygame.font.SysFont('comicsans', 100, True)


# bird data
class Bird:
    size = 25;

    def __init__(self, jump_count, x, y, score):
        self.jump_count = jump_count
        self.x = x
        self.y = y
        self.score = score


bird_1 = Bird(0, 50, 275, 0)

# pipe data
class Pipe:
    gap = 150
    width = 100
    vel = 7

    def __init__(self, x, y, toplength, passed):
        self.x = x
        self.y = y
        self.toplength = toplength
        self.passed = passed


pipe_1 = Pipe(400, 0, 100, False)
pipe_2 = Pipe(700, 0, 240, False)
pipe_3 = Pipe(1000, 0, 160, False)

# anything that needs to be output on the screen is here
def redrawGameWindow():
    win.blit(bg, (0, 0))
    win.blit(fb, (bird_1.x, bird_1.y))
    win.blit(top_pipe, (pipe_1.x, -550 + pipe_1.toplength))
    # pygame.draw.rect(win, (81, 240, 37), (pipe_1.x, pipe_1.y, Pipe.width, pipe_1.toplength))
    win.blit(bottom_pipe, (pipe_1.x, pipe_1.toplength + Pipe.gap))
    #pygame.draw.rect(win, (81, 240, 37), (pipe_1.x, pipe_1.y + pipe_1.toplength + Pipe.gap, Pipe.width, win_height - pipe_1.toplength - Pipe.gap))
    win.blit(top_pipe, (pipe_2.x, -550 + pipe_2.toplength))
    # pygame.draw.rect(win, (81, 240, 37), (pipe_2.x, pipe_2.y, Pipe.width, pipe_2.toplength))
    win.blit(bottom_pipe, (pipe_2.x, pipe_2.toplength + Pipe.gap))
    #pygame.draw.rect(win, (81, 240, 37), (pipe_2.x, pipe_2.y + pipe_2.toplength + Pipe.gap, Pipe.width, win_height - pipe_2.toplength - Pipe.gap))
    win.blit(top_pipe, (pipe_3.x, -550 + pipe_3.toplength))
    # pygame.draw.rect(win, (81, 240, 37), (pipe_3.x, pipe_3.y, Pipe.width, pipe_3.toplength))
    win.blit(bottom_pipe, (pipe_3.x, pipe_3.toplength + Pipe.gap))
    #pygame.draw.rect(win, (81, 240, 37), (pipe_3.x, pipe_3.y + pipe_3.toplength + Pipe.gap, Pipe.width, win_height - pipe_3.toplength - Pipe.gap))
    score_text = score_font.render('Score: ' + str(bird_1.score), True, (0, 0, 0))
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
        bird_1.jump_count = 13
    if keys[pygame.K_ESCAPE]:
        run = False

    # bird fall
    bird_1.y = bird_1.y - bird_1.jump_count
    if bird_1.jump_count != -17:
        bird_1.jump_count = bird_1.jump_count - 2

    # move pip
    pipe_1.x = pipe_1.x - Pipe.vel
    pipe_2.x = pipe_2.x - Pipe.vel
    pipe_3.x = pipe_3.x - Pipe.vel

    if pipe_1.x < -100:
        pipe_1.x = pipe_3.x + 300
        pipe_1.toplength = ((pipe_1.toplength * 367) + 1) % 381 + 10
        pipe_1.passed = False
    if pipe_2.x < -100:
        pipe_2.x = pipe_1.x + 300
        pipe_2.toplength = ((pipe_2.toplength * 536) + 1) % 381 + 10
        pipe_2.passed = False
    if pipe_3.x < -100:
        pipe_3.x = pipe_2.x + 300
        pipe_3.toplength = ((pipe_3.toplength * 737) + 1) % 381 + 10
        pipe_3.passed = False

    # score increase
    if pipe_1.x < 50 and pipe_1.passed is False:
        pipe_1.passed = True
        bird_1.score = bird_1.score + 1
    if pipe_2.x < 50 and pipe_2.passed is False:
        pipe_2.passed = True
        bird_1.score = bird_1.score + 1
    if pipe_3.x < 50 and pipe_3.passed is False:
        pipe_3.passed = True
        bird_1.score = bird_1.score + 1

    redrawGameWindow()

    # touch floor
    if bird_1.y >= 500 + Bird.size:
        bird_1.y = 500 + Bird.size
        redrawGameWindow()
        score_text = score_font.render('You lose', True, (0, 0, 0))
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

    if ((pipe_1.x - Bird.size <= bird_1.x <= pipe_1.x + Pipe.width) and (bird_1.y <= pipe_1.toplength or pipe_1.toplength + Pipe.gap <= bird_1.y + Bird.size)) \
            or ((pipe_2.x - Bird.size <= bird_1.x <= pipe_2.x + Pipe.width) and (bird_1.y < pipe_2.toplength or pipe_2.toplength + Pipe.gap < bird_1.y + Bird.size)) \
            or ((pipe_3.x - Bird.size <= bird_1.x <= pipe_3.x + Pipe.width) and (bird_1.y < pipe_3.toplength or pipe_3.toplength + Pipe.gap < bird_1.y + Bird.size)):
        # if pipe_1.x - Pipe.vel < bird_1.x + Bird.size:
        #    pipe_1.x = bird_1.x + Bird.size
        #    pipe_2.x = pipe_1.x + 300
        #    pipe_3.x = pipe_2.x + 300
        redrawGameWindow()
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
