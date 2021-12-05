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
        await ctx.send("eth.py is loaded.")

    # Read Messages
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            author = str(message.author)
            valid_bots = ['ETH Hook#0000'] #'TrollEpollEolE#5214'
            if author in valid_bots:
                currency_dict = positions_check()
                messageContent = message.content

                #################  ETHEREUM  ##################
                if ("ETHUSD" in messageContent):
                    
                    #Buy Ethereum
                    if ("RSI" in messageContent):

                        #Determine if we own ETH
                        eth = "Ethereum"
                        if eth not in currency_dict:
                            trigger_rsi("ETH", "True")
                            print("We currently do not hold Ethereum")
                            await message.channel.send("Pending ETH BUY order! \nCurrent ETH price: {}".format(bot_check_crypto_prices("LTC")))
                            created_at, bp = start_order("ETH", "BUY", currency_dict)
                            #failed due to time
                            if created_at == "Time Error":
                                await message.channel.send("ETH BUY order did not process because percentage never dropped far enough from last sell order.")
                                trigger_rsi("ETH","False")
                                reset_obv("ETH")
                            else:
                                #Eth Ordered
                                av_price = order_status("ETH", "BUY", created_at)
                                if av_price == None:
                                    await message.channel.send("ETH BUY order did not process. Check Errors")
                                else: 
                                    await message.channel.send("ETH BUY order filled at price {} with estimated buy power: {}".format(av_price, bp))
                                trigger_rsi("ETH","False")
                                reset_obv("ETH")
                        else:
                            await message.channel.send("We already own ETH!")
                    
                    #Sell Ethereum
                    if ("Alligator" in messageContent):

                        #Determine if we own ETH
                        eth = "Ethereum"
                        if eth in currency_dict:
                            trigger_alligator("ETH", "True")
                            await message.channel.send("Pending ETH SELL order of quantity: {} \nCurrent ETH price: {}".format(currency_dict['Ethereum'], bot_check_crypto_prices("ETH")))
                            status, created_at = start_order("ETH", "SELL", currency_dict)
                            if status == True:
                                #ETH sold
                                await message.channel.send("ETH SELL order filled at price: {}".format(order_status("ETH", "SELL", created_at)))
                                trigger_alligator("ETH", "False")
                                reset_wt("ETH")
                            else:
                                await message.channel.send("ETH SELL order did not process. Reason: {}".format(created_at))
                                trigger_alligator("ETH", "False")

                        else:
                            await message.channel.send("No ETH to sell!")
        except:
            print("avoiding a crash!")
            test()

def test():
    print("We are still working!")

def setup(client):
    client.add_cog(Robin_Cog(client))