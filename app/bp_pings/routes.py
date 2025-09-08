from flask import render_template, request, session
from app import socketioApp
from flask_socketio import emit
import os
import csv
import threading
import subprocess
from . import pings
import re


# socketio = SocketIOA(app)

llistaHosts = []
event = threading.Event()


@pings.route('/pings')
def fPings():
	if "username" in session:
		return render_template( 'pings.html', titol="Pings" )
	else:
		return "Accés prohibit."



@pings.route('/carregarTaula/')
def carregarTaula():
  fitxer = request.args.get('fitxer')
  print('fitxer', fitxer )
  # return 'nothing'
  # event.set()  # event = True

  global llistaHosts
  llistaHosts = []
  
  rutaApp = os.path.dirname(__file__)
  print( 'rutaApp', rutaApp )
  
  try:
    with open( rutaApp+'/../static/' + fitxer + '.csv', newline='' ) as f:
      reader = csv.reader(f)
      for row in reader:
        llistaHosts.append(row)

    return { 'llista': llistaHosts }
  except Exception as err:
      print(f"Unexpected {err=}, {type(err)=}")





###################  PINGS  ######################


@socketioApp.on('arranca_pings')
def ejecutarPings():
	print( "\n*** ARRANCA PINGS ***\n" )
	global event

	event.clear()  # event = False
	global llistaHosts
	
	for idx_fila, host in enumerate(llistaHosts):
		threading.Thread( target=doPings, args=( host[0], idx_fila, event) ).start()





def doPings( host, index_fila, event ):
	print( "*** DO PINGS ***")
	#print( "app.app_context", app.app_context() )
	# global socketioApp
	swResposta = ""
	
	socketioApp.emit('recepcioDades', { 'accio': 'pings', 'fila': index_fila, 'valor': "Iniciant pings..."})

	while True:
		respostaTF = true_false_ping( host ) 
		print( "Fila", index_fila, "respostaTF", respostaTF )

		if respostaTF != swResposta:
			if respostaTF:
				socketioApp.emit('recepcioDades', {'accio': 'pings', 'fila': index_fila, 'valor': "OK"}) 
			else:
				socketioApp.emit('recepcioDades', {'accio': 'pings', 'fila': index_fila, 'valor': "KO"})

		
		if event.is_set():
			print("S'ATURA AQUESTA TAREA")
			socketioApp.emit('recepcioDades', {'accio': 'pings', 'fila': index_fila, 'valor': ""})
			break

		swResposta = respostaTF
		# time.sleep(2)


def true_false_ping (adress):
		reply = subprocess.run(
			['/bin/ping', '-c', '3', adress],
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
		print("ESTIC A PARAR PINGS")
		global socketioApp
		global event
		event.set()  # event = True
		
		print( "event.is_set() :  ", event.is_set())
		socketioApp.emit('pingsAturats', f"S'ha donat oooordre d'aturada de pings. EVENT.IS_SET = {event.is_set()}")






###################  TRACEROUTE  ######################



@socketioApp.on('arranca_traceroute')
def ejecutarLatencia():
	print( "\n*** ARRANCA LATENCIES ***\n" )
	global event

	event.clear()  # event = False
	global llistaHosts
	
	for idx_fila, host in enumerate(llistaHosts):
		threading.Thread( target=analizar_traceroute, args=( host[0], idx_fila, event) ).start()





def analizar_traceroute( host, index_fila, event ):
	print( "*** DO TRACEROUTE ***")
	
	socketioApp.emit('recepcioDades', {'accio': 'traceroute', 'fila': index_fila, 'valor': "Iniciant traceroute..."})


	"""
	Analiza la salida de traceroute para encontrar problemas de latencia y pérdida de paquetes.
	"""
	texto_traceroute = ejecutar_traceroute( host )

	lineas = texto_traceroute.strip().split('\n')
	# Nos saltamos la primera línea, que es informativa
	resultados_saltos = lineas[1:]
		
	informe = {
		"saltos_problematicos": [],
		"perdida_paquetes": [],
		"resumen": "La conexión parece estable."
	}

	if not resultados_saltos or "Error" in texto_traceroute:
		socketioApp.emit('recepcioDades', {'accio': 'traceroute', 'fila': index_fila, 'valor': texto_traceroute})
		return
		# informe["resumen"] = "No se pudo completar el traceroute."
		# return informe

	for linea in resultados_saltos:
		print( "LINEA:", linea )
		
		# Extraemos todos los números flotantes de la línea, que suelen ser las latencias
		tiempos = re.findall(r"(\d+\,\d+)\s*ms", linea)

		# Convertim les comes dels numeros flotants per punts.
		tiempos = map( lambda x: x.replace(",", "."), tiempos )
		print( "TIEMPOS: ", tiempos )
				
		# Detectar pérdida de paquetes
		if '* * *' in linea:
			numero_salto = linea.strip().split()[0]
			informe["perdida_paquetes"].append(int(numero_salto))
			continue # Pasamos a la siguiente línea

		# Detectar alta latencia
		umbral_ms = 20.0
		if tiempos:
			salto_ip = linea.strip().split()[1]
			for t in tiempos:
				print( float(t), " > ", umbral_ms, ":", float(t) > umbral_ms)
				if float(t) > umbral_ms:
					informe["saltos_problematicos"].append({
						"ip": salto_ip,
						"latencia": float(t)
					})
					break # Con un tiempo alto es suficiente para marcar el salto

	if informe["saltos_problematicos"] or informe["perdida_paquetes"]:
		socketioApp.emit('recepcioDades', {'accio': 'traceroute', 'fila': index_fila, 'valor': f"Possibles problemes a la xarxa. [{texto_traceroute}]"})
		return
		# informe["resumen"] = "¡Atención! Se han detectado posibles problemas en la red."

	socketioApp.emit('recepcioDades', {'accio': 'traceroute', 'fila': index_fila, 'valor': f"Latencia Ok. [{texto_traceroute}]"})
	return
	# return informe





def ejecutar_traceroute(destino):
    """
    Ejecuta el comando traceroute para un destino y devuelve la salida.
    El argumento -n hace que no resuelva los nombres, haciendo la ejecución más rápida.
    """
    print(f"Ejecutando traceroute hacia {destino}...")
    try:
        # Usamos -n para evitar la resolución de DNS y hacer el proceso más rápido.
        # timeout es un comando de linux que para el proceso si dura mas de X segundos
        comando = ['timeout', '30', 'traceroute', destino]
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            check=True  # Lanza una excepción si el comando falla
        )
        return resultado.stdout
    except FileNotFoundError:
        return "Error: El comando 'traceroute' no está instalado o no se encuentra en el PATH."
    except subprocess.CalledProcessError as e:
        return f"Error durante la ejecución de traceroute: {e.stderr}"
    except Exception as e:
        return f"Ha ocurrido un error inesperado: {e}"