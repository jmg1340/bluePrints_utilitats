from flask import render_template, request, session, Response
from . import portes
from decouple import config
from app import mongo
from bson import json_util
from bson.objectid import ObjectId
import pymongo


@portes.route('/getUsuarisPerTrax/<lloc>', methods=['GET'])
def fgetUsuarisPerTrax( lloc ):
	print( "\n\nestic a GET de /getUsuarisPerTrax/<id>")
	

	try:
		usuariBSON = mongo.db.persones.find({"traxs": { "$all": [lloc] } })
		usuariBSONtoJSON = json_util.dumps( usuariBSON )
		print ("\nusuariBSONtoJSON", usuariBSONtoJSON)

		return Response(
			usuariBSONtoJSON,
			mimetype="application/json"
		)

	except pymongo.errors.PyMongoError as e:
		print ("ERROR SERVIDOR AL OBTENIR INFO DELS USUARIS PER TRAX SELECCIONAT" )
		print (e)
		return { "missatge": "Error al OBTENIR INFO DELS USUARIS PER TRAX SELECCIONAT" }



@portes.route('/modificarTraxsDelUsuari/<id>', methods=['PUT'])
def fmodificarTraxsDelUsuari( id ):
	print( "\n\nestic a PUT de /updatdeleteUsuariDelTraxeUsuari/<id>")
	dades = request.get_json() 
	print("\ndades:", dades)

	try:
		resultatBSON = mongo.db.persones.update_one({"_id": ObjectId( id )}, {"$pull": {"traxs": dades["trax"]}})
		print("resultatBSON", resultatBSON)
		# print("resultatBSON modificats:", str(resultatBSON.raw_result["nModified"]))
		resultatBSONtoJSON = json_util.dumps( resultatBSON.raw_result )
		print ("\nresultatBSONtoJSON", resultatBSONtoJSON)

		return Response(
			resultatBSONtoJSON,
			mimetype="application/json"
		)

	except pymongo.errors.PyMongoError as e:
		print ("ERROR SERVIDOR AL ELIMINAR UN TRAX DE L'USUARI" )
		print (e)
		return { "missatge": "Error al ELIMINAR UN TRAX DE L'USUARI" }



@portes.route('/modificarTraxs/<lloc>', methods=['PUT'])
def fmodificarTraxs( lloc ):
	print( "\n\nestic a PUT de /modificarTraxs/<lloc>")
	dades = request.get_json() 
	print("\ndades:", dades)
	print("lloc", lloc)

	try:
		resultatBSON = mongo.db.traxs.update_one({"lloc": lloc}, {"$set": {"lloc": dades["lloc"], "connexio": dades["connexio"], "model": dades["model"], "ns": dades["ns"] }})
		print("resultatBSON", resultatBSON)
		# print("resultatBSON modificats:", str(resultatBSON.raw_result["nModified"]))
		resultatBSONtoJSON = json_util.dumps( resultatBSON.raw_result )
		print ("\nresultatBSONtoJSON", resultatBSONtoJSON)

		return Response(
			resultatBSONtoJSON,
			mimetype="application/json"
		)

	except pymongo.errors.PyMongoError as e:
		print ("ERROR SERVIDOR AL MODIFICAR DADES D'UN TRAX" )
		print (e)
		return { "missatge": "Error al MODIFICAR DADES D'UN TRAX" }
