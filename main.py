import pygame
import neat
import pickle
import os
from objects import *
from config_variables import *
import random

pygame.font.init()

random.seed(287)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird - Manual/AI Mode")

MODE = "manual"  # or 'ai'

# Load trained genome
with open("best_flappy_model.pkl", "rb") as f:
    winner = pickle.load(f)

config_path = os.path.join(os.path.dirname(__file__), "config")
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)
net = neat.nn.FeedForwardNetwork.create(winner, config)


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def draw_button(win, active):
    color = (0, 200, 0) if active else (200, 0, 0)
    pygame.draw.rect(win, color, (10, 70, 130, 30), border_radius=5)
    label = BUTTON_FONT.render("AUTO: ON" if active else "AUTO: OFF", True, (255,255,255))
    win.blit(label, (20, 75))

def death_screen():
    win.blit(BG_IMG, (0, 0))
    death_text = STAT_FONT.render("YOU DIED!!!", True, (255, 0, 0))
    retry_text = STAT_FONT.render("Press R to Retry or ", True, (255, 255, 255))
    retry_text2 = STAT_FONT.render("M for Menu", True, (255, 255, 255))
    
    win.blit(death_text, ((WIN_WIDTH - death_text.get_width()) // 2, 200))
    win.blit(retry_text, ((WIN_WIDTH - retry_text.get_width()) // 2, 300))
    win.blit(retry_text2, ((WIN_WIDTH - retry_text2.get_width()) // 2, 400))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                    waiting = False
                elif event.key == pygame.K_m:
                    main_menu()
                    waiting = False

def main_menu():
    global MODE
    run = True
    clock = pygame.time.Clock()
    

    while run:
        clock.tick(30)
        win.blit(BG_IMG, (0, 0))
        title = STAT_FONT.render("Flappy Bird", True, (255, 255, 255))
        instruction = STAT_FONT.render("Press SPACE to Play", True, (255, 255, 255))
        mode_info = STAT_FONT.render(f"Current Mode: {'AI' if MODE == 'ai' else 'Manual'}", True, (255, 255, 0))
        toggle_info = BUTTON_FONT.render("Press 'A' or Click Box to Toggle", True, (255, 255, 255))
        made_by = BUTTON_FONT.render("~ Made by Uni-Creator", True, (255, 255, 255))

        win.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 200))
        win.blit(instruction, (WIN_WIDTH // 2 - instruction.get_width() // 2, 250))
        win.blit(mode_info, (WIN_WIDTH // 2 - mode_info.get_width() // 2, 300))
        win.blit(toggle_info, (WIN_WIDTH // 2 - toggle_info.get_width() // 2, 350))
        win.blit(made_by,  (WIN_WIDTH // 2 - made_by.get_width() // 2, 500))


        draw_button(win, MODE == "ai")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                if event.key == pygame.K_a:
                    MODE = "ai" if MODE == "manual" else "manual"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 10 <= x <= 170 and 70 <= y <= 110:
                    MODE = "ai" if MODE == "manual" else "manual"

def game_loop():
    global MODE
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    clock = pygame.time.Clock()
    score = 0
    run = True
    high_score = load_high_score()
    SPEED = 30

    while run:
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if MODE == "manual" and event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_a:
                    MODE = "ai" if MODE == "manual" else "manual"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 10 <= x <= 170 and 70 <= y <= 110:
                    MODE = "ai" if MODE == "manual" else "manual"

        if MODE == "ai":
            pipe_ind = 0
            if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
            output = net.activate((bird.y,
                                   abs(bird.y - pipes[pipe_ind].height),
                                   abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        bird.move()

        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                death_screen()
                return

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            if score % 20 == 0:
                SPEED += 10
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            death_screen()
            return

        base.move()

        # Draw everything
        win.blit(BG_IMG, (0, 0))
        for pipe in pipes:
            pipe.draw(win)
        base.draw(win)
        bird.draw(win)
        draw_button(win, MODE == "ai")

        score_text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
        high_score_text = STAT_FONT.render("High Score: " + str(high_score), 1, (255, 215, 0))
        win.blit(score_text, (WIN_WIDTH - score_text.get_width() - 10, 10))
        win.blit(high_score_text, (10, 10))

        pygame.display.update()

if __name__ == '__main__':
    main_menu()
