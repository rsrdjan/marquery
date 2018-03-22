#!/usr/bin/env python3

# marquery - CLI tool for accessing latest financial market info
# Copyright (C) 2018 Srdjan Rajcevic [srdjan[@]rajcevic.net]

# Uses free AlphaVantage Inc. API [www.alphavantage.co]
# Author does not guarantee for accuracy of data. Use at your own risk.

import argparse
import requests
import sys
from decimal import Decimal

# URL & API KEY - Change URL if necessary, enter your own API key

url = "https://www.alphavantage.co/query"
apikey = ""

# Functions 

def dump_file(out,dump):
    filename = str(dump[0])
    try:
        f = open(filename,"w")
        f.write(str(out))
        f.close()
    except Exception as e:
        print("Error: {}.".format(e))

def get_url(url,urlparams):
    try:
        req = requests.get(url, params=urlparams)
        out = req.json()
        return out
    except requests.exceptions.BaseHTTPError as e:
        print(e)
        sys.exit()

def handle_stock(url,apikey,symbol,interval,dump):
    function = "TIME_SERIES_INTRADAY"
    if interval == None:
        interval = "1min"
    else:
        interval = interval + "min"
    outputsize = "compact"
    datatype = "json"
    urlparams = {'function' : function, 'symbol' : symbol, 'interval' : interval, 'outputsize' : outputsize, 'datatype' : datatype, 'apikey' : apikey}

    out = get_url(url,urlparams)

    if dump != None:
        dump_file(out,dump)
        sys.exit()
    else:
        try:
            meta = out['Meta Data']
            ts_key = "Time Series (" + interval + ")"
            ts_data = out[ts_key]
            last_data = ts_data[next(iter(ts_data))]
        except Exception as e:
            print("Error: {}. Try again later.".format(e))
            sys.exit()

        info = meta['1. Information']
        symb = meta['2. Symbol']
        time = meta['3. Last Refreshed']

        ls_open = last_data['1. open']
        ls_high = last_data['2. high']
        ls_low = last_data['3. low']
        ls_close = last_data['4. close']
        ls_volume = last_data['5. volume']


        print("\n{}".format(info))
        print("======================================")
        print("Company exchange symbol: {}".format(symb.upper()))
        print("Time: {}\n".format(time))
        print("Stock value (USD):")
        print("======================================")
        print("Open: {} | High: {} | Low: {} | Close: {} | Volume: {}\n".format(ls_open,ls_high,ls_low,ls_close,ls_volume))

def handle_crypto(url,apikey,symbol,market,dump):
    function = "DIGITAL_CURRENCY_INTRADAY"
    if market == None:
        market = "EUR"
    datatype = "json"

    urlparams = {'function' : function, 'symbol' : symbol, 'market' : market, 'datatype' : datatype, 'apikey' : apikey}

    out = get_url(url,urlparams)

    if dump != None:
        dump_file(out,dump)
        sys.exit()
    else:
        try:
            meta = out['Meta Data']
            information = meta['1. Information']
            dc_code = meta['2. Digital Currency Code']
            dc_name = meta['3. Digital Currency Name']
            m_code = meta['4. Market Code']
            m_name = meta['5. Market Name']
            time = meta['7. Last Refreshed']
            time_zone = meta['8. Time Zone']
        except Exception as e:
            print("Error: {}.Try again later.".format(e))
            sys.exit()

        dc_data = out['Time Series (Digital Currency Intraday)']
        
        last_data = dc_data[next(iter(dc_data))]
        p_market = "1a. price (" + market.upper() + ")"
        price_in_market = last_data[p_market]
        price_in_usd = last_data['1b. price (USD)']
        volume = last_data['2. volume']
        market_cap = last_data['3. market cap (USD)']

        print("\n{}".format(information))
        print("======================================")
        print("Digital currency code: {}, ({})".format(dc_code,dc_name))
        print("Market code: {}, ({})".format(m_code,m_name))
        print("Time: {} | Time zone: {}\n".format(time,time_zone))
        print("Digital currency value:")
        print("======================================")
        print("Price in " + market.upper() + ": {} | Price in USD: {} | Volume: {} | Market cap (USD): {}\n".format(price_in_market,price_in_usd,volume,market_cap))

def handle_fx(url,apikey,currencies,dump):
    function = "CURRENCY_EXCHANGE_RATE"
    from_currency = currencies[0]
    to_currency = currencies[1]

    urlparams = {'function' : function, 'from_currency' : from_currency, 'to_currency' : to_currency, 'apikey' : apikey}

    out = get_url(url,urlparams)

    if dump != None:
        dump_file(out,dump)
        sys.exit()
    else:
        try:
            info = out['Realtime Currency Exchange Rate']
            from_c = info['1. From_Currency Code']
            to_c = info['3. To_Currency Code']
            ex_rate = info['5. Exchange Rate']
        except Exception as e:
            print("Error: {}.Try again later.".format(e))
            sys.exit()

        print("\n1 {} = {} {}.\n".format(from_c.upper(),ex_rate,to_c.upper()))

# Argument parser

parser = argparse.ArgumentParser(description="CLI tool for accessing latest financial market info")
group = parser.add_mutually_exclusive_group()

group.add_argument("-s","--stock", help="Stock exchange symbol", type=str)
group.add_argument("-c","--crypto",help="Cryptocurrency symbol", type=str)
group.add_argument("-f","--fx",help="Exchange rate FROM currency TO currency",nargs=2,type=str)
parser.add_argument("-m", "--market", help="Choose market (default: EUR)", type=str)
parser.add_argument("-i", "--interval", help="Show data from specific time interval (in minutes)", type=str)
parser.add_argument("-d", "--dump", help="Dump query result in JSON format into DUMP file", nargs=1)

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_usage()
    sys.exit()
if args.stock != None:
    handle_stock(url,apikey,args.stock,args.interval,args.dump)
elif args.crypto != None:
    handle_crypto(url,apikey,args.crypto,args.market,args.dump)
elif args.fx != None:
    handle_fx(url,apikey,args.fx,args.dump)

    

