#!/bin/env python

import eventlet
eventlet.monkey_patch()

from app import create_app, socketioApp

app = create_app()

if __name__ == '__main__':
    socketioApp.run(app, host='0.0.0.0', port=5000, debug=True)    
    # socketioApp.run(app)
