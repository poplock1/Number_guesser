import numpy as np
import settings as stg
import pygame
import math
import gui


class Grid():
    def __init__(self):
        self.rows = stg.grid_x
        self.cols = stg.grid_y
        self.len = stg.grid_x * stg.grid_y
        self.grid = np.zeros((self.rows, self.cols), dtype=float)
        self.block_size = stg.display_x//stg.grid_x
        self.board_text = gui.TextWindow(
            stg.text1_x, stg.text1_y, stg.text1_w, stg.text1_h, stg.text1_text_color, stg.text1_text, stg.text1_font)

    def draw(self, surface):
        for row in range(self.rows):
            for column in range(self.cols):
                self.rect = pygame.Rect(column*self.block_size, row
                                        * self.block_size, self.block_size, self.block_size)
                if self.grid[row][column] == 0:
                    pygame.draw.rect(surface, stg.WHITE, self.rect)
                if self.grid[row][column] == 1:
                    pygame.draw.rect(surface, stg.BLACK, self.rect)
        self.board_rect = pygame.Rect(
            0, 0, (self.rows*self.block_size), (self.cols*self.block_size))
        pygame.draw.rect(surface, stg.GREY, self.board_rect, 6)
        self.info_rect = pygame.Rect(0, 560, self.rows*self.block_size,
                                     150)
        pygame.draw.rect(surface, stg.GREY, self.info_rect, 6)
        if 1 not in self.grid:
            self.board_text.draw(surface)

    def get_pixel(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.pixel = (int(math.floor(self.mouse_pos[1]//self.block_size)), int(
            math.floor(self.mouse_pos[0]//self.block_size)))

    def update(self):
        self.get_pixel()
        if self.pixel[0] in range(27) and self.pixel[1] in range(27):
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
