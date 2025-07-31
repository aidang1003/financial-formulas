import imp
import os
import sys
from portfolio import create_app


wsgi = imp.load_source('wsgi', 'finance/__init__.py')


# Add your project directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

application = create_app()
