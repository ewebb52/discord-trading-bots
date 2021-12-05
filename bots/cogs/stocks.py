from tradingview_ta import TA_Handler, Interval
import discord
from discord.ext import commands, tasks
from cogs.scanner import *

#Variables
client = commands.Bot(command_prefix="$")
channel = client.get_channel(12345678910)

class Stocks(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Check if scan.py is loaded
    @commands.command()
    async def loaded(self, ctx):
        await ctx.send("scan.py is loaded.")


    list_returned = []
    x = None
    #Scan a specific stock
    @commands.command()
    async def scan(self, ctx, stock):
        list_returned = scan_individual(stock)
        for i in list_returned:
            if (i.ema200 > i.close):
                x = "Below"
            else:
                x = "Above"

        await ctx.send("""
        Symbol:       {} 
Last Close:   {} 
RSI:          {} 
Last Price {} EMA200""".format(i.symbol, i.close, i.rsi, x))
        list_returned.clear()


    #Scan entire market
    @commands.command(aliases=['market scan'])
    async def scan_market(self, ctx, market='combined'):
        s = ""
        t = ""
        if (market == 'combined'):
            rsi_list, ema_list, combined_list = scan_list()
            print("RSI: {}".format(len(rsi_list)))
            print("EMA: {}".format(len(ema_list)))
            print("Combined: {}".format(len(combined_list)))
            if (len(combined_list) == 0):
                await ctx.send("No stocks in market currently meet condition.")
            else:
                for i in combined_list:
                    t = ("{} at {} w/ RSI {} \n".format(i.symbol, i.close, int(i.rsi)))
                    s = s + t
                await ctx.send("Stocks with low RSI and below EMA200: \n\n" + s)
        if (market == 'rsi'):
            rsi_list, ema_list, combined_list = scan_list()
            if (len(rsi_list) == 0):
                await ctx.send("No stocks in market currently meet condition.")
            else:
                for i in rsi_list:
                    t = ("{} at {} w/ RSI {} \n".format(i.symbol, i.close, int(i.rsi)))
                    s = s + t
                await ctx.send("Stocks with low RSI: \n\n" + s)
        if (market == 'ema'):
            rsi_list, ema_list, combined_list = scan_list()
            if (len(ema_list) == 0):
                await ctx.send("No stocks in market currently meet condition.")
            else:
                for i in ema_list:
                    t = ("{} at {} w/ RSI {} \n".format(i.symbol, i.close, int(i.rsi)))
                    s = s + t
                await ctx.send("Stocks below EMA200: \n\n" + s)
        
def setup(client):
    client.add_cog(Stocks(client))
