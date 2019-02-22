"""
Created on Tue Apr 02 19:05:14 2018

@authors: Jim Fuller, Rashid Baishev, Kyle Venable

"""

### CAPSTONE APPLICATION PROJECT SUBMISSION (SEC College Football Word Challenge) ###
    # This program is based on the word-guessing game "Hangman", with a college football-themed twist.
    # "Hangman" is fun to play - but can be boring.  Our goal here is to use visuals and sounds to add
    # another dimension for fun.  The football-themed scoring also makes for a more competitive and
    # challenging experience.  The user will have the option to select menu items to receive info ABOUT
    # the game, select an Auburn/Alabama IRON BOWL mode, START the game and QUIT the game.  Enjoy!

# Imports
import random
import pygame
import sys
import time
from pygame.locals import *


# Set up pygame (Initialize)
pygame.init()
mainClock = pygame.time.Clock()

# Set up the game window
WINDOWWIDTH = 800
WINDOWHEIGHT = 820
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
pygame.display.set_caption('SEC College Football Word Challenge')


# Set up game colors
BLACK = (0, 0, 0)
CRIMSON = (158,27,50)
GRAY = (130,138,143)
RED = (255, 0, 0)
MRED = (186,12,47) 
ORED = (200,16,46)
DGREEN = (0, 128, 0)
BLUE = (0, 0, 255)
FBLUE = (0,33,165)
DBLUE = (37,72,116)
LBLUE = (0, 200, 255)
BROWN = (128,128,0)
WHITE = (255,255,255)
ORANGE = (232,119,34)
DORANGE = (250,70,22)
TORANGE = (255,130,0)
SKIN = (160,160,60)
DGREY = (25,25,25)
GREY = (50,50,50)
LGRAY = (204,204,204)
LGREY = (160,160,160)
GREEN = (0, 160, 0)
CARDINAL = (157,34,53)
GOLD = (241,184,45)
MGOLD = (253,208,35)
DGOLD = (134,109,75)
PURPLE = (70,29,124)
WBLUE = (0,51,160)
SMOKEY = (88,89,91)
GARNET = (115,0,10)
MAROON = (120,0,0)
DMAROON = (80,0,0)
NAVY = (19,41,75)
SECY = (255,208,70)
SECB = (0,71,137)

# Setup dictionary of team info
team = { "auburn":[(ORANGE, DBLUE),("WAR EAGLE!")],
        "arkansas":[(CARDINAL, WHITE),("GO HOGS!")],
        "missouri":[(BLACK, GOLD),("GO TIGERS!")],
        "vanderbilt":[(BLACK, DGOLD),("GO COMMS!")],
        "lsu":[(PURPLE, MGOLD),("GO TIGERS!")],
        "georgia":[(MRED, BLACK),("GO DAWGS!")],
        "kentucky":[(WBLUE, WHITE),("GO CATS!")],
        "florida":[(FBLUE, DORANGE),("GO GATORS!")],
        "tennessee":[(TORANGE, SMOKEY),("GO VOLS!")],
        "scarolina":[(GARNET, BLACK),("GO COCKY!")],
        "mstate":[(MAROON, LGRAY),("BULLDOGS!")],
        "olemiss":[(ORED, NAVY),("GO REBELS!")],
        "texam":[(DMAROON, WHITE),("GO AGGIES!")],
        "alabama":[(CRIMSON, GRAY),("ROLL TIDE!")]}

# set up the game sounds
correctSound = pygame.mixer.Sound('sounds\correct.wav')
incorrectSound = pygame.mixer.Sound('sounds\incorrect.wav')
changeSides = pygame.mixer.Sound('sounds\whistle.wav')

# Set up variables
guess = ''
missedLetters = ''
correctLetters = ''
cursor = [240, 190, 50, 50] # Start position for the cursor on the menu
option = [0,'ABOUT the GAME','IRON BOWL Mode','NORMAL Mode','QUIT the Game',0,'',0] # menu options
score = [0,0,'',0,0]# [0-Player Rounds,1-Team Rounds,2-Result,3-Player Games, 4-Team Games]
gameIsDone = False
s = 0 # Round counter
h = [280,259,1,40,40,1,100,100,0,0,150,240,13]
p = [150,259,1,40,40,0,100,100,0,0,150,240,13]
guessed = [0,'',0] # [0-(0 invalid guess, 1 valid guess),1-Screen Prompt,2-Keyboard delay
infoDisplayText = ['SEC College Football Word Challenge']
banner =[50,50,0,0,0,0,0,0]# Start point for SEC College Football Word Challenge banner text or logo
show = [0,60,True,True]# 0-Actual FPS, 1-Max FPS
textFile = open('wordlist.txt','r')
roundNo = 0

# Controls menu cursor distance (up or down)
MOVESPEED = 50

# Set up game fonts
smallFont = pygame.font.SysFont(None, 20)
basicFont = pygame.font.SysFont(None, 24)
boardFont = pygame.font.SysFont(None, 30)
guessFont = pygame.font.SysFont(None, 36)
titleFont = pygame.font.SysFont(None, 48)
bannerFont = pygame.font.SysFont(None, 64)

# Set up word dictionary
roundOrder = textFile.readline().split()
wordList0 = textFile.readline().split()

# Word list
words={roundOrder[0]:wordList0}
textFile.close()

# Random Word generator
def getRandomWord(wordDict):
    wordKey = random.choice(list(wordDict.keys()))
    wordIndex = random.randrange(0,len(wordDict[wordKey]))
    return [wordDict[wordKey][wordIndex], wordKey]

# Sequential word generator (Round order info)
def getNextRound(wordDict):
    wordKey = roundOrder[0]
    wordIndex = random.randrange(0,len(wordDict[wordKey]))
    return [wordDict[wordKey][wordIndex], wordKey]

# Home team (Auburn) assignment
def selectTeam(teamDict):
    for key in teamDict.keys():
        if key == "auburn":
            teamKey = key
    return [teamKey, teamDict[teamKey]]

# This prints out home team (Auburn) info to console (for test purposes)
# CODE CAN BE REMOVED LATER - WON'T HURT ANYTHING IF IT STAYS #
selTeam = selectTeam(team)
print(selTeam)

# Random visiting team generator (no duplication with home team)
def randomTeam(teamDict):
    teamDict.pop("auburn")
    teamKey = random.choice(list(teamDict.keys()))
    return [teamKey, teamDict[teamKey]]
    
# This prints out random team info to console (for test purposes)
# CODE CAN BE REMOVED LATER - WON'T HURT ANYTHING IF IT STAYS #
randTeam = randomTeam(team) 
print(randTeam)

# Team color assigments
color1 = selTeam[1][0][0] # Home team (Auburn) main color
color2 = selTeam[1][0][1] # Home team (Auburn) secondary color
color3 = randTeam[1][0][0] # Visiting team main color
color4 = randTeam[1][0][1] # Visiting team secondary color

# Team sound assignments
hteamScore = pygame.mixer.Sound("sounds\\" + "\\" + selTeam[0] + ".wav")
vteamScore = pygame.mixer.Sound("sounds\\" + "\\" + randTeam[0] + ".wav")

#### END AREA FOR: TEAM SELECTION AND LOGIC  ####################################################################

#### START AREA FOR: DISPLAY ORDER ############################################################################## 

# This determines display order
def infoDisplay(who,time):
    count=0
    who[12]=13
    who[11]=240
    who[10]=150

    while count < time:
        if who[2] == who[12]:
            count+=1
        if who[2]< who[12]:
            who[2] += 1
        if who[2] >who[12]:
            who[2] -= 1
        if who[0] > who[10]:
            who[0]-=10
        if who[0] < who[10]:
            who[0]+=10
        if who[1] > who[11]:
            who[1]-=10
        if who[1] < who[11]:
            who[1]+=10
        if count >(time-11):
            who[12]=1
            who[11]=259
        background()
        field()
        football()
        displayBoard(s, missedLetters, correctLetters, secretWord)
        
#### END AREA FOR: DISPLAY ORDER ################################################################################ 
####
#### START AREA FOR: FIELD GRAPHICS (INCLUDING FOOTBALL) ########################################################

# Background color
def background():
        windowSurface.fill(LBLUE)
        
# Draw the football - the ellipses move down and the rectangles elongate
def football():
    move1 = 378 
    move2 = 380
    move3 = 388
    move4 = 389  
    
    # Draw football
    pygame.draw.ellipse(windowSurface, BLACK, (288,move1,29,48),0) # footlball outline
    pygame.draw.ellipse(windowSurface, BROWN, (290,move2,25,44),0) # football fill
    pygame.draw.rect(windowSurface, BLACK,(300,move3,4,27),0)  
    pygame.draw.rect(windowSurface, WHITE,(301,move4,2,25),0)  

    # Control movement of football
    for i in range (len(secretWord)):
        if secretWord[i] in correctLetters:
            move = int(175/len(secretWord))
            
            # new footbal position
            pygame.draw.ellipse(windowSurface, BLACK, (288,move1-move,29,48),0) 
            pygame.draw.ellipse(windowSurface, BROWN, (290,move2-move,25,44),0) 
            pygame.draw.rect(windowSurface, BLACK,(300,move3-move,4,27),0)  
            pygame.draw.rect(windowSurface, WHITE,(301,move4-move ,2,25),0) 

            move1 = move1 - move
            move2 = move2 - move
            move3 = move3 - move
            move4 = move4 - move
            
        else:
            move = 0        

# Build the field (left position, top position, width, length)
def field():
    
    textdown1 = guessFont.render('FIRST DOWN', True, WHITE,) # down 1 text
    textdown1s = guessFont.render('FIRST DOWN', True, BLACK,) # down 1 text shadow
    windowSurface.blit(textdown1s, (227,103)) # draw down 1 text shadow
    windowSurface.blit(textdown1, (224,100)) # draw down 1 text
   
    # Draw the field and stadium sections
    pygame.draw.ellipse(windowSurface, BLACK, (84, 144, 430, 518),0) # Stadium outline
    pygame.draw.ellipse(windowSurface, LGREY, (88, 148, 422, 510),0) # Stadium
    pygame.draw.rect(windowSurface, BLACK,(196, 188, 208, 428)) # Field outline 
    pygame.draw.rect(windowSurface, WHITE,(200, 192, 200, 420)) # Field lines 
    pygame.draw.rect(windowSurface, GREEN,(204, 196, 192, 402)) # Field grass
    pygame.draw.rect(windowSurface, color1,(204, 196, 192, 30)) # Top endzone grass
    pygame.draw.rect(windowSurface, color3,(204, 578, 192, 30)) # Bottom endzone grass
    
    # Draw the yard lines (left,top,width from left,length from top)
    pygame.draw.rect(windowSurface, WHITE,(200, 224, 200, 3)) # Top goalline    
    pygame.draw.rect(windowSurface, WHITE,(200, 259, 200, 3)) # Top 10 yard line
    pygame.draw.rect(windowSurface, WHITE,(200, 294, 200, 3)) # Top 20 yard line
    pygame.draw.rect(windowSurface, WHITE,(200, 329, 200, 3)) # Top 30 yard line
    pygame.draw.rect(windowSurface, WHITE,(200, 364, 200, 3)) # Top 40 yard line
    pygame.draw.rect(windowSurface, WHITE,(200, 399, 200, 3)) # 50 yard line (mid-field)   
    pygame.draw.rect(windowSurface, WHITE,(200, 434, 200, 3)) # Bottom 40 yard line
    pygame.draw.rect(windowSurface, WHITE,(200, 469, 200, 3)) # Bottom 30 yard line
    pygame.draw.rect(windowSurface, WHITE,(200, 504, 200, 3)) # Bottom 20 yard line
    pygame.draw.rect(windowSurface, WHITE,(200, 539, 200, 3)) # Bottom 10 yard lineh
    pygame.draw.rect(windowSurface, WHITE,(200, 574, 200, 3)) # Bottom goalline 

    # Fans in left stands (front row)
    pygame.draw.circle(windowSurface, color1, (182, 226), 10)
    pygame.draw.circle(windowSurface, color1, (182, 251), 10)
    pygame.draw.circle(windowSurface, color1, (182, 276), 10)
    pygame.draw.circle(windowSurface, color2, (182, 301), 10)
    pygame.draw.circle(windowSurface, color2, (182, 326), 10)
    pygame.draw.circle(windowSurface, color2, (182, 351), 10)
    pygame.draw.circle(windowSurface, color1, (182, 376), 10)
    pygame.draw.circle(windowSurface, color1, (182, 401), 10)
    pygame.draw.circle(windowSurface, color2, (182, 426), 10)
    pygame.draw.circle(windowSurface, color2, (182, 451), 10)
    pygame.draw.circle(windowSurface, color1, (182, 476), 10)
    pygame.draw.circle(windowSurface, color2, (182, 501), 10)
    pygame.draw.circle(windowSurface, color1, (182, 526), 10)
    pygame.draw.circle(windowSurface, color1, (182, 551), 10)
    pygame.draw.circle(windowSurface, color2, (182, 576), 10)
    
    # Fans in left stands (middle row)
    pygame.draw.circle(windowSurface, color1, (160, 238), 10)
    pygame.draw.circle(windowSurface, color2, (160, 263), 10)
    pygame.draw.circle(windowSurface, color2 , (160, 288), 10)
    pygame.draw.circle(windowSurface, color1, (160, 313), 10)
    pygame.draw.circle(windowSurface, color1, (160, 338), 10)
    pygame.draw.circle(windowSurface, color1, (160, 363), 10)
    pygame.draw.circle(windowSurface, color2, (160, 388), 10)
    pygame.draw.circle(windowSurface, color1, (160, 413), 10)
    pygame.draw.circle(windowSurface, color2, (160, 438), 10)
    pygame.draw.circle(windowSurface, color1, (160, 463), 10)
    pygame.draw.circle(windowSurface, color1, (160, 488), 10)
    pygame.draw.circle(windowSurface, color2, (160, 513), 10)
    pygame.draw.circle(windowSurface, color2, (160, 538), 10)
    pygame.draw.circle(windowSurface, color1, (160, 563), 10)
    
    # Fans in left stands (back row)
    pygame.draw.circle(windowSurface, color1, (138, 276), 10)
    pygame.draw.circle(windowSurface, color1, (138, 301), 10)
    pygame.draw.circle(windowSurface, color1, (138, 326), 10)
    pygame.draw.circle(windowSurface, color2, (138, 351), 10)
    pygame.draw.circle(windowSurface, color1, (138, 376), 10)
    pygame.draw.circle(windowSurface, color1, (138, 401), 10)
    pygame.draw.circle(windowSurface, color2, (138, 426), 10)
    pygame.draw.circle(windowSurface, color2, (138, 451), 10)
    pygame.draw.circle(windowSurface, color1, (138, 476), 10)
    pygame.draw.circle(windowSurface, color2, (138, 501), 10)
    pygame.draw.circle(windowSurface, color2, (138, 526), 10)

    # Fans in left stands (nosebleed row)
    pygame.draw.circle(windowSurface, color2, (116, 313), 10)    
    pygame.draw.circle(windowSurface, color1, (116, 338), 10)
    pygame.draw.circle(windowSurface, color1, (116, 363), 10)
    pygame.draw.circle(windowSurface, color2, (116, 388), 10)
    pygame.draw.circle(windowSurface, color1, (116, 413), 10)
    pygame.draw.circle(windowSurface, color1, (116, 438), 10)
    pygame.draw.circle(windowSurface, color1, (116, 463), 10)
    pygame.draw.circle(windowSurface, color2, (116, 488), 10)  


    # Fans in right stands (front row)
    pygame.draw.circle(windowSurface, color3, (417, 226), 10)
    pygame.draw.circle(windowSurface, color3, (417, 251), 10)
    pygame.draw.circle(windowSurface, color4, (417, 276), 10)
    pygame.draw.circle(windowSurface, color3, (417, 301), 10)
    pygame.draw.circle(windowSurface, color4, (417, 326), 10)
    pygame.draw.circle(windowSurface, color4, (417, 351), 10)
    pygame.draw.circle(windowSurface, color3, (417, 376), 10)
    pygame.draw.circle(windowSurface, color4, (417, 401), 10)
    pygame.draw.circle(windowSurface, color4, (417, 426), 10)
    pygame.draw.circle(windowSurface, color3, (417, 451), 10)
    pygame.draw.circle(windowSurface, color3, (417, 476), 10)
    pygame.draw.circle(windowSurface, color3, (417, 501), 10)
    pygame.draw.circle(windowSurface, color4, (417, 526), 10)
    pygame.draw.circle(windowSurface, color4, (417, 551), 10)
    pygame.draw.circle(windowSurface, color3, (417, 576), 10)
    
    # Fans in right stands (middle row)
    pygame.draw.circle(windowSurface, color4, (439, 238), 10)
    pygame.draw.circle(windowSurface, color4, (439, 263), 10)
    pygame.draw.circle(windowSurface, color4, (439, 288), 10)
    pygame.draw.circle(windowSurface, color3, (439, 313), 10)
    pygame.draw.circle(windowSurface, color4, (439, 338), 10)
    pygame.draw.circle(windowSurface, color4, (439, 363), 10)
    pygame.draw.circle(windowSurface, color4, (439, 388), 10)
    pygame.draw.circle(windowSurface, color3, (439, 413), 10)
    pygame.draw.circle(windowSurface, color4, (439, 438), 10)
    pygame.draw.circle(windowSurface, color4, (439, 463), 10)
    pygame.draw.circle(windowSurface, color4, (439, 488), 10)
    pygame.draw.circle(windowSurface, color3, (439, 513), 10)
    pygame.draw.circle(windowSurface, color3, (439, 538), 10)
    pygame.draw.circle(windowSurface, color3, (439, 563), 10)
    
    # Fans in right stands (back row)
    pygame.draw.circle(windowSurface, color3, (461, 276), 10)
    pygame.draw.circle(windowSurface, color4, (461, 301), 10)
    pygame.draw.circle(windowSurface, color4, (461, 326), 10)
    pygame.draw.circle(windowSurface, color3, (461, 351), 10)
    pygame.draw.circle(windowSurface, color3, (461, 376), 10)
    pygame.draw.circle(windowSurface, color4, (461, 401), 10)
    pygame.draw.circle(windowSurface, color4, (461, 426), 10)
    pygame.draw.circle(windowSurface, color4, (461, 451), 10)
    pygame.draw.circle(windowSurface, color3, (461, 476), 10)
    pygame.draw.circle(windowSurface, color4, (461, 501), 10)
    pygame.draw.circle(windowSurface, color3, (461, 526), 10)

    # Fans in right stands (nosebleed row)
    pygame.draw.circle(windowSurface, color3, (483, 313), 10)    
    pygame.draw.circle(windowSurface, color4, (483, 338), 10)
    pygame.draw.circle(windowSurface, color4, (483, 363), 10)
    pygame.draw.circle(windowSurface, color3, (483, 388), 10)
    pygame.draw.circle(windowSurface, color3, (483, 413), 10)
    pygame.draw.circle(windowSurface, color3, (483, 438), 10)
    pygame.draw.circle(windowSurface, color4, (483, 463), 10)
    pygame.draw.circle(windowSurface, color4, (483, 488), 10)
    
    # Fans in top stands
    pygame.draw.circle(windowSurface, color1, (238, 174), 10)
    pygame.draw.circle(windowSurface, color2, (263, 174), 10)
    pygame.draw.circle(windowSurface, color2, (288, 174), 10)
    pygame.draw.circle(windowSurface, color1, (313, 174), 10)
    pygame.draw.circle(windowSurface, color2, (338, 174), 10)
    pygame.draw.circle(windowSurface, color1, (363, 174), 10)
    
    # Fans in bottom stands
    pygame.draw.circle(windowSurface, color3, (238, 630), 10)
    pygame.draw.circle(windowSurface, color4, (263, 630), 10)
    pygame.draw.circle(windowSurface, color3, (288, 630), 10)
    pygame.draw.circle(windowSurface, color3, (313, 630), 10)
    pygame.draw.circle(windowSurface, color4, (338, 630), 10)
    pygame.draw.circle(windowSurface, color4, (363, 630), 10)

    # Number the yard lines (left)
    textTL10 = guessFont.render("10",True, WHITE,) # Left/top 10 yard line number
    textTL10 = pygame.transform.rotate(textTL10, 270)
    windowSurface.blit(textTL10, (207,249))
    textTL20 = guessFont.render("20",True, WHITE,) # Left/top 20 yard line number
    textTL20 = pygame.transform.rotate(textTL20, 270)
    windowSurface.blit(textTL20, (207,281))
    textTL30 = guessFont.render("30",True, WHITE,) # Left/top 30 yard line number
    textTL30 = pygame.transform.rotate(textTL30, 270)
    windowSurface.blit(textTL30, (207,316))
    textTL40 = guessFont.render("40",True, WHITE,) # Left/top 40 yard line number
    textTL40 = pygame.transform.rotate(textTL40, 270)
    windowSurface.blit(textTL40, (207,352))
    textL50 = guessFont.render("50",True, WHITE,) # 50 yard line number
    textL50 = pygame.transform.rotate(textL50, 270)
    windowSurface.blit(textL50, (207,387))
    textBL40 = guessFont.render("40",True, WHITE,) # Left/bottom 40 yard line number
    textBL40 = pygame.transform.rotate(textBL40, 270)
    windowSurface.blit(textBL40, (207,422))
    textBL30 = guessFont.render("30",True, WHITE,) # Left/bottom 30 yard line number
    textBL30 = pygame.transform.rotate(textBL30, 270)
    windowSurface.blit(textBL30, (207,456))
    textBL20 = guessFont.render("20",True, WHITE,) # Left/bottom 20 yard line number
    textBL20 = pygame.transform.rotate(textBL20, 270)
    windowSurface.blit(textBL20, (207,491))
    textBL10 = guessFont.render("10",True, WHITE,) # Left/bottom 10 yard line number
    textBL10 = pygame.transform.rotate(textBL10, 270)
    windowSurface.blit(textBL10, (207,529))
    
    # Number the yard lines (right)
    textTR10 = guessFont.render("10",True, WHITE,) # Right/top 10 yard line number
    textTR10 = pygame.transform.rotate(textTR10, 90)
    windowSurface.blit(textTR10, (368,246))
    textTR20 = guessFont.render("20",True, WHITE,) # Right/top 20 yard line number
    textTR20 = pygame.transform.rotate(textTR20, 90)
    windowSurface.blit(textTR20, (368,282))
    textTR30 = guessFont.render("30",True, WHITE,) # Right/top 30 yard line number
    textTR30 = pygame.transform.rotate(textTR30, 90)
    windowSurface.blit(textTR30, (368,317))
    textTR40 = guessFont.render("40",True, WHITE,) # Right/top 40 yard line number
    textTR40 = pygame.transform.rotate(textTR40, 90)
    windowSurface.blit(textTR40, (368,351))
    textR50 = guessFont.render("50",True, WHITE,) # 50 yard line number
    textR50 = pygame.transform.rotate(textR50, 90)
    windowSurface.blit(textR50, (368,388))
    textBR40 = guessFont.render("40",True, WHITE,) # Right/bottom 40 yard line number
    textBR40 = pygame.transform.rotate(textBR40, 90)
    windowSurface.blit(textBR40, (368,421))
    textBR30 = guessFont.render("30",True, WHITE,) # Right/bottom 30 yard line number
    textBR30 = pygame.transform.rotate(textBR30, 90)
    windowSurface.blit(textBR30, (368,457))
    textBR20 = guessFont.render("20",True, WHITE,) # Right/bottom 20 yard line number
    textBR20 = pygame.transform.rotate(textBR20, 90)
    windowSurface.blit(textBR20, (368,492))
    textBR10 = guessFont.render("10",True, WHITE,) # Right/bottom 10 yard line number
    textBR10 = pygame.transform.rotate(textBR10, 90)
    windowSurface.blit(textBR10, (368,526))

#### END AREA FOR: FIELD GRAPHICS ###############################################################################
####
#### START AREA FOR: GAME ORDER #################################################################################    

# Controls order (gameplay)
def gameover(who):
    while who[6]<who[7]:
        who[6]+=2
        update()
    who[7]=200
    while who[6]>who[7]:
        who[6]-=2
        who[1]-=2
        who[5]=''
        update()

#### END AREA FOR: GAME ORDER ###################################################################################        
####        
#### START AREA FOR: GUESS LOGIC ################################################################################

# Gets the players guess & ensures guess is valid
def getGuess(alreadyGuessed):
    while event.type == KEYDOWN:
        global guess
        guessed[0]=1
        guessed[2]=15
        guess = event.dict['unicode']
        guess = guess.lower()
        if event.key == K_9: # Show FPS
            if show[0] == 1:
                show[0] = 0 
            else:
                show[0] = 1 
        if event.key == K_8:
            if show[2] == True:
                show[2] = False 
            else:
                show[2] = True  
        if event.key == K_7: # Show Background
            if show[3] == True:
                show[3] = False 
            else:
                show[3] = True  
        if event.key == K_EQUALS: # Increase max FPS
            show[1] += 5 
        if event.key == K_MINUS: # Decrease max FPS
            show[1] -= 5
        if len(guess) != 1:
                    guessed[0]=0
                    guessed[1]='Please enter a single letter'
                    break
        elif str(guess) in alreadyGuessed:
                    guessed[0]=0
                    guessed[1]='Pick a different letter'
                    break
        elif str(guess) not in 'abcdefghijklmnopqrstuvwxyz':
                    guessed[0]=0
                    guessed[1]='Please enter a letter'
                    break
        else:
                    guessed[1]=''
                    return guess
    else:
        guessed[0]=0
        guessed[2]=0
        return

#### END AREA FOR: GUESS LOGIC ##################################################################################
####        
#### START AREA FOR: DISPLAYS FOR GUESSES AND TEAM GRAPHICS #####################################################
        
# Updates the screen with the guesses, correct letters, teams logos & mascots, scores
def displayBoard(display,missedLetters, correctLetters, secretWord):
    blanks = '-' * len(secretWord)
    blankText = titleFont.render(blanks, True, BLACK,)
    windowSurface.blit(blankText, (225,720))
    pygame.draw.rect(windowSurface, BLACK,(604,100,148,580),3)
    pygame.draw.rect(windowSurface, WHITE,(606,102,144,20))
    pygame.draw.rect(windowSurface, BLACK,(604,100,148,24),3)
    pygame.draw.rect(windowSurface, BLACK,(604,394,148,34),3) # message rectangle (above mascot)

    # Display used letter box and scores
    title = basicFont.render('Used Letters', True, RED,)
    scoreboard = titleFont.render(str(score[0]), True, BLACK,) # team 1 score
    scoreboard2 = titleFont.render(str(score[1]), True, BLACK,) # team 2 score
    guessText = basicFont.render(guessed[1], True, BLACK,)
    windowSurface.blit(guessText, (225,690))
    windowSurface.blit(title,(628,105))
    windowSurface.blit(scoreboard,(124,110))
    windowSurface.blit(scoreboard2,(442,110))
    
    # Display SEC logo
    pygame.draw.rect(windowSurface, BLACK,(604,240,148,3),0)
    pygame.draw.rect(windowSurface, BLACK,(604,246,148,3),0)
    sec = pygame.image.load("logos\sec_board.jpg")
    windowSurface.blit(sec, (606,243))    
    
    # Display team logos
    t1logo = ("logos\\" + selTeam[0] + ".jpg")
    team1 = pygame.image.load(t1logo) # team 1 logo 
    windowSurface.blit(team1, (100,20)) # draw team 1 logo
    t2logo = ("logos\\" + randTeam[0] + ".jpg")
    team2 = pygame.image.load(t2logo) # team 2 logo
    windowSurface.blit(team2, (420,20)) # draw team 2 logo

    # Display home mascot
    hmascot = ("mascots\\" + selTeam[0] + "_mas.jpg")
    team3 = pygame.image.load(hmascot) # team 1 logo 
    windowSurface.blit(team3, (606,429)) # draw team 1 logo    

    # home pep messages
    hr = selTeam[1][1]
    pygame.draw.rect(windowSurface, color1,(606,396,144,30))
    hresult = boardFont.render(hr, True, WHITE,)
    windowSurface.blit(hresult, (610,402))

    
    if score[2]!='':
        pygame.draw.rect(windowSurface, RED,(606,396,144,30))
        
        result = boardFont.render(score[2], True, WHITE,)
        windowSurface.blit(result, (610,402))
        
        answer = titleFont.render(secretWord, True, WHITE,)
        windowSurface.blit(answer, (225,760))

        
    for i in range (len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks [i+1:]
            correctText = titleFont.render(blanks, True, BLACK,)
            pygame.draw.rect(windowSurface, LBLUE,(225, 720, 300,40))
            windowSurface.blit(correctText, (225,720))
       
    if display == 0:
        football()

    # Display second down and missed letter from first down
    elif display >=1:
        pygame.draw.rect(windowSurface, WHITE,(606,124,144,30)) # first missed letter backgroud
        pygame.draw.rect(windowSurface, BLACK,(605,124,146,30),1) # first missed letter outline
        textdown2 = guessFont.render('SECOND DOWN', True, WHITE,) # down 2 text
        textdown2s = guessFont.render('SECOND DOWN', True, BLACK,) # down 2 text shadow
        textmiss1 = guessFont.render(missedLetters[0].lower(), True, BLUE,) # first missed letter
        pygame.draw.rect(windowSurface, LBLUE,(190,90,230,40)) # draw down 2 background
        windowSurface.blit(textdown2s, (211,103)) # draw down 2 text shadow
        windowSurface.blit(textdown2, (208,100)) # draw down 2 text
        windowSurface.blit(textmiss1, (670,126)) # draw first missed letter 
        
        # Display third down and missed letter from second down
        if display >= 2:
            pygame.draw.rect(windowSurface, WHITE,(606,153,144,30)) # second missed letter background
            pygame.draw.rect(windowSurface, BLACK,(605,153,146,30),1) # second missed letter outline
            textdown3 = guessFont.render('THIRD DOWN', True, WHITE,) # down 3 text
            textdown3s = guessFont.render('THIRD DOWN', True, BLACK,) # down 3 text shadow
            textmiss2 = guessFont.render(missedLetters[1].lower(), True, BLUE,) # second missed letter
            pygame.draw.rect(windowSurface, LBLUE,(202,90,218,40))  # draw down 3 background
            windowSurface.blit(textdown3s, (223,103)) # draw down 3 text shadow
            windowSurface.blit(textdown3, (220,100)) # draw down 3 text
            windowSurface.blit(textmiss2, (670,155)) # draw second missed letter

            # Display fourth down and missed letter from third down
            if display >= 3:
                pygame.draw.rect(windowSurface, WHITE,(606,182,144,30)) # third missed letter background
                pygame.draw.rect(windowSurface, BLACK,(605,182,146,30),1) # third missed letter outline
                textdown4 = guessFont.render('FOURTH DOWN', True, WHITE,) # down 4 text 
                textdown4s = guessFont.render('FOURTH DOWN', True, BLACK,) # down 4 text shadow
                textmiss3 = guessFont.render(missedLetters[2].lower(), True, BLUE,) # third missed letter
                pygame.draw.rect(windowSurface, LBLUE,(190,90,230,40)) # draw down 4 background
                windowSurface.blit(textdown4s, (211,103)) # draw down 4 text shadow
                windowSurface.blit(textdown4, (208,100)) # draw down 4 text
                windowSurface.blit(textmiss3, (670,184)) # draw third missed letter

                # Display change down and missed letter from fourth down
                if display >= 4:
                    pygame.draw.rect(windowSurface, WHITE,(606,211,144,30)) # fourth missed letter background
                    pygame.draw.rect(windowSurface, BLACK,(605,211,146,30),1) # fourth missed letter outline
                    textdown5 = guessFont.render('TURN OVER!', True, WHITE,) # down change text
                    textdown5s = guessFont.render('TURN OVER!', True, RED,) # down change text shadow
                    textmiss4 = guessFont.render(missedLetters[3].lower(), True, BLUE,) # fourth missed letter
                    pygame.draw.rect(windowSurface, LBLUE,(202,90,218,40)) # draw down change background
                    windowSurface.blit(textdown5s, (227,103)) # draw down change text shadow
                    windowSurface.blit(textdown5, (224,100)) # draw down change text 
                    windowSurface.blit(textmiss4, (670,213)) # draw fourth missed letter
                    
                    # Reveal secret word
                    answer = titleFont.render(secretWord, True, WHITE,) # show word
                    windowSurface.blit(answer, (225,760))
                    
                    # Display visitor mascot
                    vmascot = ("mascots\\" + randTeam[0] + "_mas.jpg")
                    team5 = pygame.image.load(vmascot) # team 1 logo 
                    windowSurface.blit(team5, (606,429)) # draw team 1 logo
                    
                    # visitor pep messages
                    vr = randTeam[1][1]
                    pygame.draw.rect(windowSurface, color3,(606,396,144,30))
                    vresult = boardFont.render(vr, True, WHITE,)
                    windowSurface.blit(vresult, (610,402))

#### END AREA FOR: DISPLAYS FOR GUESSES AND TEAM GRAPHICS #######################################################
####
#### START AREA FOR: MAIN GAME LOOP (INCLUDING CLOCK DISPLAY) ###################################################

# Draw the window onto the screen (updates)
def update():
    background()
    field()
    football()
    displayBoard(s, missedLetters, correctLetters, secretWord)
    framerate()
    pygame.display.update()

# Start functions
def start():
    background()
    field()
    football()
    infoDisplay(p,150)
    framerate()
    pygame.display.update()

# Adjust graphics frame rate
def framerate():
    mainClock.tick(show[1])
    fps=int(mainClock.get_fps())
    if show[0]==1: 
        texts = smallFont.render(str(fps), True, BLACK,)
        text = smallFont.render(str(fps), True, WHITE,)
        windowSurface.blit(texts, (780,460))
        windowSurface.blit(text, (781,461))
        text1s = smallFont.render(str(show[1]), True, BLACK,) 
        text1 = smallFont.render(str(show[1]), True, WHITE,) 
        windowSurface.blit(text1s, (780,450))
        windowSurface.blit(text1, (781,451))

# Opening menu
def menu():
   
    # Run the menu loop
    moveUp = False
    moveDown = False
    while option[5]==0:# Option [5] is the selection output bit for menu
        
        # Check for keyboard events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                
                    # Change the keyboard variables
                    if event.key == K_UP or event.key == ord('w'):#cursor Up
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == ord('s'):#cursor Down
                        moveUp = False
                        moveDown = True
                    if event.key == K_9: # Show FPS
                        if show[0] == 1:
                            show[0] = 0 
                        else:
                            show[0] = 1  
                    if event.key == K_8: 
                        if show[2] == True:
                            show[2] = False 
                        else:
                            show[2] = True 
                    if event.key == K_7: # Show Background
                        if show[3] == True:  
                            show[3] = False 
                        else:
                            show[3] = True 
                    if event.key == K_EQUALS: # Increase max FPS
                        show[1] += 5  
                    if event.key == K_MINUS: # Decrease max FPS
                        show[1] -= 5  

                    # Select options using spacebar        
                    if event.key == K_RETURN or event.key == K_SPACE: # Select current option
                        
                        # Selection option for About menu item
                        if cursor[1]==190:
                            option[7]=6000
                            about()
                        
                        # Selection option for Time Change menu item                                
                        if cursor[1]==240:
#                            option[5]=2
                            option[7]=6000
                            about()
    
                        # Selection option for Start Game menu item    
                        if cursor[1]==290:
                            option[5]=3
                            secretWord,secretKey = getNextRound(words)
                        
                        # Selection option for Quit Game
                        if cursor[1]==340:
                            pygame.quit()
                            sys.exit()                            
                            
            # Option to escape window               
            if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_UP or event.key == ord('w'):
                        moveUp = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveDown = False

        # Move the cursor
        if moveDown and cursor[1] < 300:
            cursor[1] += MOVESPEED
            moveDown = False
        if moveUp and cursor[1] > 200:
            cursor[1] -= MOVESPEED
            moveUp = False

        # Draw the background onto the surface & draw the banner
        background()
        drawBanner()

        ## Comments for menu items
        # Comment for Team Selection           
        if cursor[1]==190:
            cursor[2]=231
            option[6]='Rules and Info ABOUT the Game'            
        # Comment for Game Length
        if cursor[1]==240:
            cursor[2]=408
            option[6]='IRON BOWL Mode - Scoring: YOU [7] ALABAMA [7]'
        # Comment for Start Game
        if cursor[1]==290:
            cursor[2]=218
            option[6]='NORMAL Mode - Scoring: YOU [7] OPPONENT [3]'
        # Comment for Quit Game            
        if cursor[1]==340:
            cursor[2]=204
            option[6]='QUIT the Game'
            
        # Draw the cursor onto the surface
        pygame.draw.rect(windowSurface, BLACK, (cursor[0],cursor[1],cursor[2],cursor[3]),1)

        # Draw the options onto the surface
        text1s = guessFont.render(option[1], True, WHITE,)
        text1 = guessFont.render(option[1], True, BLACK,)
        text2s = guessFont.render(option[2], True, WHITE,)
        text2 = guessFont.render(option[2], True, BLACK,)
        text3s = guessFont.render(option[3], True, WHITE,)
        text3 = guessFont.render(option[3], True, BLACK,)
        text4s = guessFont.render(option[4], True, WHITE,)
        text4 = guessFont.render(option[4], True, BLACK,)
        text5s = basicFont.render(option[6], True, SECB,)
        text6 = pygame.image.load("logos\sec.png")
        text6s = pygame.image.load("logos\sec_logo.png")
        windowSurface.blit(text1s, (250,200))
        windowSurface.blit(text1, (252,202))
        windowSurface.blit(text2s, (250,250))
        windowSurface.blit(text2, (252,252))
        windowSurface.blit(text3s, (250,300))
        windowSurface.blit(text3, (252,302))
        windowSurface.blit(text4s, (250,350))
        windowSurface.blit(text4, (252,352))
        windowSurface.blit(text5s, (250,400))
        windowSurface.blit(text6, (banner[0],banner[1]))
        windowSurface.blit(text6s, (290,450))
        backgroundAnim()
        framerate()

        # Draw the window onto the screen
        pygame.display.update()

# Draw the banner section
def drawBanner():
    pygame.draw.line(windowSurface,WHITE,(0,70),(800,70),49)
    pygame.draw.line(windowSurface,BLACK,(0,46),(800,46),3)
    pygame.draw.line(windowSurface,BLACK,(0,93),(800,93),3)

# Animate the banner text and background
def backgroundAnim():
        if banner[0]<=800:
            banner[0]+=1
        if banner[0]>800:
            banner[0]=-700
        if banner[2]<=800:
            banner[2]+=1
        if banner[2]>800:
            banner[2]=0
        if banner[3]<=800:
            banner[3]+=2
        if banner[3]>800:
            banner[3]=0
        if banner[4]<=800:
            banner[4]+=3
        if banner[4]>800:
            banner[4]=0
        if banner[5]<=800:
            banner[5]+=4
        if banner[5]>800:
            banner[5]=0
        if banner[6]>800:
            banner[6]=-150
        banner[7]+=1
        if banner[7]>10:
            banner[7]=0
            banner[6]+=1

# Info for "About" section            
def about():
    while option[7]>=0:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_SPACE: # SPACE BAR to return to main menu
                    option[7]=0
            if event.type == KEYUP:
                if event.key == K_RETURN:
                    option[7]=0
                    menu()

        background()
        drawBanner()
        
        # Text assignment for About section
        text1 = guessFont.render("    Welcome to the SEC College Football Word Challenge!", True, WHITE,)
        text2 = boardFont.render('Based on the word-guessing game "Hangman", this game adds a football', True, BLACK,)
        text3 = boardFont.render('theme that makes for fun visuals and a competitive challenge.' , True, BLACK,)
        text4 = boardFont.render('You are Aubie, the Auburn University mascot, competing against other ' , True, BLACK,)
        text5 = boardFont.render('random mascots of the SEC nation for spelling superiority.', True, BLACK,)
        text6 = boardFont.render("Rules and functions are simple:",True, BLACK,)
        text6b = boardFont.render("1). Use UP/DOWN keys to cycle through menus || SPACE BAR to select",True, BLACK,)
        text6c = boardFont.render("2). Tap a LETTER key to submit a guess || SPACE BAR will exit screens",True, BLACK,)
        text7 = boardFont.render("3). You have 10 minutes to defeat your opponent for WORD supremacy.",True, BLACK,)
        text7b = boardFont.render("4). You have four (4) downs to guess the secret word.",True, BLACK,)
        text8 = boardFont.render("      a). If you succeed, you get seven (7) points.",True, BLACK,)
        text9 = boardFont.render("      b). If you fail, the opposing team gets three(3) points.",True, BLACK,)
        text10 = boardFont.render("5). Play continues until time expires and a champion is crowned.",True, BLACK,)
        text11 = boardFont.render("GOOD LUCK and ...",True, BLACK,)
        
        text12s = bannerFont.render("WAR  EAGLE!",True, ORANGE,) # Text Shadow
        text12 = bannerFont.render("WAR  EAGLE!",True, DBLUE,)
        
        # Banner logo in About section
        text13 = pygame.image.load("logos\sec.png") 
        
        # Draw text to About section
        windowSurface.blit(text1, (50,150)) 
        windowSurface.blit(text2, (50,220))
        windowSurface.blit(text3, (50,250))
        windowSurface.blit(text4, (50,300))        
        windowSurface.blit(text5, (50,330))
        windowSurface.blit(text6, (50,380))
        windowSurface.blit(text6b, (50,410))
        windowSurface.blit(text6c, (50,440))
        windowSurface.blit(text7, (50,470))
        windowSurface.blit(text7b, (50,500))
        windowSurface.blit(text8, (50,530))
        windowSurface.blit(text9, (50,560))
        windowSurface.blit(text10, (50,590))
        windowSurface.blit(text11, (50,640))
        
        windowSurface.blit(text12s, (48,718)) # Draw WAR EAGLE! shadow  
        windowSurface.blit(text12, (50,720)) # Draw WAR EAGLE!

        # Draw banner logo to About section
        windowSurface.blit(text13, (banner[0]-2,banner[1]-2))
        
        # Update animation
        backgroundAnim()
        option[7]-=1
        framerate()
        pygame.display.update()            

    ##### CLOCK #####
# Clock frame rate information and time duration
frame_count = 0
frame_rate = 60
start_time = 600 # adjust (in seconds) for clock duration
    ##### CLOCK #####

# Run the game loop
menu()            
secretWord,secretKey = getNextRound(words)
start()
infoDisplay(h,int(show[1]*2.5)) 

while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RETURN or event.key == K_SPACE: # SPACE BAR to return to main menu
                option[7]=0 
        if event.type == KEYUP:
            if event.key == K_RETURN:
                option[7]=0 
                menu()
                
        
    ##### START MAIN CLOCK SECTION #################### 
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
 
    # --- Timer going up ---
    # Calculate total seconds
    total_seconds = frame_count // frame_rate
 
    # Divide by 60 to get total minutes
    minutes = total_seconds // 60
 
    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60
 
    # --- Timer going down ---
    # Calculate total seconds
    total_seconds = start_time - (frame_count // frame_rate)
    if total_seconds < 0:
        total_seconds = 0
 
    # Divide by 60 to get total minutes
    minutes = total_seconds // 60
 
    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60
 
    # Use python string formatting to format in leading zeros
    output_string = "{0:02}:{1:02}".format(minutes, seconds)
 
    # Blit (draw) clock text to screen
    text = titleFont.render(output_string, True, BLACK)
    windowSurface.blit(text, [255, 20])
 
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    frame_count += 1
 
    # Limit frames per second
    mainClock.tick(show[0])
 
    # Go ahead and update the screen with drawn items.
    pygame.display.update()
    
    ##### END MAIN CLOCK SECTION ######################   

    # Guess logic and update
    update()
    if guessed[2]>0:# Guess input keyboard delay
        guessed[2]-=1
    else:
        if guessed[0] == 0:
            getGuess(missedLetters + correctLetters)
        else:
            guessed[0]=0
            if str(guess) in secretWord:
                correctSound.play()
                correctLetters = correctLetters + guess
                foundAllLetters = True
                for i in range(len(secretWord)):
                    if secretWord[i] not in correctLetters:
                        foundAllLetters = False
                        break
                    
                # Guess logic and control for success in guessing secert word
                if foundAllLetters:
                    score[2]='TOUCHDOWN'
                    hteamScore.play()
                    h[7]=h[1]  
                    
                    gameover(h)
                    score[0]+=7
                    roundNo+=1
                    if roundNo>8:
                        roundNo=0
                        score[2]=''
                        score[3]+=1
                        infoDisplay(p,int(show[1]*2.5))
                        infoDisplay(h,int(show[1]*2.5))
                        gameIsDone = True
                    else:
                        score[2]=''
                        guess = ''
                        missedLetters = ''
                        correctLetters = ''
                        if option[5]==3:
                            secretWord,secretKey = getNextRound(words)
                        else:
                            secretWord,secretKey = getRandomWord(words)
                        gameIsDone = False
                        guessed=[0,'',0]
                        s = 0
                        h = [280,259,1,40,40,0,100,100,0,0,150,240,13]
                        p = [150,259,1,40,40,0,100,100,0,0,150,240,13]
                        start()

            else:
                # Guess logic and control for failure to guess secert word
                missedLetters = missedLetters + str(guess)
                football()
                s+= 1
                if len(missedLetters) < 4:
                    incorrectSound.play()
                if len(missedLetters) == 4:
                            score[2]='TURNOVER!'
                            changeSides.play()
                            vteamScore.play()
                            p[7]=p[1]
                            
                            score[4]+=1
                            displayBoard(s, missedLetters, correctLetters, secretWord)
                            gameover(p)
                            infoDisplay(h,int(show[1]*2.5))  
                            infoDisplay(p,int(show[1]*2.5))  
                            gameIsDone = True
                            score[1]+=3 

            # Game finished logic
            if gameIsDone:
                    roundNo=0
                    score[2]=''
                    guess = ''
                    missedLetters = ''
                    correctLetters = ''
                    option[5]=0
                    if option[5]==3:
                        secretWord,secretKey = getNextRound(words)
                    else:
                        secretWord,secretKey = getRandomWord(words)
                    gameIsDone = False
                    guessed=[0,'',0]
                    s = 0
                    h = [280,259,1,40,40,0,100,100,0,0,150,240,13]
                    p = [150,259,1,40,40,0,100,100,0,0,150,240,13]
                    start()

#### END AREA FOR: MAIN GAME LOOP (INCLUDING CLOCK DISPLAY) #####################################################