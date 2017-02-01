from stupidmeteo import app
import os
os.environ[FLASKR_SETTINGS] = 'config.py'
if __name__ == "__main__":
        app.run()
