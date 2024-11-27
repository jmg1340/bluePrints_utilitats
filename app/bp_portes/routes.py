from flask import render_template, request, session, url_for
from . import portes
from decouple import config
import app.bdd as dbase

db = dbase.connexioBDD()

@portes.route('/getUsuaris', methods=['GET'])
def fgetPortes():
	if "username" in session:
		usuarisRebuts = db['persones'].find()
		print( "USUARIS REBUTS", usuarisRebuts )
		return render_template( 'portes.html', titol="Accessos a portes", usuaris = usuarisRebuts )
	else:
		return "Accés prohibit."

	

@portes.route('/getFiltre', methods=['POST'])
def fgetFiltre( ):
	print( "estic a POST de getFiltre")
	dades = request.get_json() 
	# print("dadesFormulari", dadesFormulari)
	txtBuscar = dades['txtBuscar']
	print("dades['txtBuscar']", txtBuscar)
	
	try:
		print("DINTRE DEL TRY")
		usuarisFiltrats = db['persones'].find()
		# print("TOTAL usuaris:", usuarisFiltrats )
		# print("TOTAL usuaris:", usuarisFiltrats.count() )
		# print( "Num usuaris filtrats", usuarisFiltrats.count() )
		return render_template( 'portes.html', titol="Accessos a portes2", usuaris = usuarisFiltrats )
	except:
		print ("ERROR SERVIDOR AL FILTRAR" )
		return { "missatge": "Error al filtrar usuaris" }

 






