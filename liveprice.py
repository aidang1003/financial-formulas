from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import os

class PriceData():
    def __init__(self):
        self.data = "No Data Yet"
        self.chainIds = '1027,8085,15060,25147'
        self.ethPrice = 0
        self.stEthPrice = 0
        self.rEthPrice = 0
        self.swEthPrice = 0

    def __repr__(self):
        return (f'Eth Price >> {self.ethPrice}\n'
                f'stEth Price >> {self.stEthPrice}\n'
                f'rEth Price >> {self.rEthPrice}\n'
                f'swEth Price >> {self.swEthPrice}\n'
                f'data >> {self.data}'
        )

    def retrieve(self):
        # Load .env variables
        load_dotenv()


        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        parameters = {
            'id': self.chainIds, # All IDs od cryptos to update price on
            'aux': "is_fiat",
            'convert': "USD"
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': os.getenv('COIN_MARKETCAP_API_KEY'),
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            self.data = data

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def getPrice(self):
        self.retrieve()
        self.ethPrice = self.data['data']['1027']['quote']['USD']['price']
        self.stEthPrice = self.data['data']['8085']['quote']['USD']['price']
        self.rEthPrice = self.data['data']['15060']['quote']['USD']['price']
        self.swEthPrice = self.data['data']['25147']['quote']['USD']['price']
        return
    
    def getEthPrice(self):
        return self.ethPrice
    
    def getStEthPrice(self):
        return self.stEthPrice
    
    def getREthPrice(self):
        return self.rEthPrice
    
    def getSwEthPrice(self):
        return self.swEthPrice