from flask import Flask
from flask import render_template, request, redirect

app = Flask(__name__)

class Finance():
    def __init__(self, periodicPayment, ratePerPeriod, periods):
        self.periodicPayment = periodicPayment
        self.ratePerPeriod = ratePerPeriod
        self.periods = periods        

    def fvAnnuity(self):
        return f'${round(self.periodicPayment * ((((1+self.ratePerPeriod) ** self.periods) - 1) / self.ratePerPeriod) , 2)}'
    
    def pvAnnuity(self):
        return f'${round(self.periodicPayment * ((1-(1+self.ratePerPeriod) ** (-1 * self.periods)) / self.ratePerPeriod) , 2)}'


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


@app.route('/fvAnnuity', methods=["GET","POST"])
def fvAnnuity():
    
    if request.method == "POST":
        form = request.form
        fPeriodicPayment = float(form['fPeriodicPayment'])
        fRatePerPeriod = float(form['fRatePerPeriod'])
        fPeriods = float(form['fPeriods'])

        finance = Finance(fPeriodicPayment, fRatePerPeriod, fPeriods)
        
        fvAnnuity = finance.fvAnnuity()

        return render_template('annuity.html', fvAnnuity=fvAnnuity)

    return render_template('annuity.html')

@app.route('/pvAnnuity', methods=["GET","POST"])
def pvAnnuity():
    
    if request.method == "POST":
        form = request.form
        pPeriodicPayment = float(form['pPeriodicPayment'])
        pRatePerPeriod = float(form['pRatePerPeriod'])
        pPeriods = float(form['pPeriods'])

        finance = Finance(pPeriodicPayment, pRatePerPeriod, pPeriods)
        
        pvAnnuity = finance.pvAnnuity()

        return render_template('annuity.html', pvAnnuity=pvAnnuity)

    return render_template('annuity.html')

if __name__ == '__main__':
    app.run(debug=True)