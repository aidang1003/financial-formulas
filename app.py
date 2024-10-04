from flask import Flask, session
from flask import render_template, request, redirect
from liveprice import PriceData

app = Flask(__name__)

class Finance():
    def __init__(self, annuityType, periodicPayment, ratePerPeriod, periods):
        self.annuityType = annuityType
        self.periodicPayment = periodicPayment
        self.ratePerPeriod = ratePerPeriod
        self.periods = periods        

    def annuity(self):
        if self.annuityType == "fvAnnuity":
            return f'${round(self.periodicPayment * ((((1+self.ratePerPeriod) ** self.periods) - 1) / self.ratePerPeriod) , 2)}'
        elif self.annuityType == "pvAnnuity":
            return f'${round(self.periodicPayment * ((1-(1+self.ratePerPeriod) ** (-1 * self.periods)) / self.ratePerPeriod) , 2)}'
        else:
            return "Error in annuity function. Likely there was not a correct annuity type supplied"

class Bond():
    def __init__(self, faceValue, purchasePrice, yearsToMaturity, rateOfYield=.07):
        self.faceValue = faceValue
        self.purchasePrice = purchasePrice
        self.yearsToMaturity = yearsToMaturity
        self.rateOfYield = rateOfYield


    def bondEquivalentYield(self):
        return f'{round(100 * ((self.faceValue - self.purchasePrice) / self.purchasePrice) * (1 / self.yearsToMaturity), 4)}%'
    
class Allocation():
        def __init__(self, minimumPrice, maximumPrice, ethAmount, stEthAmount, rEthAmount, swEthAmount, usdHoldings, factor=2):
            # Eth min and max anticipated range
            self.minimumPrice = minimumPrice
            self.maximumPrice = maximumPrice

            # Return Eth price data from Coin Marketcap
            priceData = PriceData()
            priceData.getPrice()
            self.ethPrice = priceData.getEthPrice()
            self.stEthPrice = priceData.getStEthPrice()
            self.rEthPrice = priceData.getREthPrice()
            self.swEthPrice = priceData.getSwEthPrice()

            # Calculations
            self.ethHoldings = ethAmount * self.ethPrice
            self.stEthHoldings = stEthAmount * self.stEthPrice
            self.rEthHoldings = rEthAmount * self.rEthPrice
            self.swEthHoldings = swEthAmount * self.swEthPrice
            self.totalEthHoldingsInUsd = self.ethHoldings + self.stEthHoldings + self.rEthHoldings +  self.swEthHoldings
            self.usdHoldings = usdHoldings
            self.factor = factor


        def formattingValue(self):
            # Calculates an "a" value so each input returns an output in percentage
            # adding in x and y offset values later
            return 1 / (self.maximumPrice ** self.factor)
        
        def usdAllocation(self):
            a = self.formattingValue()
            self.usdAllocationPercentage = a * (self.ethPrice ** self.factor) #self.eth price needs to become a weighted average?
            result = 100 * self.usdAllocationPercentage
            return f'{round(result,3)}%'
        
        def ethAllocation(self):
            self.ethAllocationPercentage = 1 - self.usdAllocationPercentage
            reuslt = 100 * self.ethAllocationPercentage
            return f'{round(reuslt,3)}%'
                        
        def currentUsdAllocation(self):
            self.currentUsdAllocationPercentage = (self.usdHoldings / (self.totalEthHoldingsInUsd + self.usdHoldings))
            result = 100 * self.currentUsdAllocationPercentage
            return f'{round(result,3)}%'

        def currentEthAllocation(self):
            self.currentEthAllocationPercentage  = (self.totalEthHoldingsInUsd / (self.totalEthHoldingsInUsd + self.usdHoldings))
            result = 100 * self.currentEthAllocationPercentage
            return f'{round(result ,3)}%'
        
        def getEthHoldingsInEth(self):
            return self.totalEthHoldingsInUsd / self.ethPrice
        
        def transferAmount(self):
            difference = self.currentUsdAllocationPercentage - self.usdAllocationPercentage
            differenceInUsd = difference * (self.totalEthHoldingsInUsd + self.usdHoldings)
            return f'${round(abs(differenceInUsd),2)}'



@app.route('/')
def index():
    return render_template('index.html', pageTitle='Homepage')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/annuity')
def annuity():
    return render_template('annuity.html')

@app.route('/bond')
def bond():
    session["pFaceValue"] = 1000
    return render_template('bond.html', UserInput=UserInput)

@app.route('/allocation')
def allocation():
    return render_template('allocation.html')

@app.route('/allocation', methods=["GET","POST"])
def allocationPercentage():
    
    if request.method == "POST":
        form = request.form
        pMinimumPrice = float(form['fMinimumPrice'])
        pMaximumPrice = float(form['fMaximumPrice'])
        # USD holdings
        pUsdHoldings = float(form['fUsdHoldings'])
        # Eth holdings
        pEthHoldings = float(form['fEthHoldings'])
        pstEthHoldings = float(form['fstEthHoldings'])
        prEthHoldings = float(form['frEthHoldings'])
        pswEthHoldings = float(form['fswEthHoldings'])


        allocation = Allocation(pMinimumPrice,pMaximumPrice,pEthHoldings,pstEthHoldings,prEthHoldings,pswEthHoldings,pUsdHoldings)
        
        totalEthHoldingsInEth = allocation.getEthHoldingsInEth()
        
        usdAllocation = allocation.usdAllocation()
        ethAllocation = allocation.ethAllocation()
        currentUsdAllocation = allocation.currentUsdAllocation()
        currentEthAllocation = allocation.currentEthAllocation()

        transferAmount = allocation.transferAmount()

        #session['fUserInput'] = {'pMinimumPrice' : pMinimumPrice}

        return render_template('allocation.html',totalEthHoldingsInEth=totalEthHoldingsInEth,
            usdAllocation=usdAllocation, ethAllocation=ethAllocation,currentEthAllocation=currentEthAllocation,
            currentUsdAllocation=currentUsdAllocation, transferAmount=transferAmount)
    
    #session['fUserInput'] = {'pMinimumPrice' : pMinimumPrice}
    return render_template('allocation.html')

@app.route('/annuity', methods=["GET","POST"])
def processAnnuity():
    
    if request.method == "POST":
        form = request.form
        pAnnuity = form['annuity_type']
        pPeriodicPayment = float(form['fPeriodicPayment'])
        pRatePerPeriod = float(form['fRatePerPeriod'])
        pPeriods = float(form['fPeriods'])

        finance = Finance(pAnnuity, pPeriodicPayment, pRatePerPeriod, pPeriods)
        
        annuity = finance.annuity()

        return render_template('annuity.html', annuity=annuity)

    return render_template('annuity.html')

@app.route('/bond', methods=["GET","POST"])
def bondEquivalentYield():
    if request.method == "POST":
        form = request.form
        pFaceValue = float(form['fFaceValue'])
        pPurchasePrice = float(form['fPurchasePrice'])
        pYeastoMaturity = float(form['fDaystoMaturity']) / 365

        bond = Bond(pFaceValue, pPurchasePrice, pYeastoMaturity)
        
        bondEquivalentYield = bond.bondEquivalentYield()
        session['bondEquivalentYield'] = bondEquivalentYield

        return render_template('bond.html', bondEquivalentYield=bondEquivalentYield, session=session)

    

    return render_template('bond.html', session=session)

if __name__ == '__main__':
    app.run(debug=True)