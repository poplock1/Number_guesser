import numpy as np
import settings as stg
import pygame
import math


class Grid():
    def __init__(self):
        self.rows = stg.grid_x
        self.cols = stg.grid_y
        self.len = stg.grid_x * stg.grid_y
        self.grid = np.zeros((self.rows, self.cols), dtype=float)
        self.block_size = stg.display_x//stg.grid_x

    def draw(self, surface):
        for row in range(self.rows):
            for column in range(self.cols):
                self.rect = pygame.Rect(column*self.block_size, row
                                        * self.block_size, self.block_size, self.block_size)
                if self.grid[row][column] == 0:
                    pygame.draw.rect(surface, stg.WHITE, self.rect)
                if self.grid[row][column] == 1:
                    pygame.draw.rect(surface, stg.BLACK, self.rect)

    def get_pixel(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.pixel = (int(math.floor(self.mouse_pos[1]//self.block_size)), int(
            math.floor(self.mouse_pos[0]//self.block_size)))

    def update(self):
        self.get_pixel()
        if self.grid[self.pixel[0]][self.pixel[1]] == 0:
            self.grid[self.pixel[0] + 1][self.pixel[1] + 1] = 1
            self.grid[self.pixel[0] + 1][self.pixel[1]] = 1
            self.grid[self.pixel[0] + 1][self.pixel[1] - 1] = 1
            self.grid[self.pixel[0] - 1][self.pixel[1] + 1] = 1
            self.grid[self.pixel[0] - 1][self.pixel[1]] = 1
            self.grid[self.pixel[0] - 1][self.pixel[1] - 1] = 1
            self.grid[self.pixel[0]][self.pixel[1] + 1] = 1
            self.grid[self.pixel[0]][self.pixel[1]] = 1
            self.grid[self.pixel[0]][self.pixel[1] - 1] = 1
