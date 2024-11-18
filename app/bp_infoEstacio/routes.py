from flask import render_template, request, session, url_for
from . import info_estacio
from decouple import config

import time
import subprocess
import os


@info_estacio.route('/infoEstacio', methods=['GET'])
def fFormulariEstacio():
	if "username" in session:
		return render_template( 'infoEstacio.html', titol="Informació estacions plataforma" )
	else:
		return "Accés prohibit."

	

@info_estacio.route('/getInfoEstacio', methods=['POST'])
def fgetInfoEstacio():
	print( "estic a POST de getInfoEstacio")
	dades = request.get_json() 
	# print("dadesFormulari", dadesFormulari)
	host = dades['host']
	cmd = dades['cmd']
	print("dades['cmd']", cmd)
	print("dades['host']", host)
	
	try:
		# password = os.getenv("PWDASE")
		# Del fitxer .env llegim el valor de la calu 'entorn'
		password = config('PWDASE')

	except:
		return { "missatge": "NO s'ha establert PWDASE" }

	ssh_cmd = f"/usr/bin/sshpass -p {password} ssh -p 22 -l root -o StrictHostKeyChecking=no {host} '{cmd}'"
	print("SSH_CMD\n", ssh_cmd)
	try:
		resultat = subprocess.run( ssh_cmd )
	except subprocess.CalledProcessError as e:
		return { "missatge": "No s'ha pogut executar el comandament: " }
	except:
		return { "missatge": "Error intern del servidor" }

	output = resultat.stdout
	output = output.replace('\n', '<br/>')
	output = output.replace(' ', '&nbsp;')
 
	return { "missatge": output }




