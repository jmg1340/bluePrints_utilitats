from flask import render_template, request, session
import requests
from app import socketioApp
from flask_socketio import emit
import os
import csv
import threading
import time
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
  print( rutaApp+'/../static/' + fitxer + '.csv' )

  try:
    with open( rutaApp+'/../static/' + fitxer + '.csv', newline='' ) as f:
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
	print("MAC:", mac)

	## localitzar el Vendor:
	try:
		print("Buscant vendor a: ", "https://api.macvendors.com/" + mac)
		v = requests.get("https://api.macvendors.com/" + mac )
		print ( v.status_code )
		if v.status_code == 200:
			return v.text
		elif v.status_code == 404:
			return "Vendor no trobat"
		else:
			return v.text

	except :
		return "ERROR REQUEST del GET VENDOR"






@socketioApp.on('buscar_mac')
def buscarMac(mac):

	print( "\n*** COMENÇA BUSQUEDA DE MAC ALS SWITCHS ***\n" )
	print( "MAC a buscar: ", mac)


	event.clear()  # event = False
	global llistaHosts

	for idx_fila, host in enumerate(llistaHosts):
		ipDeTorn = host[0]
		nomSW = host[1]
		try:
			threading.Thread( target=buscaMAC, args=( mac, ipDeTorn, nomSW, idx_fila, event) ).start()
		except Exception as e:
			print( f"Error thread del {nomSW}: {e}" )




def buscaMAC( mac, ipSW, nomSW, index_fila, event ):
	print( "*** Buscant MAC al switch ***")
	url = "http://172.31.230.30/get_interfaces.php?hostname=" + nomSW + "&hostaddress=" + ipSW

	for intent in range(1,4):    # 3 intents
		socketioApp.emit('recepcioDades', {'fila': index_fila, 'text': f"Recuperant informació del switch ... [ intent {intent}/3 ]", 'colorBg': "lightyellow", "colorText": "black"})


		try:
			respostaCapturaTextURL = requests.get( url )

			if respostaCapturaTextURL.status_code == 200:
					contingutURL = respostaCapturaTextURL.text
					# if nomSW == "SW-AMU139V0-66": print( "Contingut SW-AMU139V0-66 : ", contingutURL ) 
					coincidencia = coincidencies( contingutURL, mac )
					if coincidencia:
							socketioApp.emit('recepcioDades', {'fila': index_fila, 'text': coincidencia, 'colorBg': "lightgreen", "colorText": "black"})
					else:
							socketioApp.emit('recepcioDades', {'fila': index_fila, 'text': "no hi ha coincidencies", 'colorBg': "white", "colorText": "black"})

					break

			else:
					print( "Error del switch: ", nomSW, ipSW)
					mstgError = f"Error {respostaCapturaTextURL.status_code} en la recuperació de dades del switch."
					print( mstgError )
					socketioApp.emit('recepcioDades', {'fila': index_fila, 'text': mstgError, 'colorBg': "red", "colorText": "white"})
					# raise ValueError (f"Error {respostaCapturaTextURL.status_code} en la recuperació de dades del switch.")
					# self.taula.set( index_fila, column="col2", value=f"Error {respostaCapturaTextURL.status_code}" )
					# self.taula.item( index_fila, tags='fonsVermell' )

			# if respostaCapturaTextURL.status_code == 503:
					# print( f"{nomSW}: --> {respostaCapturaTextURL.status_code}, {respostaCapturaTextURL.json()} " )

		except requests.exceptions.ConnectionError as exc:
			socketioApp.emit('recepcioDades', {'fila': index_fila, 'text': exc, 'colorBg': "red", "colorText": "white"})
			print(exc)
			break

		except ValueError as ve:
			socketioApp.emit('recepcioDades', {'fila': index_fila, 'text': ve, 'colorBg': "red", "colorText": "white"})
			print(ve)

		time.sleep(3)


	# print( f"pendent: {threading.enumerate()}" )
	# self.etiqThreads['text'] = f"Pendents: {len(threading.enumerate()) - 2}"
	socketioApp.emit('tasquesPendents', f"Pendents: {len(threading.enumerate()) - 4}" )




def coincidencies( txtURL, txtMAC ):
	arrLinies = txtURL.split("<tr>")
	#print("arrLinies", arrLinies)

	for linia in arrLinies:

		if txtMAC.lower() in linia.lower():
			#return ">>>>>>> MAC trobada al SW !")
			# mac trobada. Ara cal veure que no sigui cap dels següents ports "invalids"
			for portInvalid in ("gigabitethernet25", "gigabitethernet26", "gigabitethernet27", "gigabitethernet28"):
				if portInvalid in linia: return False

			if linia.startswith("<td>up") or linia.startswith("<td>down"):
				print( "LINIA: ", linia )
				return linia


	return False





