import pygame
from math import sin
from abc import ABC, abstractmethod

class Entity(ABC,pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.frame_index = 0
		self.animation_speed = 0.15
		self.direction = pygame.math.Vector2()
	
	@abstractmethod
	def move(self,speed):
		pass
	@abstractmethod
	def collision(self,direction):
		pass
	@abstractmethod
	def wave_value(self):
		pass