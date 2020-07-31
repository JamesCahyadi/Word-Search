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
        self.ans = []
        self.words = []
        self.wordBankColours = []
        self.clicked = []

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
    
    def draw_wordBank(self):
        # WORDS label
        # title_label = Board.TITLE_FONT.render("WORDS", 1, BLACK)
        # WIN.blit(title_label, (self.cols * Board.TILE_WIDTH + 10, 10))
        # Wordbank words
        for i in range(len(self.words)):
            wb_label = Board.WORD_BANK_FONT.render(self.words[i], 1, self.wordBankColours[i])
            WIN.blit(wb_label, (self.cols * Board.TILE_WIDTH + 10, (wb_label.get_height() * i * 2) + 10))


    def generate_words(self, numWords):
        # generate a list of random words
        rw = RandomWords()
        randWords = rw.random_words(count=numWords)

        for word in randWords:
            # convert each word to uppercase and append to words list
            self.words.append(word.upper())
            # default colour for word bank words
            self.wordBankColours.append(CORAL)


    def setup(self):
        for word in self.words:

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
                            self.ans.append(ans_value)
                            break

        for ans_pos_word in self.ans:
            for ans_pos_letter in ans_pos_word:
                self.arr[ans_pos_letter[0]][ans_pos_letter[1]][1] = GREEN

    def checkSolved(self, row, col):
        # append the clicked row and col position onto self.clicked as a list
        self.clicked.append([row, col])
        # The first letter clicked will always be coloured to prevent spam clicking to reveal words
        if len(self.clicked) == 1:
            self.arr[row][col][1] = RED
        # more than two elements in clickd list
        else:
            # iterate through the answers list, one word (sublist) at a time
            #  want to check matches on a per word basis
            for ans_pos_word in self.ans:
                # valid means the clicked are meaningful clicks that are on the right track of making a word
                valid = False
                # matches is the number of list pairs that match in the clicked list and the answers sublist
                matches = 0
                # iterate through the clicked list
                for clicked_pos in self.clicked:
                    if clicked_pos in ans_pos_word:
                        # if the clicked pos matches with a pos in the answers sublist, add a match 
                        matches += 1
                        # change this colour because it is a letter that is part of a word
                        self.arr[clicked_pos[0]][clicked_pos[1]][1] = RED
                
                # word is completed
                if matches and matches == len(self.clicked):
                    valid = True
                    # cross off the word somehow...
                    break

            # clicks are forming a word, reset the clicked array and undo the colour changes that were made to clicked list
            if not valid:
                print("invalid")
                # reset the previously clicked positions to black
                for clicked_pos in self.clicked:
                    self.arr[clicked_pos[0]][clicked_pos[1]][1] = BLACK
                # reset the clicked array
                self.clicked = []
                print(self.clicked)


                                
def main():
    run = True
    FPS = 60
    boardRows = 23
    boardCols = 25
    numWords = 25

    board = Board(boardRows, boardCols)

    # wordBank will contain a random word and colour code
    board.generate_words(numWords)

    # answers is a dict that contains where each letter of each word is on the board
    board.setup()
    print(board.ans)

    def redraw():
        pygame.draw.rect(WIN, BLACK, (0, 0, WIDTH, HEIGHT))
        board.draw()
        board.draw_wordBank()
        

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
                    board.checkSolved(row, col)
                    # board.arr[row][col][1] = RED

main()
