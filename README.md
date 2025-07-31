# Financial Formulas
---

## Basic structure for starting a Flask project with Jinja templates

1. Clone this repository to local computer

2. Create a new virtual environment

   - Windows: `py -m venv ./venv`
   - Mac: `python -m venv ./venv`

3. Activate the new virtual environment

   - Windows: `.\venv\Scripts\activate`
   - Mac: `source ./venv/bin/activate`

4. Install the dependencies `pip install -r requirements.txt`

5. Initialize the db `flask --app finance init-db`

6. Start the app `flask --app finance run --debug`

---

## Manage Git in the command line

1. Make a new repository by running `git init` in the folder.

2. Track all the files in the new local repository `git add .`

3. Make the first commit of this new project `git commit -m 'first commit of <project name> from flask_template'`

4. On Github, create a new repository. _DO NOT_ initialize it

5. Connect the local repository to the new Github repository `git remote add origin <<repository_URL>>`

6. Create and change to a new local development branch `git checkout b <<branch_name>>`

---

## Manage Dependencies

Install the dependencies `pip install -r requirements.txt`

List dependencies: `pip list`

Add dependencies to the requirements.txt: `pip freeze > requirements.txt`

---

## Manage CoinMarketCap API

1. Create an API key at https://coinmarketcap.com/api/

2. Create a .env file in the ..\financial-formulas\finance folder

3. Copy this text to your .env file `COIN_MARKETCAP_API_KEY = **YOUR API KEY HERE** `

---

## Usefule Testing Commands

1. `pytest` to initiate the test
2. `coverage run -m pytest` measures the coverage of the tests
3. `coverage report` returns the coverage report to the command line
4. `coverage html` return to an HTML instead

---

## Deploy To a Server

1. `py -m build --wheel`

2. `pip install flaskapp-1.0.0-py3-none-any.whl`

3. `flask --app flaskapp init-db`

4. `pip install waitress`

5. `waitress-serve --call 'flaskapp:create_app'`

---

## Automatic Allocation #TODO
1) Deposit to Aave
2) Withdraw from Aave
3) Transfer on Uniswap, matcha, or 0x?
4) Integrarte Metamask