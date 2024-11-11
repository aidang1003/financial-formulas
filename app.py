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
        if arrData['annuityType'] == 0:
            arrData['annuityType'] = 1
        self.annuityType = arrData['annuityType']
        self.periodicPayment = arrData['periodicPayment']
        self.ratePerPeriod = arrData['ratePerPeriod']
        self.periods = arrData['periods']     

    def annuity(self):
        if self.annuityType == -1:
            return round(self.periodicPayment * ((((1+self.ratePerPeriod) ** self.periods) - 1) / self.ratePerPeriod) , 2)
        elif self.annuityType == 1:
            return round(self.periodicPayment * ((1-(1+self.ratePerPeriod) ** (-1 * self.periods)) / self.ratePerPeriod) , 2)
        else:
            return "Error in annuity function. Likely there was not a correct annuity type supplied"



@app.route('/annuity', methods=["GET","POST"])
def processAnnuity():
    if request.method == "GET":
        if session['annuityType'] and session['periodicPayment'] and session['ratePerPeriod'] and session['periods']:
            pass
        else:
            session['annuityType'] = 1
            session['periodicPayment'] = 1000
            session['ratePerPeriod'] = .02
            session['periods'] = 5



    if request.method == "POST":
        form = request.form
        session['annuityType'] = float(form['fAnnuityType'])
        session['periodicPayment'] = float(form['fPeriodicPayment'])
        session['ratePerPeriod'] = float(form['fRatePerPeriod'])
        session['periods'] = float(form['fPeriods'])

        annuity = Annuity(session)
        
        session['annuity'] = annuity.annuity()

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
        if session["faceValue"] and session["purchasePrice"] and session["daysToMaturity"]:
            pass
        else:
            session["faceValue"] = 1000
            session["purchasePrice"] = 980
            session["daysToMaturity"] = 60

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
        if session['pMinimumPrice'] and session['pMaximumPrice'] and session['pUsdHoldings'] and session['pEthHoldings'] and session['pstEthHoldings'] and session['prEthHoldings'] and session['pswEthHoldings']:
            pass
        else:
            session['pMinimumPrice'] = 0
            session['pMaximumPrice'] = 12500
            session['pUsdHoldings'] = 1000
            session['pEthHoldings'] = 10
            session['pstEthHoldings'] = 10
            session['prEthHoldings'] = 10
            session['pswEthHoldings'] = 10

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

        if 1==0: #Used for debugging, comment this out for the page to run normally
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