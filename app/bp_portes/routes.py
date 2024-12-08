from flask import render_template, request, session, Response
from . import portes
from decouple import config
from app import mongo
from bson import json_util
from bson.objectid import ObjectId
import pymongo



@portes.route('/getTraxs', methods=['GET'])
def fgetTraxs( ):
	print( "\n\nestic a GET de getTraxs")
	
	try:
		traxsBSON = mongo.db.traxs.find()
		traxsBSONtoJSON = json_util.dumps( traxsBSON )
		print ("\ntraxsBSONtoJSON", traxsBSONtoJSON)

		return Response(
			traxsBSONtoJSON,
			mimetype="application/json"
		)

	except pymongo.errors.PyMongoError as e:
		print ("ERROR SERVIDOR AL OBTENIR TRAXs" )
		print (e)
		return { "missatge": "Error al OBTENIR TRAXs" }




@portes.route('/getUsuaris', methods=['GET'])
def fgetUsuaris():
	if "username" in session:
		try:
			usuarisRebutsBSON = mongo.db.persones.find()
			return render_template( 'usuaris.html', titol="Accessos a portes", usuaris = usuarisRebutsBSON )
		
		except pymongo.errors.PyMongoError as e:
			print ("ERROR SERVIDOR AL LLISTAR TOTS ELS USUARIS" )
			print (e)
			return { "missatge": "Error al llistar tots els usuaris" }
	
	else:
		return "Accés prohibit."

	



@portes.route('/setFiltre', methods=['POST'])
def fgetFiltre( ):
	print( "\n\nestic a POST de setFiltre")
	dades = request.get_json() 
	# print("dadesFormulari", dadesFormulari)
	txtBuscar = dades['txtBuscar']
	print("\ndades['txtBuscar']:", txtBuscar)
	

	try:
		usuarisFiltratsBSON = mongo.db.persones.find( {"$or": [ { "nom": { '$regex': txtBuscar, "$options": "i" }}, { "numero":  { '$regex': txtBuscar } } ]})
		usuarisBSONtoJSON = json_util.dumps( usuarisFiltratsBSON )
		print ("\nusuarisBSONtoJSON", usuarisBSONtoJSON)

		return Response(
			usuarisBSONtoJSON,
			mimetype="application/json"
		)

	except pymongo.errors.PyMongoError as e:
		print ("ERROR SERVIDOR AL FILTRAR USUARI" )
		print (e)
		return { "missatge": "Error al FILTRAR USUARI" }

 



@portes.route('/getUsuari/<id>', methods=['GET'])
def fgetUsuari( id ):
	print( "\n\nestic a GET de /getUsuari/<id>")
	

	try:
		usuariBSON = mongo.db.persones.find({"_id": ObjectId( id )})
		usuariBSONtoJSON = json_util.dumps( usuariBSON )
		print ("\nusuariBSONtoJSON", usuariBSONtoJSON)

		return Response(
			usuariBSONtoJSON,
			mimetype="application/json"
		)

	except pymongo.errors.PyMongoError as e:
		print ("ERROR SERVIDOR AL OBTENIR INFO DE L'USUARI SELECCIONAT" )
		print (e)
		return { "missatge": "Error al OBTENIR INFO DE L'USUARI SELECCIONAT" }






@portes.route('/updateUsuari/<id>', methods=['PUT'])
def fupdateUsuari( id ):
	print( "\n\nestic a PUT de /updateUsuari/<id>")
	dades = request.get_json() 
	print("\ndades:", dades)
	

	try:
		resultatBSON = mongo.db.persones.update_one({"_id": ObjectId( id )}, {"$set": {"numero": dades.numero, "nom": dades.nom, "traxs": dades.traxs}})
		resultatBSONtoJSON = json_util.dumps( resultatBSON )
		print ("\nresultatBSONtoJSON", resultatBSONtoJSON)

		return Response(
			resultatBSONtoJSON,
			mimetype="application/json"
		)

	except pymongo.errors.PyMongoError as e:
		print ("ERROR SERVIDOR AL ACTUALITZAR DADES DE L'USUARI" )
		print (e)
		return { "missatge": "Error al ACTUALITZAR DADES DE L'USUARI" }







