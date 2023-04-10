#Breakthrough: an abstract strategy board game invented by Dan Troyka in 2000
#This version is developed by Shawn Stone for the CMSC 405 class
# 10-31-22
# the rules of the game are included in the assignment descrption.
import pygame, sys, random
from pygame.locals import *
# The red player is implemented by a PlayerAI.  In this simple version
# the AI is a random agent.  The student must develope a sophisticated AI
# implementing maximin with alpha-beta pruning.  
from PlayerAI import PlayerAI
import time
clock = pygame.time.Clock() # used in setting time between frames


pygame.init() #initialize pygame to use needed functions

FPS = 4 # frames per second setting
fpsClock = pygame.time.Clock() #This method controls frame rate
timeLimit = 1 # the red player has a time limit per move.
# if the red player goes over this limit then red forfiets.
allowance = 0.05 # there is a .05 allownce to exit out of the recursive
# flow of the alph-beta algorithm
# set up the window
DISPLAYSURF = pygame.display.set_mode((900, 900))# nine locations 100x100
pygame.display.set_caption('Breakthrough!')
WHITE = (255, 255, 255)

#import images for the game board and its communication
board = pygame.image.load('matt.jpg')
blue = pygame.image.load('blue.jpg')
red=pygame.image.load('red.jpg')
highlight=pygame.image.load('highlight.jpg')
Hblue=pygame.image.load('hblue.jpg')
Hred=pygame.image.load('hred.jpg')
Bwins=pygame.image.load('bluewins.jpg')
Rwins=pygame.image.load('redwins.jpg')
G=pygame.image.load('G.jpg')
Q=pygame.image.load('Q.jpg')


#the game manager keeps track of the game as it progresses.
class GameManager(object):
    def __init__(self):
        self.state=[] # this is game board (0) clear (1) red (2) blue
        self.moveSet=[] # this remembers the moves possible for blue

    # this returns a copy of the current game state
    def getCopyofGameState(self):
        return self.state
    #this method sets up a clear inital board
    def initializeGame(self):
        #set the board to the start state
        self.state=[[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2]]

        DISPLAYSURF.fill(WHITE) #clears screen to white
        
        DISPLAYSURF.blit(board,(0,0)) #plops board on screen

        offsetx=125 # offset X to put in correct location on board
        offsety=125 # offset Y to put in correct location on board

        # first row of red placed
        for i in range(8):
            DISPLAYSURF.blit(red,(offsetx+i*100,offsety))
        # second row of red placed    
        offsety=225
        for i in range(8):
            DISPLAYSURF.blit(red,(offsetx+i*100,offsety))
        #place first blue row
        offsety=725
        for i in range(8):
            DISPLAYSURF.blit(blue,(offsetx+i*100,offsety))
        # place second blue row
        offsety=825
        for i in range(8):
            DISPLAYSURF.blit(blue,(offsetx+i*100,offsety))
#this method checks if there is a blue piece at (I,J)            
    def isBlueQ(self,I,J):
    
        if self.state[I][J]==2:
            return True
        else:
            return False
# what is a legal move is decided by where the current location is (CI,CJ)
# and where it wants to move (I,J)
    def isLegalMoveQ(self,CI,CJ,I,J):
        # blue can't move into a blue space
        if self.isBlueQ(I,J):
            return False
        
        check=(I,J)
        #must check if can move forward
        # blue can't move forward into a red space

        if CJ==J:
            if self.state[I][J]==1:
                return False

        return check in self.moveSet

# this method serves two purposes for the blue player.  It returns the moves possible
# and changes the look of the board to show what moves are possible.
# this is why moveSet is an internal variable.  This data must be maintaned on exit for later use.
    def moveEvent(self,I,J):
        legalMoves=[[[0,-100],[100,-100]],[[-100,-100],[0,-100],[100,-100]],[[-100,-100],[0,-100],[100,-100]],[[-100,-100],[0,-100],[100,-100]],[[-100,-100],[0,-100],[100,-100]],
                    [[-100,-100],[0,-100],[100,-100]],[[-100,-100],[0,-100],[100,-100]],[[-100,-100],[0,-100]]]
        self.moveSet=[]
        for block in legalMoves[J]:
            x=100*J+125
            y=100*I+125
            i=int(block[1]/100)
            j=int(block[0]/100)
            self.moveSet.append((I+i,J+j))
            if self.state[I+i][J+j]==2:
                DISPLAYSURF.blit(Hblue,(x+block[0],y+block[1]))
            elif self.state[I+i][J+j]==1:
                DISPLAYSURF.blit(Hred,(x+block[0],y+block[1]))
            else:
                DISPLAYSURF.blit(highlight,(x+block[0],y+block[1]))
        return self.moveSet

# Perform the legal blue move and update the state.
    
    def moveBlue(self,CI,CJ,I,J):
        self.state[CI][CJ]=0
        self.state[I][J]=2
        
#perform the legal red move and update the state       
    def moveRed(self,CI,CJ,I,J):
        
        self.state[CI][CJ]=0
        
        self.state[I][J]=1
        
# wipe the baord clean       
    def resetBoard(self):
        DISPLAYSURF.fill(WHITE) #clears screen to white
        
        DISPLAYSURF.blit(board,(0,0))
        
#place the peices onto the board
        
    def plopPieces(self):
        for i in range(8):
            for j in range(8):
                x=int(100*j+125)
                y=int(100*i+125)
                if self.state[i][j]==1:
                    DISPLAYSURF.blit(red,(x,y))

                if self.state[i][j]==2:
                    DISPLAYSURF.blit(blue,(x,y))

# after blue makes a move the game manager checks if blue wins                    
    def didBlueWin(self):
        for i in range(8):
            if self.state[0][i]==2:
                return True
        return False
# after red makes a move the game manager checks if red wins 
    def didRedWin(self):
        for i in range(8):
            if self.state[7][i]==1:
                return True
        return False
        
def main():
    gameManager = GameManager() # Runs the game and keeps track of the state.

    gameManager.initializeGame() # setup the board and graphics of the board
    pygame.display.update() #show the user the game board
    
    click=0 # this is essential for the blue player as they click on the board
    moveSet=[] # the possible legal moves for blue when a peice is clicked
    CI=0 #the I location of the peice clicked
    CJ=0 #the J location of the peice clicked
    playerAI=PlayerAI() # the provided players AI.  This is what you provide.
    gameOn=True # the inner while loop is the current game loop.

    #the outer game loop is for initializing a new game if G is pressed after the first run game
    while True:
        
        while gameOn:
            pygame.display.update() #as each new state takes place update the state to the screen

            # if click ==2 then blue made a successful move and it is reds turn.
            if click==2:
                #reds move
                s=gameManager.getCopyofGameState() # get current game state to pass to the Player AI
                startTime=time.process_time()
                #the player AI return the location of the peice that will move (CI,CJ) and where it will move to (I,J)
                CI,CJ,I,J=playerAI.getMoveRed(s)
                endTime=time.process_time()
                #check if red took to long.  If it did then it forfiets the game
                if (endTime-startTime)-allowance>timeLimit:
                    print("overtime")
                    print("blue is the winner")
                    gameManager.resetBoard()
                               
                    gameManager.plopPieces()
                    DISPLAYSURF.blit(Bwins,(400,300))
                    pygame.display.update() 
                    gameOn=False
                    
                    break
                #make red move and update board
                gameManager.moveRed(CI,CJ,I,J)
                gameManager.resetBoard()     
                gameManager.plopPieces()

                #check if red won
                if gameManager.didRedWin():
                    print("Red is the winner")
                    DISPLAYSURF.blit(Rwins,(400,300))
                    pygame.display.update() 
                    gameOn=False
                    break
                else:
                    click=0 # clears blue for its next move
                           
            #listen for an event from the mouse
            for event in pygame.event.get():
                #if you click the red x of the window the game quits
                if event.type == QUIT:
                   pygame.quit()
                   return
                # if the mouse is clicked read its position on the game board
                elif event.type == MOUSEBUTTONDOWN:
                   pos = pygame.mouse.get_pos() # read the position from the mouse event
                   #convert this position to the integer square coordinates on the board
                   J=int((pos[0]-100)/100)
                   I=int((pos[1]-100)/100)
                 
                   # after blue is selected the next click is where blue should go.  This checks for a legal move and moves the token if it is legal.
                   if click==1:
                       # check is click was in a legal position
                       if gameManager.isLegalMoveQ(CI,CJ,I,J):
                           
                           gameManager.moveBlue(CI,CJ,I,J)
                           
                           gameManager.resetBoard()
                       
                           gameManager.plopPieces()
                           click=2
                           if gameManager.didBlueWin():
                               print("blue is the winner")
                               gameManager.resetBoard()
                               
                               gameManager.plopPieces()
                               DISPLAYSURF.blit(Bwins,(400,300))
                               pygame.display.update() 
                               gameOn=False
                               break
                           
                           
                       else:
                           
                           click=0
                       gameManager.resetBoard()
                       
                       gameManager.plopPieces()
                       pygame.display.update() 
                  
                   # check if a blue peice has been chosen to move    
                   if click==0: 
                       #first check if a 2 exists at this location
                       if gameManager.isBlueQ(I,J):
                           gameManager.resetBoard()
                       
                           gameManager.plopPieces()
                           gameManager.moveEvent(I,J)
                           CI=I
                           CJ=J
                           click=1
        #some one won the game at this point.  Check to see if the game goes on (G) or quits(Q)                   
        DISPLAYSURF.blit(G,(825,25))
        DISPLAYSURF.blit(Q,(25,825))
        pygame.display.update()
        for event in pygame.event.get():
                if event.type == QUIT:
                   pygame.quit()
                   return
                elif event.type == MOUSEBUTTONDOWN:
                   
                   pos = pygame.mouse.get_pos()
                   J=int((pos[0]-100)/100)
                   I=int((pos[1]-100)/100)
                   
                   if I==7 and J==0:
                       pygame.quit()
                       return

                   if I==0 and J==7:
                        gameManager = GameManager()

                        gameManager.initializeGame()
                        pygame.display.update() #send new image to screen
    
                        click=0
                        moveSet=[]
                        CI=0
                        CJ=0
                        playerAI=PlayerAI()
                        gameOn=True
                    
                
    clock.tick(60)
    
   

    

if __name__ == '__main__':
    main()



