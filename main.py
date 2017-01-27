#-*- encoding: utf-8
# Stupid Meteo


#import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, make_response,flash,jsonify
     
import logging
from logging.handlers import RotatingFileHandler
from PIL import Image, ImageFont, ImageDraw
import base64
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import tempfile
import os
import cStringIO

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)
app.config.from_object(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
    #DATABASE=os.path.join(app.root_path, 'apollo.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#def init_db():
#    with app.app_context():
#        db = get_db()
#        with app.open_resource('apollo_schema.sql', mode='r') as f:
#            db.cursor().executescript(f.read())
#        db.commit()

#def connect_db():
#    """Connects to the specific database."""
#    rv = sqlite3.connect(app.config['DATABASE'])
#    rv.row_factory = sqlite3.Row
#    return rv

#def get_db():
#    """Opens a new database connection if there is none yet for the
#    current application context.
#    """
#    if not hasattr(g, 'sqlite_db'):
#        g.sqlite_db = connect_db()
#    return g.sqlite_db

#@app.teardown_appcontext
#def close_db(error):
#    """Closes the database again at the end of the request."""
#    if hasattr(g, 'sqlite_db'):
#        g.sqlite_db.close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def proporziona_testo(font,fontsize,text,fraction,image):
    while font.getsize(text)[0] < fraction*image.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", fontsize)
        # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    return fontsize

def apply_watermark(image):
    draw = ImageDraw.Draw(image)
    text = "StupidMeteo, powered by Dark Sky API"
    font = ImageFont.truetype('arial.ttf', 12)
    textwidth, textheight = draw.textsize(text, font)
    # calculate the x,y coordinates of the text
    margin = 5
    x = width - textwidth - margin
    y = height - textheight - margin
    # draw watermark in the bottom right corner
    draw.text((x, y), text, font=font)
    image.save('cats.png')
    return image

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        app.logger.debug(request.form['city'])
        if 'file0' not in request.files:
            #flash('No file part')
            flash("No sux files: %s" % (request.files))
            return redirect(request.url)
        file = request.files['file0']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        elif file and allowed_file(file.filename):
            #flash('OK image received')
            #return redirect(request.url)
            filename = secure_filename(file.filename)
            # salviamo il file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = open(os.path.join(app.config['UPLOAD_FOLDER'],filename),"rb")
            img = Image.open(data)
            draw = ImageDraw.Draw(img)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            # portion of image width you want text width to be
            W,H = img.size
            city_fraction = 0.4
            weather_fraction = 0.9
            city = u'Milano'
            txt = u"2.67°C Sereno\nVento: 0.44 Km/h"
            city_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",1) 
            weather_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",1) 
            city_fontsize = proporziona_testo(city_font,1,city,city_fraction,img)
            city_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", city_fontsize)
            weather_fontsize = proporziona_testo(weather_font,1,txt,weather_fraction,img)
            weather_font = font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", weather_fontsize)
            w, h = draw.textsize(city,city_font)
            draw.text((((W-w-5)/2),(H-h/2)/1.25), city, fill="white",font=city_font)
            w, h = draw.textsize(txt,weather_font)
            draw.text(((W-w-5)/2,(H-h-2)), txt, fill="white",font=weather_font)
            display = cStringIO.StringIO()
            img.save(display,format='PNG')
            display.seek(0)
            newimg = display.read()
            b64 = base64.b64encode(newimg)
            return render_template('image.html',foto=b64)
        else:
            flash('Forbidden file type')
            return redirect(request.url)
    else:
        return render_template('upload.html')
