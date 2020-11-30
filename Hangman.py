#Hangman Finished - 5/27/2019 10:30pm Monday
import random, time, re

def hangMan():
    print('****----------****')
    print('Welcome to Hangman')
    print('****----------****')

    p1 = input('Enter Name for Player 1: ')
    p2 = input('\nEnter Name for Player 2: ')

    print('\nNow, ' + p2 + ', look away as ' + p1 + ' enters their choice of words')
    print('Please enter 5 words, one at a time')

    words = []
    wcount = 5
    while wcount > 0 :
        if wcount == 1:
            custWords = input(p1 + ', please enter ' + str(wcount) + ' more word: ').lower()
        else:
            custWords = input(p1 + ', please enter ' + str(wcount) + ' more words: ').lower()

            

        #NEED ERROR CATCH FOR STRING
            
        wcount -= 1
        words.append(custWords)
        

    def hungFace():
        print('         ~~~~~~~~            ')
        print('         |      |            ')
        print('        (| 0  0 |)           ')
        print('         |  UU  |            ')
        print('         |      |            ')
        print('           |  |              ')
        print('           |  |              ')

    def hungOneLimb():
        print('         ~~~~~~~~            ')
        print('         |      |            ')
        print('        (| 0  0 |)           ')
        print('         |  UU  |            ')
        print('         |      |            ')
        print('           |  |              ')
        print('           |  |              ')
        print('           |  \\             ')
        print('           |  |\\            ')
        print('           |  | \\           ')
        print('           |  |  \\          ')
        print('           |  |   \\()       ')
        print('           |  | ()( )()      ')
        print('           |  |  () ()       ')
        
    def hungTwoLimbs():
        print('         ~~~~~~~~            ')
        print('         |      |            ')
        print('        (| 0  0 |)           ')
        print('         |  UU  |            ')
        print('         |      |            ')
        print('           |  |              ')
        print('           |  |              ')
        print('          //  \\             ')
        print('         //|  |\\            ')
        print('        // |  | \\           ')
        print('       //  |  |  \\          ')
        print('    ()//   |  |   \\()       ')
        print('  ()( )()  |  | ()( )()      ')
        print('   () ()   |  |  () ()       ')

    def hungThreeLimbs():
        print('         ~~~~~~~~            ')
        print('         |      |            ')
        print('        (| 0  0 |)           ')
        print('         |  UU  |            ')
        print('         |      |            ')
        print('           |  |              ')
        print('           |  |              ')
        print('          //  \\             ')
        print('         //|  |\\            ')
        print('        // |  | \\           ')
        print('       //  |  |  \\          ')
        print('    ()//   |  |   \\()       ')
        print('  ()( )()  |  | ()( )()      ')
        print('   () ()   |  |  () ()       ')
        print('          //                 ')
        print('         //                  ')
        print('        //                   ')
        print('       //                    ')
        print('      //                     ')
        print(' ()__//                      ')
        print(' ()   \                      ')
        print(' ()____)                     ')

    def hungFourLimbs():
        print('         ~~~~~~~~            ')
        print('         |      |            ')
        print('        (| 0  0 |)           ')
        print('         |  UU  |            ')
        print('         |      |            ')
        print('           |  |              ')
        print('           |  |              ')
        print('          //  \\             ')
        print('         //|  |\\            ')
        print('        // |  | \\           ')
        print('       //  |  |  \\          ')
        print('    ()//   |  |   \\()       ')
        print('  ()( )()  |  | ()( )()      ')
        print('   () ()   |  |  () ()       ')
        print('          //  \\             ')
        print('         //    \\            ')
        print('        //      \\           ')
        print('       //        \\          ')
        print('      //          \\         ')
        print(' ()__//            \\__()    ')
        print(' ()   \            /   ()    ')
        print(' ()____)          (____()    ')

    def hungDead():
        print('         ~~~~~~~~            ')
        print('         |      |            ')
        print('        (| X  X |)           ')
        print('         |  UU  |            ')
        print('         |      |            ')
        print('           |  |              ')
        print('           |  |              ')
        print('          //  \\             ')
        print('         //|  |\\            ')
        print('        // |  | \\           ')
        print('       //  |  |  \\          ')
        print('    ()//   |  |   \\()       ')
        print('  ()( )()  |  | ()( )()      ')
        print('   () ()   |  |  () ()       ')
        print('          //  \\             ')
        print('         //    \\            ')
        print('        //      \\           ')
        print('       //        \\          ')
        print('      //          \\         ')
        print(' ()__//            \\__()    ')
        print(' ()   \            /   ()    ')
        print(' ()____)          (____()    ')

    def cls(num_lines):
        print('\n' * int(num_lines))

    hung = False

    #Picking random word from Player 1's list
    rwPick = random.choice(words)
    if wcount == 0:
        #clear screen to hide player 1's words
        cls(40)
    
    print('A word from ' + p1 + "'s" + ' list of words has been picked by random.\n')
    print(p2 + ', you will guess letter by letter until you believe you know the word.')

    correctLetters = []
    incorrectLetters = []
    wordCharCount = len(rwPick)
    rwp = []
    for letters in rwPick:
        x = format(letters)
        rwp.append(x)

        
    glCount = 0    
    #Number of times to guess the correct word
    guessCount = 3
    while not hung:
        if glCount > 0:
            letterGuess = input(p1 + ', Guess another letter: ').lower()
        else:               #Changing grammar for more realistic feel 
            letterGuess = input(p1 + ', Guess a letter: ').lower()
        #Error catch if Guessed Letter is NOT a letter type
        if letterGuess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Uh Oh! Guess not valid. Please try a letter value.')
            continue

        elif letterGuess not in rwp:
            if str(letterGuess) in incorrectLetters:
                print('Oops! You already entered that letter. Try a different letter.')
                continue
            else:
                print('Uh Oh! That letter is not in the word')
                print('Please try again')
                incorrectLetters.append(letterGuess)

        elif letterGuess in correctLetters:
            print('You have already entered that letter. Try a different letter.')
            continue
                

        elif letterGuess in rwp:
            letter_index = rwp.index(letterGuess)
            multLetters = rwp.count(letterGuess)
            if letterGuess in correctLetters:#catching a letter that has already been entered correctly
                print('You have already entered that letter. Try a different letter.')
                continue
        
            else:
                if multLetters > 1:
                    print('Correct! There are ' + str(multLetters) + ' of those. Guess another letter')
                    while multLetters >= 1:
                        correctLetters.append(letterGuess)
                        rwp.remove(letterGuess)
                        wordCharCount -= 1
                        multLetters -= 1
                        
                else:
                    print('Correct! There is 1 of those. Guess another letter')
                    correctLetters.append(letterGuess)
                    wordCharCount -= 1
                    rwp.remove(letterGuess)
        #Tracking 'Hung' status after every guess
        if len(incorrectLetters) == 1:
            hungFace()
        elif len(incorrectLetters) == 2:
            hungOneLimb()
        elif len(incorrectLetters) == 3:
            hungTwoLimbs()
        elif len(incorrectLetters) == 4:
            hungThreeLimbs()
        elif len(incorrectLetters) == 5:
            hungFourLimbs()
            print('YOU HAVE ONE LAST CHANCE TO GUESS UNTIL YOU ARE HUNG!!!')
        elif len(incorrectLetters) == 6:
            hungDead()
            print('The word was:', rwPick)
            break
        print('Correct Letters: ', correctLetters)
        print('Incorrect Letters: ', incorrectLetters)
        #Adding to guess count
        glCount += 1
        
        #Entering loop to guess chosen word
        if wordCharCount == 0:
            print('You have all of the letters necessary to form the word')
            print('You have 3 guesses. Good Luck!')
            while guessCount > 0:
                guessWord = input('What is your guess: ')

                try:
                    guessWord == str
                except:
                    print('TypeError!')
                    print('Please enter your guess in word form')
                    continue
                
                if guessWord != rwPick:
                    guessCount -= 1
                    print("Uh Oh! That's not it")
                    print('You have ' + str(guessCount) + ' guess left.')
                    if guessCount > 0:
                        continue
                    elif guessCount == 0:
                        print('Unfortunately, you did not guess the correct word')
                        print('Better Luck Next Time!')
                        break
                
                elif guessWord == rwPick:
                    print('***********************************')
                    print('!!!!!!!!!!CONGRATULATIONS!!!!!!!!!!')
                    print('***********************************')
                    print(rwPick + ' was the correct answer!')
                    print('YOU WIN! YOU WIN! YOU WIN! YOU WIN!')
                    hung = True
                    break
            
            
hangMan()
print('Thanks for playing Hangman!')
playAgain = input('Would you like to play again? Y or N: ').lower()

gameEnd = False
while not gameEnd:
    if playAgain == 'n':
        print('Speak with the developer if you would like to play again later.')
        print('Thanks for Playing!')
        time.sleep(1.5)
        quit()
    elif playAgain == 'y':
        print('Loading Hangman...')
        time.sleep(3)
        hangMan()









