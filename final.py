import random
import time

values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
#suites = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
suites = ['♥', '♣', '♦', '♠']
startingMoney = 1000




class Cards:
    """A data type representing an arbitrary number of cards with the purpose of playing Blackjack
    """

    def __init__(self, values, suites, numDecks, startingMoney):
        """Construct objects of type Deck, with the given values and suites. You can choose to use more than one deck, as well as set the starting player cash."""
        self.values = values
        self.suites = suites
        self.deck = []
        self.numDecks = numDecks
        self.createDeck(self.numDecks)

        self.playerMoney = startingMoney
        self.playerBet = 0

        self.playerHand = []
        self.playerHandValue = 0
        self.dealerHand = []
        self.dealerHandValue = 0

        self.roundCounter = 0   # It this necessary?

        # We do not need to return anything from a constructor!
    
    def createDeck(self, numDecks=1):
        '''Generates the deck of cards. You can choose to use more than one deck.'''
        
        for d in range(numDecks):
            for s in suites:
                for v in values:
                    self.deck += [v+s]
                    #add to dictionary here when doing ASCII cards

    def dealCards(self):
        dealerCardsDelt = 2
        for i in range(dealerCardsDelt): #dealing cards for the player(s)
            drawnCard = random.choice(self.deck)
            self.playerHand += [drawnCard]
            (self.deck).remove(drawnCard)
        
        playerCardsDelt = 2
        for i in range(playerCardsDelt): #dealing cards for the dealer
            drawnCard = random.choice(self.deck)
            self.dealerHand += [drawnCard]
            (self.deck).remove(drawnCard)

    def asciiCards(self): #will build this later to make pretty looking ascii cards, and store them in a dictionary (probably do the storing in the constructor)
        pass

    def __repr__(self):
        """This method returns a string representation
           for an object of type Cards.
        """
        s = '\nDealer: '                          # The string to return
        
        s += ('? ') # hole card
        for card in self.dealerHand[1:]: #rest of dealer's cards
            s += (card + ' ')
        s += '\n'

        s += '---------------' + "\n"   # border between cards
        s += 'Player: '
        for card in self.playerHand: #player's cards
            s += (card + ' ')
        s += '\n'

        return s       # The table is complete; return it'''
    
    def revealCards(self):
        '''same as __rept__, except the hole card is revealed
        '''
        s = '\nDealer: '                          # The string to return
        
        for card in self.dealerHand: #rest of dealer's cards
            s += (card + ' ')
        s += '\n'

        s += '---------------' + "\n"   # border between cards
        s += 'Player: '
        for card in self.playerHand: #player's cards
            s += (card + ' ')
        s += '\n'

        print(s)
    
    def handValue(self, whichHand):
        '''Calculates the value of the player or dealer's hand, determined by 'whichHand'. Counts aces as an 11, unless the total value is greater than 21.'''

        numAces = 0

        if whichHand == 'player':
            handVal = self.playerHandValue
            hand = self.playerHand
        elif whichHand == 'dealer':
            handVal = self.dealerHandValue
            hand = self.dealerHand

        for x in hand:
            if 'K' in x or 'Q' in x or 'J' in x:
                handVal += 10
            elif 'A' in x:
                handVal += 11
                numAces += 1
            elif '10' in x:
                handVal += 10
            else:
                handVal += int(x[0])
         
        """if numAces > 1:
            handVal = 'blackjack' # bug? this might cause a problem b/c a string not int"""

        if handVal > 21: # this is an 'elif' if uncommenting above!!!
            for x in hand:
                if 'A' in x: # bug? might be a problem if there's multiple aces in hand?
                    handVal -= 10  # making the ace equal to 1 (instead of 11)
                    if handVal <= 21:
                        break
        
        return handVal
    
    def playerBust(self):
        '''Checks if the player busts.'''

        if self.handValue('player') > 21:
            print('You bust! Your bet is forfeit.')
            self.playerMoney -= self.playerBet
            print('-$' + str(self.playerBet))
            return True
        return False
    
    def dealerBust(self):
        '''Checks if the dealer busts.'''
        #print('debug: dealer bust')
        if self.handValue('dealer') > 21:
            print('The dealer busts! You just made double your money.')
            self.playerMoney += self.playerBet #SHOULD THIS BE * 2 ?
            print('+$' + str(self.playerBet))
            return True
        return False

    def gameOver(self):
        '''Prompts player to start a new game.'''
        time.sleep(1)
        print('The dealer reveals his hand:')
        self.revealCards()
        print('Your current balance is: $'+ str(self.playerMoney))
        yesOrNo = str(input('Would you like to start another game? '))

        while yesOrNo != 'yes' and yesOrNo != 'no':
            yesOrNo = str(input("Illegal input. Yes or no?: "))
        
        if yesOrNo == 'yes':
            d = Cards(self.values, self.suites, self.numDecks, self.playerMoney)
            d.hostBlackjack()
        if yesOrNo == 'no':
            time.sleep(0.5)
            print('You leave the table with $' + str(self.playerMoney)+'.')
            return
    
    def hit(self, whichHand):
        '''Adds a card to the the player or dealer's hand'''

        if whichHand == 'player':
            drawnCard = random.choice(self.deck)
            self.playerHand += [drawnCard]
            (self.deck).remove(drawnCard)
        elif whichHand == 'dealer':
            drawnCard = random.choice(self.deck)
            self.dealerHand += [drawnCard]
            (self.deck).remove(drawnCard)
    
    def hostBlackjack(self, minBet = 5, maxBet = 100):
        ''' Hosts a singleplayer game of blackjack against an AI dealer. Can optionally input min and max bets.
        '''
        
        print('Welcome to Blackjack!')
        time.sleep(.5)
        self.createDeck() # Generates table
        self.dealCards()

        # Betting
        time.sleep(.5)
        print('This table has a $' +str(minBet)+ ' minimum and a $' +str(maxBet)+ ' maximum.')

        time.sleep(.5)
        print('Your current balance is: $'+ str(self.playerMoney))
        self.playerBet = int(input('Please place a bet: $'))

        while self.playerBet > maxBet or self.playerBet < minBet:     # If illegal bet
            self.playerBet = int(input("Illegal bet. Place a new one: "))

        ###### Game begins: ######
        time.sleep(0.5)
        print(self)     # Maybe eventually include an animation?

        if self.handValue('player') == 21 and self.handValue('dealer') != 21:
            print('Blackjack! You win 1.5x your original bet')
            self.playerMoney += self.playerBet * 1.5
            return self.gameOver()
        
        while not self.playerBust():
            hitOrStand = str(input('Do you want to hit or stand? '))
            while hitOrStand != 'hit' and hitOrStand != 'stand':     # If illegal input
                hitOrStand = str(input("Illegal input. Do you want to hit or stand? "))

            time.sleep(0.5)
            if hitOrStand == 'hit':  #need to make it ignore caps
                self.hit('player')
                print(self)
            elif hitOrStand == 'stand':
                self.dealerAI()
                #print('debug: Ends things here boo bam')
                return

        #self.playerBust()  Why did commenting this out fix the double bust bug??
        return self.gameOver()



    def dealerAI(self):
        '''Dealer hits or stands, then the dealer's cards are revealed and the game ends
        '''
        #print('debug- dealerAI starts')
        while self.handValue('dealer') < 17:
            print('The dealer hits.')
            time.sleep(1)
            self.hit('dealer') #adds card to dealer hand and subtracts from deck
            v = self.handValue('dealer')
            #print("debug- V: " + str(v))
            print(self)
        #print('debug- dealerAI while loop ends')


        if self.handValue('dealer') > 21:
            #print('debug- dealer bust if runs')
            self.dealerBust()
            return self.gameOver()
        #print('debug- dealerAI if statement passed')


        print('The dealer stands.')
        
        if self.isBlackjack('dealer'): # Dealer blackjack
            time.sleep(0.5)
            print('The dealer has a blackjack. Your bet is swept!')
            self.playerMoney -= self.playerBet
            print('-$' + str(self.playerBet))
            self.gameOver()
        
        elif self.handValue('player') > self.handValue('dealer'): # Player wins
            time.sleep(0.5)
            print('Your hand beats the dealer\'s!')
            self.playerMoney += self.playerBet * 2
            print('+$' + str(2*self.playerBet))
            self.gameOver()
        
        elif self.handValue('player') == self.handValue('dealer'): # Neither wins
            time.sleep(0.5)
            print('Push! Nobody wins. You keep your bet.') # Bug!! Didn't print this on a push!
            self.gameOver()

        elif self.handValue('player') < self.handValue('dealer'): # Dealer wins
            time.sleep(0.5)
            print('The dealer wins! You loose your bet.')
            self.playerMoney -= self.playerBet
            print('-$' + str(self.playerBet))
            self.gameOver()
        #print('debug: dealerAI returning')
        return

    def isBlackjack(self, whichHand):
        '''Checks if a hand is a blackjack
        '''
        numA = 0

        if whichHand == 'dealer':
            hand = self.dealerHand
        elif whichHand == 'player':
            hand = self.playerHand
        
        if len(hand) == 2:
            for x in hand:
                if 'A' in x:
                    numA += 1
            if numA == 1 and self.handValue(whichHand) == 21:
                return True
        return False

    

d = Cards(values, suites, 1, startingMoney)
d.hostBlackjack()
#d.dealCards()
#print(d)