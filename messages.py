import pygame

class Message:
    def __init__(self, messages, display_surface):
        pygame.init()
        self.display_surface = display_surface
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.timer = pygame.time.Clock()
        self.messages = messages
        self.counter = 0
        self.speed = 3
        self.active_message = 0
        self.message = self.messages[self.active_message]
        self.done = False
        self.running = True
        self.split_screen = True

        # Transition
        self.alpha = 0
        self.transitioning_in = True
        self.transitioning_out = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
                    if not self.done:
                        # Skip typing effect
                        self.counter = self.speed * len(self.message)
                        self.done = True
                    else:
                        # Go to next message or end
                        if self.active_message < len(self.messages) - 1:
                            self.active_message += 1
                            self.message = self.messages[self.active_message]
                            self.counter = 0
                            self.done = False
                        else:
                            self.transitioning_out = True

    def update(self):
        if self.counter < self.speed * len(self.message):
            self.counter += 1
        elif self.counter >= self.speed * len(self.message):
            self.done = True

        if self.transitioning_in:
            self.alpha += 3
            if self.alpha >= 255:
                self.alpha = 255
                self.transitioning_in = False
        elif self.transitioning_out:
            self.alpha -= 3
            if self.alpha <= 0:
                self.alpha = 0
                self.running = False

    def render(self):
        if self.split_screen:
            split_surface = pygame.Surface((1280, 220))
            split_surface.set_alpha(self.alpha)
            split_surface.fill((0, 0, 0))
            self.display_surface.blit(split_surface, (0, 500))

            text = self.font.render(self.message[0:self.counter // self.speed], True, 'white')
            split_surface.blit(text, (10, 10))
            self.display_surface.blit(split_surface, (0, 500))

    def run(self):
        while self.running:
            self.timer.tick(60)
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
