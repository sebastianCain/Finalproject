#!/usr/bin/python
import random
import cgi,cgitb,os

cgitb.enable()

#the field storage is a global variable.
#Since your page has exactly one, you can
#just acccess it from anywhere in the program.
form = cgi.FieldStorage()

#here is the edit
def header():
        return """content-type: text/html

    <!DOCTYPE HTML>
    <html>
    <head>
    <title>page of my website...</title>
    <link rel="stylesheet" href="style.css" type="text/css"/>
    </head>
    <body>
        <h1> Play Blackjack! </h1>
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
            userInfo = line.split(";")
            line = userInfo[0].split(",")
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
    return '<h2><a href="'+page+securefields()+action+'">'+text+'</a></h2>'

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

def dealCards(x,y):
    x.append(random.choice(deck.keys()))
    x.append(random.choice(deck.keys()))
    y.append(random.choice(deck.keys()))
    y.append(random.choice(deck.keys()))

def cardsToImgs(L):
    htmlStr = ""
    for i in L:
        words = i.split(" ")
        htmlStr += '<img src="images/'+(words[0])[0]+(words[2])[0]+'.png" width="72px" height="96px" alt="'+i+'">'
    return htmlStr

def cardsToImgsCpu(L):
    htmlStr = '<img src="images/blue_back.png" width="72px" height="96px" alt="'+L[0]+'">'
    for i in L[1:]:
        words = i.split(" ")
        htmlStr += '<img src="images/'+(words[0])[0]+(words[2])[0]+'.png" width="72px" height="96px" alt="'+i+'">'
    return htmlStr


def outfilewrite(useracct,outcome):
    leaders=open('users.txt','r')
    stuff=leaders.read().split('\n')
    leaders.close()
    datalist=[]
    for iteminlist in stuff:
        datalist.append(iteminlist.split(','))
    ctr=0
    rowtomodnum=0
    while ctr < len(datalist):
        if useracct in datalist[ctr]:#SPECIFIC TO USER ACCOUNT
            rowtomodnum=ctr
        ctr+=1
    rowtomod=datalist[rowtomodnum]
    if len(rowtomod)<4:
        rowtomod.append('0')
        rowtomod.append('0')
    if outcome == 'win':#WHERE OUTCOME IS
        newnum=int(rowtomod[2])+1
        rowtomod[2]=str(newnum)
    else:
        newnum=int(rowtomod[3])+1
        rowtomod[3]=str(newnum)        
    datalist[rowtomodnum]=rowtomod
    #for each element in the datalist,
    #we need to make a string out of it by joining the elements with commas
    counter= 0
    string=''
    counter2=0
    while counter < len(datalist):
        while counter2 < len(datalist[counter]):
            if counter2 !=len(datalist[counter])-1:
                string+=datalist[counter][counter2]+','
                counter2+=1
            else:
                string+=datalist[counter][counter2]
                counter2+=1
        counter2=0
        datalist[counter]=string
        string=''
        counter+=1
    writeout=''
    for element in datalist:
        writeout+=element+'\n'
    lastly=open("users.txt",'w')
    lastly.write(writeout)
    lastly.close()
    
    
def game():
    htmlStr = ""
    file=open("loggedin.txt",'r')
    data=file.read().split("\n")
    file.close()
    newData = ""
    alert = ""
    userCards = []
    cpuCards = []
    gameOver = False
    cpuActions = []
    #
    useracct=form.getvalue('user')
    #
    for i in data:
        x = i.split(";")
        userInfo = x[0].split(",")
        if userInfo[0] == form["user"].value:
            if len(x) > 1 and "action" in form.keys():
                userCards = x[1].split(",")
                cpuCards = x[2].split(",")
                if form['action'].value == "stand":
                    if sumOfCards(cpuCards) < 17:
                        cpuCards.append(random.choice(deck.keys()))
                        cpuActions.append("hits")
                        while sumOfCards(cpuCards) < 17:
                            cpuCards.append(random.choice(deck.keys()))
                            cpuActions.append("hits")
                        cpuActions.append("stands")
                    if sumOfCards(cpuCards) > 21:
                        alert = "The CPU has " + str(sumOfCards(userCards)) + " more than 21, so you win!"
                        gameOver = True
                        outfilewrite(useracct,'win')
                    elif sumOfCards(userCards) > sumOfCards(cpuCards):
                        alert = "You are closer to 21 than the CPU, so you win!"
                        gameOver = True
                        outfilewrite(useracct,'win')
                    else:
                        alert = "The CPU is closer to 21 than you, so you lose :("
                        gameOver = True
                        outfilewrite(useracct,'lose')
                elif form['action'].value == "hit":
                    userCards.append(random.choice(deck.keys()))
                    if sumOfCards(userCards) > 21:
                        alert = "You have " + str(sumOfCards(userCards)) + ", which is over 21, so you lose."
                        gameOver = True
                        outfilewrite(useracct,'lose')
                    elif sumOfCards(cpuCards) < 17:
                        cpuCards.append(random.choice(deck.keys()))
                        cpuActions.append("hits")
                    else:
                        cpuActions.append("stands")
                    if sumOfCards(cpuCards) > 21:
                        alert = "The AI has " + str(sumOfCards(userCards)) + ", more than 21, so you win!"
                        gameOver = True
                        outfilewrite(useracct,'win')
                elif form['action'].value == "restart":
                    userCards = []
                    cpuCards = []
                    alert = ""
                    dealCards(userCards, cpuCards)
            else:
                dealCards(userCards, cpuCards)

            userString = ",".join(userCards)
            cpuString = ",".join(cpuCards)
            newLineArr = [x[0], userString, cpuString]
            line = ";".join(newLineArr)
            newData += line + "\n"
        else:
            newData += i + "\n"
    newfile = open("loggedin.txt", "w")
    newfile.write(newData)
    newfile.close()
    
    cpuActionStr = "The CPU " + ", then ".join(cpuActions) + "."
    if gameOver:
        htmlStr += "Your cards:<br>" + cardsToImgs(userCards) + "<br><h2>You have " + str(sumOfCards(userCards)) + " in total</h2><br>"
        if len(cpuActions) != 0:
            htmlStr += cpuActionStr + "<br><br>"
        htmlStr += "CPU cards:<br>" + cardsToImgs(cpuCards) + "<br><h2>The CPU has " + str(sumOfCards(cpuCards)) + " in total</h2><br>"
        htmlStr += makeLink("page1.py","Restart", "&action=restart")
    else:
        htmlStr += "Your cards:<br>" + cardsToImgs(userCards) + "<br><h2>You have " + str(sumOfCards(userCards)) + " in total</h2>"
        htmlStr += makeLink("page1.py","Hit","&action=hit") + makeLink("page1.py","Stand", "&action=stand")
        if len(cpuActions) != 0:
            htmlStr += "<br><h2>The CPU " + cpuActions[len(cpuActions)-1] + ".</h2><br>"
        else:
            htmlStr += "<br><h2>The CPU ...</h2>"
        htmlStr += "CPU cards:<br>" + cardsToImgsCpu(cpuCards)
    htmlStr += "<br><br><h2>" + alert + "</h2><br><br>"
    return htmlStr
            
def loggedIn():
    return game()

def notLoggedIn():
    return "Whoops, seems like you're not logged in yet. Login up at the top, or create an account if you don't have one yet!"


def main():
    body = ""
    #use this to add stuff to the page that anyone can see.
    body += '<nav> <ul>'
    body += "<li><h2>"+makeLink("login.html","Login","")+"</h2></li>"
    body += "<li><h2>"+makeLink("create.html","Sign Up","")+"</h2></li>"
    body += "<li><h2>"+makeLink("page1.py","Play","")+"</h2></li>"
    body += "<li><h2>"+makeLink("page2.py","Leaders","")+"</h2></li>"
    body += "<li><h2>"+makeLink("page3.py","Statistics","")+"</h2></li>"
    body += "<li><h2>"+makeLink("logout.py","Logout","")+"</h2></li>"


    body += '</ul></nav><br><br><br><br><br>\n'

    #determine if the user is properly logged in once. 
    isLoggedIn = authenticate()

    #use this to determine if you want to show "logged in " stuff, or regular stuff
    if isLoggedIn:
        body += loggedIn()
    else:
        body += notLoggedIn()

    #anyone can see this
    #body += ""
    
    #attach a logout link only if logged in
    #if isLoggedIn:
        #body+= makeLink("logout.py","Click here to log out","")+"<br>"

    #make links that include logged in status when the user is logged in
    #body += makeLink("page1.py","here is page one","")+'<br>'
    #body += makeLink("page2.py","here is page two","")+'<br>'

    #finally print the entire page.
    print header() + body + footer()

main()
