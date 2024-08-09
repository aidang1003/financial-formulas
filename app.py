from flask import Flask
from flask import render_template, request, redirect

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


@app.route('/')
def index():
    return render_template('index.html', pageTitle='Homepage')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/annuity')
def annuity():
    return render_template('annuity.html')

@app.route('/bonds')
def bond():
    return render_template('bond.html')


@app.route('/Annuity', methods=["GET","POST"])
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

@app.route('/Bond', methods=["GET","POST"])
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