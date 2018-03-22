# marquery
CLI tool for accessing latest financial market info
Very simple, yet handy. If you ever wanted to quickly check current stock price(s), or value of crypto currency, or you want to get latest foreign exchange rate, marquery is for you.

usage: marquery.py [-h] [-s STOCK | -c CRYPTO | -f FX FX] [-m MARKET]
                   [-i INTERVAL] [-d DUMP]

CLI tool for accessing latest financial market info

optional arguments:

  -h, --help            show this help message and exit
  
  -s STOCK, --stock       STOCK Stock exchange symbol
                        
  -c CRYPTO, --crypto     CRYPTO Cryptocurrency symbol
                        
  -f FX FX, --fx FX FX    Exchange rate FROM currency TO currency
  
  -m MARKET, --market     MARKET Choose market (default: EUR)
                        
  -i INTERVAL, --interval INTERVAL Show data from specific time interval (in minutes)
                        
  -d DUMP, --dump DUMP    Dump query result in JSON format into DUMP file
