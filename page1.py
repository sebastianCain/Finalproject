#!/usr/bin/python
import random
import cgi,cgitb,os

cgitb.enable()

#the field storage is a global variable.
#Since your page has exactly one, you can
#just acccess it from anywhere in the program.
form = cgi.FieldStorage()

def header():
        return """content-type: text/html

    <!DOCTYPE HTML>
    <html>
    <head>
    <title>page of my website...</title>
    <link rel="stylesheet" href="style.css" type="text/css"/>
    </head>
    <body>
        <h1> This is the FIRST page! </h1>
    """


def footer():
    return """</body>
</html>"""


def authenticate():
    if 'user' in form and 'magicnumber' in form:
        #get the data from form, and IP from user.
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        IP = 'NULL'
        if 'REMOTE_ADDR' in os.environ:
            IP = os.environ["REMOTE_ADDR"]
        #compare with file
        text = open('loggedin.txt').read().split("\n")
        for line in text:
            line = line.split(",")
            if line[0]==user:#when you find the right user name
                if line[1]==magicnumber and line[2]==IP:
                    return True
                else:
                    return False
        return False#in case user not found
    return False #no/missing fields passed into field storage


#either returns ?user=__&magicnumber=__  or an empty string.
def securefields():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        return "?user="+user+"&magicnumber="+magicnumber
    return ""
#makes a link, link will include secure features if the user is logged in
def makeLink(page, text, action):
    return '<a href="'+page+securefields()+action+'">'+text+'</a><br>'

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

def sumOfCards(L):
    total = 0
    for i in L:
        total += deck[i]
    return total	

def game():
    htmlStr = ""
    file=open("loggedin.txt",'r')
    data=file.read().split("\n")
    file.close()
    newData = ""
    alert = ""
    userCards = []
    cpuCards = []
    for i in data:
        x = i.split(",")
        if x[0] == form["user"].value:
            if len(x) > 3:
                #actions
                userCards = x[3::]
                cpu = random.randrange(17,26)
                if form['action'].value == "stand":
                    if cpu > 21:
                        alert += "YOU WIN!!"
                    elif sumOfCards(userCards) > 21:
                        alert += "YOU LOSE!!"
                    elif sumOfCards(userCards) >= cpu:
                        alert += "YOU WIN!!"
                    else:
                        alert += "YOU LOSE!!"
                elif form['action'].value == "hit":
                    userCards.append(random.choice(deck.keys()))
            else:
                #deal
                userCards.append(random.choice(deck.keys()))
                userCards.append(random.choice(deck.keys()))
            x = x[:3] + userCards
            htmlStr += "Your cards:" + str(x[3::])
            line = ",".join(x)
            newData += line + "\n"
        else:
            newData += i + "\n"
    newfile = open("loggedin.txt", "w")
    newfile.write(newData)
    newfile.close()
    htmlStr += "<br><br>" + alert
    htmlStr += "<br><br>" + makeLink("page1.py","Hit","&action=hit") + "<br>" + makeLink("page1.py","Stand", "&action=stand")
    return htmlStr
            
def loggedIn():
    return game()

def notLoggedIn():
    return "Whoops, seems like you're not logged in yet. Login up at the top, or create an account if you don't have one yet!"


def main():
    body = ""
    #use this to add stuff to the page that anyone can see.
    body += ""

    #determine if the user is properly logged in once. 
    isLoggedIn = authenticate()

    #use this to determine if you want to show "logged in " stuff, or regular stuff
    if isLoggedIn:
        body += loggedIn()
    else:
        body += notLoggedIn()

    #anyone can see this
    body += ""
    
    #attach a logout link only if logged in
    if isLoggedIn:
        body+= makeLink("logout.py","Click here to log out","")+"<br>"

    #make links that include logged in status when the user is logged in
    body += makeLink("page1.py","here is page one","")+'<br>'
    body += makeLink("page2.py","here is page two","")+'<br>'

    #finally print the entire page.
    print header() + body + footer()

main()
