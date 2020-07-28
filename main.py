import pygame
import tensorflow as tf
import sys
import settings as stg
import matplotlib.pyplot as plt
from board import Grid
import gui
import numpy as np

print(tf.__version__)


class Game():
    def __init__(self):
        pygame.init()
        self.game_display = pygame.display.set_mode(
            (stg.display_x, stg.display_y))
        pygame.display.set_caption(stg.display_title)
        self.running = True
        self.guessing = False
        self.drawing = True
        self.clock = pygame.time.Clock()
        self.click = False
        self.prediction_text = None
        self.info_screen = False

    def new_board(self):
        if self.running:
            self.board = Grid(self)

    def new_guess(self):
        self.info_button = gui.Button(stg.button1_x, stg.button1_y, stg.button1_w, stg.button1_h,
                                      stg.button1_text_color, stg.button1_bg, stg.button1_text, stg.button1_font)
        while self.running:
            self.new_board()
            self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.click = False

        self.mouse_pos = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_ESCAPE]:
            self.playing = False
            self.running = False
            pygame.quit()
            sys.exit()
        if self.keys[pygame.K_SPACE]:
            self.drawing = False
            self.guessing = True
        if self.keys[pygame.K_c]:
            self.new_board()

    def update(self):
        self.check_mouse_pos()
        if not self.info_screen:
            if self.drawing:
                if self.click:
                    self.board.update()
            elif self.guessing:
                self.guess()

    def draw(self):
        self.game_display.fill(stg.BG_COLOR)
        self.info_button.draw(self.game_display)
        self.board.draw(self.game_display)
        if self.prediction_text:
            self.prediction_text.draw(self.game_display)
        # if self.info_screen:
        #     self.board.board_info_text.draw(self.game_display)
        pygame.display.update()

    def check_mouse_pos(self):
        if self.click:
            if self.mouse_pos[0] in range(self.info_button.x, self.info_button.x + self.info_button.w):
                if self.mouse_pos[1] in range(self.info_button.y, self.info_button.y + self.info_button.y):
                    if not self.info_screen:
                        self.info_screen = True
                        self.new_board()
                        pygame.time.wait(100)
                    else:
                        self.info_screen = False
                        pygame.time.wait(100)

    def guess(self):
        self.tf_model = tf.keras.models.load_model('num_reader.model')
        # self.data = self.overwriting_data()
        self.data = np.reshape(self.board.grid, (-1, 28, 28))
        self.predictions = self.tf_model.predict(self.data)
        self.prediction = (np.argmax(self.predictions[0]))
        self.prediction_text = gui.TextWindow(stg.text2_x, stg.text2_y, stg.text2_w, stg.text2_h,
                                              stg.text2_text_color, (f'{stg.text2_text}{self.prediction}'), stg.text2_font)
        self.guessing = False
        self.drawing = True

    # def overwriting_data(self):
    #     mnist = tf.keras.datasets.mnist
    #     (x_train, y_train), (x_test, y_test) = mnist.load_data()
    #     x_train = tf.keras.utils.normalize(x_train, axis=1)
    #     x_test = tf.keras.utils.normalize(x_test, axis=1)

    #     for row in range(28):
    #         for col in range(28):
    #             x_test[0][row][col] = self.board.grid[row][col]
    #     plt.imshow(x_test[2])
    #     plt.show()
    #     print(x_test[2])
    #     print(self.board.grid)
    #     return x_test


game = Game()

while game.running:
    game.new_guess()

pygame.quit()
