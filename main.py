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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #data = request.get_data()
        app.logger.info(request.files)
        return render_template('upload.html')
        # salviamo il file
        #newfile = tempfile.NamedTemporaryFile(mode='wb',delete=False)
        #nome_newfile = newfile.name
        #newfile.write(data)
        #newfile.close()
#            data = open(os.path.join(app.config['UPLOAD_FOLDER'],filename),"rb")
        #display = cStringIO.StringIO()
        #display.write(data)
        #display.seek(0)
        #file = request.data
        #return render_template('image.html')
        img = Image.open(nome_newfile)
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        fontsize = 1  # starting font size
        # portion of image width you want text width to be
        img_fraction = 0.50
        txt = u"Milano 2.67 °C\nVento: 0.44 Km/h\nClear"
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", fontsize)
        while font.getsize(txt)[0] < img_fraction*img.size[0]:
             # iterate until the text size is just larger than the criteria
             fontsize += 1
             font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", fontsize)
        # optionally de-increment to be sure it is less than criteria
        fontsize -= 1
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", fontsize)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((0, -1),txt,(255,255,255),font=font)
        display = cStringIO.StringIO()
        img.save(display,format='PNG')
        display.seek(0)
        newimg = display.read()
        b64 = base64.b64encode(newimg)
        return render_template('image.html',foto=b64)
#        #return render_template('image.html',foto=b64)
#        # check if the post request has the file part
#        if 'file' not in request.files:
#            #flash('No file part')
#            flash("No sux data: %s" % (request.files))
#            return redirect(request.url)
#        file = request.files['file']
#        # if user does not select file, browser also
#        # submit a empty part without filename
#        if file.filename == '':
#            flash('No sux file')
#            return redirect(request.url)
#        elif file and allowed_file(file.filename):
#            #flash('OK image received')
#            #return redirect(request.url)
#            filename = secure_filename(file.filename)
#            # salviamo il file
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            data = open(os.path.join(app.config['UPLOAD_FOLDER'],filename),"rb")
#            img = Image.open(data)
#            draw = ImageDraw.Draw(img)
#            # font = ImageFont.truetype(<font-file>, <font-size>)
#            fontsize = 1  # starting font size
#            # portion of image width you want text width to be
#            img_fraction = 0.50
#            txt = u"Milano 2.67 °C\nVento: 0.44 Km/h\nClear"
#            font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", fontsize)
#            while font.getsize(txt)[0] < img_fraction*img.size[0]:
#                # iterate until the text size is just larger than the criteria
#                fontsize += 1
#                font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", fontsize)
#            # optionally de-increment to be sure it is less than criteria
#            fontsize -= 1
#            font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", fontsize)
#            # draw.text((x, y),"Sample Text",(r,g,b))
#            draw.text((0, -1),txt,(255,255,255),font=font)
#            display = cStringIO.StringIO()
#            img.save(display,format='PNG')
#            display.seek(0)
#            newimg = display.read()
#            b64 = base64.b64encode(newimg)
#            return render_template('image.html',foto=b64)
#        else:
#            flash('Forbidden file type')
#            return redirect(request.url)
    else:
        return render_template('upload.html')

if __name__ == '__main__':
    handler = RotatingFileHandler('stupidmeteo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
