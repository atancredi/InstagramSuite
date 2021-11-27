import instaloader
import requests
import json
from datetime import datetime

now = datetime.now()

# list to dictionary
def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

L = instaloader.Instaloader()

user = "grandefumoo"

#get pwd
password = json.loads(open("../credentials.json","r").read())[user]

# Login or load session
L.login(user, password)
print("login eseguito\n")

# Obtain profile metadata
profile = instaloader.Profile.from_username(L.context, "asciughino_")

dataStructure = []
totalPosts = []

print("inizio ad iterare sui post\n")
#Itero in tutti i post
likes = []
nlikes = 0
for post in profile.get_posts():

    #creo la lista temporanea dello scorrimento dei post
    tmp = []
    
    #cerco tutti quelli che hanno messo like al post
    for liker in post.get_likes():
        if liker.username not in likes:
            likes.append(liker.username)

    #raccolgo le informazioni sul post
    tmp.append("PostURL")
    tmp.append("https://instagram.com/p/"+post.shortcode+"/") #URL del post
    tmp.append("ThumbURL")
    tmp.append(post.url) #URL della thumbnail del post
    tmp.append("DateCreation")
    tmp.append(str(post.date_utc)) #Data di creazione UTC
    tmp.append("nLikes")
    tmp.append(post.likes) #numero di likes
    nlikes += int(post.likes)
    tmp.append("nComments")
    tmp.append(post.comments) #numero di commenti incluse le risposte
    tmp.append("PostType")
    tmp.append(post.typename) #tipo di post
    tmp.append("nMedia")
    tmp.append(post.mediacount) #numero di elementi nel post
    #PostLocation è una classe!!
    #tmp.append(post.PostLocation.name+""+","+post.PostLocation.lat+","+post.PostLocation.lng) #nome, latitudine e longitudine della location
    
    #aggiungo la lista temporanea alla struttura dei posts
    totalPosts.append(Convert(tmp))
    print("post iterato\n")

print("inizio ad iterare negli username\n")
#Itero nella lista degli usernames
nfollowers = 0
for followee in profile.get_followers():

    nfollowers += 1

    username = followee.username

    #creo la lista temporanea nello scorrimento dei followers
    tmp = []
    tmp.append("username")
    #appendo il follower alla lista temporanea
    tmp.append(username)
    
    #se il follower è nella lista degli attivi lo marchio come attivo
    tmp.append("isGhost")
    if username in likes:
        tmp.append(0)
    else:
        tmp.append(1)

    #appendo la lista alla dataStructure
    dataStructure.append(Convert(tmp))

#Rinomino i file della scansione prima di questa in last_*
f = open("..\\data\\followers_localStorage.json", "w+")

k = open("..\\data\\posts_localStorage.json", "w+")

#Scrivo i dati rilevanti della scansione
j = open("..\\data\\data_localStorage.json", "a")
data = []
data.append(now.strftime("%d/%m/%Y %H:%M:%S"))
data.append(nfollowers)
data.append(nlikes)
j.write(json.dumps(data))


print("scrivo nei file\n")
f.write(json.dumps(dataStructure))
k.write(json.dumps(totalPosts))

f.close()
j.close()
k.close()

print("finito!")
