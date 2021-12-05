# THIS IS THE MAIN ROBOT
import discord
from discord.ext import commands, tasks

def run_rcb():
    client = commands.Bot(command_prefix="!")
    @client.event
    async def on_ready():
        client.load_extension('cogs.listen')
        print("RCB is ready.")

    #@client.event
    #async def on_message():


    #Test ping
    @client.command()
    async def ping(ctx):
        await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


    #Clear Messages
    @client.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)

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
    async def reload(ctx, extension):
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
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

    client.run('Nzc4NDUwMjE0NjQxOTkxNzMx.X7SKQg.EbKgWT7_Yg2uW-7ItosZT6zZmrc')
