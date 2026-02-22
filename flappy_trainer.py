import pygame
import neat
import os
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pickle
from objects import *
from config_variables import *
from NNdraw import NN


best_nn = None



plot_scores = [0]
mean_scores = [0]

def live_plot():
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title("Flappy Bird AI Training")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Score")
    best_line, = ax.plot([], [], label='Best Score')
    mean_line, = ax.plot([], [], label='Mean Score')
    ax.legend()

    def update():
        best_line.set_data(range(1, len(plot_scores)+1), plot_scores)
        mean_line.set_data(range(1, len(mean_scores)+1), mean_scores)
        ax.relim()
        ax.autoscale_view()
        plt.pause(0.01)

    return update

update_plot = live_plot()


def draw_window(win, birds, pipes, base, score, gen, best_nn):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (225,225,225))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (225,225,225))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Alive: " + str(len(birds)), 1, (225,225,225))
    win.blit(text, (10, 40))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
        
    if best_nn:
        best_nn.draw(win)


    pygame.display.update()

def main(genomes, config):
    global GEN
    GEN += 1

    nets = []
    ge = []
    birds = []
    

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0
    SPEED = 30
    run = True

    while run:
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            if ge[x].fitness > 150:
                break

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()
                
        

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            if score % 20 == 0:
                SPEED += 10
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                
        best_nn = None
        if len(ge) > 0:
            best_fitness = -float('inf')
            best_index = 0
            for i, g in enumerate(ge):
                if g.fitness > best_fitness:
                    best_fitness = g.fitness
                    best_index = i

            best_nn = NN(config, ge[best_index], (50, 150))


        base.move()
        draw_window(win, birds, pipes, base, score, GEN, best_nn)
    
        plot_scores[-1] = score
        mean = sum(plot_scores) / len(plot_scores) if plot_scores else 0
        # print(plot_scores, mean)
        mean_scores[-1] = mean
        update_plot()
        
    plot_scores.append(score)
    mean = sum(plot_scores) / len(plot_scores) if plot_scores else 0
    mean_scores.append(mean)
    update_plot()

    


def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 10)
    print("Winner:", winner)
    with open("best_flappy_model.pkl", "wb") as f:
        pickle.dump(winner, f)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config")
    run(config_path)
    print("Training Completed...")
