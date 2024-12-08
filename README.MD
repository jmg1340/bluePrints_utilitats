## App UTILITATS

Requeriments **linux** (`apt-get`):
- python3
- sshpass

<br/>

Creació d'entorn virtual (`python3 -m venv <carpeta>`) i activació (`<carpeta>/bin/activate`) per instal·lar **llibreries python** (`pip`):
- flask
- flask-socketIO
- flask-pymongo
- requests
- python-decouple

<br/><br/>
Per posar en producció instalar també:
- gunicorn
- eventlet 
  
<br>

**Settings al fitxer .env**:
- entorn (DevelopmentConfig / ProductionConfig)
- PWDASE
- PWDCOS
- MONGO_URI
  
<br/><br/>

A tenir en compte:<br/>
>Quan utilitzem el servidor de desenvolupament de flask (werkzug), desinstalar 'eventlet' sino els 'emits" dels sockets no funcionen


Per posar en producció:
- canviar entorn=ProductionConfig al fitxer .env
- instalar eventlet i gunicorn
- executar `gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 utilitats:app`

<br/><br/>
Si tornem a executar `python3 utilitats.py` hem de desinstalar 'eventlet' per a que funcionin bé els sockets. Concretament el 'emit' fet des del servidor.

<br/><br/><br/><br/>

## Mongodb
> mongoimport --db=NOM_BDD --collection=NOM_COLECCIO --jsonArray --file=NOM_FITXER.json<br/><br/>
db.createUser({ user:"NOM_USUARI", pwd:"PWD", roles:[] })<br/><br/>
db.changeUserPassword("NOM_USUARI", "PWD")

<br/><br/><br/><br/>

## [Create a systemd service script for running Gunicorn to serve your application](https://dev.to/tkirwa/create-a-systemd-service-script-for-running-gunicorn-to-serve-your-application-5aea):
- `sudo nano /etc/systemd/system/gunicornVariablesEntorn.txt` (copia pega de les variables d'entorn que apareixen a `env`)
- `sudo nano /etc/systemd/system/gunicorn.service`


<br/><br/>

[Unit]<br/>
Description=Gunicorn instance to serve application
After=network.target<br/>
<br/>
[Service]<br/>
User=your_username<br/>
Group=your_groupname<br/>
WorkingDirectory=/path/to/your/app<br/>
#Environment="PATH=/path/to/venv/bin"<br/>
EnvironmentFile=guniconrVariablesEntorn.txt<br/>
ExecStart=/path/to/venv/bin/gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 utilitats:app<br/>
ExecReload=/bin/kill -s HUP $MAINPID<br/>
KillMode=mixed<br/>
TimeoutStopSec=5<br/>
PrivateTmp=true<br/>
<br/>
[Install]<br/>
WantedBy=multi-user.target<br/>

<br/><br/>





>Reload the systemd manager configuration to make >it aware of the new service file:
>
   >`sudo systemctl daemon-reload`<br/><br/>
>Enable the service to start on boot:
>
   >`sudo systemctl enable gunicorn`<br/><br/>
>Start the service:
>
   >`sudo systemctl start gunicorn`<br/><br/>
>Verify that the service is running without >errors:
>
   >`sudo systemctl status gunicorn`<br/><br/>
>You can also restart, stop, or check the logs of >the service using systemd commands:
>
   >`sudo systemctl restart gunicorn`<br/>
   >`sudo systemctl stop gunicorn`<br/>
   >`journalctl -u gunicorn`<br/><br/>
>Finally, test your application to ensure it's >serving content as expected using curl commands >similar to what you mentioned in your >instructions.
>
>Remember that the gunicorn.service script must >be tailored to your specific environment and >application setup. Make sure to adjust paths, >usernames, and other parameters accordingly.
>
>Also, note that systemd services require >administrative privileges to manage. Be sure to >use sudo as needed while performing these steps.