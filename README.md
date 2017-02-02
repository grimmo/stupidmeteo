# Stupid Meteo
Very simple mobile web application written in Python/Flask
to upload a picture from a smartphone and overlaying text with current weather 
using [Dark Sky](http://www.darksky.net/poweredby) API and [GeoIP DB](https://geoip-db.com) for geolocation
and [Ratchet](http://www.goratchet.com) HTML/CSS templates to achieve responsiveness

## Usage:

- Create a virtualenv and activate it:
 `source your_virtualenv_path/bin/activate`
- install required modules with 
 `pip install -r requirements.txt`
 Note that you might need to install libjpeg-dev to be able to install Pillow successfully
- Sign up for an API key on [https://darksky.net/dev/](https://darksky.net/dev/)
- Create two folders to store uploaded/downloaded pictures, preferably mounted on a ram filesystem(tmpfs?)
- Rename `config.sample.py` to `config.py`
- Put your API key and the two folder absolute paths inside config.py
- Launch your application with
 `FLASK_APP=stupidmeteo.py FLASKR_SETTINGS=config.py flask run`
- Have fun!
