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
        <h1> Leaderboard </h1>
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
def makeLink(page, text):
    return '<a href="'+page+securefields()+'">'+text+'</a>'


def getinfo():
    leaders=open("users.txt",'r')
    stuff=leaders.read().split('\n')
    leaders.close()
    datalist=[]
    for iteminlist in stuff:
            datalist.append(iteminlist.split(','))
    datalist[:]=datalist[1:-1]
    return datalist

def points(useracct):
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
        return "0"
    else:
        return str(int(rowtomod[2])*10+int(rowtomod[3])*3)

def wins(useracct):
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
        return "0"
    else:
        return rowtomod[2]
def losses(useracct):
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
        return "0"
    else:
        return rowtomod[3]
    

useracct=form.getvalue('user')

def topten():
    leaders=open('users.txt','r')
    stuff=leaders.read().split('\n')
    leaders.close()
    #rank by wins
    newstuff=[]
    for item in stuff:
        newstuff+=[item.split(',')]
    filtered=[]
    for item in newstuff:
        if len(item) >= 4:
            filtered.append(item)
    #filtered[num][2] gives the amount of wins
    winlist=[]
    for player in filtered:
        winlist+=[int(player[2])]
    winlist=sorted(winlist)[::-1]
    if len(winlist) > 10:
        winlist[:]=winlist[:10]
    top10=[]
    for value in winlist:
        for player in filtered:
            if int(player[2])==value:
                top10+=[player[0]]
    finalstr='<u><h2><b>Here are the top players:</b></h2></u>'
    for player in top10:
        finalstr+='<h3>'+player+'</h3>'
    return finalstr
                    
    

def loggedIn():
    return "<hr><h2><b><u>Personal Score:</u></b></h2><h3>POINTS:"+points(useracct)+'</h3><h3>WINS:'+wins(useracct)+'</h3><h3>LOSSES:'+losses(useracct)+'</h3></hr>'

def notLoggedIn():
    return "Whoops, seems like you're not logged in yet. Login up at the top, or create an account if you don't have one yet!"
    
def main():
    body = ""
    #use this to add stuff to the page that anyone can see.
    body += '<nav><ul>'
    body += "<li><h2>"+makeLink("login.html","Login")+"</h2></li>"
    body += "<li><h2>"+makeLink("create.html","Sign Up")+"</h2></li>"
    body += "<li><h2>"+makeLink("page1.py","Play")+"</h2></li>"
    body += "<li><h2>"+makeLink("page2.py","Leaders")+"</h2></li>"
    body += "<li><h2>"+makeLink("page3.py","Statistics")+"</h2></li>"
    body += "<li><h2>"+makeLink("logout.py","Logout")+"</h2></li>"


    body += '</ul></nav><br><br><br><br><br>\n'
    body += str(topten())

    #determine if the user is properly logged in once. 
    isLoggedIn = authenticate()
    
    #use this to determine if you want to show "logged in " stuff, or regular stuff
    if isLoggedIn:
        body += loggedIn()
    else:
        body += notLoggedIn()

    #anyone can see this
    #body += "<hr>other stuff can go here<hr>\n"
    
    #attach a logout link only if logged in
    #if isLoggedIn:
    #    body+= makeLink("logout.py","Click here to log out")+"<br>"

    #make links that include logged in status when the user is logged in
    #body += makeLink("page1.py","here is page one")+'<br>'
    #body += makeLink("page2.py","here is page two")+'<br>'

    #finally print the entire page.
    print header() + body + footer()

main()
