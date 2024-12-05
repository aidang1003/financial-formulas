from flask import Blueprint, Flask, render_template, url_for, session, request

annuity_bp = Blueprint("annuity", __name__)

@annuity_bp.route('/annuity', methods=["GET","POST"])
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
        session['periodicPayment'] = float(form['PeriodicPayment'])
        session['ratePerPeriod'] = float(form['RatePerPeriod'])
        session['periods'] = float(form['Periods'])

        annuity = Annuity(session)
        
        session['annuity'] = annuity.fvOrPvOfAnnuity()

    return render_template('annuity.html', session=session)


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
        elif self.annuityType == 'PV': # Calculates the Present Value of an annuity
            return round(self.periodicPayment * ((1-(1+self.ratePerPeriod) ** (-1 * self.periods)) / self.ratePerPeriod) , 2)
        else:
            return "Error in annuity function. Likely there was not a correct annuity type supplied"
