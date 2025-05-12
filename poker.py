from cards import *
from mcts import MCTS
import time

HANDS = {0 : "High Card", 1 : "One Pair", 2 : "Two Pair", 3 : "Three of a Kind", 4 : "Straight", 5 : "Flush", 6 : "Full House", 7 : "Four of a Kind", 8 : "Straight Flush", 9 : "Royal Flush"}

def decision(myHole: List[int], knownBoard: List[int], deck: List[int]): #run MCTS on current deck and known board
    tree = MCTS(myHole, knownBoard, deck)
    tree.executeMCTS() #run tree search at each phase

    winProb = 0.0
    if (tree.visits > 0):
        winProb = tree.wins / tree.visits #calculate win probability

    choice = "FOLD"
    if (winProb >= 0.5):
        choice = "STAY"
    
    return choice, winProb, tree.visits

def main():
    deck = initDeck() #initialize deck
    myHole = drawCards(deck, 2) #draw bot's hole cards
    print("Bot hole cards:", printCard(myHole[0]), printCard(myHole[1]), "\n")

    knownBoard = list() #initialize list of community cards

    dealingPhases = [("Pre-Flop", 3), ("Flop", 1), ("Turn", 1), ("River", 0)]

    for phase, numCards in dealingPhases: #traverse through dealing phases
        choice, winProb, sims = decision(myHole, knownBoard, deck)

        print(f"{phase} Decision: {choice} | "f"Win%: {winProb:.2%} over {sims} sims | "f"Board: {[printCard(c) for c in knownBoard]}")

        if (choice == "FOLD"):
            print(f"Bot folded at {phase}")
            return
        
        if (numCards > 0): #deal more community cards
            newCards = drawCards(deck, numCards)
            knownBoard.extend(newCards)
            print(f"Community card(s) revealed: {[printCard(c) for c in newCards]}\n")

    oppHole = drawCards(deck, 2) #simulate opponent cards from remaining deck
    print("\nOpponent hole cards:", printCard(oppHole[0]), printCard(oppHole[1]))
    print("Final Board:", [printCard(c) for c in knownBoard])

    myScore, myHand = evalBoard(myHole, knownBoard) #evaluate potential bot hands
    oppScore, oppHand = evalBoard(oppHole, knownBoard) #evaluate potential opponent hands
    if myScore >= oppScore:
        winner = "BOT"
        winHand, loseHand = myHand, oppHand
        winningScore, losingScore = myScore, oppScore
    else:
        winner = "OPPONENT"
        winHand, loseHand = oppHand, myHand
        winningScore, losingScore = oppScore, myScore

    print(f"\n** {winner} WINS **\n")
    print(f"Winning hand: {[printCard(c) for c in winHand]} --> {HANDS[winningScore[0]]}")
    print(f"Losing hand: {[printCard(c) for c in loseHand]} --> {HANDS[losingScore[0]]}")

if __name__ == "__main__":
    main()