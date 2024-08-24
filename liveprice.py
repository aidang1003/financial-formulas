from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import os

class PriceData():
    def __init__(self):
        self.data = "No Data Yet"

    def __repr__(self):
        return f'Data >> {self.data}'


    def retrieve(self):
        # Load .env variables
        load_dotenv()


        url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start':'1',
            'limit':'5000',
            'convert':'USD'
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

    def getData(self):
        return self.data
    


priceData = PriceData()
print(priceData)
priceData.retrieve()
print(priceData)

  