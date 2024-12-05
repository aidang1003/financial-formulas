from flask import Flask, session, render_template, request, redirect
from dotenv import load_dotenv
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv(override=True) # load data from the .env file
    app.config.from_mapping(
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY'), # set the secret key
        DATABASE=os.path.join(app.instance_path, 'finance.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    @app.route('/')
    def index():
        return render_template('index.html', pageTitle='Homepage', session=session)

    @app.route('/index')
    def home():
        return render_template('index.html', session=session)
    
    from . import db
    db.init_app(app)

    from . import annuity
    app.register_blueprint(annuity.annuity_bp)

    from . import bond
    app.register_blueprint(bond.bond_bp)

    from . import allocation
    app.register_blueprint(allocation.allocation_bp)

    return app