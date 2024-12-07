from flask import render_template, request, session, url_for, jsonify
from . import portes
from decouple import config
import app.bdd as dbase
import json

db = dbase.connexioBDD()

@portes.route('/getUsuaris', methods=['GET'])
def fgetPortes():
	if "username" in session:
		try:
			usuarisRebuts = db['persones'].find()
			print( "USUARIS REBUTS", usuarisRebuts )
			return render_template( 'portes.html', titol="Accessos a portes", usuaris = usuarisRebuts )
		except:
			print ("ERROR SERVIDOR AL LLISTAR TOTS ELS USUARIS" )
			return { "missatge": "Error al llistar tots els usuaris" }
	else:
		return "Accés prohibit."

	

@portes.route('/setFiltre', methods=['POST'])
def fgetFiltre( ):
	print( "estic a POST de getFiltre")
	dades = request.get_json() 
	# print("dadesFormulari", dadesFormulari)
	txtBuscar = dades['txtBuscar']
	print("dades['txtBuscar']:", txtBuscar)
	

	try:
		usuarisFiltrats = db['persones'].find( {"$or": [ { "nom": { '$regex': txtBuscar, "$options": "i" }}, { "numero":  { '$regex': txtBuscar } } ]},{ "_id": 0, "numero": 1, "nom": 1, "traxs": 1 })

		resultat = []
		for registre in usuarisFiltrats:
			print( registre )
			resultat.append(registre)
		# print("TOTAL usuaris:", usuarisFiltrats.count() )
		# print( "Num usuaris filtrats", usuarisFiltrats.count() )

		return resultat
		# return render_template( 'portes.html', titol="Accessos a portes2", usuaris = usuarisFiltrats )
		# return usuarisFiltrats
		# return redirect( url_for("fgetPortes", usuaris = usuarisFiltrats))
		# return jsonify({'redirect': url_for("getUsuaris", usuaris = usuarisFiltrats )})
		# return jsonify({'redirect': render_template( 'portes.html', titol="Accessos a portes2", usuaris = usuarisFiltrats )})
		# return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

	except:
		print ("ERROR SERVIDOR AL FILTRAR USUARIS" )
		return { "missatge": "Error al filtrar usuaris" }

 

# @portes.errorhandler(BadRequest)
# def handle_bad_request(e):
# 	return 'bad request!', 400






