# Flask Template

Basic structure for starting a Flask project with Jinja templates

1. Clone this repository to local computer

2. Rename the directory to reflect the new project name

3. Delete .git folder

4. Create a new virtual environment

   - Windows: `python -m venv ./venv`
   - Mac: `python -m venv ./venv`

5. Activate the new virtual environment

   - Windows: `.\venv\Scripts\activate`
   - Mac: `source ./venv/bin/activate`

6. Install the dependencies `pip install -r requirements.txt`

---

# Manage Git in the command line

1. Make a new repository by running `git init` in the folder.

2. Track all the files in the new local repository `git add .`

3. Make the first commit of this new project `git commit -m 'first commit of <project name> from flask_template`

4. On Github, create a new repository. _DO NOT_ initialize it

5. Connect the local repository to the new Github repository `git remote add origin <<repository_URL>>`

6. Create and change to a new local development branch `git checkout b <<branch_name>>`

---

# Manage Dependencies

List dependencies: `pip list`

Add dependencies to the requirements.txt: `pip freeze > requirements.txt`
