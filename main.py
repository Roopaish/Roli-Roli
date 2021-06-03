import neverSleep
neverSleep.awake('https://Roli-Roli.roopaish.repl.co')

import discord, os, requests, json, random

from replit import db

token = os.environ['TOKEN']

# to sense sad word and give uplifting_words
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
starter_uplifting_words = ["Cheer up!", "Hang in there!"]


# generate random jokes
def random_joke():
    response = requests.get(
        'https://official-joke-api.appspot.com/random_joke')
    json_data = json.loads(response.text)
    joke = json_data['setup'] + '\n\n' + json_data['punchline']
    return joke


# genrate programming jokes
def programming_joke():
    response = requests.get(
        'https://official-joke-api.appspot.com/jokes/programming/random')
    json_data = json.loads(response.text)
    joke = json_data[0]['setup'] + '\n\n' + json_data[0]['punchline']
    return joke


# update uplifting_words
def update_uplifting_words(msg):
    if 'uplifting_words' in db.keys():
        uplifting_words = db['uplifting_words']
        uplifting_words.append(msg)
        db['uplifting_words'] = uplifting_words
    else:
        db['uplifting_words'] = [msg]


# delete uplifting_words
def delete_uplifting_words(index):
    uplifting_words = db['uplifting_words']
    if (len(uplifting_words) > index):
        del uplifting_words[index]
        db['uplifting_words'] = uplifting_words


# respond to word or not
if 'responding' not in db.keys():
    db['responding'] = True

# Connection to discord
client = discord.Client()


# register event when bot is ready
@client.event
async def on_ready():
    print(f"You are Logged in as {client.user}")


# sensing message
@client.event
async def on_message(message):
    # checking if the msg is by bot itself
    if message.author == client.user:
        return

    msg = message.content

    # helper/intro command
    if msg.startswith("$h"):
        await message.channel.send(
            'Hey There! I am roli. \nI am here to assist you to bring laughter in your miserable life.\n\n$j -> random joke\n$p -> programming joke\n$responding -> set if the bot will respond to sad message or not\n$list -> list all uplifting words\n$new msg -> add new uplifting message\n$del index -> delete uplifting message\nInstall Link -> https://discord.com/api/oauth2/authorize?client_id=849639569733058590&permissions=2151148096&scope=bot'
        )

    # get jokes with commands
    if msg.startswith('$j'):
        await message.channel.send(random_joke())
    if msg.startswith('$p'):
        await message.channel.send(programming_joke())

    # sensing sad words
    if db['responding']:
        options = starter_uplifting_words
        if 'uplifting_words' in db.keys():
            options += db['uplifting_words']

        if any(word in msg for word in sad_words):
            await message.channel.send(
                f'{random.choice(options)}\nI have something to make you laugh\n\n{random_joke()}'
            )

    if msg.startswith('$responding'):
        value = msg.split('$responding ', 1)[1]

        if value.lower() == "true":
            db['responding'] = True
            await message.channel.send('Responding is on.')
        else:
            db['responding'] = False
            await message.channel.send('Responding is off.')

    # adding new uplifting words
    if msg.startswith('$new'):
        uplifting_msg = msg.split("$new ", 1)[1]
        update_uplifting_words(uplifting_msg)
        await message.channel.send('New uplifting word added!')

    # deleting new uplifting words
    if msg.startswith('$del'):
        uplifting_words = []
        if 'uplifting_words' in db.keys():
            index = int(msg.split('$del', 1)[1])
            delete_uplifting_words(index)
            uplifting_words = db['uplifting_words']

        await message.channel.send(uplifting_words.value)

    # listing uplifting words
    if msg.startswith('$list'):
        uplifting_words = []
        if 'uplifting_words' in db.keys():
            uplifting_words = db['uplifting_words']
        await message.channel.send(uplifting_words.value)


client.run(token)
