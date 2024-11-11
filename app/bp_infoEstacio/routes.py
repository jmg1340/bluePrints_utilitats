from flask import render_template, request, session, url_for
from . import info_estacio

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
		password = os.getenv("PWDASE")
	except:
		return "*** NO s'ha establert la variable d'entorn PWDASE ***"

	ssh_cmd = f"sshpass -p {password} ssh -p 22 -l root -o StrictHostKeyChecking=no {host} '{cmd}'"
	status, output = subprocess.getstatusoutput( ssh_cmd )

	output = output.replace('\n', '<br/>')
	output = output.replace(' ', '&nbsp;')
 
	return { "missatge": output }




