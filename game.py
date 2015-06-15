#!/usr/bin/python
print "Content-Type: text/html\n"
print ""
import random
import cgi

deck = {}
def createDeck():
    for i in range(1,53):
        facevalue = i % 13
        string = ""
        value = 0
        if facevalue == 1:
            string += "Ace"
            value = 1
        elif facevalue == 11:
            string += "Jack"
            value = 10
        elif facevalue == 12:
            string += "Queen"
            value = 10
        elif facevalue == 0:
            string += "King"
            value = 10
        else:
            string += str(facevalue)
            value = facevalue
        
        string += " of "
        
        if i <= 13:
            string += "Spades"
        elif i <= 26:
            string += "Clubs"
        elif i <= 39:
            string += "Diamonds"
        else:
             string += "Hearts"
        
        deck[string]=value
    
createDeck()
print deck

cpushow=[]
playershow=[]
def deal():
    cpushow=[random.choice(deck.keys()),random.choice(deck.keys())]
    playershow=[random.choice(deck.keys()),random.choice(deck.keys())]
    
    
'''    
def updatevals():    
    cpuvalue=0
    playervalue=0
    for card in cpushow:
        cpuvalue+=deck[card]
    for card in playershow:
        playervalue+=deck[card]
        
def playerhit():
    player.append(random.choice(deck.keys()))


mutant=cgi.FieldStorage()

newdic={}
for key in mutant.keys():
    newdic[key]=mutant[key].value
    
print newdic
playerval=newdic["playerval"]
cpuval=newdic["cpuval"]

def game():
    if usrval in newdic and cpuval in newdic:#game has started
        if cpuval>21 or 
'''                
