# ecommerce-automation
This project is a search automation for different ecommerce platforms

## setting up project
`sudo apt install python=3.10.0`
`python -m venv venv`
`source ./venv/bin/activate`
`pip install -r requirements.txt`

## start app
`python manage.py runserver`

## setting up product scrapper package (optional)
`cd ./product_scrapper`
`python setup.py sdist bdist_wheel`
`pip install .`