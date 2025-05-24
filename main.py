try:
    import pygame
except ImportError:
    print("Kamu belum memiliki modul pygame, silahkan install pygame terlebih dahulu.")
    print("Kamu bisa menginstallnya dengan perintah: *pip install pygame* ")
    import sys
    sys.exit(1)
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
        self.selected_character = None
        self.level = Level()

        # load start screen background
        self.start_bg = pygame.image.load('graphics/readme/menu_utama.png').convert()
        self.OurTeam_bg = pygame.image.load('graphics/readme/OurTeam_bg.png').convert()
        self.guide_bg = pygame.image.load('graphics/readme/guide.png').convert()
        self.character_select_bg = pygame.image.load('graphics/readme/pilih_karakter.png').convert()

        # load button
        self.button_start = pygame.image.load('graphics/button/button_start.png').convert_alpha()
        self.button_start_pressed = pygame.image.load('graphics/button/button_start.png').convert_alpha()
        self.button_start_rect = self.button_start.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 100))

        self.button_OurTeam = pygame.image.load('graphics/button/button_OurTeam.png').convert_alpha()
        self.button_OurTeam_pressed = pygame.image.load('graphics/button/button_OurTeam.png').convert_alpha()
        self.button_OurTeam_rect = self.button_OurTeam.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 100 + 90))

        self.button_guide = pygame.image.load('graphics/button/button_guide.png').convert_alpha()
        self.button_guide_pressed = self.button_guide.copy()
        self.button_guide_rect = self.button_guide.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 100 + 2 * 90))

        self.button_exit = pygame.image.load('graphics/button/button_exit.png').convert_alpha()
        self.button_exit_pressed = pygame.image.load('graphics/button/button_exit.png').convert_alpha()
        self.button_exit_rect = self.button_exit.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 100 + 3 * 90))

        # load
        pygame.mixer.init()
        self.background_sound = pygame.mixer.Sound('audio/jungle_sound.mpeg')
        self.background_sound.play(loops=-1)  # play sound in a loop
        self.button_click_sound = pygame.mixer.Sound('audio/click_sound.ogg')
        self.main_sound = pygame.mixer.Sound('audio/main.ogg')
        self.main_sound.set_volume(0.2)

    def show_start_screen(self):
        button_start_pressed = False
        button_OurTeam_pressed = False
        button_guide_pressed = False
        button_exit_pressed = False
        hovered_button = None

        while True:
            self.screen.blit(self.start_bg, (0, 0))

            # Draw the appropriate button images based on the button_pressed state
            if button_start_pressed:
                self.screen.blit(self.button_start_pressed, self.button_start_rect)
            else:
                self.screen.blit(self.button_start, self.button_start_rect)

            if button_OurTeam_pressed:
                self.screen.blit(self.button_OurTeam_pressed, self.button_OurTeam_rect)
            else:
                self.screen.blit(self.button_OurTeam, self.button_OurTeam_rect)
            
            if button_guide_pressed:
                self.screen.blit(self.button_guide_pressed, self.button_guide_rect)
            else:
                self.screen.blit(self.button_guide, self.button_guide_rect)

            if button_exit_pressed:
                self.screen.blit(self.button_exit_pressed, self.button_exit_rect)
            else:
                self.screen.blit(self.button_exit, self.button_exit_rect)

            if hovered_button:
                hover_rect = getattr(self, f"button_{hovered_button}_rect")
                hover_surf = pygame.Surface(hover_rect.size)
                hover_surf.fill((128, 128, 128))
                hover_surf.set_alpha(128)
                self.screen.blit(hover_surf, hover_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_start_rect.collidepoint(event.pos):
                        button_start_pressed = True
                        self.button_click_sound.play()  # play button click sound
                    if self.button_OurTeam_rect.collidepoint(event.pos):
                        button_OurTeam_pressed = True
                        self.button_click_sound.play()  # play button click sound
                    if self.button_guide_rect.collidepoint(event.pos):
                        button_guide_pressed = True
                        self.button_click_sound.play()
                    if self.button_exit_rect.collidepoint(event.pos):
                        button_exit_pressed = True
                        self.button_click_sound.play()  # play button click sound

                if event.type == pygame.MOUSEBUTTONUP:
                    if button_start_pressed and self.button_start_rect.collidepoint(event.pos):
                        button_start_pressed = False
                        self.background_sound.stop()  # stop the background sound
                        self.main_sound.play(loops=-1)
                        self.show_character_select_screen()
                        return  # keluar dari fungsi ini dan mulai game
                    if button_OurTeam_pressed and self.button_OurTeam_rect.collidepoint(event.pos):
                        button_OurTeam_pressed = False
                        self.show_OurTeam_screen()
                    if button_guide_pressed and self.button_guide_rect.collidepoint(event.pos):
                        button_guide_pressed = False
                        self.show_guide_screen()
                    if button_exit_pressed and self.button_exit_rect.collidepoint(event.pos):
                        button_exit_pressed = False
                        pygame.quit()
                        sys.exit()


                if event.type == pygame.MOUSEMOTION:
                    # Check if the mouse is hovering over any button
                    if self.button_start_rect.collidepoint(event.pos):
                        hovered_button = 'start'
                    elif self.button_OurTeam_rect.collidepoint(event.pos):
                        hovered_button = 'OurTeam'
                    elif self.button_guide_rect.collidepoint(event.pos):
                        hovered_button = 'guide'
                    elif self.button_exit_rect.collidepoint(event.pos):
                        hovered_button = 'exit'
                    else:
                        hovered_button = None

    def show_OurTeam_screen(self):
        while True:
            self.screen.blit(self.OurTeam_bg,(0, 0))
  
            # back text
            OurTeam_font = pygame.font.SysFont('Comic Sans MS', 40)
            back_text = OurTeam_font.render('Tap dimana saja untuk kembali', True, 'gray')
            back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGTH - 50))
            self.screen.blit(back_text, back_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
                
    def show_guide_screen(self):
        while True:
            self.screen.blit(self.guide_bg,(0, 0))
  
            # back text
            guide_font = pygame.font.SysFont('Comic Sans MS', 40)
            back_text = guide_font.render('Tap dimana saja untuk kembali', True, 'gray')
            back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGTH - 50))
            self.screen.blit(back_text, back_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

    def show_character_select_screen(self):
        original_char1 = pygame.image.load('graphics/characters/char1.png').convert_alpha()
        original_char2 = pygame.image.load('graphics/characters/char2.png').convert_alpha()

        base_scale = 1.5
        hover_scale = 1.7
        current_scale1 = base_scale
        current_scale2 = base_scale

        font = pygame.font.Font(UI_FONT, 30)
        instruction = font.render("Pilih Karakter", True, 'white')
        hovered = None

        while True:
            self.screen.blit(self.character_select_bg, (0, 0))
            self.screen.blit(instruction, instruction.get_rect(center=(WIDTH // 2, 100)))

            target_scale1 = hover_scale if hovered == 'char1' else base_scale
            target_scale2 = hover_scale if hovered == 'char2' else base_scale
            current_scale1 += (target_scale1 - current_scale1) * 0.1
            current_scale2 += (target_scale2 - current_scale2) * 0.1

            size1 = (int(original_char1.get_width() * current_scale1), int(original_char1.get_height() * current_scale1))
            size2 = (int(original_char2.get_width() * current_scale2), int(original_char2.get_height() * current_scale2))
            character1_img = pygame.transform.smoothscale(original_char1, size1)
            character2_img = pygame.transform.smoothscale(original_char2, size2)

            char1_rect = character1_img.get_rect(center=(WIDTH // 3, HEIGTH // 2))
            char2_rect = character2_img.get_rect(center=(2 * WIDTH // 3, HEIGTH // 2))

            if hovered == 'char1':
                glow = pygame.Surface(char1_rect.size, pygame.SRCALPHA)
                pygame.draw.ellipse(glow, (0, 0, 139, 80), glow.get_rect())
                self.screen.blit(glow, char1_rect)
            elif hovered == 'char2':
                glow = pygame.Surface(char2_rect.size, pygame.SRCALPHA)
                pygame.draw.ellipse(glow, (0, 0, 139, 80), glow.get_rect())
                self.screen.blit(glow, char2_rect)

            self.screen.blit(character1_img, char1_rect)
            self.screen.blit(character2_img, char2_rect)

            pygame.display.update()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    if char1_rect.collidepoint(event.pos):
                        hovered = 'char1'
                    elif char2_rect.collidepoint(event.pos):
                        hovered = 'char2'
                    else:
                        hovered = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if char1_rect.collidepoint(event.pos):
                        self.selected_character = 'char1'
                        self.level = Level(selected_character=self.selected_character)
                        return
                    elif char2_rect.collidepoint(event.pos):
                        self.selected_character = 'char2'
                        self.level = Level(selected_character=self.selected_character)
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
                    if event.key == pygame.K_p:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()