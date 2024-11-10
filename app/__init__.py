from flask import Flask, render_template, redirect, url_for, session
from flask_socketio import SocketIO
import os
# from routes import *
import app.configuracioEntorn

socketioApp = SocketIO()

def create_app():
  app = Flask(__name__)


  # ----- configuració ENTORN ------
  # Les opcions de configuracio (SECRET_KEY, DEBUG, ...) les importem d'alguna de les clases de 'configuracioEntorn.py'
  appSettingsModule = os.getenv("APP_SETTINGS_MODULE")
  print('--- >> APP_SETTINGS_MODULE:', appSettingsModule)
  app.config.from_object(f"app.configuracioEntorn.{appSettingsModule}")
  #app.config['SECRET_KEY'] = 'secret!'
  print( "configuracio entorn DEBUG: ", app.config['DEBUG'] )
  print( "configuracio entorn SECRET_KEY: ", app.config['SECRET_KEY'] )



  socketioApp.init_app(app)

  with app.app_context():
    # app.socketioApp = socketioApp

    # ----- registre de BLUEPRINTS -----
    from bp_login import login
    app.register_blueprint(login)

    from bp_pings import pings
    app.register_blueprint(pings)

    from bp_perfilsNFS import perfils
    app.register_blueprint(perfils)

    from bp_infoEstacio import info_estacio
    app.register_blueprint(info_estacio)



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
