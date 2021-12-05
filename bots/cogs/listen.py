import time
import datetime as dt
import csv
import discord
from cogs.handle_orders import positions_check
from discord.ext import commands, tasks
from discord.utils import get
from cogs.call import make_call

client = commands.Bot(command_prefix="!")

class Listen(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['loaded?'])
    async def loaded(self, ctx):
        await ctx.send("listen.py is loaded.")

    @commands.command()
    async def update_holdings(self, ctx):
        with open('/home/HOMEDIR/discord/bots/txt/eth_rec.csv', mode='a') as ltc_csv:
            fields = ['crypto', 'order', 'price', 'date']
            writer = csv.writer(ltc_csv)
            writer.writerow(fields)

    # Read Messages
    @commands.Cog.listener()
    async def on_message(self, message):
        author = str(message.author)
        date = dt.datetime.now()
        messageContent = message.content
        print("{} at {}:  {}".format(author, date, messageContent))
        #'Bitcoin Hook#0000', 
        user_authors = ['XXXXXXXXXXX', 'XXXXXXXXXXXXXXXX'] #ETH Hook#0000 #LTC Hook#0000
        channel = client.get_channel(12345678910)
        #Call only if action needs to be taken
        #ETH
        if author == "ETH Hook#0000":
            currency_dict = positions_check()
            if "RSI" in messageContent:
                if "Ethereum" not in currency_dict:
                    await message.channel.send("ETH RSI Alert")
                    #await message.channel.send("ETH RSI Alert. Making call")
                    #make_call(messageContent, author)
            if "Alligator" in messageContent:
                if "Ethereum" in currency_dict:
                    await message.channel.send("ETH Alligator Alert")
                    #await message.channel.send("ETH Alligator Alert. Making call")
                    #make_call(messageContent, author)
        #LTC
        if author == "LTC Hook#0000":
            currency_dict = positions_check()
            if "RSI" in messageContent:
                if "Litecoin" not in currency_dict:
                    await message.channel.send("LTC RSI Alert")
                    #await message.channel.send("LTC RSI Alert. Making Call")
                    #make_call(messageContent, author)
            if "Alligator" in messageContent:
                if "Litecoin" in currency_dict:
                    await message.channel.send("LTC Alligator Alert")
                    #await message.channel.send("LTC Alligator Alert. Making call")
                    #make_call(messageContent, author)
        
        #Checks for OBV Webhooks
        if author == 'OBV Hook#0000':
            obv_to_csv(messageContent)

        #Checks for STOCH Webhook
        # if author == 'Stoch Hook#0000':
        #     stoch_to_csv(messageContent)

        #CHecks for WaveTrend
        if author == 'WaveTrend Hook#0000':
            wt_to_csv(messageContent)

        #Deletes commands from users
        if "!clear" not in message.content and author in user_authors and not channel:
            try:
                time.sleep(3)
                await message.delete()
            except:
                print("Igonoring error")
                
def obv_to_csv(messageContent):
    #Separate Message
    array = messageContent.split(' ')
    obv = array[2]
    dt = array[4]
    array2 = dt.split("T")
    date = array2[0]
    time = array2[1]

    #On Balance Volumes
    if ("LTCUSD" in messageContent):
        with open('/home/HOMEDIR/discord/bots/txt/LTC/ltc_obv.csv', mode='a') as ltc_csv2:
            fields = [date, time, obv]
            writer = csv.writer(ltc_csv2)
            writer.writerow(fields)
            ltc_csv2.close()
    if ("ETHUSD" in messageContent):
        with open('/home/HOMEDIR/discord/bots/txt/ETH/eth_obv.csv', mode='a') as eth_csv2:
            fields = [date, time, obv]
            writer = csv.writer(eth_csv2)
            writer.writerow(fields)
            eth_csv2.close()

def stoch_to_csv(messageContent):
    #Example: 2020-11-24,01:00:00Z,65.848214
    stoch = messageContent[21:30]
    date = messageContent[44:54]
    time = messageContent[55:64]

    #Stoch
    if ("LTCUSD" in messageContent and "STOCH" in messageContent):
        with open('/home/HOMEDIR/discord/bots/txt/LTC/ltc_stoch.csv', mode='a') as ltc_stoch:
            fields = [date, time, stoch]
            writer = csv.writer(ltc_stoch)
            writer.writerow(fields)
            ltc_stoch.close()
    if ("ETHUSD" in messageContent and "STOCH" in messageContent):
        with open('/home/HOMEDIR/discord/bots/txt/ETH/eth_stoch.csv', mode='a') as eth_stoch:
            fields = [date, time, stoch]
            writer = csv.writer(eth_stoch)
            writer.writerow(fields)
            eth_stoch.close()

def wt_to_csv(messageContent):
    #Separate Message
    array = messageContent.split(' ')
    g = array[3]
    r = array[5]
    b = array[7]
    dt = array[9]
    array2 = dt.split("T")
    date = array2[0]
    time = array2[1]

    #Stoch
    if ("LTCUSD" in messageContent):
        with open('/home/HOMEDIR/discord/bots/txt/LTC/ltc_wt.csv', mode='a') as ltc_wt:
            fields = [date, time, r, g, b]
            writer = csv.writer(ltc_wt)
            writer.writerow(fields)
            ltc_wt.close()
    if ("ETHUSD" in messageContent):
        with open('/home/HOMEDIR/discord/bots/txt/ETH/eth_wt.csv', mode='a') as eth_wt:
            fields = [date, time, r, g, b]
            writer = csv.writer(eth_wt)
            writer.writerow(fields)
            eth_wt.close()


def setup(client):
    client.add_cog(Listen(client))
