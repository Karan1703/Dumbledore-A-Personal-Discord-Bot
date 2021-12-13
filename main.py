import discord
import os
import requests
import json
import random
import praw
from replit import db
from keep_alive import keep_alive
from insults import get_insults
import time
import youtube_dl
import ffmpeg
import subprocess
#from tiktok import get_url



## THIS BOT WAS MADE TO ENTERTAIN MY FRIENDS IN OUR DISCORD SERVER.






#---------------------------------------------------------------------------------#
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    username="  ",
    password="",
    user_agent="redditscraper")

#---------------------------------------------------------------------------------#
client = discord.Client()

#---------------------------------------------------------------------------------#
#FOR THE POTTER MEMES

masters = [441694764119752706, 203672766426251264, 306947650484174848]
true_masters = [441694764119752706, 203672766426251264]
truth = False

def meme(sub):
    subreddit = reddit.subreddit(sub)
    top = subreddit.top("week")

    top = list(top)

    random_sub = random.choice(top)

    name = random_sub.title
    url = random_sub.url
    print(url)
    em = discord.Embed(title=name)

    em.set_image(url=url)

    return (em)


#---------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------#
#FOR THE VIDS


def video_sub(sub):
    subreddit = reddit.subreddit(sub) 
    top = subreddit.top("week") # fetches top posts of week
    top = list(top) #creates a list from top posts of week
    audio = ""

    random_sub = random.choice(top) #randomly selects a top post from the list
    name = random_sub.title #fetches title of the post
    original_url = random_sub.url #stores url
    url = random_sub.media['reddit_video']['fallback_url']
    url = url.split("?")[0]
    audio_list = url.split("/")

    del audio_list[4]
    audio_list.append("DASH_audio.mp4")

    for i in audio_list:
      if i == audio_list[-1]:
        audio += i
      else:
        audio += i + "/"
    print(audio)

    return (name, url, audio, original_url)


def process_vid(sub):
    name, url, audio_url, original_url = video_sub(sub)

    video_response = requests.get(url)
    audio_response = requests.get(audio_url)
    open("vid.mp4", 'wb').write(video_response.content)
    open("audio.mp3", 'wb').write(audio_response.content)

    return (name, original_url)





#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
#FOR THE fiftyfity posts


def fifty():
    subreddit = reddit.subreddit("fiftyfifty")
    top = subreddit.top("month", limit=50)

    top = list(top)

    random_sub = random.choice(top)

    name = random_sub.title
    url = random_sub.url

    return (name, url)


#---------------------------------------------------------------------------------#
#FOR INSULTS AND INSPIRATION

sad_words = ["flip", "berserkered","shiv"]

starter_encouragements = [] 

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global truth
    global masters
    global true_masters



    if message.author == client.user:
        return
    msg = message.content.lower()


    if msg.startswith("$masters add") and message.author.id in true_masters:
      truth_id = int(msg.split()[2])
      masters.append(truth_id)
      await message.channel.send("A master has been welcomed.")

    if msg.startswith("$masters delete") and message.author.id in true_masters:
      truth_id = int(msg.split()[2])
      masters.remove(truth_id)
      await message.channel.send("A master has been banished.")

    if msg.startswith("$masters list"):
      await message.channel.send(masters)


    if message.author.id == 494966755278716928 and truth == True:
      await message.channel.send("shut up you like kavya, but atleast you upgraded to @nxndni_676 lol")


    if msg.startswith("$truth") and message.author.id in masters:
      truth = not truth

      if truth == True:
        await message.channel.send("I now speak the truth.")
      else:
        await message.channel.send("I am silenced.")


    if msg.startswith("$cringe"):

      name, original_url = process_vid("tiktokcringe")

      em = discord.Embed(title=name)
      await message.channel.send("Processing the video...")
      await message.channel.send(embed=em)

      await message.channel.send(file=discord.File("vid.mp4", filename=None, spoiler=False))

      await message.channel.send(file=discord.File("audio.mp3", filename=None, spoiler=False))


    if msg.startswith("$flipcoin"):
        result = random.randint(0,1)
        if result == 0:
            outcome = "Heads"
        else:
            outcome = "Tails"
        await message.channel.send(outcome + "💲")

    if msg.startswith("$fights"):

      name, original_url = process_vid("fightporn")

      em = discord.Embed(title=name)
      await message.channel.send("Processing the video...")
      await message.channel.send(embed=em)

      await message.channel.send(file=discord.File("vid.mp4", filename=None, spoiler=False))

      await message.channel.send(file=discord.File("audio.mp3", filename=None, spoiler=False))

    if msg.startswith("$pottermeme"):
      await message.channel.send(embed=meme("HarryPotterMemes"))

    if msg.startswith("$nature"):
      await message.channel.send(embed=meme("EarthPorn"))

    if msg.startswith("$help"):
      await message.channel.send("Help will always be given at Hogwarts to those who ask for it. :man_mage:"
        )

    if msg.startswith("$5050"):

      name, url = fifty()
      print(name)
      print(url)
      response = requests.get(url)
      open("img.png", 'wb').write(response.content)

      time.sleep(1.5)

      await message.channel.send(embed=discord.Embed(title=name))
      await message.channel.send(file=discord.File("img.png", filename=None, spoiler=True))

    if (msg.startswith("$insult <@!441694764119752706>")) or (msg.startswith("$insult <@!203672766426251264>"))or (msg.startswith("$insult <@!791391640697831444>")) or (msg.startswith("$insult <@!801691341381566464>")):  #Karan and Horse and Dumbledore

      insult = get_insults()
      await message.delete()
      await message.channel.send("<@!" + str(message.author.id) + "> " + random.choice(insult))
      print(message.author.id)

    elif msg.startswith('$insult'):  ################################
        user = msg.split(" ")
        if len(user) > 1:
          userid = user[1]
          insult = get_insults()
          await message.delete()
          await message.channel.send(userid + " " + random.choice(insult))
        else:
            insult = get_insults()
            await message.channel.send(random.choice(insult))

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off")

    if msg.startswith("cod"):
        await message.channel.send("Study your magic kids.")

    #if msg.startswith("<@!494966755278716928>"):  #beaver
        #await message.channel.send("NIAAAA;)")
    
    if msg.startswith("jukebox"):
        await message.channel.send("-play https://open.spotify.com/playlist/12Jr0eUl336QvlbrZpEY2O?si=UTwKLeggRM284BZfQKGHiA")



keep_alive()
client.run(os.getenv('TOKEN'))
