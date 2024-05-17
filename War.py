import WarDeck as WarDeck
from WarDeck import Hand
import pygame as pygame
import sys as sys

class Image:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

def displayCard(card,x,y):
    global PlayedCards
    size = card.image.size
    carddata = card.image.tobytes()
    cardsPyImage = pygame.image.fromstring(carddata, size, 'RGBA')
    image = Image(cardsPyImage, x, y)
    PlayedCards.append(image)

def reset():
    global PlayerHand, DealerHand, PlayedCards, shifts, war, endGame
    shifts = 0
    deck1 = WarDeck.Deck()
    deck1.shuffle()
    PlayerHand = Hand(deck1, 26)
    DealerHand = Hand(deck1, 26)
    PlayedCards.clear()
    updateHandTotal(PlayerHand._cardshand)
    war = False
    event_text("Click Card Back to Start")
    alert_text("Game Started!")
    endGame = False

def playCard():
    global DealerHand, PlayerHand, PlayedCards, shifts, SHIFT, BattleCards, war, endGame, alert_texts
    
    alert_texts.clear()
    if war == False:
        PlayedCards.clear()
        shifts = 0
    winCheck()
    if endGame == False:
        DealersCard = DealerHand._cardshand.pop(0)
        PlayersCard = PlayerHand._cardshand.pop(0)
        BattleCards.append(DealersCard)
        BattleCards.append(PlayersCard)
        displayCard(DealersCard, 200+shifts*SHIFT, 175)
        displayCard(PlayersCard, 200+shifts*SHIFT, 450)
        eval(DealersCard, PlayersCard, BattleCards)
    
    print("Dealer Cards = " + str(len(DealerHand._cardshand)))
    print("Player Cards = " + str(len(PlayerHand._cardshand)))
    updateHandTotal(PlayerHand._cardshand)


def eval(DealersCard, PlayersCard, BattleCards):
    global DealerHand, PlayerHand, shifts, SHIFT, PlayedCards, war, endGame
    
    if DealersCard.value == 1 and PlayersCard.value == 1:
        event_text("War!!!")
        shifts +=1
        displayFlippedCard()
        shifts +=1
        winCheck()
        BattleCards.append(DealerHand._cardshand.pop(0))
        BattleCards.append(PlayerHand._cardshand.pop(0))
        war = True
    
    elif DealersCard.value == 1 or PlayersCard.value == 1:
        AceRule(DealersCard, PlayersCard)
    
    
    elif DealersCard.value > PlayersCard.value:
        DealersCard.inc_kills()
        event_text("Dealer Wins with "+ str(DealersCard))
        gatherCards(DealersCard, PlayersCard, DealerHand, PlayerHand, BattleCards)
        
    elif PlayersCard.value > DealersCard.value:
        PlayersCard.inc_kills()
        event_text("Player Wins with "+ str(PlayersCard))
        gatherCards(PlayersCard, DealersCard, PlayerHand, DealerHand, BattleCards)
        
    else:
        event_text("War!!!")
        shifts +=1
        displayFlippedCard()
        shifts +=1
        winCheck()
        BattleCards.append(DealerHand._cardshand.pop(0))
        BattleCards.append(PlayerHand._cardshand.pop(0))
        war = True

def gatherCards(winnerCard, loserCard, winningHand, losingHand, BattleCards):
    global war
    if winnerCard.level>1:
        extraCards = winnerCard.level-1
        alert_text(str(extraCards) + " extra card(s) taken")
        for num in range(extraCards):
            winCheck()
            if endGame == True:
                return
            BattleCards.append(winningHand._cardshand.pop(0))
            print("Took a Card")
            winCheck()
            if endGame == True:
                return
                
    for card in BattleCards:
        winningHand._cardshand.append(card)
    BattleCards.clear()
    war = False

def updateHandTotal(hand):
    global count_text, big_Font
    num_of_cards = len(hand)
    CardNumberText = big_Font.render("# of Cards: " + str(num_of_cards), True, white)
    count_text = Image(CardNumberText, 150, 580)

def displayFlippedCard():
    global shifts, SHIFT, CardBack, PlayedCards
    dealerBack=Image(CardBack,200+shifts*SHIFT, 175)
    playerBack=Image(CardBack,200+shifts*SHIFT, 450)
    PlayedCards.append(dealerBack)
    PlayedCards.append(playerBack)
    
def event_text(message):
    global event_texts
    event_texts.clear()
    EventText = big_Font.render(message, True, white)
    EventTextImage = Image(EventText, 150, 650)
    event_texts.append(EventTextImage)
    
def alert_text(message):
    global alert_texts
    alert_texts.clear()
    alertText = big_Font.render(message, True, orange)
    alertTextImage = Image(alertText, 20, 100)
    alert_texts.append(alertTextImage)
    
def winCheck():
    global PlayerHand, DealerHand, endGame
    
    if len(PlayerHand._cardshand) <=0:
        alert_text("Dealer Has Won the Game!")
        endGame = True
    elif len(DealerHand._cardshand)<=0:
        alert_text("Player Has Won the Game!")
        endGame = True
        
def AceRule(DCard, PCard):
    global DealerHand, PlayerHand, BattleCards
    if DCard.value == 1:
        if PCard.value >10:
            DCard.inc_kills()
            gatherCards(DCard, PCard, DealerHand, PlayerHand, BattleCards)
            event_text("Dealer Wins with "+ str(DCard))
        else:
            PCard.inc_kills()
            gatherCards(PCard, DCard, PlayerHand, DealerHand, BattleCards)
            event_text("Player Wins with "+ str(PCard))
    if PCard.value == 1:
        if DCard.value >10:
            PCard.inc_kills()
            gatherCards(PCard, DCard, PlayerHand, DealerHand, BattleCards)
            event_text("Player Wins with "+ str(PCard))
        else:
            PCard.inc_kills()
            gatherCards(DCard, PCard, DealerHand, PlayerHand, BattleCards)
            event_text("Dealer Wins with "+ str(DCard))
        
            

PlayedCards = []
PlayerHand = []
DealerHand = []
BattleCards = []
shifts = 0
SHIFT = 13
war = False
endGame = False

big_Font = pygame.font.init()
big_Font = pygame.font.Font(None, 36)
small_Font = pygame.font.Font(None, 20)
white = (255, 255, 255)
green = (54, 158, 23)
orange = (255, 140, 0)
grey = (241, 241, 241)
CardBack=pygame.image.load("CardBack.jpg")

static_image=[]
static_texts=[]
buttons=[]
event_texts =[]
alert_texts=[]

reset()

CardNumberText = big_Font.render("# of Cards: 26", True, white)
count_text = Image(CardNumberText, 150, 580)

DealerTitle = big_Font.render("Dealer's Hand", True, white)
PlayerTitle = big_Font.render("Player's Hand", True, white)
DealerTitleImg= Image(DealerTitle, 300, 50)
PlayerTitleImg= Image(PlayerTitle, 300, 350)

static_texts.append(DealerTitleImg)
static_texts.append(PlayerTitleImg)

DealerCardBack = Image(CardBack, 500, 80)
PlayerCardBack = Image(CardBack, 50, 580)

static_image.append(DealerCardBack)
static_image.append(PlayerCardBack)




resetButtonText = small_Font.render("New Game", True, orange)
resetButtonTextImage = Image(resetButtonText, 50, 44)
ButtonRectangle = pygame.Surface((100, 40))
resetButtonImage= Image(ButtonRectangle, 30, 30)
buttons.append(resetButtonImage)
buttons.append(resetButtonTextImage)


#Making a pygame window
window = pygame.display.set_mode((800,700))
pygame.init()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] >=resetButtonImage.x and mousePos[0] <= resetButtonImage.x + resetButtonImage.image.get_width() and mousePos[1] >= resetButtonImage.y and mousePos[1]<=resetButtonImage.y+resetButtonImage.image.get_height():
                print("Reset Clicked")
                reset()
            elif mousePos[0] >= PlayerCardBack.x and mousePos[0] <= (PlayerCardBack.x + CardBack.get_width()) and mousePos[1]>= PlayerCardBack.y and mousePos[1] <= PlayerCardBack.y + CardBack.get_height():
                print("Player Card Clicked")
                if endGame == False:
                    playCard()
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    
    window.fill(green)
    for card in PlayedCards:
        card.draw(window)
    for image in static_texts:
        image.draw(window)
    for image in static_image:
        image.draw(window)
    for image in buttons:
        image.draw(window)
    for image in event_texts:
        image.draw(window)
    for image in alert_texts:
        image.draw(window)
    count_text.draw(window)
    pygame.display.flip()
