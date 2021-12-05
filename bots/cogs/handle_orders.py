import robin_stocks as r
import time
import datetime
import pyotp
import csv

##############################
import getpass
import os
import pickle
import random
import robin_stocks.helper as helper
import robin_stocks.urls as urls
###############################

#totp = pyotp.TOTP("DKNPSL7Z5DQ4CNFQ").now()

###################### BEGIN ORDER FUNCTIONS ########################
def start_order(symbol, order_type, currency_dict):
    #bp = 1.5                          #TODO DELETE
    bp = determine_buying_power(check_acc_bp(), symbol, currency_dict)
    print("\n!!!!{} {} started!!!!".format(symbol, order_type))
    if order_type == "BUY":
        created_at, bp = buy_order(symbol, order_type, bp)
        print("after buy_order")
        return created_at, bp
    if order_type == "SELL":
        status, created_at = sell_order(symbol, order_type, currency_dict) 
        return status, created_at

def buy_order(symbol, order_type, bp):
    timer = []
    timer.clear()
    #Variables
    other = ""
    if symbol == "ETH":
        other = ["LTC", "Litecoin"]
    if symbol == "LTC":
        other = ["ETH", "Ethereum"]
    #Begin Buy Checks
    while (check_rsi(symbol)):
        #Check if other RSI has been Triggered
        crypto_price = bot_check_crypto_prices(symbol)
        print("{} Price: {}  Buying Power Attempt:{}".format(symbol, crypto_price, bp))
        if (get_percentage(symbol, crypto_price, order_type)):
            print("after checking percentage")
            if (check_obv(symbol)):
                print("Buying with buying power of: {}".format(bp))
                created_at = order_crypto(symbol, bp)       #TODO UNCOVER
                time.sleep(2)
                return created_at, bp
            else:
                print("Waiting 7 min for OBV to meet requirements...")
                date = datetime.datetime.now()
                print(date)
                time.sleep(420)
        else:
            timer.append(1)
            if len(timer) > 10:
                return "Time Error", False
            print("Waiting 7 min to meet percentage requirements...")
            date = datetime.datetime.now()
            print(date)
            time.sleep(420)

def sell_order(symbol, order_type, currency_dict):
    #Variables
    timer = []
    timer.clear()
    key = ""
    if symbol == "ETC":
        key == "Ethereum"
    if symbol == "LTC":
        key == "Litecoin"
    #Begin Sell Checks
    while (check_alligator(symbol)):
        date = datetime.datetime.now()
        print(date)
        time.sleep(420)
        crypto_price = bot_check_crypto_prices(symbol)
        if (get_percentage(symbol, crypto_price, order_type)):
            if (check_wt(symbol)):
                print("Selling")
                created_at = sell_crypto(symbol, currency_dict[key])
                time.sleep(5)
                return True, created_at
            else:
                timer.append(1)
                if len(timer) > 5:
                    timer.clear()
                    return False, "WaveTrend timed out."
                else:
                    date = datetime.datetime.now()
                    print(date)
                    print("Waiting 7 minutes for Stoch to meet requierments...")
                    time.sleep(420)
        else:
            print("Percentage to sell is not high enough. Holding instead.")
            return False, "Percentage is not over %6"


############################ RESET FILES ###########################
def reset_wt(symbol):
    #Find last items History
    filename = ""
    if symbol == "ETH":
        filename = '/home/edw2139/discord/bots/txt/ETH/eth_wt.csv'
    if symbol == "LTC":
        filename = '/home/edw2139/discord/bots/txt/LTC/ltc_wt.csv'

    f = open(filename, "w+")
    f.close()

def reset_obv(symbol):
    #Find last items History
    filename = ""
    if symbol == "ETH":
        filename = '/home/edw2139/discord/bots/txt/ETH/eth_obv.csv'
    if symbol == "LTC":
        filename = '/home/edw2139/discord/bots/txt/LTC/ltc_obv.csv'

    f = open(filename, "w+")
    f.close()

def reset_stoch(symbol):
    #Find last items History
    filename = ""
    if symbol == "ETH":
        filename = '/home/edw2139/discord/bots/txt/ETH/eth_stoch.csv'
    if symbol == "LTC":
        filename = '/home/edw2139/discord/bots/txt/LTC/ltc_stoch.csv'

    f = open(filename, "w+")
    f.close()


######################### CHECK VARIABLES ###########################
def check_wt(symbol):
    #Find last items History
    filename = ""
    if symbol == "ETH":
        filename = '/home/edw2139/discord/bots/txt/ETH/eth_wt.csv'
    if symbol == "LTC":
        filename = '/home/edw2139/discord/bots/txt/LTC/ltc_wt.csv'
    #Read File
    wt_data = []
    wt_data.clear()
    with open(filename, mode='r') as rec: 
        reader = csv.reader(rec, delimiter=',') 
        for row in reader: 
            if row:
                # Date, Time, G, R, B
                columns = [row[0], row[1], row[2], row[3], row[4]] 
                wt_data.append(columns) 
        rec.close()
    #Compare OBV's, ensure we are rising before buying
    latest_dp = float(wt_data[-1][2])
    seven_min_ago_dp = float(wt_data[-7][2])
    percentage = (abs(latest_dp - seven_min_ago_dp) / seven_min_ago_dp) * 100
    print("Percentage: {}  (must meet 18%)".format(percentage))
    if ((percentage > 18) and (latest_dp < seven_min_ago_dp)):
        return True
    else:
        return False

def check_stoch(symbol):
    #Find last items History
    filename = ""
    if symbol == "ETH":
        filename = '/home/edw2139/discord/bots/txt/ETH/eth_stoch.csv'
    if symbol == "LTC":
        filename = '/home/edw2139/discord/bots/txt/LTC/ltc_stoch.csv'
    #Read File
    stoch_data = []
    stoch_data.clear()
    with open(filename, mode='r') as rec: 
        reader = csv.reader(rec, delimiter=',') 
        for row in reader: 
            if row:
                # Date, Time, Data
                columns = [row[0], row[1], row[2]] 
                stoch_data.append(columns) 
        rec.close()
    #Compare OBV's, ensure we are rising before buying
    latest_dp = float(stoch_data[-1][2])
    seven_min_ago_dp = float(stoch_data[-7][2])
    if (latest_dp < seven_min_ago_dp):
        return True
    else:
        return False

def check_obv(symbol):
    #Find last items History
    filename = ""
    if symbol == "ETH":
        filename = '/home/edw2139/discord/bots/txt/ETH/eth_obv.csv'
    if symbol == "LTC":
        filename = '/home/edw2139/discord/bots/txt/LTC/ltc_obv.csv'
    #Read File
    obv_data = []
    obv_data.clear()
    with open(filename, mode='r') as rec: 
        reader = csv.reader(rec, delimiter=',') 
        for row in reader: 
            if row:  
                # Date, Time, Data
                columns = [row[0], row[1], row[2]] 
                obv_data.append(columns) 
        rec.close()
    #Compare OBV's, ensure we are rising before buying
    latest_dp = float(obv_data[-1][2])
    seven_min_ago_dp = float(obv_data[-7][2])
    print("Latest OBV: {} 7Min ago OBV: {}".format(latest_dp, seven_min_ago_dp))
    if (latest_dp > seven_min_ago_dp):
        return True
    else:
        return False

def check_alligator(symbol):
    alligator_status = []
    alligator_status.clear()
    file = ""
    if symbol == "ETH":
        file = '/home/edw2139/discord/bots/txt/ETH/eth_alligator.csv'
    if symbol == "LTC":
        file = '/home/edw2139/discord/bots/txt/LTC/ltc_alligator.csv'
    # Read File
    with open(file, mode='r') as rec:
        reader = csv.reader(rec)        
        for row in reader:
            for i in row:
                alligator_status.append(i)
        rec.close()
    #Check  Status
    if alligator_status[0] == "True":
        return True
    else:
        return False

def check_rsi(symbol):
    rsi_status = []
    rsi_status.clear()
    file = ""
    if symbol == "ETH":
        file = '/home/edw2139/discord/bots/txt/ETH/eth_rsi_status.csv'
    if symbol == "LTC":
        file = '/home/edw2139/discord/bots/txt/LTC/ltc_rsi_status.csv'
    # Read File
    with open(file, mode='r') as rec:
        reader = csv.reader(rec)        
        for row in reader:
            for i in row:
                rsi_status.append(i)
        rec.close()
    #Check Status
    if rsi_status[0] == "True":
        return True
    else:
        return False


##########333333333####### TRIGGERS #########################3#
def trigger_alligator(symbol, trigger):
    file = ""
    if symbol == "ETH":
        file = '/home/edw2139/discord/bots/txt/ETH/eth_alligator.csv'
    if symbol == "LTC":
        file = '/home/edw2139/discord/bots/txt/LTC/ltc_alligator.csv'
    
    if trigger == "True":    
        with open(file, mode='w') as rec:
            field = ["True"]
            writer = csv.writer(rec)
            writer.writerow(field)
            rec.close()
    else:
        with open(file, mode='w') as rec:
            field = ["False"]
            writer = csv.writer(rec)
            writer.writerow(field)
            rec.close()

def trigger_rsi(symbol, trigger):
    file = ""
    if symbol == "ETH":
        file = '/home/edw2139/discord/bots/txt/ETH/eth_rsi_status.csv'
    if symbol == "LTC":
        file = '/home/edw2139/discord/bots/txt/LTC/ltc_rsi_status.csv'
    
    if trigger == "True":    
        with open(file, mode='w') as rec:
            field = ["True"]
            writer = csv.writer(rec)
            writer.writerow(field)
            rec.close()
    else:
        with open(file, mode='w') as rec:
            field = ["False"]
            writer = csv.writer(rec)
            writer.writerow(field)
            rec.close()


####################### Get Percentage #########################
def get_percentage(symbol, current_price, order):   #last sell must be 1.5% higher than new buy
    prev_order_info = []
    prev_order_info.clear()
    
    #Find last items History
    filename = ""
    if symbol == "ETH":
        filename = '/home/edw2139/discord/bots/txt/ETH/eth_rec.csv'
    if symbol == "LTC":
        filename = '/home/edw2139/discord/bots/txt/LTC/ltc_rec.csv'
    with open(filename, mode='r') as rec:
        reader = csv.reader(rec, delimiter=',')        
        for row in reader:
            for i in row:
                prev_order_info.append(i)
        rec.close()
    
    # Calculate Percentage:
    prev_value = float(prev_order_info[2])
    new_value = float(current_price)
    print("Order: {}  Old price: {}  Current Price: {}  ".format(order, prev_value, new_value))
    percentage = (abs(prev_value - new_value) / new_value) * 100
    print("Percentage: ", percentage)
    if ((order == "BUY") and (prev_order_info[1] == "SELL") and (new_value < prev_value)):
        if (percentage > 1.5):
            print("buy percentage of %1 met")
            return True
        else:
            return False
    if ((order == "SELL") and (prev_order_info[1] == "BUY") and (new_value > prev_value)):
        if (percentage > 6):
            print("Sell percentage of %6 met")
            return True
        else:
            return False


############################# ACCOUNT ###############################
def determine_buying_power(account_avaliable, symbol, currency_dict):
    #Buying ETH
    if symbol == "ETH":
        ltc = "Litecoin"
        if ltc in currency_dict:
            return account_avaliable - 10
        else:
            return (account_avaliable / 2) - 10
    #BUYING LTC
    if symbol == "LTC":
        eth = "Ethereum"
        if eth in currency_dict:
            return account_avaliable - 10
        else:
            return (account_avaliable / 2) - 10
    else:
        print("Error in handle_orders.py/determine_buying_price")
        exit

# Check Current crypto Prices
def bot_check_crypto_prices(crypto_symbol):
    login()
    price = r.crypto.get_crypto_quote(crypto_symbol)
    mark_price = (price['mark_price'])
    return mark_price

# Get Full BP
def check_acc_bp():
    login()
    profileData = r.load_account_profile()
    crypto_bp = float(profileData['crypto_buying_power'])
    return crypto_bp


######################### ORDERS #############################
# Check Previous order information
def order_status(symbol, order, created_at):
    filename = ""
    if symbol == "ETH":
        filename = '/home/edw2139/discord/bots/txt/ETH/eth_rec.csv'
    if symbol == "LTC":
        filename = '/home/edw2139/discord/bots/txt/LTC/ltc_rec.csv'
    while True:
        print("checking order status...")
        login()
        orders = r.get_all_crypto_orders()
        if (orders[0]['created_at'] == created_at):
            if (orders[0]['state']) == "filled":
                print("Order Filled!")
                av_price = (float(orders[0]['average_price']))
                date = orders[0]['updated_at']
                with open(filename, mode='w') as rec:
                    field = [symbol, order, av_price, date]
                    writer = csv.writer(rec)
                    writer.writerow(field)
                    rec.close()
                return av_price
            else:
                time.sleep(5)
        else:
            return None

#Buy Crypto
def order_crypto(symbol, amount):
    login()
    quantity = float(amount)
    print("in order crypto")
    order = r.order_buy_crypto_by_price(symbol, quantity, 'ask_price', 'gtc')
    return order['created_at']

# #Sell Crypto
def sell_crypto(symbol, amount):
    login()
    order = r.orders.order_sell_crypto_by_quantity(symbol, amount, 'mark_price', 'gtc')
    return order['created_at']

# Cancel Orders
def cancel():
    login()
    r.orders.cancel_all_crypto_orders()
    print("Orders Cancelled!")


######################## ACCOUNT INFORMATION #######################
#Check Positions
def positions_check():
    login()
    currency_dict = {}
    currency_dict.clear()
    d = r.crypto.get_crypto_positions()
    for i in d:
        quantity = float(i['quantity_available'])
        if (quantity > 0):
            currency_name = i['currency']['name']
            currency_dict[currency_name] = quantity
    return currency_dict

#Login
def login():
    totp = pyotp.TOTP("DKNPSL7Z5DQ4CNFQ").now()
    #new_login(username='ewebb4952@gmail.com', password='@1jN%NQYj9D4TR', expiresIn=86400, scope='internal', by_sms=True, store_session=True, mfa_code=totp)
    "now here"
    r.login('ewebb4952@gmail.com','@1jN%NQYj9D4TR', mfa_code=totp)
    return 1



############################################################################################################
def generate_device_token():
    """This function will generate a token used when loggin on.

    :returns: A string representing the token.

    """
    rands = []
    for i in range(0, 16):
        r = random.random()
        rand = 4294967296.0 * r
        rands.append((int(rand) >> ((3 & i) << 3)) & 255)

    hexa = []
    for i in range(0, 256):
        hexa.append(str(hex(i+256)).lstrip("0x").rstrip("L")[1:])

    id = ""
    for i in range(0, 16):
        id += hexa[rands[i]]

        if (i == 3) or (i == 5) or (i == 7) or (i == 9):
            id += "-"

    return(id)


def respond_to_challenge(challenge_id, sms_code):
    """This function will post to the challenge url.

    :param challenge_id: The challenge id.
    :type challenge_id: str
    :param sms_code: The sms code.
    :type sms_code: str
    :returns:  The response from requests.

    """
    url = urls.challenge_url(challenge_id)
    payload = {
        'response': sms_code
    }
    return(helper.request_post(url, payload))


def new_login(username=None, password=None, expiresIn=86400, scope='internal', by_sms=False, store_session=True, mfa_code=None):
    """This function will effectively log the user into robinhood by getting an
    authentication token and saving it to the session header. By default, it
    will store the authentication token in a pickle file and load that value
    on subsequent logins.

    :param username: The username for your robinhood account, usually your email.
        Not required if credentials are already cached and valid.
    :type username: Optional[str]
    :param password: The password for your robinhood account. Not required if
        credentials are already cached and valid.
    :type password: Optional[str]
    :param expiresIn: The time until your login session expires. This is in seconds.
    :type expiresIn: Optional[int]
    :param scope: Specifies the scope of the authentication.
    :type scope: Optional[str]
    :param by_sms: Specifies whether to send an email(False) or an sms(True)
    :type by_sms: Optional[boolean]
    :param store_session: Specifies whether to save the log in authorization
        for future log ins.
    :type store_session: Optional[boolean]
    :param mfa_code: MFA token if enabled.
    :type mfa_code: Optional[str]
    :returns:  A dictionary with log in information. The 'access_token' keyword contains the access token, and the 'detail' keyword \
    contains information on whether the access token was generated or loaded from pickle file.

    """
    device_token = generate_device_token()
    home_dir = os.path.expanduser("~")
    data_dir = os.path.join(home_dir, ".tokens")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    creds_file = "robinhood.pickle"
    pickle_path = os.path.join(data_dir, creds_file)
    # Challenge type is used if not logging in with two-factor authentication.
    if by_sms:
        challenge_type = "sms"
    else:
        challenge_type = "email"

    url = urls.login_url()
    payload = {
        'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
        'expires_in': expiresIn,
        'grant_type': 'password',
        'password': password,
        'scope': scope,
        'username': username,
        'challenge_type': challenge_type,
        'device_token': device_token
    }

    if mfa_code:
        payload['mfa_code'] = mfa_code

    # If authentication has been stored in pickle file then load it. Stops login server from being pinged so much.
    if os.path.isfile(pickle_path):
        # If store_session has been set to false then delete the pickle file, otherwise try to load it.
        # Loading pickle file will fail if the acess_token has expired.
        if store_session:
            try:
                with open(pickle_path, 'rb') as f:
                    pickle_data = pickle.load(f)
                    access_token = pickle_data['access_token']
                    token_type = pickle_data['token_type']
                    refresh_token = pickle_data['refresh_token']
                    # Set device_token to be the original device token when first logged in.
                    pickle_device_token = pickle_data['device_token']
                    payload['device_token'] = pickle_device_token
                    # Set login status to True in order to try and get account info.
                    helper.set_login_state(True)
                    helper.update_session(
                        'Authorization', '{0} {1}'.format(token_type, access_token))
                    # Try to load account profile to check that authorization token is still valid.
                    res = helper.request_get(
                        urls.portfolio_profile(), 'regular', payload, jsonify_data=False)
                    # Raises exception is response code is not 200.
                    res.raise_for_status()
                    return({'access_token': access_token, 'token_type': token_type,
                            'expires_in': expiresIn, 'scope': scope, 'detail': 'logged in using authentication in {0}'.format(creds_file),
                            'backup_code': None, 'refresh_token': refresh_token})
            except:
                print(
                    "ERROR: There was an issue loading pickle file. Authentication may be expired - logging in normally.", file=helper.get_output())
                helper.set_login_state(False)
                helper.update_session('Authorization', None)
        else:
            os.remove(pickle_path)

    # Try to log in normally.
    if not username:
        username = input("Robinhood username: ")
        payload['username'] = username

    if not password:
        password = getpass.getpass("Robinhood password: ")
        payload['password'] = password

    data = helper.request_post(url, payload)
    # Handle case where mfa or challenge is required.
    if data:
        if 'mfa_required' in data:
            mfa_token = input("Please type in the MFA code: ")
            payload['mfa_code'] = mfa_token
            res = helper.request_post(url, payload, jsonify_data=False)
            while (res.status_code != 200):
                mfa_token = input(
                    "That MFA code was not correct. Please type in another MFA code: ")
                payload['mfa_code'] = mfa_token
                res = helper.request_post(url, payload, jsonify_data=False)
            data = res.json()
        elif 'challenge' in data:
            challenge_id = data['challenge']['id']
            sms_code = input('Enter Robinhood code for validation: ')
            res = respond_to_challenge(challenge_id, sms_code)
            while 'challenge' in res and res['challenge']['remaining_attempts'] > 0:
                sms_code = input('That code was not correct. {0} tries remaining. Please type in another code: '.format(
                    res['challenge']['remaining_attempts']))
                res = respond_to_challenge(challenge_id, sms_code)
            helper.update_session(
                'X-ROBINHOOD-CHALLENGE-RESPONSE-ID', challenge_id)
            data = helper.request_post(url, payload)
        # Update Session data with authorization or raise exception with the information present in data.
        if 'access_token' in data:
            token = '{0} {1}'.format(data['token_type'], data['access_token'])
            helper.update_session('Authorization', token)
            helper.set_login_state(True)
            data['detail'] = "logged in with brand new authentication code."
            if store_session:
                with open(pickle_path, 'wb') as f:
                    pickle.dump({'token_type': data['token_type'],
                                 'access_token': data['access_token'],
                                 'refresh_token': data['refresh_token'],
                                 'device_token': device_token}, f)
        else:
            raise Exception(data['detail'])
    else:
        raise Exception('Error: Trouble connecting to robinhood API. Check internet connection.')
    return(data)

@helper.login_required
def logout():
    """Removes authorization from the session header.

    :returns: None

    """
    helper.set_login_state(False)
    helper.update_session('Authorization', None)