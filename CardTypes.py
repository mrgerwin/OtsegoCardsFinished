from Cards import Card

class FaceCard(Card):
    def __init__(self, suit, number, value, image):
        Card.__init__(self, suit, number, value, image)
        self.kills = 0
        self.level = 1
    
    def __repr__(self):
        return "Level " + str(self.level) +" "+ self.number + " of " + self.suit +" with " + str(self.kills)+ " Kills"

    def inc_kills(self):
        self.kills += 1
        if self.kills % 3 == 0:
            self.level +=1