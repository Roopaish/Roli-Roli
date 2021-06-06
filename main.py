### Keep the server running all the time
# import neverSleep

# neverSleep.awake('https://Roli-Roli.roopaish.repl.co')

import discord, os, requests, json, random
from discord.ext import commands

### Using replit database
from replit import db

### Getting token from environment
token = os.environ['TOKEN']

### Extensions

### Connection to discord
client = commands.Bot(command_prefix=".")


### Register event when bot is ready
@client.event
async def on_ready():
    print(f"You are Logged in as {client.user}")


### Bot commands with functions

# Greetings
@client.command(name = 'hi', aliases = ['hey', 'hello'])
async def hi(ctx):
    await ctx.send('>>> ```Hey there!\
                \nI am Roli.\
                \nI am here to make you laugh and play music for you.```')

# Check ping
@client.command()
async def ping(ctx):
    await ctx.send(f'**Pong!** {round(client.latency * 1000)}ms')

# Clear messages
@client.command()
# @commands.has_permissions(manage_message = True)
# @commands.has_role("admin")
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)

# Generate random jokes
def random_joke():
    response = requests.get(
        'https://official-joke-api.appspot.com/random_joke')
    json_data = json.loads(response.text)
    joke = json_data['setup'] + '\n\n' + json_data['punchline']
    return joke

@client.command(aliases=['rj'])
async def random_jokes(ctx):
    await ctx.send(random_joke())


# Generate programming jokes
def programming_joke():
    response = requests.get(
            'https://official-joke-api.appspot.com/jokes/programming/random')
    json_data = json.loads(response.text)
    joke = json_data[0]['setup'] + '\n\n' + json_data[0]['punchline']
    return joke

@client.command(aliases=['pj'])
async def programming_jokes(ctx):
    await ctx.send(programming_joke())


# Respond to sad words or not
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
starter_uplifting_words = ["Cheer up!", "Hang in there!"]

if 'responding' not in db.keys():
    db['responding'] = True


# Toggle responding to sad message
@client.command(aliases=['respond'])
async def responding(ctx, value):
    if value.lower() == "true":
        db['responding'] = True
        await ctx.send('Responding is on.')
    else:
        db['responding'] = False
        await ctx.send('Responding is off.')


# Add new uplifting words
def update_uplifting_words(msg):
    if 'uplifting_words' in db.keys():
        uplifting_words = db['uplifting_words']
        uplifting_words.append(msg)
        db['uplifting_words'] = uplifting_words
    else:
        db['uplifting_words'] = [msg]


@client.command()
async def new(ctx, *, words):
    update_uplifting_words(words)
    await ctx.send('New uplifting words added!')


# Delete uplifting_words
def delete_uplifting_words(index):
    uplifting_words = db['uplifting_words']
    if (len(uplifting_words) > index):
        del uplifting_words[index]
        db['uplifting_words'] = uplifting_words


@client.command(aliases = ['del'])
async def delete_words(ctx, index):
    deleted_words = ''
    if 'uplifting_words' in db.keys():
        deleted_words = db['uplifting_words'][int(index) - 1]
        delete_uplifting_words(int(index) - 1)

    await ctx.send(f'\'{deleted_words}\' deleted.')


# list all uplifting words
@client.command('list')
async def list_words(ctx):
    uplifting_words = []
    if 'uplifting_words' in db.keys():
        uplifting_words = db['uplifting_words']
    await ctx.send(uplifting_words.value)


# Sensing messages in server
@client.event
async def on_message(message):
    # processing commands in order to use commands decorator
    await client.process_commands(message)
    # checking if the msg is by bot itself
    if message.author == client.user:
        return

    msg = message.content

    if db['responding']:
        options = starter_uplifting_words
        if 'uplifting_words' in db.keys():
            options += db['uplifting_words']

        if any(word in msg for word in sad_words):
            await message.channel.send(
                f'{random.choice(options)}\nI have something to make you laugh\n\n{random_joke()}'
            )


client.run(token)

