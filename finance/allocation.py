from flask import Blueprint, Flask, render_template, url_for, session, request
from liveprice import PriceData
from dotenv import load_dotenv
import os
    
allocation_bp = Blueprint("allocation", __name__)

@allocation_bp.route('/allocation', methods=["GET","POST"])
def allocation():
    if request.method == "GET":
        if 'pMinimumPrice' not in session:
            session["pMinimumPrice"] = request.args.get('pMinimumPrice', default=0, type=float)
        if 'pMaximumPrice' not in session:
            session["pMaximumPrice"] = request.args.get('pMaximumPrice', default=12500, type=float)
        if 'pUsdHoldings' not in session:
            session["pUsdHoldings"] = request.args.get('pUsdHoldings', default=10000, type=float)
        if 'pEthHoldings' not in session:
            session["pEthHoldings"] = request.args.get('pEthHoldings', default=10, type=float)
        if 'pstEthHoldings' not in session:
            session["pstEthHoldings"] = request.args.get('pstEthHoldings', default=10, type=float)
        if 'prEthHoldings' not in session:
            session["prEthHoldings"] = request.args.get('prEthHoldings', default=10, type=float)
        if 'pswEthHoldings' not in session:
            session["pswEthHoldings"] = request.args.get('pswEthHoldings', default=10, type=float)


    if request.method == "POST":
        form = request.form
        session['pMinimumPrice'] = float(form['fMinimumPrice'])
        session['pMaximumPrice'] = float(form['fMaximumPrice'])
        # USD holdings
        session['pUsdHoldings'] = float(form['fUsdHoldings'])
        # Eth holdings
        session['pEthHoldings'] = float(form['fEthHoldings'])
        session['pstEthHoldings'] = float(form['fstEthHoldings'])
        session['prEthHoldings'] = float(form['frEthHoldings'])
        session['pswEthHoldings'] = float(form['fswEthHoldings'])

        if 1==1: #Used for debugging, comment this out for the page to run normally
            session['pUsdHoldings'] = float(os.getenv('COINBASE_USD_HOLDINGS')) + float(os.getenv('GMX_USD_HOLDINGS'))
            session['pEthHoldings'] = float(os.getenv('ETH_HOLDINGS')) + float(os.getenv('GMX_WETH_HOLDINGS'))
            session['pstEthHoldings'] = float(os.getenv('STETH_HOLDINGS'))
            session['prEthHoldings'] = float(os.getenv('RETH_HOLDINGS'))
            session['pswEthHoldings'] = float(os.getenv('SWETH_HOLDINGS'))

        # Create Allocation object
        allocation = Allocation(session)
        
        # Set total eth holdings
        session['totalEthHoldingsInEth'] = allocation.getEthHoldingsInEth()
        
        # Set desired and current allocation percentages
        session['currentPerUsdAllocation'] = allocation.currentPerUsdAllocation()
        session['currentEthAllocation'] = allocation.currentEthAllocation()
        session['desiredUsdAllocation'] = allocation.desiredUsdAllocation()
        session['desiredEthAllocation'] = allocation.desiredEthAllocation()

        # Amount to convert
        session['transferAmount'] = allocation.transferAmount()
    
    return render_template('allocation.html', session=session)


class Allocation():
    def __init__(self, session, factor=2):
        # Eth min and max anticipated range
        self.minimumPrice = session['pMinimumPrice']
        self.maximumPrice = session['pMaximumPrice']

        # Return Eth price data from Coin Marketcap
        priceData = PriceData()
        priceData.getPrice()
        self.ethPrice = priceData.getEthPrice()
        self.stEthPrice = priceData.getStEthPrice()
        self.rEthPrice = priceData.getREthPrice()
        self.swEthPrice = priceData.getSwEthPrice()

        # Calculations
        self.ethHoldings = session['pEthHoldings'] * self.ethPrice
        self.stEthHoldings = session['pstEthHoldings'] * self.stEthPrice
        self.rEthHoldings = session['prEthHoldings'] * self.rEthPrice
        self.swEthHoldings = session['pswEthHoldings'] * self.swEthPrice
        self.totalEthHoldingsInUsd = self.ethHoldings + self.stEthHoldings + self.rEthHoldings +  self.swEthHoldings
        self.usdHoldings = session['pUsdHoldings']
        self.factor = factor


    def formattingValue(self):
        # Calculates an "a" value so each input returns an output in percentage
        # adding in x and y offset values later
        return 1 / (self.maximumPrice ** self.factor)
                    
    def currentPerUsdAllocation(self):
        self.currentPerUsdAllocation = (self.usdHoldings / (self.totalEthHoldingsInUsd + self.usdHoldings))
        result = 100 * self.currentPerUsdAllocation
        return round(result,3)

    def currentEthAllocation(self):
        self.currentEthAllocationPercentage  = (self.totalEthHoldingsInUsd / (self.totalEthHoldingsInUsd + self.usdHoldings))
        result = 100 * self.currentEthAllocationPercentage
        return round(result,3)
    
    def desiredUsdAllocation(self):
        a = self.formattingValue()
        self.desiredUsdAllocation = a * (self.ethPrice ** self.factor) #self.eth price needs to become a weighted average?
        result = 100 * self.desiredUsdAllocation
        return round(result,3)
    
    def desiredEthAllocation(self):
        self.desiredEthAllocation = 1 - self.desiredUsdAllocation
        result = 100 * self.desiredEthAllocation
        return round(result,3)
    
    def getEthHoldingsInEth(self):
        return round(self.totalEthHoldingsInUsd / self.ethPrice, 4)
    
    def transferAmount(self):
        difference = self.currentPerUsdAllocation - self.desiredUsdAllocation
        differenceInUsd = difference * (self.totalEthHoldingsInUsd + self.usdHoldings)
        return abs(round(differenceInUsd,2))
