from Cards import Card
from CardTypes import FaceCard
import random
from PIL import Image
import pygame
import sys

class Deck:
    def __init__(self):
        self._cards = []
        self.populate()
    def __repr__(self):
        thecards = ""
        for card in self._cards:
            thecards += str(card)
            thecards += ", "
        return thecards
    def populate(self):
        suits = ["clubs", "hearts", "spades", "diamonds"]
        numbers = ["A","2","3","4","5","6","7","8","9","10", "J", "Q", "K"]
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        cards=[]
        images = self.makeCardImages()
        i = 0
        for suit in suits:
            for number in numbers:
                if i%13>0 and i%13<10:
                    cards.append( Card(suit, number, values[i%13], images[i]))
                else:
                    cards.append(FaceCard(suit, number, values[i%13], images[i]))
                i += 1
        self._cards = cards
    def shuffle(self):
        random.shuffle(self._cards)
        
    def makeCardImages(self):
        #Openning up the image
        cards = Image.open("playing-cards.png")
        #Get the size of the card
        size = cards.size
        #Found the width of one card
        width = size[0]//13
        #Found the height of one card
        height = size[1]//4
        cardImages=[]
        for j in range(4):
            for i in range(13):
                singleCardImage=cards.crop((width*i,height*j,width*(i+1),height*(j+1)))
                cardImages.append(singleCardImage)
        return cardImages
        
        
class Hand:
    def __init__(self, deck, number=5):
        self._cardshand=[]
        self.deal(deck, number)
    def __repr__(self):
        thecards=""
        for card in self._cardshand:
            thecards += str(card)
            thecards += ", "
        return thecards

    def deal(self, deck, number=5):
        hand=[]
        for card in range(number):
            self._cardshand.append(deck._cards.pop(0))
        



