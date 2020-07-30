import pygame
import time
import random
import string
from random_words import RandomWords


pygame.init()

WIDTH, HEIGHT = 1000, 690
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Search")

GREEN = (152,251,152)
BEIGE = (249, 228, 183)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CORAL = (240, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
COLOURS = [BLACK, BEIGE, YELLOW]


class Board:
    TILE_WIDTH = 30
    TILE_HEIGHT = 30
    TITLE_FONT = pygame.font.SysFont("Roboto", 30)
    TILE_FONT = pygame.font.SysFont("Roboto", 22)
    WORD_BANK_FONT = pygame.font.SysFont("Roboto", 16)

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.arr = [[[0, COLOURS[0]] for col in range(self.cols)] for row in range(self.rows)]

    def draw(self):
        # Draw the board
        for row in range(self.rows):
            for col in range(self.cols):
                # Draw the tiles
                pygame.draw.rect(WIN, BEIGE, (col * Board.TILE_WIDTH, row * Board.TILE_HEIGHT, Board.TILE_WIDTH, Board.TILE_WIDTH))
                # Replace the 0 tile with a random letters
                if self.arr[row][col][0] == 0:
                    letter = random.choice(string.ascii_uppercase)
                    self.arr[row][col][0] = letter

                letter_label = Board.TILE_FONT.render(self.arr[row][col][0], 1, self.arr[row][col][1])
                WIN.blit(letter_label, 
                (int(col * Board.TILE_WIDTH + ((Board.TILE_WIDTH - letter_label.get_width()) / 2))
                , int(row * Board.TILE_HEIGHT + ((Board.TILE_HEIGHT - letter_label.get_height()) / 2))))
    
    def draw_wordBank(self, wordBank):
        # WORDS label
        # title_label = Board.TITLE_FONT.render("WORDS", 1, BLACK)
        # WIN.blit(title_label, (self.cols * Board.TILE_WIDTH + 10, 10))
        # Wordbank words
        for i in range(len(wordBank)):
            wb_label = Board.WORD_BANK_FONT.render(wordBank[i][0], 1,wordBank[i][1])
            WIN.blit(wb_label, (self.cols * Board.TILE_WIDTH + 10, (wb_label.get_height() * i * 2) + 10))


    def generate_words(self, numWords):
        # generate a list of random words
        rw = RandomWords()
        words = rw.random_words(count=numWords)
        # convert each word to uppercase
        upperWords = [[word.upper(), CORAL] for word in words]
        return upperWords

    def setup(self, words):
        answers = {}
        for word in words:

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
                # print("----------------------")
                # print(word)
                # print(row,col)
                # print(directions)

                for direction in direction_keys:
                    # Valid direction
                    if directions[direction][2] == 1:
                        # print(direction)
                        # Ensure there will be no overwrites
                        for i in range(wordLength):
                            pos = self.arr[row + (i * directions[direction][1])][col + (i * directions[direction][0])][0]
                            # If position isn't empty (contains a letter already) find a new direction
                            if pos != 0 and pos != word[i]:
                                break
                            # Successfully traversed through whole word and each position is valid
                            if i == wordLength - 1:
                                nextWord = True
                        
                        # Add current word to the board, also it is safe to move on the nextWord
                        if nextWord:
                            ans_value = []
                            for i in range(wordLength):
                                ans_value.append([row + (i * directions[direction][1]), col + (i * directions[direction][0])])
                                self.arr[row + (i * directions[direction][1])][col + (i * directions[direction][0])][0] = word[i]
                            answers[word] = ans_value
                            break
        return answers

        # def checkSolved(self, wordBank, words, answers, clickedRow, clickedCol):
        #     for word in words:
        #         for ans_pos in answers[word]:



                                
def main():
    run = True
    FPS = 60
    boardRows = 23
    boardCols = 25
    numWords = 25

    board = Board(boardRows, boardCols)

    # wordBank will contain a random word and colour code
    wordBank = board.generate_words(numWords)

    # words contains only the words from wordBank
    words = []
    for word in wordBank:
        words.append(word[0])

    # answers is a dict that contains where each letter of each word is on the board
    answers = board.setup(words)


    def redraw():
        pygame.draw.rect(WIN, BLACK, (0, 0, WIDTH, HEIGHT))
        board.draw()
        board.draw_wordBank(wordBank)
        

        pygame.display.update()

    while run:
       
        redraw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                col = mouseX // Board.TILE_WIDTH
                row = mouseY // Board.TILE_HEIGHT
                if(row >= 0 and col >= 0 and row < boardRows and col < boardCols):
                    # board.checkSolved(wordBank, words, answers, col, row)
                    board.arr[row][col][1] = RED

        print(wordBank)
        print('---')
        print(answers)

main()