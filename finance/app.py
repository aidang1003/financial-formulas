from flask import Flask, session, render_template, request, redirect
from dotenv import load_dotenv
import os
from annuity import annuity_bp
from bond import bond_bp
from allocation import allocation_bp


app = Flask(__name__, instance_relative_config=True)



app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY') #set a secret key to use for session instance

app.register_blueprint(annuity_bp)
app.register_blueprint(bond_bp)
app.register_blueprint(allocation_bp)


@app.route('/')
def index():
    return render_template('index.html', pageTitle='Homepage', session=session)

@app.route('/index')
def home():
    return render_template('index.html', session=session)





if __name__ == '__main__':
    load_dotenv(override=True)
    app.run(debug=True)