## App UTILITATS

Requeriments **linux** (`apt-get`):
- python3
- sshpass

<br/>

Creacio d'entorn virtual (`python3 -m venv <carpeta>`) i activació (`<carpeta>/bin/activate`) per instal·lar **llibreries python** (`pip`):
- flask
- flask-socketIO
- requests
Per posar en producció:
- gunicorn
- eventlet ( per posar app en producció)
  
<br>

**Variables d'entorn** (`export variable=`):
- APP_SETTINGS_MODULE (DevelopmentConfig / ProductionConfig)
- PWDASE
- PWDCOS
  


Per posar en producció:
- canviar APP_SETTINGS_MODULE=ProductionConfig
- executar `gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 utilitats:app`