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
    def __init__(self):
        self.hasgone=[]
        self.z=(0,0)


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
        #print chosenIndex

        "Add more of your code here if you want to"
        waytovec = {'North':(0,1), 'South':(0,-1), 'East':(1,0), 'West':(-1,0), 'Stop':(0,0)}
        self.hasgone.append(waytovec[legalMoves[chosenIndex]])
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "[Project 3] YOUR CODE HERE"
        direc = [(0,0), (0,1), (0,-1), (1,0), (-1, 0)]
        ghostpos = [i.getPosition() for i in newGhostStates]
        dangerzone = [(x+i, y+j) for (x, y) in ghostpos for (i,j) in direc]
        x=100000000
        Food = list(currentGameState.getFood())
        if not Food[self.z[0]][self.z[1]]:
            for i in range(len(Food)):
                for j in range(len(Food[0])):
                    if Food[i][j]:
                        if manhattanDistance(newPos, (i,j))<x:
                            self.z=(i,j)
                            x=manhattanDistance(newPos, self.z)
        fooddirec=[]
        if newPos[0]>self.z[0]:
            fooddirec.append("West")
        if newPos[0]<self.z[0]:
            fooddirec.append("East")
        if newPos[1]>self.z[1]:
            fooddirec.append("South")
        if newPos[1]<self.z[1]:
            fooddirec.append("North")
        if newPos in dangerzone:
            k= -100000
        elif currentGameState.hasFood(newPos[0], newPos[1]):
            k= 50000
        elif action == Directions.STOP:
            k= -2000
        elif action in fooddirec:
            k=200
        elif newPos not in self.hasgone:
            k= 8
        else:
            k= -3
        return successorGameState.getScore()+k


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

        "[Project 3] YOUR CODE HERE"
        return self.minimax(gameState, 0)[0]
        util.raiseNotDefined()

    def minimax(self, gameState, depth):
        currentAgentIndex = depth % gameState.getNumAgents()
        if depth >= self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if currentAgentIndex == 0:
            value = (None, -float('Inf'))
            for action in gameState.getLegalActions(0):
                v = self.minimax(gameState.generateSuccessor(0, action), depth + 1)
                if v[1] > value[1]:
                    value = (action, v[1])
        else:
            value = (None, float('Inf'))
            for action in gameState.getLegalActions(currentAgentIndex):
                v = self.minimax(gameState.generateSuccessor(currentAgentIndex, action), depth + 1)
                if v[1] < value[1]:
                    value = (action, v[1])
        return value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        "[Project 3] YOUR CODE HERE"
        return self.alphabeta(gameState, 0, -float('Inf'), float('Inf'))[0]
        util.raiseNotDefined()

    def alphabeta(self, gameState, depth, alpha, beta):
        currentAgentIndex = depth % gameState.getNumAgents()
        if depth >= self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if currentAgentIndex == 0:
            value = (None, -float('Inf'))
            for action in gameState.getLegalActions(0):
                v = self.alphabeta(gameState.generateSuccessor(0, action), depth + 1, alpha, beta)
                if v[1] > value[1]:
                    value = (action, v[1])
                alpha = max(alpha, v[1])
                if beta < alpha:
                    break
        else:
            value = (None, float('Inf'))
            for action in gameState.getLegalActions(currentAgentIndex):
                v = self.alphabeta(gameState.generateSuccessor(currentAgentIndex, action), depth + 1, alpha, beta)
                if v[1] < value[1]:
                    value = (action, v[1])
                beta = min(beta, v[1])
                if beta < alpha:
                    break
        return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """

    "[Project 3] YOUR CODE HERE"

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

