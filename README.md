on-the-grid
===========

A web-app for keeping track of those delicious Off The Grid SF food trucks.

## Getting Started

First make sure you have pip and virtualenv installed. Then install the required packages with

    $source venv/bin/activate
    $pip install -r requirements.txt

Then you can start the application locally with

    $foreman start

If you want to deploy to Heroku then you can do

    $heroku login
    $git push heroku master
    $heroku open
    
Enjoy :)