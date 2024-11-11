from flask import render_template, request, session
from app import socketioApp
from flask_socketio import emit
import os
import csv
import threading
import subprocess
from . import swPM


# socketio = SocketIOA(app)

llistaHosts = []
event = threading.Event()


@swPM.route('/swPortMac')
def fSwPortMac():
	if "username" in session:
		return render_template( 'swPortMac.html', titol="Localitzar MAC als SWITCHS" )
	else:
		return "Accés prohibit."



@swPM.route('/carregarSwitchs/')
def fCarregarSwitchs():
  fitxer = 'switchs'
  print('fitxer', fitxer )
  # return 'nothing'
  # event.set()  # event = True

  global llistaHosts
  llistaHosts = []
  
  rutaApp = os.path.dirname(__file__)
  print( 'rutaApp', rutaApp )
  
  try:
    with open( rutaApp + '/static/' + fitxer + '.csv', newline='' ) as f:
      reader = csv.reader(f)
      for row in reader:
        llistaHosts.append(row)

    return { 'llista': llistaHosts }
  except Exception as err:
      print(f"Unexpected {err=}, {type(err)=}")



@swPM.route('/getVendor')
def getVendor():
	print( "estic a la funció GETVENDOR")
	mac = request.args.get('mac')

	## localitzar el Vendor:
	try:
		v = request.get("https://api.macvendors.com/" + mac )
		print ( v.status_code )
		if v.status_code == 200:
			return v.text
		elif v.status_code == 404:
			return "Vendor no trobat"
		else:
			return v.text

	except request.exceptions.ConnectionError as exc:
		v = exc['errors'].detail





@socketioApp.on('buscar_mac')
def ejecutarPings():

	print( "\n*** COMENÇA BUSQUEDA DE MAC ALS SWITCHS ***\n" )
    
	event.clear()  # event = False
	global llistaHosts
	
	for idx_fila, host in enumerate(llistaHosts):
		threading.Thread( target=buscaMAC, args=( host[0], idx_fila, event) ).start()





def buscaMAC( host, index_fila, event ):
	print( "*** Buscant MAC al switch ***")
	#print( "app.app_context", app.app_context() )
	# global socketioApp
	swResposta = ""


	
	socketioApp.emit('recepcioDades', {'fila': index_fila, 'valor': "Inici pings..."})

	while True:
		respostaTF = true_false_ping( host ) 
		print( "Fila", index_fila, "respostaTF", respostaTF )
		#with app.test_request_context('arranca_pings'):

		if respostaTF != swResposta:
			# datahora = str(datetime.now())[:-7]
			if respostaTF:
				#print( 'respostaTF', respostaTF )
				socketEmes = ""
				socketioApp.emit('recepcioDades', {'fila': index_fila, 'valor': "OK"}) 
				#print( socketEmes )
			else:
				
				socketioApp.emit('recepcioDades', {'fila': index_fila, 'valor': "KO"})


		if event.is_set():
			
			socketioApp.emit('recepcioDades', {'fila': index_fila, 'valor': ""})

			break

		swResposta = respostaTF
		# time.sleep(2)


def true_false_ping (adress):
		reply = subprocess.run(
			['ping', '-c', '3', adress],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
    		encoding='utf-8'
    )

		if reply.returncode == 0:
			return True 
		else:
			return False



@socketioApp.on('parar_pings')
def pararPings():
		global socketioApp
		event.set()  # event = True
		socketioApp.emit('pingsAturats', "S'ha donat ordre d'aturada de pings")



