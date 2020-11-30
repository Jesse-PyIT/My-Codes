#WOF_AI
import random, time
class AI:
    def __init__(self, name, score, endTurn=False):
        self.name = name
        self.score = score
        self.endTurn = endTurn
        self.correctLetters = 0

    def guess(self):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        chosenLetter = random.choice(letters)
        print(str(self.name.title() + ' has guessed: ' + chosenLetter.upper()).center(127))
        return chosenLetter

    def spin(self, wheel):
        value = random.choice(wheel)
        '''Add code for wheel value landing on bankrupt and free play'''
        return value
    
    def editScore(self, value, add=True):
        if add == True:
            self.score += value
        else:
            self.score -= value
        print(str(self.name.title() + '\'s new score is ' + str(self.score)).center(127))

    #shuffling each word in the puzzle 50 times
    #to generate a random guess of the whole puzzle
    #thus giving the AI player somewhat of a chance
    #to guess the puzzle correctly and add a more
    #realistic feel for the human players
    def solve(self, puzzle):
        solveGuess = False
        pSplit = puzzle.split()
        aiPuzzleGuess = []
        for i in pSplit:
            for y in range(50):
                RI = random.sample(i, len(i))
                riJ = ''.join(RI)
                if riJ == i:
                    aiPuzzleGuess.append(riJ)
                    break
                elif riJ != i:
                    continue
            if riJ != i:
                aiPuzzleGuess.append(riJ)
        aiPG = ' '.join(aiPuzzleGuess)
        return aiPG
