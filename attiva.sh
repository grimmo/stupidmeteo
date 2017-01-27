#!/bin/bash
source venv/bin/activate
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASKR_SETTINGS=config.py
flask run
