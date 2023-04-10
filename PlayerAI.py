#Programmer Name: Braidyn Britt
#Date: 12/11/2022
#Description: Breakthrough is a chess based game where the player can move a piece forware or diagonally one space. 
# The pieces can take enemy pieces that are at the diagnols. This file is an AI program that allows for the player
# to go against the AI. The AI uses Maximin with alpha-beta pruning against the player to make an intelligent move.
# Time limit that I am using is 1 second.

# this is the red player code.  It is set up for a random agent at this time.
# you have to smarten it up!  You must use a maximin with alpha-beta pruning 

#Imports libraries to allow the use of random (to help randomize moves) and time(to make sure moves are made within time limit)
import random
import time

#Global variables. These are the initial variabels for V. V is to know when the move needs to be replaced 
PINFINITY = 1000000000
MINFINITY = -1000000000

#This is the AI class. This contains the heuristics, maximin functions, and any function that is needed to help decide a move
class PlayerAI(object):
    #Initilizer function (not used)
    def __init__(self):
        self.dumb = 0
    
    #Copies the actual board into an empty board. This is created because deepcopy was taking too long. Takes in old board. Returns copy
    def newCopy(self, state):
        #creates a new empty board
        newState = [[0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]]

        for j in range(8): # each column
            for i in range(8): #each row
                newState[i][j] = state[i][j] #copy the numbers 0, 1, or 2 from actual board into new board
        return newState #returns the copy

    #This function makes a move to update the board so the AI can traverse the tree based off moves. Takes in a move, player, and state.
    #Returns new board if move is made otherwise returns the old board. Move is a list of 4 items. index 0 and 1 are initial location. 
    #Index 2 and 3 are next location.
    def makeMove(self, move, state, player):
        if state[move[0]][move[1]] != 0: #If there is no piece in initial spot do nothing
            newState = self.newCopy(state) #Makes a new copy of the passed in board
            newState[move[0]][move[1]] = 0 #sets initial piece spot to be empty
            newState[move[2]][move[3]] = player #sets where the piece is going to move to the passed in player
            return newState #returns new board after move is made
        return state #if no move is made then just returns original board

    #From original AI code given in class. Takes in a board, and a column(J) and row(I) position. Checks if the piece that is going to be
    # moved is the correct color.
    def isRedQ(self,state,I,J): 
        if state[I][J] == 1: #If given [I][J] position has a red player Return True. Otherwise return False
            return True
        else:
            return False
        
    #Checks if the red piece is blocked by another piece or not. Takes in a current location (CJ and CI) and a next location (I and J).
    def isLegalMoveQRed(self,state,CI,CJ,I,J):
        if self.isRedQ(state,I,J): #if next location has a red player already there then return false
            return False
        if CJ == J: #if move is go straight.
            if state[I][J] == 2: #check if there is a blue player straight ahead. If there is then ai cannot move
                return False

        return True # if next position is open then return true.

    #Takes in the current board. Returns a list of all potential legal moves that could be taken.
    def returnLegalMoversRed(self,state):
        legalMovers = [] #initialize empty list of moves

        for j in range(8): #For all columns
            for i in range(8): #For all rows
                
                if state[i][j] == 1: #If the location is a red piece
                    
                    moves = self.moveEventRed(i,j) #Get all potential moves of the row and column being looked at. 


                    #moves is a list of 2 items. Next row and next column. For each potential move
                    for block in moves:
                        I = block[0] #I is the next row to move
                        
                        J = block[1] #J is the next column to move into
                        
                        if self.isLegalMoveQRed(state,i,j,I,J): #If the next position is open 
                            legalMovers.append([i,j,I,J]) # append current position and next position to the list of potential moves

        return legalMovers #return list of moves

    #same function as isRedQ. Takes in same things and returns true or false. 1 minor tweak to adjust for blue instead of red
    def isBlueQ(self,state,I,J):
        if state[I][J] == 2: #If the position is a blue piece
            return True
        else:
            return False
    
    #Same function as isLegalMoveQRed. 2 minor tweaks to adjust for blue. Takes in same things as red function and returns same things.
    def isLegalMoveQBlue(self,state,CI,CJ,I,J):
        if self.isBlueQ(state,I,J): #If there is a blue piece in the next position
            return False
        if CJ ==J :
      
            if state[I][J] == 1: #If the forward direction has a red piece
                
                return False

        return True
    
    #Same function as returnLegalMoversRed. Takes in same thing and returns same thing. 4 minor changes to adjust for blue instead of red
    def returnLegalMoversBlue(self,state):
        legalMovers = []

        for j in range(8):
            for i in range(7, -1,-1): #for all rows but go backwards to start at blues side.
                 
                if state[i][j] == 2: #if position has a blue piece
                    
                    moves=self.moveEventBlue(i,j) #Get all potential moves for blue
                    for block in moves:
                        I = block[0]
                        J = block[1]
                        if self.isLegalMoveQBlue(state,i,j,I,J): #if nothing is blocking blue
                            legalMovers.append([i,j,I,J])
        return legalMovers

    #Gets all potential moves for red. Forward and both diagonals. Takes in a pieces position I and J. Return potential moves.
    def moveEventRed(self,I,J):
        #List of legal moves for each column. First number is an increase in row. 2nd number is a decrease, increase, or no change in column
        legalMoves = [[[1,0],[1,1]],
                    [[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],
                    [[1,-1],[1,0]]]
        moveSet = [] #empty list of moves
        for block in legalMoves[J]: #for each list in legal moves
            moveSet.append((I + block[0],J + block[1])) #add current row + 1 and current column + increase or decrease by 1 or 0.
            
        return moveSet  #return moves

    #Same function as moveEventRed. Takes in and returns same things. 1 minor tweak for blue change.
    def moveEventBlue(self,I,J):
        legalMoves = [[[1,0],[1,1]],
                    [[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],[[1,-1],[1,0],[1,+1]],
                    [[1,-1],[1,0]]]
        moveSet = []
        for block in legalMoves[J]:
            moveSet.append((I - block[0],J + block[1]))# add current row - 1 to have blue move forward (up the board).
            
        return moveSet    
    
    #checks if passed in board is a terminal State (Winning/losing state). Takes in a board returns a true or false
    def isTerminalRed(self, state):
        for j in state[7]:#for each column in the last row of the board
            if j == 1: #If there is a red piece in any location
                return True #return that it is a terminal state
        return False #otherwise return that it is not

    #same function is isTerminalRed with 2 minor changes to work for blue. Takes in and returns the same thing
    def isTerminalBlue(self, state):
        for j in state[0]: #for each column in the first row of the board
            if j == 2: #if there is a blue piece in any of the positions
                return True #return true if there is a terminal state
        return False #otherwise return false

    #Checks if next move is winning or losing move. Takes in a state and player. Returns points to assign if a move is worse or better.
    def H1(self, state, player):
        value = 0 #initilize return value to 0
        if player == 1: #if passed in player is red
            if self.isTerminalRed(state): #if reds next move is a winning move then award 50,000 points.
                value = 50000
            if self.isTerminalBlue(state): #if reds next moves allows a blue win punish by 100,000 points.
                value = -50000
        else: #if passed in player is blue
            if self.isTerminalBlue(state): #if blues next move is a winning move then award 50,000 points
                value = -50000
            if self.isTerminalRed(state): #if blues next move allows a red win then punish 100,000 points
                value = 50000
        return value #return the points

    #Checks who has higher amount of players. Takes in the next board and the player. Returns points for if move is worse or better
    def H2(self, state, player):
        rTotal = 0 #initialize red total. This is used to count how many red pieces there are
        bTotal = 0 #initialize blue total. This us used to count how many blue pieces ther are
        for i in range(8): #for each row count how many of each piece is in each row then add them together.
            rTotal += state[i].count(1)
            bTotal += state[i].count(2)

        if player == 1: #if passed in player is red then return the count of red pieces mulitplied by 10. Can be 160 points at most.
            return rTotal * 10
        else: #if passed in player is blue then return count of blue players * -10. Can be -160 points at most.
            return bTotal * -10

    
    #Closer to win heursitic. Takes in a state and player. Then returns points for if move is better or worse to make.
    def H3(self, state, player):
        value = 0 #sets return value to 0
        Rvalue = 0 #sets red piece value to 0
        Bvalue = 0 #sets blue piece value to 0
        for i in range(8): #for each row starting at the top of the board
            Rvalue = ((2**i) * state[i].count(1)) #count red pieces in row. Multiple this count by 2 raise to the row number.
            #makes sure each move forward is worth more the further down the board

        for i in range(7, -1, -1): #for each row starting at the bottom of the row
            val = 7 - i #take difference between 7 and the row the loop is on. This gives how many spaces forward blue has moved
            Bvalue = ((2**val) * state[i].count(2)) * -1 #Does the same as for the red count except negative

        if player == 1: #if player is red
            if Rvalue > Bvalue: #if there is a higher red value than blue
                value = Rvalue #positive points set to value to award red
            elif Rvalue < Bvalue: #if blue is further up than red
                value = Rvalue * -1 #negatice points set to value to punish red
        else: #if player is blue. Check same values against each other. Negative points award blue. Positive punish blue
            if Rvalue > Bvalue:
                value = Bvalue * -1
            elif Rvalue < Bvalue:
                value = Bvalue
        return value/2 #Value can be very large. Return value/2

    def utilityRed(self, state): #takes in next move board. Adds all heuristics together. Passes in 1 to all heuristcs. Totals reds points
        v = self.H1(state, 1) + self.H2(state, 1) + self.H3(state, 1)
        return v, 1 #return the reds points and 1. 1 is a placeholder number

    def utilityBlue(self, state): #same function as utilityRed except 2 is passed into all heuristics for blue player
        v = self.H1(state, 2) + self.H2(state, 2) + self.H3(state, 2)
        return v, 1

    #Max gets points for red. Replaces next move to be made if the new move rewards more points. Most was done in class.
    #Takes in a board, alpha, beta, depth, and starting time. Alpha and beta is to move max and min numbers through the functions.
    def maxValue(self, state, alpha, beta, depth, t1):
        timer = time.time() - t1 #gets difference of time to see how much time has passed
        if self.isTerminalRed(state) or depth == 0 or timer > .8: #if the state is terminal, hit max depth, or has gone over time
            return self.utilityRed(state) #get heuristic values

        depth = depth - 1 #decreased depth for max depth
        v = MINFINITY #sets v to initial -infinity
        move = [] #initiliaze empty move list
        randList = [] #initialize random move list to make sure moves dont go left to right
        actions = self.returnLegalMoversRed(state) #gets all moves that can be made

        #this for loop helps randomize move
        for i in range(len(actions)): #get each index number of actions
            randList.append(i) #append this number to a list
        random.shuffle(randList) #shuffle the list to pull out a random move to be made

        for i in randList: #for each index in randList
            a = actions[i] #a is the action of that index
            state = self.makeMove(a, state, 1) #make the move on the board with red player to allow board change
            v2, a2 = self.minValue(state, alpha, beta, depth, t1) #run min part of maximin and set things returned to v2 and a2
            if v2 > v: #if v2 is higher than v set v to v2 and replace next move to be made
                v = v2
                move = a
                alpha = max(alpha, v) #get maximum number to bring up the tree
            if v >= beta: #if v is greater then beta return the move to be made
                return v, move
        return v, move #once the loop is finished return v and move to be made

    #min part of maximin. Almost the same as maxValue function with a few minor changes
    def minValue(self, state, alpha, beta, depth,t1):
        timer = time.time() - t1
        if self.isTerminalBlue(state) or timer > .8 or depth == 0:
            return self.utilityBlue(state)
        depth -= 1
        v = PINFINITY #sets v to positive infinity
        move = []
        randList = []
        actions = self.returnLegalMoversBlue(state) #gets all blue legal moves

        for i in range(len(actions)):
            randList.append(i)
        random.shuffle(randList)

        for i in randList:
            a = actions[i]
            state = self.makeMove(a, state, 2) #make move on board with blue player
            v2, a2 = self.maxValue(state, alpha, beta, depth, t1)  #run max part of maximin
            if v2 < v:
                v = v2
                move = a
                beta = min(beta, v) #get minimum number for beta to bring up tree
            if v <= alpha: #if v is less than alpha return the move
                return v, move
        
        return v, move

    #gets AI move and runs the start of the maximin tree
    def getMoveRed(self,gameState):
        I = 0 #initialize next row position
        J = 0 #initialize next column position
        CI = 0 #initialize current row position
        CJ = 0 #initialize current column position
        alpha = MINFINITY #initialize alpha and beta as starting values of negative infinity and positive infinity
        beta = PINFINITY
        t1 = time.time() #get start time of function so then function wont go over that
        v, move = self.maxValue(gameState, alpha, beta, 7, t1) #start max value. Pass in current board, initial alpha and beta, max depth, and start time.
        #V is a placeholder. Move[0] and move[1] is a current column and current row. Move[2] and move[3] is next column and next row
        CI = move[0] #set values to variables to make it easier to retun
        CJ = move[1]
        I = move[2]
        J = move[3]
        return CI,CJ,I,J #return current location and next location

