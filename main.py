import neat
import pygame
import os

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
    size = 25

    def __init__(self, jump_count, x, y, score):
        self.jump_count = jump_count
        self.x = x
        self.y = y
        self.score = score


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


# anything that needs to be output on the screen is here
def redrawGameWindow(birds, pipe_1, pipe_2, pipe_3, score):
    win.blit(bg, (0, 0))
    for i, _ in enumerate(birds):
        win.blit(fb, (birds[i].x, birds[i].y))
    win.blit(top_pipe, (pipe_1.x, -550 + pipe_1.toplength))
    # pygame.draw.rect(win, (81, 240, 37), (pipe_1.x, pipe_1.y, Pipe.width, pipe_1.toplength))
    win.blit(bottom_pipe, (pipe_1.x, pipe_1.toplength + Pipe.gap))
    # pygame.draw.rect(win, (81, 240, 37), (pipe_1.x, pipe_1.y + pipe_1.toplength + Pipe.gap, Pipe.width, win_height - pipe_1.toplength - Pipe.gap))
    win.blit(top_pipe, (pipe_2.x, -550 + pipe_2.toplength))
    # pygame.draw.rect(win, (81, 240, 37), (pipe_2.x, pipe_2.y, Pipe.width, pipe_2.toplength))
    win.blit(bottom_pipe, (pipe_2.x, pipe_2.toplength + Pipe.gap))
    # pygame.draw.rect(win, (81, 240, 37), (pipe_2.x, pipe_2.y + pipe_2.toplength + Pipe.gap, Pipe.width, win_height - pipe_2.toplength - Pipe.gap))
    win.blit(top_pipe, (pipe_3.x, -550 + pipe_3.toplength))
    # pygame.draw.rect(win, (81, 240, 37), (pipe_3.x, pipe_3.y, Pipe.width, pipe_3.toplength))
    win.blit(bottom_pipe, (pipe_3.x, pipe_3.toplength + Pipe.gap))
    # pygame.draw.rect(win, (81, 240, 37), (pipe_3.x, pipe_3.y + pipe_3.toplength + Pipe.gap, Pipe.width, win_height - pipe_3.toplength - Pipe.gap))
    score_text = score_font.render('Score: ' + str(score), True, (0, 0, 0))
    win.blit(score_text, (10, 10))
    pygame.display.update()


# running config
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 1000)


# main loop
def main(genomes, config):
    nets = []
    ge = []
    birds = []

    for _, i in genomes:
        net = neat.nn.FeedForwardNetwork.create(i, config)
        nets.append(net)
        birds.append(Bird(0, 50, 275, 0))
        i.fitness = 0
        ge.append(i)

    pipe_1 = Pipe(400, 0, 100, False)
    pipe_2 = Pipe(700, 0, 240, False)
    pipe_3 = Pipe(1000, 0, 160, False)
    score = 0

    running = True
    while running:
        pygame.time.delay(25)

        # quit gen if none left
        if len(birds) == 0:
            running = False
            break

        # encourage thr bird to stay alive longer
        for i, _ in enumerate(birds):
            ge[i].fitness += 0.1

        # if exit the window the code stops
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # input detect
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            pygame.quit()
            quit()

        # jump or not
        if (50 <= pipe_1.x < pipe_2.x < pipe_3.x) or (pipe_1.x < 50 <= pipe_2.x < pipe_3.x):
            for i, _ in enumerate(birds):
                output = nets[i].activate((birds[i].y, abs(birds[i].y - pipe_1.toplength), abs(birds[i].y - (pipe_1.toplength + Pipe.gap)), pipe_1.x - birds[i].x))
                # print("pipe 1")
                if output[0] > 0.5:
                    # print("%d jumped" % i)
                    birds[i].jump_count = 13
        if (50 <= pipe_2.x < pipe_3.x < pipe_1.x) or (pipe_1.x < 50 <= pipe_2.x < pipe_3.x):
            for i, _ in enumerate(birds):
                output = nets[i].activate((birds[i].y, abs(birds[i].y - pipe_2.toplength), abs(birds[i].y - (pipe_2.toplength + Pipe.gap)), pipe_2.x - birds[i].x))
                # print("pipe 2")
                if output[0] > 0.5:
                    # print("%d jumped" % i)
                    birds[i].jump_count = 13
        if (50 <= pipe_3.x < pipe_1.x < pipe_2.x) or (pipe_2.x < 50 <= pipe_3.x < pipe_1.x):
            for i, _ in enumerate(birds):
                output = nets[i].activate((birds[i].y, abs(birds[i].y - pipe_3.toplength), abs(birds[i].y - (pipe_3.toplength + Pipe.gap)), pipe_3.x - birds[i].x))
                # print("pipe 3")
                if output[0] > 0.5:
                    # print("%d jumped" % i)
                    birds[i].jump_count = 13

        # bird fall
        for i, _ in enumerate(birds):
            birds[i].y = birds[i].y - birds[i].jump_count
            if birds[i].jump_count != -17:
                birds[i].jump_count = birds[i].jump_count - 2

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
            for i in ge:
                i.fitness += 5
            pipe_1.passed = True
            score = score + 1
        if pipe_2.x < 50 and pipe_2.passed is False:
            for i in ge:
                i.fitness += 5
            pipe_2.passed = True
            score = score + 1
        if pipe_3.x < 50 and pipe_3.passed is False:
            for i in ge:
                i.fitness += 5
            pipe_3.passed = True
            score = score + 1

        for i in birds:
            redrawGameWindow(birds, pipe_1, pipe_2, pipe_3, score)

        # touch floor
        for i, _ in enumerate(birds):
            if birds[i].y >= 500 + Bird.size:
                birds[i].y = 500 + Bird.size
                ge[i].fitness -= 1
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        # touch pip
        for i, _ in enumerate(birds):
            if ((pipe_1.x - Bird.size <= birds[i].x <= pipe_1.x + Pipe.width) and (
                    birds[i].y <= pipe_1.toplength or pipe_1.toplength + Pipe.gap <= birds[i].y + Bird.size)) \
                    or ((pipe_2.x - Bird.size <= birds[i].x <= pipe_2.x + Pipe.width) and (
                    birds[i].y < pipe_2.toplength or pipe_2.toplength + Pipe.gap < birds[i].y + Bird.size)) \
                    or ((pipe_3.x - Bird.size <= birds[i].x <= pipe_3.x + Pipe.width) and (
                    birds[i].y < pipe_3.toplength or pipe_3.toplength + Pipe.gap < birds[i].y + Bird.size)):
                ge[i].fitness -= 1
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)


# start of the program
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
