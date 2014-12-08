on-the-grid
===========

A web-app for keeping track of those delicious Off The Grid SF food trucks.

## Getting Started

First make sure you have pip and virtualenv installed. Then install the required packages with

    $source venv/bin/activate
    $pip install -r requirements.txt

Then install PostgreSQL and create a database called "onthegrid".

    $createdb onthegrid

Then you can start the application locally with

    $foreman start

If you want to deploy to Heroku then you can do

    $heroku login

You have to set some secret keys like this

    $heroku config:set HIPCHAT_API_TOKEN=YOUR_API_TOKEN
    $heroku config:set HIPCHAT_ROOM_ID=YOUR_ROOM_ID
    $heroku config:set OFFTHEGRID_LOCATION="5th and Minnas"
    $heroku config:set FACEBOOK_APP_ID=YOUR_FB_APP_ID
    $heroku config:set FACEBOOK_APP_SECRET=YOUR_SECRET

And finally launch

    $git push heroku master
    $heroku run python manage.py makemigrations vendorlist
    $heroku run puthon mange.py migrate
    $heroku open
    
Enjoy :)