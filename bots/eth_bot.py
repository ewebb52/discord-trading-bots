#ETH Bot
import discord
from discord.ext import commands, tasks

def run_eth():
    client = commands.Bot(command_prefix="+")

    @client.event
    async def on_ready():
        client.load_extension('cogs.eth')
        print("ETH Bot is ready.")

    #@client.event
    #async def on_message():

    #Test ping
    @client.command()
    async def ping(ctx):
        await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

    @client.command()
    async def kill(ctx):
        await ctx.send("Robinhood Bot shutting down!")
        client.close()

    ##########Begin of Cogs#############
    #Load
    @client.command()
    async def load(ctx, extension):
        client.load_extension(f'cogs.{extension}')

    #Unload
    @client.command()
    async def unload(ctx, extension):
        client.unload_extension(f'cogs.{extension}')

    #Reload
    @client.command()
    async def reload(ctx):
        client.unload_extension(f'cogs.eth')
        client.load_extension(f'cogs.eth')
    ##########End of Cogs###############

    ######## Error Handlings ###########
    #General Error Handling
    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please pass in all required arguments.")

    # #Reload Error Handing
    # @reload.error
    # async def clear_error(ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send("Please check to see if module was loaded in the first place")
    # ###### End Error Handlings #########

    client.run('NzgwMTg1NTI0OTI0MTg2NjY1.X7raZA.tfELJMG4qQuh0R6B5yTlxkm1SJc')
