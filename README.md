# ecommerce-automation
This project is a search automation for different ecommerce platforms

## setting up project
`sudo apt install python=3.10.0`
`python -m venv venv`
`pip install -r requirements.txt`

## start app
`python manage.py runserver`

## setting up product scrapper package (optional)
for windows: `./venv/Scripts/activate`
for linux: `./venv/bin/activate`
`cd ./product_scrapper`
`python setup.py sdist bdist_wheel`
`pip install .`