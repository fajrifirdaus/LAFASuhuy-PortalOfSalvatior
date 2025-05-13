import pygame, sys
from settings import *
from level import Level
from popup_text import *


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('PORTAL OF SALVATIOR')
        self.clock = pygame.time.Clock()
        self.level = Level()


        # load start screen background
        self.start_bg = pygame.image.load('graphics/readme/menu_utama.png').convert()
        self.credits_bg = pygame.image.load('graphics/readme/credits_bg.png').convert()


        # load button
        self.button_start = pygame.image.load('graphics/button/button_start.png').convert_alpha()
        self.button_start_pressed = pygame.image.load('graphics/button/button_start.png').convert_alpha()
        self.button_start_rect = self.button_start.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 100))
        self.button_credits = pygame.image.load('graphics/button/button_credits.png').convert_alpha()
        self.button_credits_pressed = pygame.image.load('graphics/button/button_credits.png').convert_alpha()
        self.button_credits_rect = self.button_credits.get_rect(center=(WIDTH // 2, HEIGTH // 2 ))
        self.button_exit = pygame.image.load('graphics/button/button_exit.png').convert_alpha()
        self.button_exit_pressed = pygame.image.load('graphics/button/button_exit.png').convert_alpha()
        self.button_exit_rect = self.button_exit.get_rect(center=(WIDTH // 2, HEIGTH // 2 + 100))


        # load
        pygame.mixer.init()
        self.background_sound = pygame.mixer.Sound('audio/jungle_sound.mpeg')
        self.background_sound.play(loops=-1)  # play sound in a loop
        self.button_click_sound = pygame.mixer.Sound('audio/click_sound.ogg')
        self.main_sound = pygame.mixer.Sound('audio/main.ogg')
        self.main_sound.set_volume(0.2)


    def show_start_screen(self):
        button_start_pressed = False
        button_credits_pressed = False
        button_exit_pressed = False
        hovered_button = None


        while True:
            self.screen.blit(self.start_bg, (0, 0))


            # Draw the appropriate button images based on the button_pressed state
            if button_start_pressed:
                self.screen.blit(self.button_start_pressed, self.button_start_rect)
            else:
                self.screen.blit(self.button_start, self.button_start_rect)


            if button_credits_pressed:
                self.screen.blit(self.button_credits_pressed, self.button_credits_rect)
            else:
                self.screen.blit(self.button_credits, self.button_credits_rect)


            if button_exit_pressed:
                self.screen.blit(self.button_exit_pressed, self.button_exit_rect)
            else:
                self.screen.blit(self.button_exit, self.button_exit_rect)


            # Change button color if hovered
            if hovered_button == 'start':
                button_surf = pygame.Surface((self.button_start_rect.width, self.button_start_rect.height))
                button_surf.fill((128, 128, 128))
                button_surf.set_alpha(128)
                self.screen.blit(button_surf, self.button_start_rect)
            elif hovered_button == 'credits':
                button_surf = pygame.Surface((self.button_credits_rect.width, self.button_credits_rect.height))
                button_surf.fill((128, 128, 128))
                button_surf.set_alpha(128)
                self.screen.blit(button_surf, self.button_credits_rect)
            elif hovered_button == 'exit':
                button_surf = pygame.Surface((self.button_exit_rect.width, self.button_exit_rect.height))
                button_surf.fill((128, 128, 128))
                button_surf.set_alpha(128)
                self.screen.blit(button_surf, self.button_exit_rect)


            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_start_rect.collidepoint(event.pos):
                        button_start_pressed = True
                        self.button_click_sound.play()  # play button click sound
                    if self.button_credits_rect.collidepoint(event.pos):
                        button_credits_pressed = True
                        self.button_click_sound.play()  # play button click sound
                    if self.button_exit_rect.collidepoint(event.pos):
                        button_exit_pressed = True
                        self.button_click_sound.play()  # play button click sound


                if event.type == pygame.MOUSEBUTTONUP:
                    if button_start_pressed and self.button_start_rect.collidepoint(event.pos):
                        button_start_pressed = False
                        self.background_sound.stop()  # stop the background sound
                        self.main_sound.play(loops=-1)
                        return  # keluar dari fungsi ini dan mulai game
                    if button_credits_pressed and self.button_credits_rect.collidepoint(event.pos):
                        button_credits_pressed = False
                        self.show_credits_screen()
                    if button_exit_pressed and self.button_exit_rect.collidepoint(event.pos):
                        button_exit_pressed = False
                        pygame.quit()
                        sys.exit()


                if event.type == pygame.MOUSEMOTION:
                    # Check if the mouse is hovering over any button
                    if self.button_start_rect.collidepoint(event.pos):
                        hovered_button = 'start'
                    elif self.button_credits_rect.collidepoint(event.pos):
                        hovered_button = 'credits'
                    elif self.button_exit_rect.collidepoint(event.pos):
                        hovered_button = 'exit'
                    else:
                        hovered_button = None


    def show_credits_screen(self):
        credits_font = pygame.font.SysFont('Comic Sans MS', 40)
        credits_lines = [  
        ]


        while True:
            self.screen.blit(self.credits_bg,(0, 0))


            for i, line in enumerate(credits_lines):
                credits_text = credits_font.render(line, True, 'white')
                credits_rect = credits_text.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 100 + i * 50))
                self.screen.blit(credits_text, credits_rect)
               
            # back text
            back_text = credits_font.render('Tap dimana saja untuk kembali', True, 'gray')
            back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGTH - 50))
            self.screen.blit(back_text, back_rect)


            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return


    def run(self):
        self.show_start_screen()  # tampilkan layar awal sebelum game mulai
        # self.opening_message = show_opening_popup(self.display_surface)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()


            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()