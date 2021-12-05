#ETH Bot
import discord
from discord.ext import commands, tasks

def run_ltc():
    client = commands.Bot(command_prefix="+")

    @client.event
    async def on_ready():
        client.load_extension('cogs.ltc')
        print("LTC Bot is ready.")

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
        client.unload_extension(f'cogs.ltc')
        client.load_extension(f'cogs.ltc')
    ##########End of Cogs###############

    ######## Error Handlings ###########
    #General Error Handling
    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please pass in all required arguments.")


    client.run('NzgwMTk3MjQ0ODQ5NzUwMDU3.X7rlTg.2UQ8B7cyxZDjZ3M0dYFdAlA9f_c')
