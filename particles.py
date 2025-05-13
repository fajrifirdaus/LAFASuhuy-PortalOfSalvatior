import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic

            'nova': import_folder('graphics/particles/nova/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),

            # attacks 
            'slash': import_folder('graphics/particles/slash'),
            'leaf_attack': import_folder('graphics/particles/leaf_attack'),

            # monster deaths
            'siMerah': import_folder('graphics/particles/siMerah'),
            'siHijau': import_folder('graphics/particles/siHijau'),

            # leafs 
            'leaf': (
                import_folder('graphics/particles/leaf1'),
                import_folder('graphics/particles/leaf2'),
                import_folder('graphics/particles/leaf3'),
                import_folder('graphics/particles/leaf4'),
                import_folder('graphics/particles/leaf5'),
                import_folder('graphics/particles/leaf6'),
                self.reflect_images(import_folder('graphics/particles/leaf1')),
                self.reflect_images(import_folder('graphics/particles/leaf2')),
                self.reflect_images(import_folder('graphics/particles/leaf3')),
                self.reflect_images(import_folder('graphics/particles/leaf4')),
                self.reflect_images(import_folder('graphics/particles/leaf5')),
                self.reflect_images(import_folder('graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        if animation_frames and len(animation_frames) > 0:
            ParticleEffect(pos, animation_frames, groups)
        else:
            print(f"[WARNING] Leaf particle frames kosong!")

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames.get(animation_type)

        # Kalau animasi adalah tuple (misal: leaf)
        if isinstance(animation_frames, tuple):
            animation_frames = choice(animation_frames)

        # Cek apakah frames ada dan tidak kosong
        if animation_frames and len(animation_frames) > 0:
            ParticleEffect(pos, animation_frames, groups)
        else:
            print(f"[WARNING] Particle type '{animation_type}' tidak valid atau kosong!")


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15

        # Proteksi: gunakan surface kosong kalau frames kosong
        if animation_frames and len(animation_frames) > 0:
            self.frames = animation_frames
        else:
            print("[ERROR] ParticleEffect dibuat dengan frames kosong!")
            self.frames = [pygame.Surface((1, 1))]  # fallback aman

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
