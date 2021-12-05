import time
import datetime
import discord
from discord.ext import commands, tasks
from cogs.handle_orders import login
import robin_stocks as r
import pyotp
import csv
import os

totp = pyotp.TOTP("DKNPSL7Z5DQ4CNFQ").now()

client = commands.Bot(command_prefix="*")

class Robin_Cog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=[])
    async def loaded(self, ctx):
        await ctx.send("robin_cog.py is loaded.")

    @commands.command()
    async def cancel(self, ctx):
        login()
        r.orders.cancel_all_crypto_orders()
        await ctx.send("Orders Cancelled.")

    @commands.command()
    async def bp(self, ctx):
        login()
        profileData = r.load_account_profile()
        #Typical Variables
        crypto_bp = profileData['crypto_buying_power']
        await ctx.send("RobinHood Buying Power: {}".format(crypto_bp))

    @commands.command()
    async def crypto_pos(self, ctx):
        s = "We currently hold: \n"
        t = ""
        login()
        currency_dict = {}
        currency_dict.clear()
        d = r.crypto.get_crypto_positions()
        for i in d:
            quantity = float(i['quantity_available'])
            if (quantity > 0):
                currency_name = i['currency']['name']
                currency_dict[currency_name] = quantity
        for k, v in currency_dict.items():
            t = ("{} {}\n".format(v, k))
            s = s + t
        await ctx.send(s)

    #Shows info about cryptocurrency
    @commands.command()
    async def crypto_prices(self, ctx):
        login()
        s = ""
        t = ""
        crypto_list = ["BTC", "LTC", "ETH"]
        for i in crypto_list:
            c = r.crypto.get_crypto_quote(i)
            t = ("{} at {}\n".format(c['symbol'], c['mark_price']))
            s = s + t
        await ctx.send("Current Crypto Prices: \n\n" + s)

    #Shows info about cryptocurrency
    @commands.command()
    async def update_rec(self, ctx, coin, order_type, cost):
        #Set Variables
        rec = coin.upper()
        order = order_type.upper()
        price = cost.upper()
        date = datetime.datetime.now()
        #Get Appropriate File
        filename = ""
        if (rec == "ETH"):
            filename = '/home/edw2139/discord/bots/txt/ETH/eth_rec.csv'
        if (rec == "LTC"):
            filename = '/home/edw2139/discord/bots/txt/LTC/ltc_rec.csv'
        #Update Record
        with open(filename, mode='w') as f:
            field = [rec, order, price, date]
            writer = csv.writer(f)
            writer.writerow(field)
            f.close()
        await ctx.send("Record Updated.")

    # Read Messages
    @commands.Cog.listener()
    async def on_message(self, message):
        messageContent = message.content
        author = str(message.author)
        


def setup(client):
    client.add_cog(Robin_Cog(client))
