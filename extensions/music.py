from discord.ext import commands
import youtube_dl

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client 
    
    # Events/Listeners Decorator 
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music bot is online.') 
    
    # Making commands
    @commands.command()
    async def pingm(self, ctx):
        await ctx.send('pong')

# Setup is necessary to run the cog
def setup(client):
    client.add_cog(Music(client))