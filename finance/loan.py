import functools
from flask import Blueprint, Flask, render_template, url_for, session, request
from werkzeug.security import check_password_hash, generate_password_hash

loan_bp = Blueprint("loan", __name__)

@loan_bp.route('/loan', methods=["GET","POST"])
def loan():
    if request.method == "GET":
        if 'presentValue' not in session:
            session["presentValue"] = request.args.get('presentValue', default=50000, type=float)
        if 'annualRate' not in session:
            session["annualRate"] = request.args.get('annualRate', default=7, type=float)
        if 'periodsPerYear' not in session:
            session["periodsPerYear"] = request.args.get('periodsPerYear', default=12, type=float)
        if 'numberOfPeriods' not in session:
            session["numberOfPeriods"] = request.args.get('numberOfPeriods', default=36, type=float)

    if request.method == "POST":
        form = request.form
        session['presentValue'] = float(form['presentValue'])
        session['annualRate'] = float(form['annualRate'])
        session['periodsPerYear'] = float(form['periodsPerYear'])
        session['numberOfPeriods'] = float(form['numberOfPeriods'])

        loan = Loan(session)
        
        session['loanPayment'] = loan.LoanPayment()

    return render_template('loan.html', session=session)


class Loan():
    def __init__(self, arrData):
        self.presentValue = arrData['presentValue']
        self.ratePerPeriod = arrData['annualRate'] / 100 / arrData['periodsPerYear']
        self.numberOfPeriods = arrData['numberOfPeriods']
  

    def LoanPayment(self):
        # Calculates a loan paymeny given a period
        return (self.ratePerPeriod * self.presentValue) / (1 - ((1 + self.ratePerPeriod) ** (-1 * self.numberOfPeriods)))
