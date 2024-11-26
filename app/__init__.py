from flask import Flask, render_template, redirect, url_for, session
from flask_socketio import SocketIO
import os
# from routes import *
import app.configuracioEntorn
from decouple import config


socketioApp = SocketIO()

def create_app():
  app = Flask(__name__)


  # ----- configuració ENTORN ------
  # Les opcions de configuracio (SECRET_KEY, DEBUG, ...) les importem d'alguna de les clases de 'configuracioEntorn.py'
  # appSettingsModule = os.getenv("APP_SETTINGS_MODULE")
  # print('--- >> APP_SETTINGS_MODULE:', appSettingsModule)
  # app.config.from_object(f"app.configuracioEntorn.{ appSettingsModule }")
  
  # Del fitxer .env llegim el valor de la calu 'entorn'
  app.config.from_object(f"app.configuracioEntorn.{ config('entorn') }")

  #app.config['SECRET_KEY'] = 'secret!'
  print( "configuracio entorn DEBUG: ", app.config['DEBUG'] )
  print( "configuracio entorn SECRET_KEY: ", app.config['SECRET_KEY'] )



  socketioApp.init_app(app)

  with app.app_context():
    # app.socketioApp = socketioApp

    # ----- registre de BLUEPRINTS -----
    from app.bp_login import login
    app.register_blueprint(login)

    from app.bp_pings import pings
    app.register_blueprint(pings)

    from app.bp_perfilsNFS import perfils
    app.register_blueprint(perfils)

    from app.bp_infoEstacio import info_estacio
    app.register_blueprint(info_estacio)

    from app.bp_swPortMac import swPM
    app.register_blueprint(swPM)

    from app.bp_portes import portes
    app.register_blueprint(portes)



  @app.route('/menu')
  def fInici():
    if "username" in session:
      return render_template( 'menu.html' )
    else:
      return "Accés prohibit."



  @app.route('/tancaSessio')
  def fTancaSessio():
    session.clear()
    return redirect( url_for('login.fLogin') )



  # app.run( host='0.0.0.0', port=5000 )

  return app
