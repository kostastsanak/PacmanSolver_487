# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        #The way to get info of our current state
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        #Pacman's position
        newPos = successorGameState.getPacmanPosition()
        #the states of the food
        newFood = successorGameState.getFood()
        #The state of the ghosts. Also didnt need to use it.
            #newGhostStates = successorGameState.getGhostStates()
        #Didnt need it. It basically informes you of the current timer and the remaining time that the ghost are going to be scared for.
            #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #food potision checking
        minFood = 99999.0
        #get closest food
        for food in newFood.asList():
            manD = manhattanDistance(newPos,food)
            if(minFood > manD):
                minFood = manD
            
        #ghost potision checking
        for ghost in successorGameState.getGhostPositions():
            #if distance <2 then the ghost is to close and pacman HAS TO move.
            if (manhattanDistance(newPos, ghost) < 3):
                return -99999.0

        #it reaches the end phase
        if(successorGameState.isWin()):
            return successorGameState.getScore()
        #return new score
        return successorGameState.getScore() + 1/minFood
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.
      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.
      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        #minimax is initiated as requested above from the comments
        #returns the minimax action from the current gameState using self.depth self.evaluationFunction
        def minimax(agent, depth, gameState):
            #contitions to return gamestate
            if depth == self.depth or gameState.isWin() or gameState.isLose():  #if the search has reached to an end return score
                #return score of end node
                return self.evaluationFunction(gameState)
            #if agent is pacman then 
            if agent == 0:  # maximize for pacman
            #find the max score
                maxScore = max(minimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
                return maxScore
            else:  #if agent>=1 then do the same for all ghosts
            # calculate the next agent and increase depth accordingly.
                nextAgent = agent + 1  
                # if we searched all ghosts then we set agent as pacman and increase depth by one
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                    depth += 1
                #find the min score
                minScore = min(minimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
                return minScore

        #initiating pacman root node move
        BestScore = float("-inf") # passing the worst possible value as best score moves
        worst = float("-inf")
        BestAction = Directions.STOP#initial Move. Basically lets the ghosts play first
        #Check every possible move available
        for move in gameState.getLegalActions(0):
            score = minimax(1, 0, gameState.generateSuccessor(0, move))
            #print(score)
            if score > BestScore:
                BestAction = move
                BestScore = score
        return BestAction

        util.raiseNotDefined()
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #couldnt make it work
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
          The expectimax function returns a tuple of (actions,
        """
        #same implemantation as minmax instead minmax we use expectimax now
        #and the ghost wont always do the best move
        def expectimax(agent, depth, gameState):
            #contitions to return gamestate
            if depth == self.depth or gameState.isWin() or gameState.isLose():  #if the search has reached to an end return score
                #return score of end node
                return self.evaluationFunction(gameState)
                
            #if agent is pacman then 
            if agent == 0:  # maximize for pacman
            #find the max score
                maxScore = max(expectimax(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
                return maxScore
            else:  #if agent>=1 then do the same for all ghosts
            # calculate the next agent and increase depth accordingly.
                nextAgent = agent + 1
                # if we searched all ghosts then we set agent as pacman and increase depth by one
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                    depth += 1
                #we dont search for the best score ghost move but the meanScore
                meanScore = sum(expectimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent)) / float(len(gameState.getLegalActions(agent)))
                return meanScore

        #initiating pacman root node move
        BestScore = float("-inf") # passing the worst possible value as best score moves
        worst = float("-inf")
        BestAction = Directions.STOP#initial Move. Basically lets the ghosts play first
        #Check every possible move available
        for move in gameState.getLegalActions(0):
            score = expectimax(1, 0, gameState.generateSuccessor(0, move))
            if score > BestScore:
                BestScore = score
                BestAction = move
        return BestAction
        
        util.raiseNotDefined()
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
      Evaluate state by  :
            * closest food
            * food left
            * capsules left
            * distance to ghost
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
