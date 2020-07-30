import pygame
import time
import random
import string
from random_words import RandomWords


pygame.font.init()

WIDTH, HEIGHT = 1000, 660
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Search")


class Board:
    TILE_WIDTH = 30
    TILE_HEIGHT = 30
    TITLE_FONT = pygame.font.SysFont("Roboto", 20, 1)

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.arr = [[0 for col in range(self.cols)] for row in range(self.rows)]

    def draw(self, window):
        white = (255, 255, 255)
        green = (0, 255, 0)
        for row in range(self.rows):
            for col in range(self.cols):
                # Draw the tiles
                pygame.draw.rect(window, white, (col * Board.TILE_WIDTH, row * Board.TILE_HEIGHT, Board.TILE_WIDTH, Board.TILE_WIDTH), 1)
                # Replace the 0 tiles with random letters
                if self.arr[row][col] == 0:
                    # Draw the letters
                    letter_label = Board.TITLE_FONT.render(random.choice(string.ascii_uppercase), 1, white)
                    WIN.blit(letter_label, 
                    (int(col * Board.TILE_WIDTH + ((Board.TILE_WIDTH - letter_label.get_width()) / 2))
                    , int(row * Board.TILE_HEIGHT + ((Board.TILE_HEIGHT - letter_label.get_height()) / 2))))
                else:
                    letter_label = Board.TITLE_FONT.render(self.arr[row][col], 1, green)
                    WIN.blit(letter_label, 
                    (int(col * Board.TILE_WIDTH + ((Board.TILE_WIDTH - letter_label.get_width()) / 2))
                    , int(row * Board.TILE_HEIGHT + ((Board.TILE_HEIGHT - letter_label.get_height()) / 2))))


    def generate_words(self, numWords):
        # generate a list of random words
        rw = RandomWords()
        words = rw.random_words(count=numWords)
        # convert each word to uppercase
        upperWords = [word.upper() for word in words]
        return upperWords

    def setup(self, wordBank):
        print(wordBank)
        for word in wordBank:

            wordLength = len(word)
            nextWord = False

            while not nextWord:
                row = random.choice(range(self.rows))
                col = random.choice(range(self.cols))

                # dictionary to determine how to build word onto board [x, y, valid]
                directions = {
                    "up": [0, -1, 1],
                    "down": [0, 1, 1],
                    "right": [1, 0, 1],
                    "left": [-1, 0, 1],
                    "upright": [1, -1, 1],
                    "upleft": [-1, -1, 1],
                    "downright": [1, 1, 1],
                    "downleft": [-1, 1, 1]
                }

                # Determine which directions are invalid, give the word length and (row, col)
                if col + wordLength > self.cols:
                    directions["right"][2] = 0
                    directions["upright"][2] = 0
                    directions["downright"][2] = 0

                if col - wordLength < 0:
                    directions["left"][2] = 0
                    directions["upleft"][2] = 0
                    directions["downleft"][2] = 0

                if row - wordLength < 0:
                    directions["up"][2] = 0
                    directions["upleft"][2] = 0
                    directions["upright"][2] = 0

                if row + wordLength > self.rows:
                    directions["down"][2] = 0
                    directions["downleft"][2] = 0
                    directions["downright"][2] = 0

                # Create and shuffle the directions so that words directions will be more random
                # Create a list of the directions
                direction_keys = list(directions.keys())
                # Shuffles the directions list
                random.shuffle(direction_keys)
                print("----------------------")
                print(word)
                print(row,col)
                print(directions)

                for direction in direction_keys:
                    # Valid direction
                    if directions[direction][2] == 1:
                        print(direction)
                        for i in range(wordLength):
                            # If position is empty (0)
                            if self.arr[row + (i * directions[direction][1])][col + (i * directions[direction][0])] == 0:
                                self.arr[row + (i * directions[direction][1])][col + (i * directions[direction][0])] = word[i]
                            # If position isn't empty (contains a letter already) find a new direction
                            else:
                                break

                            # Successfully traversed through whole word
                            if(i == wordLength - 1):
                                nextWord = True

                        if nextWord:
                            break
                                
def main():
    run = True
    FPS = 60
    boardRows = 22
    boardCols = 25
    numWords = 5

    board = Board(boardRows, boardCols)
    wordBank = board.generate_words(numWords)
    board.setup(wordBank)
    board.draw(WIN)

    def redraw():
        # pygame.draw.rect(WIN, (169,169,169), (0, 0, WIDTH, HEIGHT))

        pygame.display.update()

    while run:
       
        redraw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False



# rw = RandomWords()
# words = rw.random_words(count=10)
# print(words)

# words = rw.random_words(count=10)
# print(words)

main()