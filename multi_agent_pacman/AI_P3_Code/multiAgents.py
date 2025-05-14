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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()  # ['Stop', 'North', 'South']

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves] # [144.0, 134.0, 134.0]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

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
        newFood = successorGameState.getFood().asList()
        newGhostStates  = successorGameState.getGhostStates()
        newScaredTimes  = [ghostState.scaredTimer for ghostState in newGhostStates ]
        
        # Base score
        score = successorGameState.getScore()

        # Food proximity: closer food -> higher bonus
        if newFood:
            dists = [manhattanDistance(newPos, food) for food in newFood]
            minFoodDist = min(dists)
            score += 1.0 / (minFoodDist + 1)

        # Ghost interaction
        for idx, gs in enumerate(newGhostStates):
            ghostPos = gs.getPosition()
            dist = manhattanDistance(newPos, ghostPos)
            if newScaredTimes [idx] > 0:
                # chase scared ghosts: closer -> bigger reward
                score += 2.0 / (dist + 1)
            else:
                # avoid active ghosts: too close -> heavy penalty
                if dist > 0:
                    score -= 2.0 / dist
                else:
                    # collision: worst case
                    return -float('inf')

        # Encourage not stopping
        if action == Directions.STOP:
            score -= 0.5

        return score

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        best_action, _ = self._evaluate(gameState, agentIndex=0, currentDepth=0)
        return best_action
    
    def _evaluate(self, state, agentIndex, currentDepth):
        """
        Recursive dispatch method based on agent type and terminal conditions.
        """
        totalAgents = state.getNumAgents()

        if agentIndex >= totalAgents:
            agentIndex = 0
            currentDepth += 1

        # Terminal state or max depth reached
        if currentDepth == self.depth or state.isWin() or state.isLose():
            return None, self.evaluationFunction(state)

        if agentIndex == 0:
            return self._maximize(state, agentIndex, currentDepth)
        else:
            return self._minimize(state, agentIndex, currentDepth)

    def _maximize(self, state, agentIndex, currentDepth):
        """
        Max (Pacman) chooses the action with the highest value.
        """
        maxValue = float("-inf")
        bestAction = None

        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex, action)
            _, value = self._evaluate(successor, agentIndex + 1, currentDepth)

            if value > maxValue:
                maxValue = value
                bestAction = action

        return bestAction, maxValue

    def _minimize(self, state, agentIndex, currentDepth):
        """
        Min (Ghosts) choose the action with the lowest value.
        """
        minValue = float("inf")
        bestAction = None

        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex, action)
            _, value = self._evaluate(successor, agentIndex + 1, currentDepth)

            if value < minValue:
                minValue = value
                bestAction = action

        return bestAction, minValue

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        alpha, beta = float('-inf'), float('inf')
        bestAction = None
        value = float('-inf')

        # Max layer (Pacman)
        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            v = self._min_value(succ, 1, 0, alpha, beta, numAgents)
            if v > value:
                value, bestAction = v, action
            alpha = max(alpha, value)
        return bestAction

    def _max_value(self, state, agentIndex, currentDepth, alpha, beta, numAgents):
        # Terminal check
        if state.isWin() or state.isLose() or currentDepth == self.depth:
            return self.evaluationFunction(state)

        v = float('-inf')
        for action in state.getLegalActions(agentIndex):
            succ = state.generateSuccessor(agentIndex, action)
            v = max(v, self._min_value(succ, agentIndex+1, currentDepth, alpha, beta, numAgents))
            if v > beta:
                return v  # prune
            alpha = max(alpha, v)
        return v

    def _min_value(self, state, agentIndex, currentDepth, alpha, beta, numAgents):
        # Wrap to next agent and depth
        if agentIndex >= numAgents:
            agentIndex = 0
            currentDepth += 1

        # Terminal check
        if state.isWin() or state.isLose() or currentDepth == self.depth:
            return self.evaluationFunction(state)

        v = float('inf')
        for action in state.getLegalActions(agentIndex):
            succ = state.generateSuccessor(agentIndex, action)
            if agentIndex == numAgents - 1:
                # next is Pacman at new depth
                v = min(v, self._max_value(succ, 0, currentDepth+1, alpha, beta, numAgents))
            else:
                # next ghost
                v = min(v, self._min_value(succ, agentIndex+1, currentDepth, alpha, beta, numAgents))

            if v < alpha:
                return v  # prune
            beta = min(beta, v)
        return v

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

    Don't forget to use pacmanPosition, foods, scaredTimers, ghostPositions!
    DESCRIPTION: <write something here so we know what you did>
    """

    pacmanPosition = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimers = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()
    
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
