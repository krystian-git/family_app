## Family Organizer 
Family Organizer is a Flask app project that supports organizing day to day family members tasks.
Also calculates cost of renovating/finishing home. Compares prices in different shops, scrapps top movies of the day from www.filmweb.pl to recommend watching and checking Bitcoin price.

___
##### Why?
App was written to help me out organizing tasks for family. 
As we renovating house I wanted to track cost of it and compare prices.
I wanted to request filmweb API to get top movies, but there's NO such a thing. So decided to scrape few (you can set how many) movies of the day and display for us.
___

![](./family_app/family/static/movie_app_screenshot.png?raw=true)

Every user can have Admin, Parent or Child role, which allows/deny him to access some data.

![](./family_web_app/family/static/settings_app_screenshot.png)

You can also check pln to other top currencies rate (thanks NBP API) and Bitcoin price (thanks coindesk.com).

```python
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
        return None
    
    return pln_rate
```
___
#### Requirements:
python >= 3.6
other dependencies in  requirements.txt
___
#### How to run
You need to create .env file in main directory and put in it:

```
SECRET_KEY="Your secret key"
SQLALCHEMY_DATABASE_URI="sqlite:///your_sqlite_db_file_name.db"
```
And then pip install requirements (which is added -requirements.txt) and run in bash ( in directory where run.py file is):
```
export FLASK_APP=run.py
flask run
```
App will create default ( initial ) ADMIN user account with Admin rights, password: ADMIN and admin@admin.com email. After loging in the first time ,first step you should take is to register a new user and give it an Admin rights - then (for your safety) delete ADMIN default account and relogin.

##### Author & homepage
Krystian Polowy
www.bitbucket.com/dfkdfdfd

##### License
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
