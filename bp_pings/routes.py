from flask import render_template, request, session
from app import socketioApp
from flask_socketio import emit
import os
import csv
import threading
import subprocess
from . import pings


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
    with open( rutaApp + '/static/' + fitxer + '.csv', newline='' ) as f:
      reader = csv.reader(f)
      for row in reader:
        llistaHosts.append(row)

    return { 'llista': llistaHosts }
  except Exception as err:
      print(f"Unexpected {err=}, {type(err)=}")







# @socketioApp.on('event_pings')
# def arrancaPings(tfPings):
  
#   if tfPings == True:
#     for i in range(1,6):
#       print (i)
#       if posts[1][2] == "ko":
#         posts[1][2] = "OK"
#         index()
#       else:
#         posts[1][2] = "ko"
#         index()

#       time.sleep(2)

#       emit('recepcioDades', posts[1][2])



@socketioApp.on('arranca_pings')
def ejecutarPings():
	print( "\n*** ARRANCA PINGS ***\n" )
    
	event.clear()  # event = False
	global llistaHosts
	
	for idx_fila, host in enumerate(llistaHosts):
		threading.Thread( target=doPings, args=( host[0], idx_fila, event) ).start()





def doPings( host, index_fila, event ):
	print( "*** DO PINGS ***")
	#print( "app.app_context", app.app_context() )
	# global socketioApp
	swResposta = ""
	horaInici = ""

	
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



