import pygame
from settings import *


class Upgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.exp_font = pygame.font.Font(UI_FONT, EXP_FONT_SIZE)


        self.width = self.display_surface.get_width() * 0.8
        self.height = 60
        self.padding = 20
        self.create_items()


        self.selection_index = 0
        self.selection_time = None
        self.can_move = True


    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_DOWN] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()


            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)


    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True


    def create_items(self):
        self.item_list = []
        start_y = (self.display_surface.get_height() - (self.height + self.padding) * self.attribute_nr) // 2
        left = (self.display_surface.get_width() - self.width) // 2


        for index in range(self.attribute_nr):
            top = start_y + index * (self.height + self.padding)
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)


    def display(self):
        self.input()
        self.selection_cooldown()


        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)






class Item:
    def __init__(self, x, y, w, h, index, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.index = index
        self.font = font


    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR


        name_surf = self.font.render(f'{name}', False, color)
        cost_surf = self.font.render(f'Cost: {int(cost)}', False, color)


        name_rect = name_surf.get_rect(midleft=(self.rect.left + 10, self.rect.centery - 12))
        cost_rect = cost_surf.get_rect(midleft=(self.rect.left + 10, self.rect.centery + 12))


        surface.blit(name_surf, name_rect)
        surface.blit(cost_surf, cost_rect)


    def display_bar(self, surface, value, max_value, selected):
        bar_max_width = 200
        bar_height = 15
        fill_ratio = value / max_value
        fill_width = int(bar_max_width * fill_ratio)


        bar_x = self.rect.right - bar_max_width - 20
        bar_y = self.rect.centery - bar_height // 2


        bg_rect = pygame.Rect(bar_x, bar_y, bar_max_width, bar_height)
        fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)


        bg_color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        fill_color = 'yellow' if selected else 'white'


        pygame.draw.rect(surface, bg_color, bg_rect, border_radius=5)
        pygame.draw.rect(surface, fill_color, fill_rect, border_radius=5)


    def trigger(self, player):
        upgrade_attr = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[upgrade_attr] and player.stats[upgrade_attr] < player.max_stats[upgrade_attr]:
            player.exp -= player.upgrade_cost[upgrade_attr]
            player.stats[upgrade_attr] *= 1.2
            player.upgrade_cost[upgrade_attr] *= 1.4


            if player.stats[upgrade_attr] > player.max_stats[upgrade_attr]:
                player.stats[upgrade_attr] = player.max_stats[upgrade_attr]


    def display(self, surface, selection_index, name, value, max_value, cost):
        bg_color = UPGRADE_BG_COLOR_SELECTED if self.index == selection_index else UI_BG_COLOR
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 2, border_radius=8)


        self.display_names(surface, name, cost, self.index == selection_index)
        self.display_bar(surface, value, max_value, self.index == selection_index)
