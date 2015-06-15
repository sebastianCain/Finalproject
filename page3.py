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
    html =  """content-type: text/html

    <!DOCTYPE HTML>
    <html>
    <head>
    <title>page of my website...</title>
    <link rel="stylesheet" href="style.css" type="text/css"/>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1.1", {packages:["bar"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Card Number', 'Busted'],
    """
    statFile = open('stats.txt', 'r')
    stats = statFile.read().strip().split("\n")
    statFile.close()
    for i in stats:
        items = i.split(",")
        html += "['"+items[0]+"', "+items[1]+"],"
    
    html += """]);

        var options = {
          chart: {
            title: '',
            subtitle: '',
          }
        };

        var chart = new google.charts.Bar(document.getElementById('columnchart_material'));

        chart.draw(data, options);
      }
    </script>
    </head>
    <body>
        <h1> Statistics </h1>
    """
    return html

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
def securefields():
    if 'user' in form and 'magicnumber' in form:
        user = form.getvalue('user')
        magicnumber = form.getvalue('magicnumber')
        return "?user="+user+"&magicnumber="+magicnumber
    return ""

#makes a link, link will include secure features if the user is logged in
def makeLink(page, text):
    return '<a href="'+page+securefields()+'">'+text+'</a>'

def loggedIn():
    return '<div id="columnchart_material" style="width: 95%; height: 500px;"></div>'

def notLoggedIn():
    return '''You need to login to see more. You can log in here: <a href="login.html">here</a>\n'''


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

    #determine if the user is properly logged in once. 
    isLoggedIn = authenticate()

    #use this to determine if you want to show "logged in " stuff, or regular stuff
    if isLoggedIn:
        body += loggedIn()
    else:
        body += notLoggedIn()
    
    #finally print the entire page.
    print header() + body + footer()

main()
