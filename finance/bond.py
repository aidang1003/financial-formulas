from flask import Blueprint, Flask, render_template, url_for, session, request

bond_bp = Blueprint("bond", __name__)

class Bond():
    def __init__(self, arrData, rateOfYield=.07):
        self.faceValue = arrData['faceValue']
        self.purchasePrice = arrData['purchasePrice']
        self.yearsToMaturity = arrData['yearsToMaturity']
        self.rateOfYield = rateOfYield


    def bondEquivalentYield(self):
        return f'{round(100 * ((self.faceValue - self.purchasePrice) / self.purchasePrice) * (1 / self.yearsToMaturity), 4)}%'
    

@bond_bp.route('/bond', methods=["GET","POST"])
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