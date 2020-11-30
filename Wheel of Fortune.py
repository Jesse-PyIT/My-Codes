#Wheel of Fortune (Started: 5-27-2019 10:52pm Monday)
#(Finished v1.0: 7-3-2019 11:34pm)
#(Updated & Finished v2.0: 7-22-2019 12:41am)
#Developer(s): Jesse Douglas
import random, time, WOF_AI
from WOF_AI import *

print('Welcome to Wheel of Fortune!'.center(127))
print('Created by: JDgames | Developer(s): Jesse Douglas | Version 2.0'.center(127))

print('\n' + '\5 Game Rules \5'.center(127))
print('\775 BONUS PUZZLE \775.'.center(127))
print('\a The bonus round will display one letter at a time until a fixed'.center(127))
print('number of letters have been displayed.'.center(127))
print('\a After the puzzle is done displaying the fixed number of letters,'.center(127))
print('each player will have a chance to guess the puzzle.'.center(127))
print('\a If each player does not guess correctly, the puzzle will display one more letter.'.center(127) + '\n')
print('\a If the players continue to guess incorrectly, this process will persist'.center(127))
print('until the puzzle has displayed all of the letters in the bonus puzzle.'.center(127))
print('\a If all of the letters have been displayed in the puzzle without one of'.center(127))
print('the players guessing the puzzle correctly, a random player will be chosen'.center(127))
print('to recieve the reward for the bonus puzzle.\n'.center(127))
print('\775 Rounds \u2776, \u2777, \u2778 \775'.center(127) + '\n')
print('\a When we begin our rounds, the player will spin the wheel at the start of their turn.'.center(127))
print('\a The player will then guess a letter they think might be in the puzzle.'.center(127))
print('\a If the player guesses a correct letter, they will be asked if they want to either'.center(127))
print('Spin, Solve, or Pass.'.center(127))
print('\a If the player chooses to solve, the will have to guess the puzzle while including spaces.'.center(127))
print('\a If the player guesses the puzzle incorrectly, their turn will end and the next player will begin their turn\n'.center(127))    
print('\a When the puzzle of the round displays enough letters, the player will be asked'.center(127))
print('if they would like to attempt to solve the puzzle.'.center(127))
print('\a If the player\'s guess to solve the puzzle is incorrect,'.center(127))
print('that player\'s turn will continue as normal.\n'.center(127))
print('\u2699 Extras \u2699'.center(127))
print('\a When puzzles are displayed and the player sees a "_"(underscore) symbol,'.center(127))
print('that signifies a space in the puzzle and the player will not have to'.center(127))
print('use up a guess for any spaces that may be in the puzzle'.center(127))

print('Good Luck To All!'.center(127))

def createList(emptyList, num_items):
    while num_items > 0:
        items = random.randrange(150, 4200, 150)
        emptyList.append(items)
        num_items -= 1

phrases = []
things = []
what_are_you_doing = []
places = []
occupation = []
categories = {'Phrases':phrases, 'Things':things, 'What Are You Doing':what_are_you_doing, 'Places':places, 'Occupation':occupation}
maxPlayers = 3
playerNames = {}
player_name_list = list(playerNames.keys())
aiBots = ['Emanuel(Ai)', 'Vaughn(Ai)', 'Stacy(Ai)',
          'Vanessa(Ai)', 'Derek(Ai)', 'George(Ai)',
          'Carl(Ai)', 'Shaniquia(Ai)', 'Jaelyn(Ai)',
          'Beyonce(Ai)', 'Kim Kardashian(Ai)', 'Taco(Ai)',
          'Tall Guy(Ai)', 'Kevin(Ai)', 'Pete(Ai)',
          'Regina Phalange', 'Rafi(Ai)', 'Jenny(Ai)',
          'Jeff(Ai)', 'Ruxin(Ai)', 'Joey(Ai)',
          'Tobias(Ai)', 'Lucille(Ai)', 'Lucille2(Ai)',
          'Oscar(Ai)', 'Gob(Ai)', 'Maeby(Ai)',
          'Jack(Ai)', 'Michael(Ai)', 'Buster(Ai)',
          'Andy(Ai)', 'Valerie(Ai)', 'Woody(Ai)',
          'Harry(Ai)', 'Hermione(Ai)', 'Franchesca(Ai)',
          'Sylvia(Ai)', 'Maxwell(Ai)', 'Braydon(Ai)',
          'Melanie(Ai)', 'Maggie(Ai)', 'Brighton(Ai)',
          'Niles(Ai)', 'Cece(Ai)', 'Johnny(Ai)',
          'Fonzi(Ai)', 'Tommy(Ai)', 'Timmy(Ai)',
          'Howard(Ai)', 'Xavier(Ai)', 'Betty(Ai)',
          'Kim(Ai)', 'Marcus(Ai)', 'Ed(Ai)',
          'Brittni(Ai)', 'Harvey(Ai)', 'Andy(Ai)',
          'Whitney(Ai)', 'Bob Loblaw(Ai)', 'Jim(Ai)',
          'Shiva Comini Coma Condercrom(Ai)', 'Buzz(Ai)']
winner = {}
gameHost = input('Game Host Name: ')
        
num_of_players = 0

def writeToFile(category, puzzle):
    c = '{}'.format(category.title())
    p = '{}'.format(puzzle.title())
    if c == 'Phrases':
        with open('wofCategories/wofPhrases.txt', 'a+') as f:
            f.write(p + '\r\n')
    elif c == 'Things':
        with open('wofCategories/wofThings.txt', 'a+') as f:
            f.write(p + '\r\n')
    elif c == 'What Are You Doing':
        with open('wofCategories/wofWayd.txt', 'a+') as f:
            f.write(p + '\r\n')
    elif c == 'Places':
        with open('wofCategories/wofPlaces.txt', 'a+') as f:
            f.write(p + '\r\n')
    elif c == 'Occupation':
        with open('wofCategories/wofOccupation.txt', 'a+') as f:
            f.write(p + '\r\n')
    else:
        customFile = 'wofCategories/wof{}.txt'.format(category.title())
        with open(customFile, 'a+') as f:
            f.write(c + '\r\n')

def executeAI(puzzle, roundScores, plyrScoreTrkr, rlPuzzle, puzzleBoard, puzzlenumletters, player, wheel, endRound, rnd):
    Computer = AI(player, roundScores[plyrScoreTrkr])
    vowels = 'aeiou'
    vowelValue = 250
    turnPlay = True
    correctLetters = 0
    while turnPlay:
        sx = 0 #player score index
        print(str('Round ' + str(rnd) + ' Totals:').center(127))
        for player in player_name_list:
            print(str(player.title() + ': ' + str(roundScores[sx])).center(127))
            sx += 1
        sx = 0
            
        if Computer.endTurn == False:
            print('\n' + str(Computer.name + ' is going to spin the wheel.').center(127))
            print('Spinning...\n'.center(127))
            time.sleep(4)
            wheelValue = Computer.spin(wheel)
            print(str('The wheel landed on ' + str(wheelValue) + '\n').center(127))
            time.sleep(4)

            if wheelValue == 'Bankrupt':
                print('\n' + 'OH NO! You\'ve lost all of your earnings!'.center(127) + '\n')
                Computer.score -= Computer.score
                Computer.endTurn = True
                
            elif wheelValue == 'Lose a Turn':
                print(str(Computer.name.title() +  ' loses this turn.').center(127))
                Computer.endTurn = True

            elif wheelValue == 'Free Play':
                fpValue = 500
                guessCount = 2
                while guessCount > 0:
                    print(str(Computer.name + ' is generating a guess...').center(127))
                    time.sleep(4)
                    computerGuess = Computer.guess()
                    print('\n' + str('Checking guess for validity...').center(127) + '\n')
                    time.sleep(4)
                    if computerGuess in vowels and plyrScoreTrkr == 0:
                        print(str(Computer.name + ' cannot purchase a vowel with a score of 0.').center(127))
                        print(str(Computer.name + ' will guess again.').center(127) + '\n')
                        continue
                    
                    if computerGuess not in rlPuzzle:
                        print(str(Computer.name + '\'s guess is incorrect.').center(127) + '\n')

                        if guessCount == 1:
                            Computer.endTurn = True

                        guessCount -= 1
                    
                    elif computerGuess in rlPuzzle:
                        letLoc = rlPuzzle.index(computerGuess)
                        letCount = rlPuzzle.count(computerGuess)
                        print(str(Computer.name + '\'s guess is correct.').center(127))
                        if Computer.name == 'Fonzi(Ai)':
                            print(str(Computer.name.title() + ' says: Aaaaaaaaaay').center(127))
                        if computerGuess in vowels:
                            roundScores[plyrScoreTrkr] += vowelValue
                        else:
                            roundScores[plyrScoreTrkr] += fpValue
                        puzzlenumletters += 1
                        correctLetters += 1
                        guessCount -= 1
                        while letCount > 0:
                            puzzleBoard[letLoc] = computerGuess.upper()
                            letCount -= 1    
 
            else:#wheel lands on any other numeric value
                print(str(Computer.name + ' is generating a guess...').center(127))
                time.sleep(4)
                guess_count = 1
                while guess_count > 0:
                    computerGuess = Computer.guess()
                    print('\n' + str('Checking guess for validity...').center(127) + '\n')
                    time.sleep(4)

                    if computerGuess in vowels and roundScores[plyrScoreTrkr] == 0:
                        print(str(Computer.name.title() + ' cannot purchase a vowel with a score of 0.').center(127))
                        print(str(Computer.name + ' will guess again.').center(127) + '\n')
                        continue
                    
                    if computerGuess not in rlPuzzle:
                        if computerGuess in vowels:
                            roundScores[plyrScoreTrkr] -= vowelValue
                        else:
                            print(str(Computer.name + '\'s guess is incorrect.').center(127) + '\n')
                        Computer.endTurn = True
                        
                    elif computerGuess in rlPuzzle:
                        letLoc = rlPuzzle.index(computerGuess)
                        letCount = rlPuzzle.count(computerGuess)
                        print(str(Computer.name + '\'s guess is correct.').center(127))
                        if computerGuess in vowels:
                            roundScores[plyrScoreTrkr] += wheelValue - vowelValue
                        else:
                            roundScores[plyrScoreTrkr] += wheelValue
                        puzzlenumletters += 1
                        correctLetters += 1
                        while letCount > 0:
                            puzzleBoard[letLoc] = computerGuess.upper()
                            letCount -= 1
                    if correctLetters == 2: 
                        print(str(Computer.name.title() + ' is going to pass.').center(127))
                        Computer.endTurn = True
                    guess_count -= 1
            if puzzlenumletters >= len(puzzle) / 1.5:
                cGuess = Computer.solve(puzzle)
                if cGuess == puzzle:
                    endRound = True
                    Computer.endTurn = True
                else:
                    print(str(Computer.name.title() + '\s guess was incorrect.').center(127))
                    endRound = False
                    Computer.endTurn = True
        if Computer.endTurn == True:
            print('Moving on to the next player...'.center(127))
            time.sleep(4)
            turnPlay = False
        print('\n' + str('[' + ']['.join(puzzleBoard) + ']\n').center(127))
    return endRound, Computer.endTurn


def startGame(num_of_players):
    endStartPuzzle = False
    bPuzzleValue = 2000

    def execute_AI_BonusPuzzle(players, player_names, puzzle, rpScore):
        Computer = AI(players, rpScore)
        AIguess = Computer.solve(puzzle)
        print(str(Computer.name + ' will guess now.').center(127))
        print('Processing...\n'.center(127))
        time.sleep(4)
        if AIguess != puzzle:
            print('Sorry that was not correct\n'.center(127))
            solved = False
        elif AIguess == puzzle:
            print(str('Puzzle Answer: ' + puzzle.title()).center(127))
            print('Great! You guessed the correct answer to the puzzle!'.center(127))
            print(str(str(bPuzzleValue) + ' is added to ' + players.title() + '\'s score').center(127))
            playerNames[players] += bPuzzleValue
            solved = True
        return solved

    #Start of main loop
    while not endStartPuzzle:
        #The adding and curation of the number of players in the game
        try:
            players = int(input('\nHow many human players are playing today? (max:3): '))
        except ValueError:
            print('Please enter a numeric value.'.center(127))
            continue

        if players > 3:
            print('Sorry, there can be no more than 3 players for this game.'.center(127))
            continue

        num_of_players += players

        if players == 1:
            player1 = input('\nPlayer 1 Name: ')
            player2 = random.choice(aiBots)
            player3 = random.choice(aiBots) if random.choice(aiBots) != player2 else random.choice(aiBots)

        elif players == 2:
            player1 = input('\nPlayer 1 Name: ')
            player2 = input('\nPlayer 2 Name: ')    
            player3 = random.choice(aiBots)

        elif players == 3:
            player1 = input('\nPlayer 1 Name: ')
            player2 = input('\nPlayer 2 Name: ')
            player3 = input('\nPlayer 3 Name: ')

        elif players == 0:
            player1 = random.choice(aiBots)
            player2 = random.choice(aiBots) if random.choice(aiBots) != player1 else random.choice(aiBots)
            player3 = random.choice(aiBots) if random.choice(aiBots) != player2 else random.choice(aiBots)

        #Assigning initial 0 score for all players
        playerNames[player1] = 0
        playerNames[player2] = 0
        playerNames[player3] = 0

        player_names = list(playerNames.keys())
        print(str('Players: ' + ', '.join(player_names).title()).center(127) + '\n')

        noPuzzle = True 
        while noPuzzle:
            print(str(gameHost.title() + ', please enter the bonus category and puzzle answer.').center(127))
            print('Players, Look Away please!'.center(127))
            puzzleCategory = input('Category: ')
            bonusPuzzle = input('Bonus Puzzle: ').lower()
            bpSpaces = bonusPuzzle.count(' ')
            if bonusPuzzle == '':
                print('Please enter a puzzle answer!\n'.center(127))
                continue
            else:
                noPuzzle = False
            pc = 'wofBonusCategories/wof{}.txt'.format(puzzleCategory.title())
            bp = '{}'.format(bonusPuzzle.title())
            with open(pc, 'a+') as f:
                f.write(bp + '\r\n')
        print('\n' * 40)
        print(str('The puzzle has ' + str(len(bonusPuzzle) - bpSpaces) + ' letters').center(127))
        letterCount = 0 #tracking how many letters are added to the puzzle "board"
        bPuzzle = [] #letters from the puzzle put in by gameHost
        startPuzzle = [] #both bPuzzle and startPuzzle used to display the bonus puzzle in relation to actual game show
        
        #splitting up the puzzle answer in order to access the indexes later
        for letters in bonusPuzzle:
            if letters == ' ':
                bPuzzle.append('_')
                startPuzzle.append('_')
            else:
                bPuzzle.append(letters.upper())
                startPuzzle.append(' ')

        solved = False
        pCount = len(bonusPuzzle) - bpSpaces
        while not solved: 
            randLetter = random.choice(bPuzzle)
            rlSpot = bPuzzle.index(randLetter)

            if randLetter == ' ':
                continue
            elif randLetter not in bPuzzle:
                continue
            elif randLetter in bPuzzle:                
                startPuzzle[rlSpot] = str(randLetter)
                bPuzzle[rlSpot] = ' '
                print(str('[' + '] ['.join(startPuzzle) + ']' + '\n').center(127))
                time.sleep(1.5)
                letterCount += 1 #one letter added to display per loop
                pCount -= 1

            if pCount == 0:
                randomPlayer = random.choice(player_names)
                playerScoreTotal = playerNames.get(randomPlayer)
                playerNames[randomPlayer] += bPuzzleValue
                print(str('The puzzle answer was ' + bonusPuzzle.title() + ' and now we begin our first round!\n').center(127))
                print(str(str(randomPlayer).title() + ' was randomly chosen to add ' + str(bPuzzleValue) + ' to their total for completion of the puzzle.').center(127))
                time.sleep(4)
                solved = True
                break
            
            #chances to guess the puzzle
            if letterCount >= (len(bonusPuzzle) / 2):
                pnCount = 0
                for players in player_names:
                    print(str('The category is: ' + puzzleCategory).center(127)) 
                    pnCount += 1
                    if pnCount == 3:
                        print('One more letter is provided for you'.center(127))
                        pnCount = 0
                        continue
                    rpScore = playerNames.get(players)
                    if players in aiBots:
                        AI_Turn = execute_AI_BonusPuzzle(players, player_names, bonusPuzzle, rpScore)
                        if AI_Turn == False:
                            pnCount += 1
                            continue
                        else:
                            solved = True
                            break

                    else:
                        guess = input(str(players).title() +  ' guess the Puzzle?: ')
                        if guess != bonusPuzzle:
                            print('Sorry that was not correct\n'.center(127))
                    
                        elif guess == bonusPuzzle:
                            print(str('Puzzle Answer: ' + bonusPuzzle.title()).center(127))
                            print('Great! You guessed the correct answer to the puzzle!'.center(127))
                            print(str(str(bPuzzleValue) + ' is added to ' + players.title() + '\'s score').center(127))
                            playerNames[players] += bPuzzleValue
                            solved = True
                            break
                        
        endStartPuzzle = True            
#End of start game puzzle

startGame(num_of_players)#bonus puzzle round before round one starts
player_name_list = list(playerNames.keys())
    
print('Totals:'.center(127))
print(str(playerNames).title().center(127))
print('-'.center(131, '-'))

wheel_values = ['Bankrupt', 'Lose a Turn', 'Free Play', 'Bankrupt']

def printWheelValues(printed_items, pause, wheel_values=wheel_values):
    print('Wheel Values: '.center(127))
    w = 24
    x = printed_items
    y = 0
    while w > 0:
        print(str(str(wheel_values[y:x])).center(127))
        time.sleep(pause)   
        x += printed_items
        y += printed_items
        w -= printed_items
        
            
wheel_spots = 24
createList(wheel_values, (wheel_spots - 4))

def new_wheel(multiplier):
    #multiplying values on the wheel
    for each_value in wheel_values: 
        if each_value == 'Bankrupt' or each_value == 'Lose a Turn' or each_value == 'Free Play':
            continue
        else:
            each_value *= int(multiplier)

def spin_pass_solve(player, roundScores, plyrScoreTrkr, value, endTurn, puzzleAnswer, solved, rnd):
        decided = False
        while not decided:
            spinAgain = input(player.title() + ', would you like to spin again, solve the puzzle, or pass?: (Spin, Solve, Pass) ')

            if spinAgain == 'pass':
                print('Moving onto the next player'.center(127))
                time.sleep(1.5)
                endTurn = True
                solved = False
                decided = True

            elif spinAgain == 'spin':
                print('Spinning...'.center(127))
                time.sleep(3)
                endTurn = False
                solved = False
                decided = True
                #exit current loop; player still spinning

            elif spinAgain == 'solve':
                puzzleGuess = input('\n' +  player.title() + ', Complete the Puzzle: ')
                if puzzleGuess != puzzleAnswer:
                    print('Sorry that is not correct.'.center(127))
                    print('Moving onto the next player'.center(127))
                    decided = True #not to spin
                    endTurn = True
                    solved = False
                elif puzzleGuess == puzzleAnswer:
                    roundScores[plyrScoreTrkr] += int(value * 1.5)
                    decided = True #not to spin
                    endTurn = True
                    solved = True
                    if rnd == 1:
                        print(str('Congratulations ' + player.title() + '! You have won Round \u2776!').center(127))
                    elif rnd == 2:
                        print(str('Congratulations ' + player.title() + '! You have won Round \u2777!').center(127))
                    elif rnd == 3:
                        print(str('Congratulations ' + player.title() + '! You have won Round \u2778!').center(127))

                    print(str(player.title() + ' will add ' + str(int(value * 1.5)) + ' to their total for solving the puzzle.').center(127))
                    winner = {player:(roundScores[plyrScoreTrkr])}
            elif spinAgain != 'pass' or spinAgain != 'spin' or spinAgain !='solve':
                print('Please Enter: Pass, Spin or Solve'.center(127))
                continue
    

        return endTurn, solved
    
def spin(chosenCategory, roundScores, plyrScoreTrkr, player, roundPuzzle, puzzlenumletters, emptyRoundPuzzle, puzzleAnswer, solved, rnd):
    #player is assigned to the person who is spinning at time of function call
    #puzzlenumletters = Tracking how many letters are added to display
    endTurn = False
    solved = False
    spaces = roundPuzzle.count(' ')
    vowels = ['a', 'e', 'i', 'o', 'u']
    vowelValue = 250
    print(str('Round ' + str(rnd) + ' Totals:').center(127))

    while not endTurn:
        print(str(player_name_list[0].title() + ': ' + str(roundScores[0])).center(127))
        print(str(player_name_list[1].title() + ': ' + str(roundScores[1])).center(127))
        print(str(player_name_list[2].title() + ': ' + str(roundScores[2])).center(127))
           
        print('\n' + str('Vowels to buy are 250 each').center(127))
        print(str('Category: ' + chosenCategory.title()).center(127))
        
        if puzzlenumletters == len(roundPuzzle):
                print(str(player.title() + ', you may complete the puzzle').center(127))
                solvePuzzle = input('Puzzle Answer: ')
                if solvePuzzle == roundPuzzle:
                    winner = {player:(roundScores[plyrScoreTrkr])}
                    endTurn = True
                              
        value = random.choice(wheel_values)
        print(str('The wheel landed on ' + str(value)).center(127))
        time.sleep(2)

        if value == 'Bankrupt':
            #empties player's total and moves on to next player to spin
            print('\n' + 'OH NO! You\'ve lost all of your earnings!'.center(127))
            roundScores[plyrScoreTrkr] = 0
            endTurn = True

        elif value == 'Lose a Turn':
            #moves on to next player to spin
            print('Awwww!! So sorry you don\'t get to play this spin.'.center(127))
            print(str(player.title() + '\'s score remains the same.').center(127))
            endTurn = True

    
        elif value == 'Free Play':
            #2 guess per 1 spin
            fpValue = 500
            print('"Free Play" value worth 500 per correct guess'.center(127))
            print('\n' + str('[' + ']['.join(emptyRoundPuzzle) + ']').center(127))
            each_guess = 2
            wrongLetters = 0
            while each_guess > 0:
                print(str(player.title() + ', Guess a letter that you think may be in the puzzle.').center(127) + '\n')
                guess = input('Guess: ').lower()

                if len(guess) == 0:
                    print('Please enter your guess.'.center(127))
                    continue

                elif len(guess) > 1:
                    print('Please enter only 1 letter'.center(127))
                    continue

                if guess.isdigit() == True:
                    print('Please enter a letter value'.center(127))
                    continue
                
                if guess in vowels and roundScores[plyrScoreTrkr] == 0:
                    print('Sorry you do not have the available funds to purchase a vowel.'.center(127))
                    continue

                if guess in emptyRoundPuzzle:
                    print(str('Sorry, ' + player.title() + ' that letter has already been guessed. Be careful next time.').center(127))
                    print('Try a different letter.'.center(127))

                if guess not in roundPuzzle:
                    if guess in vowels:
                        print('Sorry that vowel is not in the puzzle'.center(127))
                    else:
                        print('Sorry that letter is not in the puzzle'.center(127))

                    #exiting loop based on 2nd guess being incorrect
                    if each_guess == 1:
                        print('Moving onto the next player...'.center(127))
                        endTurn = True
                    wrongLetters += 1
                    each_guess -= 1


                elif guess in roundPuzzle: #guess IS in puzzle
                    if guess in vowels: #guess is a vowel value
                        numLetters = roundPuzzle.count(guess)
                        roundScores[plyrScoreTrkr] += (fpValue * numLetters) - vowelValue
                        print(str('Correct! There are ' + str(numLetters) + ' of those in the puzzle\n').center(127))
                        print(str(player.title() + ' will add ' + str(int((fpValue * numLetters) - vowelValue)) + ' to their total!').center(127))
                        while numLetters > 0:
                            letterLocation = roundPuzzle.index(guess)
                            emptyRoundPuzzle[letterLocation] = guess.upper()           
                            roundPuzzle[letterLocation] = ' '
                            numLetters -= 1

                    else: #guess is a consonant value
                        numLetters = roundPuzzle.count(guess)
                        roundScores[plyrScoreTrkr] += (fpValue * numLetters)
                        print(str('Correct! There are ' + str(numLetters) + ' of those in the puzzle\n').center(127)) 
                        print(str(player.title() + ' will add ' + str(int((fpValue * numLetters) - vowelValue)) + ' to their total!').center(127))
                        while numLetters > 0:
                            letterLocation = roundPuzzle.index(guess)
                            emptyRoundPuzzle[letterLocation] = guess.upper()           
                            roundPuzzle[letterLocation] = ' '
                            numLetters -= 1
                        
                    print('\n' + str('[' + ']['.join(emptyRoundPuzzle) + ']').center(127))
                    each_guess -= 1
                    puzzlenumletters += 1
            vCount = 5
            for v in vowels:
                if v not in roundPuzzle:
                    vCount -= 1
                else:
                    break
            if vCount == 0:
                print('There are no more vowels!')                

            if endTurn == False:
                spinAgain = spin_pass_solve(player, roundScores, plyrScoreTrkr, fpValue, endTurn, puzzleAnswer, solved, rnd)
                if spinAgain == (True, True ):
                    endTurn = True
                    solved = True
                elif spinAgain == (True, False):
                    endTurn = True
                    solved = False
                elif spinAgain == (False, False):
                    endTurn = False
                    continue
        #Wheel lands on any numeric value other than the 4 set string values
        else:
            print('\n' + str('[' + ']['.join(emptyRoundPuzzle) + ']').center(127) + '\n')
            eachGuess = 1
            while eachGuess > 0:
                print(str(player.title() + ' Guess a letter that you think may be in the puzzle.').center(127))
                guess = str(input('Guess: ')).lower()

                if len(guess) == 0:
                    print('Please enter your guess'.center(127))
                    continue
                
                if len(guess) > 1:
                    print('Please enter only 1 letter'.center(127))
                    continue

                if guess.isdigit() == True:
                    print('Please enter a letter value'.center(127))
                    continue
                
                if guess in vowels and roundScores[plyrScoreTrkr] == 0:
                    print('Sorry you do not have the available funds to purchase a vowel.'.center(127))
                    print('Try a different letter'.center(127))
                    continue
                
                if guess in emptyRoundPuzzle:
                    print(str('Sorry, ' + player.title() + ' that letter has already been guessed. Be careful next time.').center(127))
                    print('\n' + 'Moving on to the next player...'.center(127))
                    time.sleep(1.5)
                    endTurn = True
                    eachGuess = 0
                if guess not in roundPuzzle:
                    if guess in vowels:
                        if roundScores[plyrScoreTrkr] == 0:
                            print(str(player.title() + ' will not recieve a negative score for guessing incorrectly').center(127))
                            continue
                        else:
                            print('Sorry that vowel is not in the puzzle'.center(127))
        
                    else:
                        print('Sorry that letter is not in the puzzle'.center(127))

                    print('\n' + 'Moving on to the next player...'.center(127))
                    time.sleep(1.5)
                    endTurn = True
                    eachGuess -= 1
                        

                elif guess in roundPuzzle:
                    if guess in vowels:
                        winning_value = value * numLetters - vowelValue    
                        numLetters = roundPuzzle.count(guess)
                        roundScores[plyrScoreTrkr] += (winning_value)
                        print(str('Correct! There are ' + str(numLetters) + ' of those in the puzzle\n').center(127)) 
                        print(str(player.title() + ' will add ' + str(value * numLetters - vowelValue) + ' to their total!').center(127))
                        while numLetters > 0:
                            letterLocation = roundPuzzle.index(guess)
                            emptyRoundPuzzle[letterLocation] = guess.upper()           
                            roundPuzzle[letterLocation] = ' '
                            numLetters -= 1
                        eachGuess -= 1
                        puzzlenumletters += 1

                        print('\n' + str('[' + ']['.join(emptyRoundPuzzle) + ']').center(127))
                        
                    else:
                        numLetters = roundPuzzle.count(guess)
                        roundScores[plyrScoreTrkr] += (value * numLetters)
                        print(str('Correct! There are ' + str(numLetters) + ' of those in the puzzle\n').center(127))  
                        print(str(player.title() + ' will add ' + str(int(value * numLetters)) + ' to their total!').center(127))
                        while numLetters > 0:

                            letterLocation = roundPuzzle.index(guess)
                            emptyRoundPuzzle[letterLocation] = guess.upper()
                            roundPuzzle[letterLocation] = '*'
                            numLetters -= 1
                            puzzlenumletters += 1
                        print('\n' + str('[' + ']['.join(emptyRoundPuzzle) + ']\n').center(127))
                        eachGuess -= 1

            vCount= 5
            for v in vowels:
                if v not in roundPuzzle:
                    vCount -= 1
                else:
                    break
            if vCount == 0:
                print('There are no more vowels!')

            
            if endTurn == False:
                spinAgain = spin_pass_solve(player, roundScores, plyrScoreTrkr, value, endTurn, puzzleAnswer, solved, rnd)
                if spinAgain == (True, True):
                    endTurn = True #ending turn
                    solved = True
                elif spinAgain == (True, False):
                    endTurn = True
                    solved = False
                elif spinAgain == (False, False): #return endTurn, solved
                    endTurn = False #Continuing turn

    return endTurn, solved

def gameRounds(rnd):
    if rnd > 1:
        new_wheel(rnd)
    print('Loading Rounds...'.center(127))
    time.sleep(8)
    if rnd == 1:
        print(str('Round \u2776 Load Complete.').center(127))
    elif rnd == 2:
        print(str('Round \u2777 Load Complete.').center(127))
    elif rnd == 3:
        print(str('Round \u2778 Load Complete.').center(127))
    print('Press ENTER to start.'.center(127))
    input()
    print('\n' * 40)
    if rnd == 1:
        print(str('Round \u2776 Has Started').center(133, '^') + '\n')
    elif rnd == 2:
        print(str('Round \u2777 Has Started').center(133, '^') + '\n')
    elif rnd == 3:
        print(str('Round \u2778 Has Started').center(133, '^') + '\n')
    print('\n' * 30)
    print(str(gameHost.title() + ', please choose the category for the puzzle.').center(127))
    print(str('Categories: ' + ', '.join([k for k in categories.keys()])).center(127))
    chosenCategory = input('Category: ').lower()
    puzzleBoard = []
    if rnd == 1:
        print(str(gameHost.title() + ', Please enter the puzzle for Round \u2776.').center(127))
    if rnd == 2:
        print(str(gameHost.title() + ', Please enter the puzzle for Round \u2777.').center(127))
    if rnd == 3:
        print(str(gameHost.title() + ', Please enter the puzzle for Round \u2778.').center(127))
    roundPuzzle = input('Puzzle: ').lower()
    writeToFile(chosenCategory, roundPuzzle)
    if len(roundPuzzle) < 2:
        print(str(gameHost + ', please enter more than 1 letter for the puzzle!').center(127))
    rPuzzleList = [letter for letter in roundPuzzle] #list comprehension for reducing lines of code
    puzzleLetterNum = len(roundPuzzle)
    puzzlenumletters = 0
    turnCount = 0 #tracking number of turns taken during round one
    for eachLetter in roundPuzzle:
        if eachLetter == ' ':
            puzzleBoard.append('_')
            puzzlenumletters += 1
        else:
            puzzleBoard.append(' ')
    spacesCount = roundPuzzle.count(' ')
    puzzleLength = (len(roundPuzzle) - int(spacesCount))
    print('\n' * 40)
    printWheelValues(8, 1)
    print(str('The puzzle has ' + str(puzzleLength) + ' letters.').center(127))
    print('\n' + str('[' + ']['.join(puzzleBoard) + ']').center(127))
    roundScores = [0, 0, 0]
    endRound = False
    winner = []
    print('\n' + str(player_name_list[0].title() + ' will start off our puzzle with a spin!').center(127))
    while not endRound:
    #main loop for current round
        plyrScoreTrkr = 0
        solved = False        
        for player in player_name_list:
            turnEnd = False
            #spinning and guessing puzzle loop
            if len(puzzleBoard) == len(roundPuzzle) % len(puzzleBoard):
                puzzleGuess = input(player.title() + ', Complete the Puzzle: ').lower()
                if puzzleGuess != roundPuzzle:
                    print(str('Sorry that is not correct.' + '\nMoving onto the next player').center(127))
                    endRound = False
                elif puzzleGuess == roundPuzzle:
                    roundScores[plyrScoreTrkr] += int(value * 1.5)
                    print(str(player + ' will add ' + str(int(value) * 1.5) + ' to their total.').center(127))
                    endRound = True

            while not turnEnd:
                if player in aiBots:
                    print(str(player + ' will start their turn.').center(127) + '\n')
                    time.sleep(2)
                         #def executeAI(puzzle, roundScores, plyrScoreTrkr, rlPuzzle, puzzleBoard, puzzlenumletters, player, wheel, endRound, rnd)
                    AI_Turn = executeAI(roundPuzzle, roundScores, plyrScoreTrkr, rPuzzleList, puzzleBoard, puzzlenumletters, player, wheel_values, endRound, rnd)
                    plyrScoreTrkr += 1 #switching to next value in roundScores
                    if AI_Turn == (True, True):
                        solved = True
                        turnEnd = True
                        winner.append(player)
                    elif AI_Turn == (False, True):
                        turnEnd = True
                else:
                    def solve_attempt():
                        puzzle_guess = input('Your guess: ').lower()
                        if puzzle_guess != roundPuzzle:
                            print('Sorry, your guess is incorrect.'.center(127))
                            print('Moving on to the next player...')
                            time.sleep(4)
                            endTurn = True
                            solved = False
                        elif puzzle_guess == roundPuzzle:
                            print('Congratulations! You have guess the puzzle correctly.'.center(127))
                            print(str(player.title() + ' will add 2500 to their score.').center(127))
                            roundScores[plyrScoreTrkr] += 2500
                            endTurn = True
                            solved = True
                        return endTurn, solved
                    if puzzlenumletters >= len(roundPuzzle) - 5:
                        print(str(player.title() + ' would you like to try and solve the puzzle?').center(127))
                        chance_to_solve = input('Solve? Yes or No: ').lower()
                        if chance_to_solve == 'yes':
                            sa = solve_attempt()
                            if sa == (True, True):
                                turnEnd = True
                                solved = True
                                endRound = True
                            elif sa == (True, False):
                                turnEnd = True
                                solved = False
                                
                    print(str(player.title() + ', Press ENTER to Spin').center(127))
                    input()
                    print('Spinning...'.center(127) + '\n')
                    time.sleep(3)
                             #def spin(chosenCategory, roundScores, plyrScoreTrkr, player, roundPuzzle, puzzlenumletters, emptyRoundPuzzle, puzzleAnswer, solved, rnd)
                    player_spin = spin(chosenCategory, roundScores, plyrScoreTrkr, player, rPuzzleList, puzzlenumletters, puzzleBoard, roundPuzzle, solved, rnd)
                    plyrScoreTrkr += 1 #switching to next value in roundScores
                    if player_spin == (True, False):#return endTurn, solved
                        print('\n' * 10)
                        turnEnd = True
                    elif player_spin == (False, False):#return endTurn, solved
                        turnEnd = False

                    elif player_spin == (True, True):#return endTurn, solved
                        turnEnd = True
                        solved = True
                        winner.append(player)
            
            if turnEnd == True and solved == True:
                endRound = True
                break
    if puzzlenumletters != puzzleLetterNum:
        puzzleBoard = [l for l in roundPuzzle]
        print('\n' + str(str('[' + ']['.join(puzzleBoard) + ']\n').upper()).center(127))

        playerNames[(player_name_list[0])] += roundScores[0]
        playerNames[(player_name_list[1])] += roundScores[1]
        playerNames[(player_name_list[2])] += roundScores[2]

    print('We will now take a short 30 second break before we continue'.center(127))
    print('INTERMISSION'.center(131, '*'))
    time.sleep(30)
            
def winnerRound():
    winner = {'x':0}        
    for p in player_name_list:
        ps = playerNames.get(p)
        wl = list(winner.keys())
        for w in wl:
            ws = winner.get(w)
            if ps > ws:
                winner = {p:ps}
            else:
                continue
    winner_list = list(winner.keys())
    winningPlayer = winner_list[0]
    winnerScore = winner.get(winningPlayer)
    winWheel = []
    consonant = 'bcdfghjkmpqvwxyz'
    vowel = 'aiou'
    consonants = [c for c in consonant]
    vowels = [v for v in vowel]
    categs = list(categories.keys())
    values = 16
    while values > 0:
        v = random.randrange(10000, 36000, 4000)
        winWheel.append(int(v))
        values -= 1
    winnerWheelValue = random.choice(winWheel)
    def executeAI_FinalPuzzle():
        computer = AI(winner_list[0], winner[(winner_list[0])])
        computerCat = random.choice(categs)
        print(str(computer.name.title() + ' is choosing a category...').center(127))
        time.sleep(4)
        print(str(computer.name.title() + ' has chosen ' + computerCat + ' as their category.').center(127))
        time.sleep(2)
        print(str(gameHost.title() + ', please enter the Final Puzzle.').center(127))
        finalPuzzle = input('Final Puzzle: ')
        cf = '{}.txt'.format(computerCat)#Formatted Category
        fpf = '{}'.format(finalPuzzle.title())#Formatted Final Puzzle
        with open(cf, 'a+') as f:
            f.write(fpf + '\r\n')
        fpLength = len(finalPuzzle)
        fpSpaces = finalPuzzle.count(' ')
        puzzleBoard = [wl for wl in finalPuzzle]
        emptyBoard = []
        for each in finalPuzzle:
            if each == ' ':
                emptyBoard.append('_')
            else:
                emptyBoard.append(' ')
        print('\n' * 40)
        givenLetters = ['r', 's', 't', 'l' ,'n', 'e']
        print(str('The puzzle has ' + str(fpLength) + ' letters.').center(127))
        print(str('Given Letters: ' + ', '.join(givenLetters).upper()).center(127))    
        print(str('Now ' + computer.name.title() + ' will spin the wheel for a random selection of value').center(127))
        print('Spinning...'.center(127) + '\n')
        
        time.sleep(5)
        print('A value has been selected and we will store that away until the puzzle is complete.'.center(127))
        time.sleep(3)
        #replacing SPACE characters with an underscore for easier UI
        for each in puzzleBoard:
            if each == ' ':
                spacePlace = puzzleBoard.index(each)
                puzzleBoard[spacePlace] = '_'

            for eachLetter in givenLetters:
                pnum = 0
                ELC = puzzleBoard.count(eachLetter)
                while ELC > 0:
                    if eachLetter not in puzzleBoard:
                        pnum += 1
                        continue
                    else:
                        EL = puzzleBoard.index(eachLetter)
                        emptyBoard[EL] = eachLetter.upper()
                        print(str('[' + ']['.join(emptyBoard) + ']').center(127))
                        print(str(', '.join(givenLetters)).upper())
                        time.sleep(1.5)
                        puzzleBoard[EL] = '*'
                        ELC -= 1
        if pnum == len(givenLetters):
            print('There were not any of the given letters in the puzzle'.center(127))
            time.sleep(1.5)

        print(str(computer.name.title() + ', will now select 3 consonants and 1 vowel.').center(127))
        computerCons = random.sample(consonants, 3)
        computerVowel = random.choice(vowels)
        winnerLetters = [', '.join(computerCons), computerVowel]
        print(str(computer.name.title() + ' has chosen ' + ', '.join(winnerLetters).upper() + ' for their letters.').center(127))
        print(str('Checking validity of ' + computer.name.title() + '\'s letters...').center(127) + '\n')
        time.sleep(2)
        #checking player-given letters in puzzle
        for eachLetter in winnerLetters:
            ELC = puzzleBoard.count(eachLetter)
            while ELC > 0:
                if eachLetter not in puzzleBoard:
                    continue
                else:
                    EL = puzzleBoard.index(eachLetter)
                    emptyBoard[EL] = eachLetter.upper()
                    print(str('[' + ']['.join(emptyBoard) + ']').center(127))
                    print(str(', '.join(givenLetters) + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + ', '.join(winnerLetters)).upper())
                    time.sleep(1.5)
                    puzzleBoard[EL] = '*'
                    ELC -= 1
        if emptyBoard == puzzleBoard:
            print(str('Congratulations ' + computer.name.title() + '! You have won the Final Puzzle!').center(127))
            solved = True

        print(str(computer.name.title() + ' will have 5 chances to correctly guess the puzzle!').center(127) + '\n')
        guessCount = 5
        solved = False
        while guessCount > 0 and solved == False:
            if guessCount == 5:
                print(str(computer.name.title() + 'is generating a guess.').center(127))
            else:
                print(str(computer.name.title() + 'is generating another guess.').center(127))
                time.sleep(4)
            winnerGuess = computer.solve(finalPuzzle)
            if winnerGuess != finalPuzzle:
                print('Sorry that is not correct. Please Try Again!'.center(127) + '\n')
                guessCount -= 1
                continue

            elif winnerGuess == finalPuzzle:
                fp = [f for f in finalPuzzle]
                print(str(str('[' + ']['.join(fp) + ']').upper()).center(127))
                print('Congratulations! You have won the Final Puzzle!'.center(127))
                winner[winningPlayer] += int(winnerWheelValue)
                solved = True
                guessCount -= guessCount

        if solved == False:
            print('Sorry! Unfortunately you did not solve the Final Puzzle'.center(127))
            print(str('Sadly you do not receive ' + str(winnerWheelValue) + ' for the final puzzle').center(127))
            print(str('Although your ending total for the game is an impressive score of ' + str(computer.score)).center(127))
            print('Thank you for playing Wheel of Fortune!'.center(127))
            print('Please contact the developer to play again!'.center(127))
        elif solved == True:
            print(str(winningPlayer.title() + ', you receive ' + str(winnerWheelValue) + ' for solving the final puzzle').center(127))
            wprint('Congrats on winning Wheel of Fortune! Please contact the developer to play again!'.center(127))
            print(str(winningPlayer.title() + '\'s ending total: ' + str(winnerScore)).center(127))
                #########END OF AI WINNER FUNCTION DEFINITION###########
                                   
    print(str(winningPlayer.title() + ', you have now made it to the Final Round').center(127))    
    if winner_list[0] in aiBots:
        executeAI_FinalPuzzle()
        print(str('Winner: ' + winningPlayer.title()).center(127))
        print(str('Score: ' + str(winnerScore)).center(127))
    else:
        playing_final_round = True
        while playing_final_round:

            print('Which category would you like for your final puzzle?'.center(127))
            print(str(', '.join(categs)).center(127))
            pcCategory = input('Category: ')

            if len(pcCategory) == 0:
                print('Please enter a category of your choosing.\n')
                continue

            print('Now the host will enter the puzzle for your Final Round'.center(127))
            while True:
                finalPuzzle = input(gameHost.title() + ', please enter the Final Puzzle: ')

                if len(finalPuzzle) == 0:
                    print('Please enter the puzzle for the final round. \n')
                    continue
                else:
                    break
            cf = '{}.txt'.format(pcCategory)#Formatted Category
            fpf = '{}'.format(finalPuzzle.title())#Formatted Final Puzzle
            with open(cf, 'a+') as f:
                f.write(fpf + '\r\n')
            fpLength = len(finalPuzzle)
            fpSpaces = finalPuzzle.count(' ')
            puzzleBoard = [wl for wl in finalPuzzle]
            emptyBoard = []
            for each in finalPuzzle:
                if each == ' ':
                    emptyBoard.append('_')
                else:
                    emptyBoard.append(' ')
            print('\n' * 40)
            givenLetters = ['r', 's', 't', 'l' ,'n', 'e']
            print(str('The puzzle has ' + str(fpLength) + ' letters.').center(127))
            print(str('Given Letters: ' + str(', '.join(givenLetters).upper())).center(127))    
            print('Now you may spin the wheel for a random selection of value'.center(127))
            input(str(winningPlayer.title() + ', press enter to spin.').center(127))
            print('Spinning...'.center(127))
            time.sleep(5)
            print('A value has been selected and we will store that away until the puzzle is complete.'.center(127))
            time.sleep(2)
            for each in puzzleBoard:
                if each == ' ':
                    spacePlace = puzzleBoard.index(each)
                    puzzleBoard[spacePlace] = '_'

            for eachLetter in givenLetters:
                pnum = 0
                ELC = puzzleBoard.count(eachLetter)
                while ELC > 0:
                    if eachLetter not in puzzleBoard:
                        pnum += 1
                        continue
                    else:
                        EL = puzzleBoard.index(eachLetter)
                        emptyBoard[EL] = eachLetter.upper()
                        print(str('[' + ']['.join(emptyBoard) + ']').center(127))
                        print(str(', '.join(givenLetters) + '\t\t\t\t\t\t\t\t\t\t\t\t\t').upper())
                        time.sleep(1.5)
                        puzzleBoard[EL] = '*'
                        ELC -= 1
            if pnum == len(givenLetters):
                print('There were not any of the given letters in the puzzle'.center(127))
                time.sleep(1.5)

            print(str(winningPlayer.title() + ', please enter 3 consonant letters and 1 vowel.').center(127))
            print('Seperate each letter with a space.'.center(127))
            winningPlayerLetters = input('Your Letters: ')
            winnerLetters = winningPlayerLetters.split()    
            print('Now we will see if your letters are in the puzzle.'.center(127))
            time.sleep(1.5)
            #checking player-given letters in puzzle
            for eachLetter in winnerLetters:
                ELC = puzzleBoard.count(eachLetter)
                while ELC > 0:
                    if eachLetter not in finalPuzzle:
                        continue
                    else:
                        EL = puzzleBoard.index(eachLetter)
                        emptyBoard[EL] = eachLetter.upper()
                        print(str('[' + ']['.join(emptyBoard) + ']').center(127))
                        print(str(', '.join(givenLetters) + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + ', '.join(winnerLetters)).upper())
                        time.sleep(1.5)
                        puzzleBoard[EL] = '*'
                        ELC -= 1
            if emptyBoard == puzzleBoard:
                print(str('Congratulations ' + winningPlayer.title() + '! You have won the Final Puzzle!').center(127))
                solved = True

            print('You have 5 chances to correctly guess the puzzle. Good Luck!'.center(127))
            guessCount = 5
            solved = False
            while guessCount > 0 and solved == False:
                  try:
                      winnerGuess = str(input('Guess the Puzzle: '))
                  except:
                      print('Please enter all letters'.center(127))
                      continue

                  if len(winnerGuess) < 1:
                      print('Please enter your answer!'.center(127))
                      continue
                  
                  elif winnerGuess != finalPuzzle:
                      print('Sorry that is not correct. Please Try Again!'.center(127))
                      guessCount -= 1
                      continue

                  elif winnerGuess == finalPuzzle:
                      fp = [f for f in finalPuzzle]
                      print(str(str('[' + ']['.join(fp) + ']').upper()).center(127))
                      print('Congratulations! You have won the Final Puzzle!'.center(127))
                      winner[winningPlayer] += int(winnerWheelValue)
                      solved = True
                      guessCount -= guessCount

            if solved == False:
                print('The Final Puzzle Is:'.center(127))
                print(str('[' + ']['.join(finalPuzzle).upper() + ']').center(127))
                print('Sorry! Unfortunately you did not solve the Final Puzzle'.center(127))
                print(str('Sadly you do not receive ' + str(winnerWheelValue) + ' for the final puzzle').center(127))
                print(str('Although your ending total for the game is an impressive score of ' + str(winnerScore)).center(127))
                print('Thank you for playing Wheel of Fortune!'.center(127))
                print('Please contact the developer to play again!'.center(127))
                print(str('Winner: ' + winningPlayer.title()).center(127))
                print(str('Score: ' + str(winnerScore)).center(127))
            elif solved == True:
                print('The Final Puzzle Is:'.center(127))
                print(str('[' + ']['.join(finalPuzzle).upper() + ']').center(127))
                print(str(winningPlayer.title() + ', you receive ' + str(winnerWheelValue) + ' for solving the final puzzle').center(127))
                print('Congrats on winning Wheel of Fortune! Please contact the developer to play again!'.center(127))
                print(str(winningPlayer.title() + '\'s ending total: ' + str(winner[winningPlayer])).center(127))

if __name__ == '__main__':
    gameRounds(1)
    gameRounds(2)
    gameRounds(3)
    winnerRound()
    print('End of Game!'.center(127))
