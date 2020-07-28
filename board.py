import numpy as np
import settings as stg
import pygame
import math
import gui


class Grid():
    def __init__(self, game):
        self.rows = stg.grid_x
        self.cols = stg.grid_y
        self.len = stg.grid_x * stg.grid_y
        self.grid = np.zeros((self.rows, self.cols), dtype=float)
        self.game_copy = game
        self.block_size = stg.display_x//stg.grid_x
        self.board_text = gui.TextWindow(
            stg.text1_x, stg.text1_y, stg.text1_w, stg.text1_h, stg.text1_text_color, stg.text1_text, stg.text1_font)
        self.board_info_text1 = gui.TextWindow(
            stg.text3_x, stg.text3_y, stg.text3_w, stg.text3_h, stg.text3_text_color, stg.text3_text, stg.text3_font)
        self.board_info_text2 = gui.TextWindow(
            stg.text4_x, stg.text4_y, stg.text4_w, stg.text4_h, stg.text4_text_color, stg.text4_text, stg.text4_font)
        self.board_info_text3 = gui.TextWindow(
            stg.text5_x, stg.text5_y, stg.text5_w, stg.text5_h, stg.text5_text_color, stg.text5_text, stg.text5_font)
        self.board_info_text4 = gui.TextWindow(
            stg.text6_x, stg.text6_y, stg.text6_w, stg.text6_h, stg.text6_text_color, stg.text6_text, stg.text6_font)

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
        if self.game_copy.info_screen:
            self.board_info_text1.draw(surface)
            self.board_info_text2.draw(surface)
            self.board_info_text3.draw(surface)
            self.board_info_text4.draw(surface)
        else:
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
