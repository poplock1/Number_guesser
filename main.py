import pygame
import tensorflow as tf
import sys
import settings as stg
import matplotlib.pyplot as plt
from board import Grid
import gui
import cv2
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

    def new_board(self):
        if self.running:
            self.board = Grid()

    def new_guess(self):
        while self.running:
            self.new_board()
            self.run()
            if self.restart():
                self.running = True
            else:
                self.running = False

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

        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_ESCAPE]:
            self.playing = False
            self.running = False
            pygame.quit()
            sys.exit()
        if self.keys[pygame.K_SPACE]:
            self.drawing = False
            self.guessing = True

    def update(self):
        if self.drawing:
            if self.click:
                self.board.update()
        elif self.guessing:
            self.guess()

    def draw(self):
        self.game_display.fill(stg.BG_COLOR)
        self.board.draw(self.game_display)
        pygame.display.update()

    def restart(self):
        pass

    def guess(self):
        self.tf_model = tf.keras.models.load_model('num_reader.model')
        # self.data = self.overwriting_data()
        self.data = np.reshape(self.board.grid, (-1, 28, 28))
        self.predictions = self.tf_model.predict(self.data)
        print(self.predictions[0])
        self.prediction = (np.argmax(self.predictions[0]))
        print("I predict this number is a:", self.prediction)
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
    #     plt.imshow(x_test[0])
    #     plt.show()
    #     return x_test


game = Game()

while game.running:
    game.new_guess()

pygame.quit()
