#!/bin/bash
source venv/bin/activate
export FLASK_APP=stupidmeteo.py
export FLASK_DEBUG=0
export FLASKR_SETTINGS=config.py
flask run
