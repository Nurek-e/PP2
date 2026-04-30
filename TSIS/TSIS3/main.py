import pygame
import sys

from ui import Button
from racer import RacerGame, WIDTH, HEIGHT
from persistence import load_settings, save_settings, load_leaderboard


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
BLUE = (80, 170, 255)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("Verdana", 22)
big_font = pygame.font.SysFont("Verdana", 42)

settings = load_settings()

state = "menu"
username = ""
game = None


def draw_title(text):
    title = big_font.render(text, True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))


def username_screen():
    global username, state

    input_active = True

    while input_active:
        screen.fill(GRAY)

        draw_title("Enter your name")

        name_text = font.render(username + "|", True, WHITE)
        screen.blit(name_text, name_text.get_rect(center=(WIDTH // 2, 250)))

        hint = font.render("Press Enter to continue", True, YELLOW)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 320)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username == "":
                        username = "Player"

                    state = "game"
                    input_active = False

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    if len(username) < 12:
                        username += event.unicode

        pygame.display.update()
        clock.tick(60)


def main_menu():
    global state, username

    play_btn = Button(150, 180, 200, 55, "Play")
    lead_btn = Button(150, 250, 200, 55, "Leaderboard")
    settings_btn = Button(150, 320, 200, 55, "Settings")
    quit_btn = Button(150, 390, 200, 55, "Quit")

    while state == "menu":
        screen.fill(GRAY)

        draw_title("Racer Game")

        play_btn.draw(screen, font)
        lead_btn.draw(screen, font)
        settings_btn.draw(screen, font)
        quit_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play_btn.is_clicked(event):
                username = ""
                state = "username"

            if lead_btn.is_clicked(event):
                state = "leaderboard"

            if settings_btn.is_clicked(event):
                state = "settings"

            if quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen():
    global state

    back_btn = Button(150, 610, 200, 50, "Back")

    while state == "leaderboard":
        screen.fill(GRAY)

        draw_title("Top 10 Leaderboard")

        data = load_leaderboard()

        y = 150

        if len(data) == 0:
            empty = font.render("No scores yet", True, WHITE)
            screen.blit(empty, empty.get_rect(center=(WIDTH // 2, 250)))
        else:
            for i, item in enumerate(data):
                text = f"{i + 1}. {item['name']} | Score: {item['score']} | Distance: {item['distance']}"
                line = font.render(text, True, WHITE)
                screen.blit(line, (40, y))
                y += 40

        back_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_btn.is_clicked(event):
                state = "menu"

        pygame.display.update()
        clock.tick(60)


def settings_screen():
    global state, settings

    sound_btn = Button(100, 180, 300, 50, "Sound: " + str(settings["sound"]))
    color_btn = Button(100, 250, 300, 50, "Car Color: " + settings["car_color"])
    diff_btn = Button(100, 320, 300, 50, "Difficulty: " + settings["difficulty"])
    back_btn = Button(100, 430, 300, 50, "Back")

    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while state == "settings":
        screen.fill(GRAY)

        draw_title("Settings")

        sound_btn.text = "Sound: " + str(settings["sound"])
        color_btn.text = "Car Color: " + settings["car_color"]
        diff_btn.text = "Difficulty: " + settings["difficulty"]

        sound_btn.draw(screen, font)
        color_btn.draw(screen, font)
        diff_btn.draw(screen, font)
        back_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if sound_btn.is_clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if color_btn.is_clicked(event):
                index = colors.index(settings["car_color"])
                index = (index + 1) % len(colors)
                settings["car_color"] = colors[index]
                save_settings(settings)

            if diff_btn.is_clicked(event):
                index = difficulties.index(settings["difficulty"])
                index = (index + 1) % len(difficulties)
                settings["difficulty"] = difficulties[index]
                save_settings(settings)

            if back_btn.is_clicked(event):
                state = "menu"

        pygame.display.update()
        clock.tick(60)


def game_over_screen():
    global state, game

    retry_btn = Button(150, 420, 200, 55, "Retry")
    menu_btn = Button(150, 500, 200, 55, "Main Menu")

    while state == "game_over":
        screen.fill((130, 0, 0))

        title = big_font.render("Game Over", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

        score_text = font.render("Score: " + str(game.score), True, WHITE)
        distance_text = font.render("Distance: " + str(game.distance), True, WHITE)
        coins_text = font.render("Coins: " + str(game.coins_count), True, WHITE)

        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, 220)))
        screen.blit(distance_text, distance_text.get_rect(center=(WIDTH // 2, 260)))
        screen.blit(coins_text, coins_text.get_rect(center=(WIDTH // 2, 300)))

        retry_btn.draw(screen, font)
        menu_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if retry_btn.is_clicked(event):
                game = RacerGame(screen, username, settings)
                state = "game"

            if menu_btn.is_clicked(event):
                state = "menu"

        pygame.display.update()
        clock.tick(60)


def run_game():
    global state, game

    game = RacerGame(screen, username, settings)

    while state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        is_over = game.run_frame()

        if is_over:
            pygame.mixer.Sound("assets/crash.wav").play()
            state = "game_over"

        pygame.display.update()
        clock.tick(60)


while True:
    if state == "menu":
        main_menu()

    elif state == "username":
        username_screen()

    elif state == "game":
        run_game()

    elif state == "game_over":
        game_over_screen()

    elif state == "leaderboard":
        leaderboard_screen()

    elif state == "settings":
        settings_screen()