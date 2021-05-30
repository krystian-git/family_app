from typing import Dict
import requests
import json


BITCOIN_CURRIENCES = ['USD', 'EUR', 'GBP']  # Bitcoin currencies to display 
PLN_CURRIENCES = ['USD', 'EUR', 'GBP', 'CHF'] # Currencies for ratio to pln


def bitcoin() -> Dict:
    """ Getting bitcoin exchange """
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json' # API endpoint for bitcoin price
    try:
        r = requests.get(url)
        jsonfile = r.text
        bitcoin = json.loads(jsonfile)
        currencies_dict = {} # Dict container for country code : bitcoin price
        for currency in BITCOIN_CURRIENCES:
            bitcoin_name, bitcoin_rate = bitcoin['bpi'][currency]['code'], bitcoin['bpi'][currency]['rate']
            currencies_dict[bitcoin_name] = bitcoin_rate[:-2]
    except:
        return None
    
    return currencies_dict


def pln() -> Dict:
    """  Getting exchange pln ratio """
    url = 'http://api.nbp.pl/api/exchangerates/tables/A/' # NBP api endpoint - exchange rates pln/...
    pln_rate = {} # Dict container for country code : pln value
    try:
        r = requests.get(url)
        jsonfile = r.text
        currency = json.loads(jsonfile)
        for i in currency[0]['rates']:
            if i['code'] in PLN_CURRIENCES:
                pln_rate[i['code']] = round(i['mid'], 3)
    except:
        # assign 0's to ratio if something's wrong with NBP database
        return None
    
    return pln_rate