# Welcome to CS162 Final Project

This repository is a copy of a private repository (hosted in university account and thus cannot be made private). The code in the repository is the resul of work of 4 people. I focused on the creation and population of database (models.py, insert_data.py in web folder) and then routing of the pages (routing.py) and then the rest of the web folder. I also worked on unit testing; yet, the testing part needs a bit of work.

We tried deploying the project to Heroku, but bumped into errors, so please 
use the code here and run the app locally. 

The login and register user does not work, but the main page can be accessed
by removing the '/register'. 

The start of a modal to leave reviews is in the review-modal branch, but this
was not working at the time of submission and was therefore not merged.




## Tailwind CSS
Make sure Node.js is downloaded. 

Run `npm install` to install npm packages from package.json.
(This does not replace requirements.txt, so `pip install -r requirements.txt` should still be run in your virtual environment). 

You can now use flask as normal with Tailwind CSS in your html files.

NOTE: if you want to update the styling in the HTML files you need to have
`npx tailwindcss -i ./web/static/src/style.css -o ./web/static/css/main.css --watch`
running in the terminal (from root folder) for the CSS to update properly with Tailwind. 
## Chart.js
Running  `npm install` will also make sure that Chart.js is installed. This 
is necessary in order to see and work with the rating charts. 

## Run Virtual Environment

Virtual environment is a key component in ensuring that the application is configured in the right environment

##### Requirements
* Python 3
* Pip 3

```bash
$ brew install python3
```

Pip3 is installed with Python3

##### Installation
To install virtualenv via pip run:
```bash
$ pip3 install virtualenv
```

##### Usage
Creation of virtualenv:

    $ virtualenv -p python3 venv

If the above code does not work, you could also do

    $ python3 -m venv venv

To activate the virtualenv:

    $ source venv/bin/activate

Or, if you are **using Windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

    $ venv\Scripts\activate

To deactivate the virtualenv (after you finished working):

    $ deactivate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt

## Environment Variables

All environment variables are stored within the `.env` file and loaded with dotenv package.

**Never** commit your local settings to the Github repository!

## Run Application

Start the server by running:

    $ export FLASK_ENV=development
    $ export FLASK_APP=web
    $ python3 -m flask run

## Unit Tests
To run the unit tests use the following commands:

    $ python3 -m venv venv_unit
    $ source venv_unit/bin/activate
    $ pip install -r requirements-unit.txt
    $ export DATABASE_URL='sqlite:///web.db'
    $ cd unit_test
    $ python3 -m unittest unit_tests

## Integration Tests
Start by running the web server in a separate terminal.

Now run the integration tests using the following commands:

    $ python3 -m venv venv_integration
    $ source venv_integration/bin/activate
    $ pip3 install -r requirements-integration.txt
    $ pytest integration_test

## Deployment
We will use Heroku as a tool to deploy your project, and it is FREE

We added Procfile to help you deploy your repo easier, 
but you may need to follow these steps to successfully deploy the project

1. You need to have admin permission to be able to add and deploy your repo to Heroku 
(Please ask your professor for permission)
2. You need to create a database for your website. 
We recommend you use [Heroku Postgres](https://dev.to/prisma/how-to-setup-a-free-postgresql-database-on-heroku-1dc1)
3. You may need to add environment variables to deploy successfully - [Resource](https://devcenter.heroku.com/articles/config-vars#using-the-heroku-dashboard)
