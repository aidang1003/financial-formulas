from flask import Flask
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
        def __init__(self, minimumPrice, maximumPrice, ethHoldings, usdHoldings, factor=2):
            self.minimumPrice = minimumPrice
            self.maximumPrice = maximumPrice
            self.ethPrice = 2100
            self.ethHoldings = ethHoldings * self.ethPrice
            self.usdHoldings = usdHoldings
            self.factor = factor


        def formattingValue(self):
            # Calculates an "a" value so each input returns an output in percentage
            # adding in x and y offset values later
            return 1 / (self.maximumPrice ** self.factor)
        
        def usdAllocation(self):
            a = self.formattingValue()
            self.usdAllocationPercentage = a * (self.ethPrice ** self.factor)
            return f'{round(100 * self.usdAllocationPercentage,3)}%'
        
        def ethAllocation(self):
            self.ethAllocationPercentage = 1 - self.usdAllocationPercentage
            return f'{round(100 * self.ethAllocationPercentage,3)}%'
                        
        def currentUsdAllocation(self):
            a = 100 * (self.usdHoldings / (self.ethHoldings + self.usdHoldings))
            return f'{round(a,3)}%'

        def currentEthAllocation(self):
            a = 100 * (self.ethHoldings / (self.ethHoldings + self.usdHoldings))
            return f'{round(a,3)}%'



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
    return render_template('bond.html')

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
        pstEthHoldings = float(form['fstEthHoldings'])
        prEthHoldings = float(form['frEthHoldings'])
        pswEthHoldings = float(form['fswEthHoldings'])
        pEthHoldings = float(form['fEthHoldings'])

        pTotalEthHoldings = pstEthHoldings + prEthHoldings + pswEthHoldings + pEthHoldings # placeholder values until integrated with CMC or Chainlink

        allocation = Allocation(pMinimumPrice, pMaximumPrice, pTotalEthHoldings, pUsdHoldings)
        
        usdAllocation = allocation.usdAllocation()
        ethAllocation = allocation.ethAllocation()
        currentUsdAllocation = allocation.currentUsdAllocation()
        currentEthAllocation = allocation.currentEthAllocation()

        return render_template('allocation.html', pTotalEthHoldings=pTotalEthHoldings,usdAllocation=usdAllocation, ethAllocation=ethAllocation, currentEthAllocation=currentEthAllocation, currentUsdAllocation=currentUsdAllocation)

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

        return render_template('bond.html', bondEquivalentYield=bondEquivalentYield)

    return render_template('bond.html')

if __name__ == '__main__':
    app.run(debug=True)