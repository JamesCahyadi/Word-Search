import pygame
import time
import random
import string
from random_words import RandomWords
import os


pygame.font.init()

WIDTH, HEIGHT = 1030, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Search")

#Load Image
MENU_BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "menu_background.jpg")), (WIDTH, HEIGHT))

BEIGE = (249, 228, 183)
BLACK = (0, 0, 0)
YELLOW = (255, 212, 100)
CORAL = (240, 128, 128)
BLUE = (21, 101, 192)
DARKBLUE = (15, 79, 153)
WHITE = (255, 255, 255)


class Board:
    TILE_WIDTH = 30
    TILE_HEIGHT = 30
    TITLE_FONT = pygame.font.SysFont("Roboto", 30)
    TILE_FONT = pygame.font.SysFont("Roboto", 25)
    WORD_BANK_FONT = pygame.font.SysFont("Roboto", 18)

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # list of the board letters
        self.board = []
        # list of the colours of each board letter
        self.boardColours = []
        # list of the positions of each answer letter
        self.ans = []
        # list of the positions that the player clicked
        self.clicked = []
        # list of the letters that have been solved: 1 means solved, 0 means unsolved or random letter
        self.locked = []
        # list of the word bank words
        self.words = []
        # list of the word bank word's colours
        self.wordBankColours = []
        # list of the reveal buttons
        self.buttons = []
        # list of the reveal button's colours
        self.buttonColours = [] 

        for row in range(self.rows):
            boardRow = []
            boardRowColours = []
            lockedRow = []
            for col in range(self.cols):
                boardRow.append(0)
                boardRowColours.append(BLACK)
                lockedRow.append(0)

            # fill the board and locked list's with zeroes
            self.board.append(boardRow)
            self.locked.append(lockedRow)

            # all the board letters default to black
            self.boardColours.append(boardRowColours)

    def draw(self):
        self.drawBoard()
        self.draw_wordBank()
        self.draw_progress()
        self.draw_buttons()

    def drawBoard(self):
        # Draw the board
        for row in range(self.rows):
            for col in range(self.cols):
                # Draw the tiles
                pygame.draw.rect(WIN, WHITE, 
                (Board.TILE_WIDTH + (col * Board.TILE_WIDTH), Board.TILE_HEIGHT + (row * Board.TILE_HEIGHT), Board.TILE_WIDTH, Board.TILE_HEIGHT))
                # Replace the 0 tile with a random letter
                if self.board[row][col] == 0:
                    letter = random.choice(string.ascii_uppercase)
                    self.board[row][col] = letter

                # draw the letters
                letter_label = Board.TILE_FONT.render(self.board[row][col], 1, self.boardColours[row][col])
                WIN.blit(letter_label, 
                (int(Board.TILE_WIDTH + (col * Board.TILE_WIDTH) + ((Board.TILE_WIDTH - letter_label.get_width()) / 2))
                , int(Board.TILE_HEIGHT + (row * Board.TILE_HEIGHT) + ((Board.TILE_HEIGHT - letter_label.get_height()) / 2))))
    
    def draw_wordBank(self):
        # word bank rectangle background
        pygame.draw.rect(WIN, WHITE, (Board.TILE_WIDTH * 1.5 + self.cols * Board.TILE_WIDTH, Board.TILE_HEIGHT,
        WIDTH - (Board.TILE_WIDTH * 1.5 + self.cols * Board.TILE_WIDTH) - Board.TILE_WIDTH, HEIGHT - (Board.TILE_HEIGHT * 2)))

        # draw the words in the word bank
        for i in range(len(self.words)):
            wb_label = Board.WORD_BANK_FONT.render(self.words[i], 1, self.wordBankColours[i])
            WIN.blit(wb_label, (Board.TILE_WIDTH * 2 + self.cols * Board.TILE_WIDTH, Board.TILE_HEIGHT + (wb_label.get_height() * i * 2) + 10))

    def draw_progress(self):
        completed = 0
        # count the number of complete words
        for colour in self.wordBankColours:
            if colour != BLACK:
                completed += 1

        # display how many words are completed
        progress_label = Board.WORD_BANK_FONT.render(f"Progress: {completed}/{len(self.wordBankColours)} | Press r to play again", 1, BLACK)
        WIN.blit(progress_label, (Board.TILE_WIDTH * 2 + self.cols * Board.TILE_WIDTH, HEIGHT - progress_label.get_height() - 30))

    def draw_buttons(self):
        reveal_label = Board.WORD_BANK_FONT.render("Reveal", 1, WHITE)
        padding = 5
        for i in range(len(self.words)):
            btnX = WIDTH - Board.TILE_WIDTH * 3 - padding
            btnY = Board.TILE_HEIGHT + (reveal_label.get_height() * i * 2) + 10 - padding
            btnWidth = reveal_label.get_width() + padding * 2
            btnHeight = reveal_label.get_height() + padding * 2

            self.buttons.append([btnX, btnY, btnWidth, btnHeight])
            # draw the reveal buttons
            pygame.draw.rect(WIN, self.buttonColours[i], self.buttons[i])
            WIN.blit(reveal_label, (btnX + padding, btnY + padding))

    def get_buttons(self):
        return self.buttons

    def button_clicked(self, index):
        self.word_completed(index)

    def setup_board(self):
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

                for direction in direction_keys:
                    # Valid direction
                    if directions[direction][2] == 1:
                        # Ensure there will be no overlap of different letter
                        for i in range(wordLength):
                            pos = self.board[row + (i * directions[direction][1])][col + (i * directions[direction][0])]
                            # If position isn't empty (contains a letter already) find a new direction
                            if pos != 0 and pos != word[i]:
                                break
                            # Successfully traversed through whole word and each position is valid
                            if i == wordLength - 1:
                                nextWord = True
                        
                        # Add current word to the board, also it is safe to move on the nextWord
                        if nextWord:
                            # list to keep track of the positions of the letters that make up a word
                            ans_value = []
                            for i in range(wordLength):
                                ans_value.append([row + (i * directions[direction][1]), col + (i * directions[direction][0])])
                                self.board[row + (i * directions[direction][1])][col + (i * directions[direction][0])] = word[i]
                            # append to answers list
                            self.ans.append(ans_value)
                            break

        # Highlight all the answers
        # for ansPosWord in self.ans:
        #     for ansPos_letter in ansPosWord:
        #         self.boardColours[ansPos_letter[0]][ansPos_letter[1]] = GREEN
    
    def generate_words(self, numWords):
        # generate a list of random words
        rw = RandomWords()
        randWords = rw.random_words(count=numWords)

        for word in randWords:
            # convert each word to uppercase and append to words list
            self.words.append(word.upper())
            # default colour for word bank words
            self.wordBankColours.append(BLACK)
            # default button colours
            self.buttonColours.append(BLUE)

    def check_solved(self, row, col):
        # append unique clicked row and col positions onto self.clicked
        if [row, col] not in self.clicked:
            self.clicked.append([row, col])
        # The first letter clicked will always be coloured to prevent spam clicking to reveal words
        if len(self.clicked) == 1:
            self.boardColours[row][col] = YELLOW
        # more than two elements in clickd list
        else:
            # iterate through the answers list, one word (sublist) at a time
            #  want to check matches on a per word basis
            for ansPosWord in self.ans:
                # valid means the clicked are meaningful clicks that are on the right track of making a word
                valid = False
                # matches is the number of list pairs that match in the clicked list and the answers sublist
                matches = 0
                # iterate through the clicked list
                for clickedPos in self.clicked:
                    if clickedPos in ansPosWord:
                        # if the clicked pos matches with a pos in the answers sublist, add a match 
                        matches += 1
                        # change this colour because it is a letter that is part of a word
                        self.boardColours[clickedPos[0]][clickedPos[1]] = YELLOW
                
                # letter being clicked are of the some word
                if matches and matches == len(self.clicked):
                    # word is complete
                    if matches == len(ansPosWord):
                        self.word_completed(self.ans.index(ansPosWord))

                    valid = True
                    break

            # clicks are not forming a word, reset the clicked list and undo the colour changes that were made to clicked list
            if not valid:
                # reset the previously clicked positions to black
                for clickedPos in self.clicked:
                    # Turn letter back into default colour
                    if self.locked[clickedPos[0]][clickedPos[1]] == 0:
                        self.boardColours[clickedPos[0]][clickedPos[1]] = BLACK
                    # Turn letter back into solved word colour
                    else:
                        self.boardColours[clickedPos[0]][clickedPos[1]] = CORAL
                # reset the clicked boarday
                self.clicked = []
                # the most recently clicked letter should remain coloured
                self.clicked.append([row, col])
                self.boardColours[row][col] = YELLOW

    def word_completed(self, index):
        # the clicked button should be dark blue, the word corresponding to that button should now be coral
        self.wordBankColours[index] = CORAL
        self.buttonColours[index] = DARKBLUE

        for ansPos in self.ans[index]:
            # the letters for that word should be coral on the board game
            self.boardColours[ansPos[0]][ansPos[1]] = CORAL
            # the tiles with the completed word are now locked (colour can't change)
            self.locked[ansPos[0]][ansPos[1]] = 1

        # reset clicked list
        self.clicked = []

                                
def main(numRows, numCols, numWords):
    run = True
    FPS = 60
    boardRows = numRows
    boardCols = numCols
    numWords = numWords

    clock = pygame.time.Clock()
    board = Board(boardRows, boardCols)
    board.generate_words(numWords)
    board.setup_board()

    def redraw():
        pygame.draw.rect(WIN, BEIGE, (0, 0, WIDTH, HEIGHT))
        board.draw()
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                col = (mouseX - Board.TILE_WIDTH) // Board.TILE_WIDTH
                row = (mouseY - Board.TILE_HEIGHT) // Board.TILE_HEIGHT
                # player pressed a letter, check if a word got solved or is on the way to being solved
                if row >= 0 and col >= 0 and row < boardRows and col < boardCols:
                    board.check_solved(row, col)
                
                btns = board.get_buttons()
                for btn in btns:
                    btnX = btn[0]
                    btnY = btn[1]
                    btnWidth = btn[2]
                    btnHeight = btn[3]
                    if mouseX >= btnX and mouseX <= btnX + btnWidth and mouseY >= btnY and mouseY <= btnY + btnHeight:
                        btnIndex = btns.index(btn)
                        board.button_clicked(btnIndex)
                        break

        keys = pygame.key.get_pressed()
        # r to restart the game
        if keys[pygame.K_r]:
            # recall main function
            main(numRows, numCols, numWords)

def menu():
    run = True
    TITLE_FONT = pygame.font.SysFont("Roboto", 70)
    SETTINGS_FONT = pygame.font.SysFont("Roboto", 30)
    SUBTITLE_FONT = pygame.font.SysFont("Roboto", 25)

    # number of rows in the board
    minRows = 18
    maxRows = 22
    numRows = maxRows

    # number of columns in the board
    minCols = 18
    maxCols = 24
    numCols = maxCols

    # number of words in the word bank
    minWords = 10
    maxWords = 24
    numWords = maxWords

    def increment(min, max, num):
        num += 1
        if(num > max):
            num = min
        return num

    # main menu
    while run:
        WIN.blit(MENU_BACKGROUND, (0, 0))
        pygame.draw.rect(WIN, WHITE, (200, 150, WIDTH - 400, HEIGHT - 400))

        TITLE_LABEL = TITLE_FONT.render("Welcome to Word Search", 1, BLACK)
        WIN.blit(TITLE_LABEL, (int((WIDTH - TITLE_LABEL.get_width())/2), 200))

        NUM_WORDS_LABEL = SETTINGS_FONT.render(f"Number of Words ({minWords}-{maxWords}): {numWords} | Press a to change", 1, BLACK)
        WIN.blit(NUM_WORDS_LABEL, (int((WIDTH - NUM_WORDS_LABEL.get_width())/2), 300))

        NUM_ROWS_LABEL = SETTINGS_FONT.render(f"Number of Rows ({minRows}-{maxRows}): {numRows} | Press s to change", 1, BLACK)
        WIN.blit(NUM_ROWS_LABEL, (int((WIDTH - NUM_ROWS_LABEL.get_width())/2), 350))

        NUM_COLS_LABEL = SETTINGS_FONT.render(f"Number of Columns ({minCols}-{maxCols}): {numCols} | Press d to change", 1, BLACK)
        WIN.blit(NUM_COLS_LABEL, (int((WIDTH - NUM_COLS_LABEL.get_width())/2), 400))

        PLAY_LABEL = SUBTITLE_FONT.render("Click anywhere to begin...", 1, WHITE, BLUE)
        WIN.blit(PLAY_LABEL, (WIDTH - PLAY_LABEL.get_width(), HEIGHT - PLAY_LABEL.get_height()))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # click anywhere to play
            if event.type == pygame.MOUSEBUTTONDOWN:
                main(numRows, numCols, numWords)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    numWords = increment(minWords, maxWords, numWords)
                if event.key == pygame.K_s:
                    numRows = increment(minRows, maxRows, numRows)
                if event.key == pygame.K_d:
                    numCols = increment(minCols, maxCols, numCols)

menu()
