from typing import List
import time
import math
from cards import evalBoard, dealCards

class Node: #represents game state at a specific dealing phase
    def __init__(self, oppHole: List[int], fullBoard: List[int]):
        self.oppHole = oppHole
        self.fullBoard = fullBoard
        self.visits = 0
        self.wins = 0
    
class MCTS: #represents a single level Monte Carlo tree
    def __init__(self, myHole: List[int], knownBoard: List[int], deck: List[int]):
        self.myHole = myHole
        self.knownBoard = knownBoard
        self.deck = deck.copy()
        self.visits = 0
        self.wins = 0
        self.children: List[Node] = []
    
    def UCB1(self, child: Node, c: float = math.sqrt(2)): #calculate UCB1 value for child node
        if (child.visits == 0): #prioritize exploration if never visited
            return float('inf')
        return (child.wins / child.visits) + (c * math.sqrt(math.log(self.visits) / child.visits))
    
    def expand(self): #expand tree with a random opponent hole and full board
        oppHole, fullBoard = dealCards(self.knownBoard, self.deck)
        node = Node(oppHole, fullBoard)
        self.children.append(node)
        return node #return new child node
    
    def select(self): #return child node with best UCB1        
        bestChild = None
        bestUCB1 = float('-inf')
        for child in self.children:
            currentUCB1 = self.UCB1(child)
            if(currentUCB1 > bestUCB1):
                bestUCB1 = currentUCB1
                bestChild = child
        return bestChild
    
    def backpropagate(self, node: Node, win: bool): #update stats up the tree
        node.visits += 1
        self.visits += 1
        if (win):
            node.wins += 1
            self.wins += 1
    
    def executeMCTS(self): #simulate cycle for 10 seconds
        timeLimit = time.time() + 10.0 #10 second limit
        while time.time() < timeLimit:
            self.expand()
            node = self.select()
            myScore, _ = evalBoard(self.myHole, node.fullBoard)
            oppScore, _ = evalBoard(node.oppHole, node.fullBoard)
            win = myScore >= oppScore #returns true if bot's hand >= opponents hand
            self.backpropagate(node, win)