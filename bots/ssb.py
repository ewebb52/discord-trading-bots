from datetime import datetime as dt
from pytz import timezone
import discord
from discord.ext import commands


def run_ssb():
    client = commands.Bot(command_prefix="$")
    @client.event
    async def on_ready():
        client.load_extension('cogs.stocks')
        print("SSB is ready.")

    #Test ping
    @client.command()
    async def ping(ctx):
        await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

    #############################TODO scan markets at 4am, 630am, 4pm
    # @client.loop(seconds=5)
    # async def check_time():
    #     tz = timezone('EST')
    #     print(dt.now(tz))
    #     channel = client.get_channel(677244478267850764)
    #     await channel.send('hello')

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

    # ######## Error Handlings ###########
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

    client.run('Nzc4ODM4ODY2OTE2MTQ3MjEw.X7X0Nw.lX8hR9y5LCArMX4qx8EytEJzCrk')
