from typing import *
from random import sample

RANKS = {0 : 2, 1 : 3, 2 : 4, 3 : 5, 4 : 6, 5 : 7, 6 : 8, 7 : 9, 8 : 10, 9 : 'J', 10 : 'Q', 11 : 'K', 12 : 'A'} #maybe dont need
SUITS = {0 : '♣', 1 : '♦', 2 : '♥', 3 : '♠'} #maybe dont need

def initDeck(): #initialize and shuffle deck
    return list(range(52))

def drawCards(deck: List, numCards: int): #return cards drawn
    cards = sample(deck, numCards) #randomly sample the number of cards
    for card in cards:
        deck.remove(card) #remove drawn cards from deck
    return cards

#(maybe dont need)
def rank(card: int): #return rank for a card integer
    return RANKS[card % 13]

#(maybe dont need)
def suit(card: int): #return suit for a card integer
    return SUITS[card // 13]

def printCard(card: int): #print readable string for a card integer
    return f"{rank(card)}{suit(card)}"

def evalHand(cards: List[int]): #evaluate 5-card hand
    ranks = [0] * 13
    suits = [0] * 4

    for card in cards: #count number of specific ranks and suits
        ranks[card % 13] += 1
        suits[card // 13] += 1
    
    flush = False
    if (max(suits) == 5): #check if flush exists
        flush = True

    straight = False
    if (max(ranks) == 1): #5 different ranks, check if potential straight exists
        uniqueRanks = list()
        for rank, count in enumerate(ranks): #create list of all unique ranks
            if (count > 0):
                uniqueRanks.append(rank)

        if (12 in uniqueRanks and 3 in uniqueRanks): #account for a potential wheel straight
            uniqueRanks.remove(12) #remove high ace
            uniqueRanks.append(-1) #add low ace
        uniqueRanks = sorted(uniqueRanks) #sort list of ranks

        straightHigh = None #highest rank in the straight
        if (uniqueRanks[-1] - uniqueRanks[0] == 4): #check if last element minus first element has difference of 4
            straightHigh = uniqueRanks[-1] #if difference is 4, that means it is a straight, so store last element
            straight = True
    
    counts = list()
    for rank, count in enumerate(ranks): #create list of counts for ranks
        if (count > 0):
            counts.append((count, rank))
    counts = sorted(counts, reverse=True) #sort by descending count and rank

