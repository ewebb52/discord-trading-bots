import time
import discord
from discord.ext import commands, tasks
from cogs.handle_orders import trigger_rsi, trigger_alligator, start_order, order_status, positions_check, reset_obv, reset_stoch, bot_check_crypto_prices, reset_wt
import robin_stocks as r
import pyotp
import csv
import os

client = commands.Bot(command_prefix="+")

class Robin_Cog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=[])
    async def loaded(self, ctx):
        await ctx.send("ltc.py is loaded.")

    # Read Messages
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            author = str(message.author)
            valid_bots = ['LTC Hook#0000'] #'TrollEpollEolE#5214'
            if author in valid_bots:
                currency_dict = positions_check()
                messageContent = message.content

                ################  LITECOIN  ####################
                if ("LTCUSD" in messageContent):

                    #Buy Litecoin
                    if ("RSI" in messageContent):

                        #Determine if we own LTC
                        ltc = "Litecoin"
                        if ltc not in currency_dict:
                            trigger_rsi("ETH", "True")
                            print("We currently do not hold Litecoin")
                            await message.channel.send("Pending LTC BUY order! \nCurrent LTC price: {}".format(bot_check_crypto_prices("LTC")))
                            created_at, bp = start_order("LTC", "BUY", currency_dict)
                            #failed due to time
                            if created_at == "Time Error":
                                await message.channel.send("ETH BUY order did not process because percentage never dropped far enough from last sell order.")
                                trigger_rsi("LTC","False")
                                reset_obv("LTC")
                            else:
                                #LTC Ordered
                                av_price = order_status("LTC", "BUY", created_at)
                                if av_price == None:
                                    await message.channel.send("LTC BUY order did not process. Check Errors")
                                else:
                                    await message.channel.send("LTC BUY order filled at price {} with estimated buying power {}".format(av_price, bp))
                                trigger_rsi("LTC","False")
                                reset_obv("LTC")
                        else:
                            await message.channel.send("We already own LTC!")
                    
                    #Sell Litecoin
                    if ("Alligator" in messageContent):
                        
                        #Determine if we own LTC
                        ltc = "Litecoin"
                        if ltc in currency_dict:
                            trigger_alligator("LTC", "True")
                            await message.channel.send("Pending LTC SELL order of quantity: {} \nCurrent LTC price: {}".format(currency_dict['Litecoin'], bot_check_crypto_prices("LTC")))
                            status, created_at = start_order("LTC", "SELL", currency_dict)
                            if status == True:
                                #LTC Sold
                                await message.channel.send("LTC SELL order filled at price: {}".format(order_status("LTC", "SELL", created_at)))
                                trigger_alligator("LTC", "False")
                                reset_wt("LTC")
                            else:
                                await message.channel.send("LTC SELL order did not process. Reason: {}".format(created_at))
                                trigger_alligator("LTC", "False")
                        else:
                            await message.channel.send("No LTC to sell!")
        except:
            print("Avoiding a crash!")
            test()

def test():
    print("We are still working!")

def setup(client):
    client.add_cog(Robin_Cog(client))