from tradingview_ta import TA_Handler, Interval

# Global Variables
symbols_object_list = []
rsi_list = []
ema_list = []
combined_list = []
symbol_list = []

class Stock:
    def __init__(self, symbol, time, ema200, ema5, rsi, close):
        self.symbol = symbol
        self.time = time
        self.ema200 = ema200
        self.ema5 = ema5
        self.rsi = rsi
        self.close = close

    def add_to_list(self):
        symbols_object_list.append(self)

def scan_list():
    clear_lists()
    f = open("/home/edw2139/discord/bots/txt/symbols.txt", "r")
    for line in f:
        symbol_list.append(line.strip().split(' ', 1))
    f.close()
    
    for i in symbol_list:
        get_symbol_info(i)

    scan_ema(symbols_object_list)
    scan_rsi(symbols_object_list)
    scan_combined(rsi_list, ema_list)
    
    return rsi_list, ema_list, combined_list 

individual = []
def scan_individual(stock_symbol):
    clear_lists()
    search_for = stock_symbol.upper()
    f = open("/home/edw2139/discord/bots/cogs/symbols.txt", "r")
    for line in f:
        if search_for in line:
            individual.append(line.strip().split(' ', 1))
    f.close()
    
    if (len(individual) == 0):
        print("Error")

    for i in individual:
        get_symbol_info(i)
    return symbols_object_list

def get_symbol_info(symbol):
    handler = TA_Handler()
    handler.set_symbol_as(symbol[0])
    handler.set_exchange_as_crypto_or_stock(symbol[1])
    handler.set_screener_as_stock("america")
    handler.set_interval_as(Interval.INTERVAL_1_HOUR)
    analysis = handler.get_analysis()
    results = analysis.indicators

    print(symbol)

    s1 = Stock(symbol[0], analysis.time, results['EMA200'], results['EMA5'], 
                results['RSI'], results['close'])
    s1.add_to_list()

def scan_ema(symbols_object_list):
    for i in symbols_object_list:
        if (i.ema200 > i.close):
            ema_list.append(i)

def scan_rsi(symbols_object_list):
    for i in symbols_object_list:
        if (i.rsi < 40):
            rsi_list.append(i)

def scan_combined(rsi_list, ema_list):
    for x in rsi_list:
        for i in ema_list:
            if (i.symbol == x.symbol):
                combined_list.append(i)

def clear_lists():
    symbols_object_list.clear()
    rsi_list.clear()
    ema_list.clear()
    combined_list.clear()
    individual.clear()
    symbol_list.clear()

def print_lists(rsi_list, ema_list, combined):
    print("RSI LIST:")
    for i in rsi_list:
        print(i.__dict__)

    print("EMA LIST:")
    for i in ema_list:
        print(i.__dict__)

    print("COMBINED LIST:")
    for i in combined_list:
        print(i.__dict__)
