import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from popup_text import *
from abc import ABC, abstractmethod

class Sprite(ABC):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.rect = pygame.Rect(position, (TILESIZE, TILESIZE))
        self.image = None

    @abstractmethod
    def enemy_update(self):
        pass

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # message flags
        self.opening_message_displayed = False

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv'),
            'crystal1': import_csv_layout('map/map_crystal1.csv'),
            'crystal2': import_csv_layout('map/map_crystal2.csv'),
            'crystal3': import_csv_layout('map/map_crystal3.csv'),
            'crystal4': import_csv_layout('map/map_crystal4.csv')
        }
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'objects': import_folder('graphics/objects'),
            'crystal1': import_folder('graphics/crystal1'),
            'crystal2': import_folder('graphics/crystal2'),
            'crystal3': import_folder('graphics/crystal3'),
            'crystal4': import_folder('graphics/crystal4')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'grass',
                                random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        if style == 'crystal1':
                            crystal1_image = choice(graphics['crystal1'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'crystal1', crystal1_image)
                        if style == 'crystal2':
                            crystal2_image = choice(graphics['crystal2'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'crystal2', crystal2_image)
                        if style == 'crystal3':
                            crystal3_image = choice(graphics['crystal3'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'crystal3', crystal3_image) 
                        if style == 'crystal4':
                            crystal4_image = choice(graphics['crystal4'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'crystal4', crystal4_image)                        
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                if col == '390': monster_name = 'siHijau'
                                else: monster_name = 'siMerah'
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'nova':
            self.magic_player.nova(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def handle_crystal_collision(self):
        crystal_types = ['crystal1', 'crystal2', 'crystal3', 'crystal4']
        for crystal_type in crystal_types:
            crystals = [sprite for sprite in self.attackable_sprites if sprite.sprite_type == crystal_type]
            for crystal in crystals:
                if crystal.rect.colliderect(self.player.rect):
                    if crystal_type == 'crystal1':
                        message = show_crystal1(self.display_surface)
                        pygame.QUIT()
                    elif crystal_type == 'crystal2':
                        message = show_crystal2(self.display_surface)
                    elif crystal_type == 'crystal3':
                        message = show_crystal3(self.display_surface)
                        pygame.QUIT()
                    elif crystal_type == 'crystal4':
                        message = show_crystal4(self.display_surface)
                        pygame.QUIT()
                    crystal.kill()  # Remove crystal tile after collision

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            if self.player.health <= 0 :
                message = show_death(self.display_surface)
                pygame.QUIT()
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            if not self.opening_message_displayed:
                self.opening_message_displayed = True
                self.opening_message = show_opening_popup(self.display_surface)
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.handle_crystal_collision()  # Check for crystal collision each frame

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__half_width = self.__display_surface.get_size()[0] // 2
        self.__half_height = self.__display_surface.get_size()[1] // 2
        self.__offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.__offset.x = player.rect.centerx - self.__half_width
        self.__offset.y = player.rect.centery - self.__half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.__offset
        self.__display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.__offset
            self.__display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
