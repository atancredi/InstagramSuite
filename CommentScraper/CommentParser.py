
#Add a logger for the exceptions
#Mettere il codice nelle condizioni di autosostentarsi nel girare per ore

import instaloader
import time
import re
import sqlite3

USERNAME = "grandefumoo"


#function that logs into instagram - add maybe a control if the user is already logged in?
def Login():
    L = instaloader.Instaloader()
    
    #Time metrics for the code
    loginTime = time.time()

    L.login(USERNAME, PASSWORD)

    loginTime = time.time() - loginTime
    
    #Creation of the "LoginData" object
    loginData = {
        
        "L": L,
        "loginTime": loginTime

        }

    return loginData

#Function that parses the text
def ParseText(type, text):
    if type == "email":
         return Parser_email(text)

#Specific Parser: email
def Parser_email(text):
    #regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text.lower())
    buffer = ""
    counter = 0
    for email in emails:
        
        if counter == len(emails)-1:
            buffer += email
        else:
            buffer += email + ","
        counter += 1
    return buffer

#Function that iterates
def CommentIterator(L, PostShortcode):
    post = instaloader.Post.from_shortcode(L.context, PostShortcode)

    iterationTime = time.time()

    commentLimit = 2000
    counter = 0

    #establish a connection with the DB
    conn = db_connect()

    for comment in post.get_comments():

        if counter < commentLimit:

            print("Testo di base del commento: "+comment.text)
            print("Autore del commento: "+comment.owner.username)


            validation = ParseText("email",comment.text)
            print("Email Rilevata: "+validation)

            if len(validation) > 0:
                #Creation of the comment object to be wrote into the DB
                detectedEmails = validation.split(",")
                for email in detectedEmails:
                    comm = {
                        "hierarchy": 0, #main comment
                        "profilo": comment.owner.username,
                        "email": email
                        }
                    db_writeMail(conn,comm)

            for answer in comment.answers:

                print("\tTesto di base della risposta: "+answer.text)
                print("\tAutore della risposta: "+answer.owner.username)
                validation = ParseText("email",answer.text)
                print("\tEmail rilevata: "+validation)

                if len(validation) > 0:
                    #Creation of the answer object to be wrote into the DB
                    detectedEmails = validation.split(",")
                    for email in detectedEmails:
                        ans = {
                            "hierarchy": 1, #answer
                            "profilo": answer.owner.username,
                            "email": email
                        }
                        db_writeMail(conn,ans)

        counter += 1

    conn.close()

    iterationTime = time.time() - iterationTime

    return {
        
        'iterationTime': iterationTime

        }

############################################# DB HANDLING

#Function that connects to the db
def db_connect():
    return sqlite3.connect("C:\\Users\\aless\\source\\Prodotti SabbieMobili\\InstagramScraping\\data\\InstagramMailingList.db")

#Function that writes into the db
def db_writeMail(conn,comment):
    
    conn.execute("INSERT INTO \"IconaBoi001\" (HIERARCHY,PROFILO,EMAIL) VALUES ('"+str(comment["hierarchy"])+"','"+comment["profilo"]+"','"+comment["email"]+"')")

    conn.commit()

    return 1

#############################################

#Main execution of the code
testPost1 = 'CQo5FhuBEch'

#iconaBoi = "CE9Fc1EDo_fGK6mvo7u3nqPzAEBkdPYCVq_7C40"
iconaBoi = "CE9Fc1EDo_f"

loginData = Login()
print(CommentIterator(loginData["L"],iconaBoi))
print(loginData["loginTime"])