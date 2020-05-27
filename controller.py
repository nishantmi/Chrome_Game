from pynput.keyboard import Key, Controller
import time
import pygame
from pygame.locals import *

keyboard = Controller()

running = True
while running:
	time.sleep(1)
	keyboard.press(Key.space)
	keyboard.release(Key.space)

	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		running = False
