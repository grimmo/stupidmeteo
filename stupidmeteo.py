#-*- encoding: utf-8
# Stupid Meteo


from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, make_response,flash,jsonify,send_from_directory
import logging
from logging.handlers import RotatingFileHandler
from PIL import Image, ImageFont, ImageDraw
from werkzeug.utils import secure_filename
from werkzeug.contrib.cache import SimpleCache
import tempfile
import os
import forecastio

STATIC_FOLDER = 'static'
DOWNLOAD_FOLDER = os.path.join(app.root_path,STATIC_FOLDER,'img/cache')
UPLOAD_FOLDER = os.path.join(DOWNLOAD_FOLDER,'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
# Max file size: 4Mb
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
# Load default config and override config from an environment variable
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
c = SimpleCache()

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

def get_weather(api_key,lat,lng):
    if c.has('weather'):
        weather = c.get('weather')
    else:
        weather = forecastio.load_forecast(api_key,lat,lng)
        c.add('weather',weather,timeout=3600)
    current = weather.currently()
    return current.summary,current.temperature,current.windSpeed

def fake_get_weather(api_key,lat,lng):
    return u"Nuvoloso","7","5","Precipitazioni assenti"


def apply_watermark(image,width,height):
    draw = ImageDraw.Draw(image)
    text = "StupidMeteo"
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",25) 
    textwidth, textheight = draw.textsize(text, font)
    # calculate the x,y coordinates of the text
    margin =3
    x = width - textwidth - margin
    y = height - textheight - margin
    # draw watermark in the bottom right corner
    draw.text((x, y), text, fill='white',font=font)
    return image

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        app.logger.debug(request.form['city'])
        if 'file0' not in request.files:
            #flash('No file part')
            app.loger.error('No file0 in request.files')
            #flash("No sux files: %s" % (request.files))
            return redirect(request.url)
        file = request.files['file0']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            app.logger.error('Filename empty')
            return redirect(request.url)
        else:
            app.logger.debug('File correctly received')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.logger.debug('File saved correctly')
            #img = output.seek(0)
            #data = open(os.path.join(app.config['UPLOAD_FOLDER'],filename),"rb")
            img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            app.logger.debug('Image opened')
            draw = ImageDraw.Draw(img)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            # portion of image width you want text width to be
            W,H = img.size
            city_fraction = 0.4
            weather_fraction = 0.9
            city = request.form['city']
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            #meteo = fake_get_weather(app.config['API_KEY'],latitude,longitude)
            meteo = get_weather(app.config['API_KEY'],latitude,longitude)
            txt = u"%s\n%s°C\n%s Km/h" % (meteo[0],meteo[1],meteo[2])
            city_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",1) 
            weather_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",1) 
            city_fontsize = proporziona_testo(city_font,1,city,city_fraction,img)
            city_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", city_fontsize)
            weather_fontsize = proporziona_testo(weather_font,1,txt,weather_fraction,img)
            weather_font = font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", weather_fontsize)
            w, h = draw.textsize(city,city_font)
            draw.text((((W-w-5)/2),(H-h/2)/1.45), city, fill="white",font=city_font)
            w, h = draw.textsize(txt,weather_font)
            draw.text(((W-w-5)/2,(H-h-2)), txt, fill="white",font=weather_font)
            app.logger.debug('Image edited')
            #img = apply_watermark(img,W,H)
            newimg = tempfile.NamedTemporaryFile(mode='w+b',bufsize=-1, suffix='.jpg',dir=app.config['DOWNLOAD_FOLDER'],prefix='newimg',delete=False)
            img.save(newimg,format='JPEG',quality=70,optimize=True)
            app.logger.debug('Image saved as %s' % newimg.name)
            #abort(500)
            return render_template('image.html',foto=os.path.join(app.config['DOWNLOAD_FOLDER'],os.path.basename(newimg.name)))
    else:
        app.logger.debug('GET request, showing empty form')
        return render_template('upload.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(STATIC_FOLDER),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(500)
def internal_error(error):
    return render_template('error_500.html',message=error)