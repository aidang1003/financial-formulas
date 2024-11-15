from flask import Flask, session
from flask import render_template, request, redirect
from liveprice import PriceData
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY') #set a secret key to use for session instance

@app.route('/')
def index():
    return render_template('index.html', pageTitle='Homepage', session=session)

@app.route('/index')
def home():
    return render_template('index.html', session=session)


class Annuity():
    def __init__(self, arrData):
        if arrData['annuityType'] == '':
            arrData['annuityType'] = 'PV'
        self.annuityType = arrData['annuityType']
        self.periodicPayment = arrData['periodicPayment']
        self.ratePerPeriod = arrData['ratePerPeriod']
        self.periods = arrData['periods']     

    def fvOrPvOfAnnuity(self):
        if self.annuityType == 'FV': # Calculates the Future Value of an annuity
            return round(self.periodicPayment * ((((1+self.ratePerPeriod) ** self.periods) - 1) / self.ratePerPeriod) , 2)
        elif self.annuityType == 'PV': # Calculatesthe Present Value of an annuity
            return round(self.periodicPayment * ((1-(1+self.ratePerPeriod) ** (-1 * self.periods)) / self.ratePerPeriod) , 2)
        else:
            return "Error in annuity function. Likely there was not a correct annuity type supplied"



@app.route('/annuity', methods=["GET","POST"])
def annuity():
    if request.method == "GET":
        if 'annuityType' not in session:
            session["annuityType"] = request.args.get('annuityType', default='PV')
        if 'periodicPayment' not in session:
            session["periodicPayment"] = request.args.get('periodicPayment', default=1000, type=float)
        if 'ratePerPeriod' not in session:
            session["ratePerPeriod"] = request.args.get('ratePerPeriod', default=.02, type=float)
        if 'periods' not in session:
            session["periods"] = request.args.get('periods', default=5, type=float)

    if request.method == "POST":
        form = request.form
        session['annuityType'] = form['AnnuityType']
        session['periodicPayment'] = 1000#float(form['PeriodicPayment'])
        session['ratePerPeriod'] = float(form['RatePerPeriod'])
        session['periods'] = float(form['Periods'])

        annuity = Annuity(session)
        
        session['annuity'] = annuity.fvOrPvOfAnnuity()

    return render_template('annuity.html', session=session)

class Bond():
    def __init__(self, arrData, rateOfYield=.07):
        self.faceValue = arrData['faceValue']
        self.purchasePrice = arrData['purchasePrice']
        self.yearsToMaturity = arrData['yearsToMaturity']
        self.rateOfYield = rateOfYield


    def bondEquivalentYield(self):
        return f'{round(100 * ((self.faceValue - self.purchasePrice) / self.purchasePrice) * (1 / self.yearsToMaturity), 4)}%'
    

@app.route('/bond', methods=["GET","POST"])
def bond():
    if request.method =='GET':
        if 'faceValue' not in session:
            session["faceValue"] = request.args.get('faceValue', default=1000, type=float)
        if 'purchasePrice' not in session:
            session["purchasePrice"] = request.args.get('purchasePrice', default=980, type=float)
        if 'daysToMaturity' not in session:
            session["daysToMaturity"] = request.args.get('daysToMaturity', default=60, type=float)



    if request.method == "POST":
        form = request.form
        session["faceValue"] = float(form['FaceValue'])
        session["purchasePrice"] = float(form['PurchasePrice'])
        session["daysToMaturity"] = float(form['DaysToMaturity'])

        session["yearsToMaturity"] = session["daysToMaturity"] / 365

        bond = Bond(session) # Feed in the session variable instead of each individual variable
         
        session['bondEquivalentYield'] = bond.bondEquivalentYield()

    return render_template('bond.html', session=session)
    
class Allocation():
        #def __init__(self, minimumPrice, maximumPrice, ethAmount, stEthAmount, rEthAmount, swEthAmount, usdHoldings, factor=2):
        def __init__(self, arrData, factor=2):
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

@app.route('/allocation', methods=["GET","POST"])
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

if __name__ == '__main__':
    load_dotenv(override=True)
    app.run(debug=True)