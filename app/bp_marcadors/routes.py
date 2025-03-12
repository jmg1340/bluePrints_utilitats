from flask import render_template, request, session, url_for
from . import marcadors
from decouple import config
import subprocess


@marcadors.route('/marcadors', methods=['GET'])
def fmarcadors():
	if "username" in session:
		return render_template( 'marcadors.html', titol="Marcadors Google Chrome" )
	else:
		return "Accés prohibit."



@marcadors.route('/getInfoMarcadors', methods=['POST'])
def fgetInfoMarcadors():
	print( "estic a POST de getInfoMarcadors")
	dades = request.get_json() 
	# print("dadesFormulari", dadesFormulari)
	host = dades['host']
	user = dades['user']
	print("dades['user']", user)
	print("dades['host']", host)
	
	try:
		# password = os.getenv("PWDASE")
		# Del fitxer .env llegim el valor de la calu 'entorn'
		password = config('PWDASE')

	except:
		return { "missatge": "NO s'ha establert PWDASE" }

	cmd = f"cat /home/{user}/.config/google-chrome/Default/Bookmarks"
	ssh_cmd = f"/bin/sshpass -p {password} ssh -p 22 -l root -o StrictHostKeyChecking=no {host} '{cmd}'"
	print("SSH_CMD\n", ssh_cmd)
	try:
		resultat = subprocess.run( ssh_cmd, shell=True, capture_output=True, text=True, check=True )
	except subprocess.CalledProcessError as e:
		# return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]<br/> [ Command: {e.cmd} ]" }
		return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]" }
	except:
		return { "missatge": "Error intern del servidor" }

	output = resultat.stdout
	# output = output.replace('\n', '<br/>')
	# output = output.replace(' ', '&nbsp;')
 
	return { "missatge": output }





@marcadors.route('/getUpdateMarcadors', methods=['POST'])
def fgetUpdateMarcadors():
	print( "estic a POST de getUpdateMarcadors")
	dades = request.get_json() 
	# print("dadesFormulari", dadesFormulari)
	host = dades['host']
	user = dades['user']
	contingut = dades['contingut']
	print("dades['user']", user)
	print("dades['host']", host)
	
	try:
		# Del fitxer .env llegim el valor de la calu 'entorn'
		password = config('PWDASE')
	except:
		return { "missatge": "NO s'ha establert PWDASE" }

	#1. generem el fitxer Bookmarks a la carpeta app\statics
	with open('/../static/Bookmarks', 'w') as f:
		f.write( contingut )


	#2. fem un backup del Bookmarks origen
	rutaDesti = f'/home/{user}/.config/google-chrome/Default'
	cmd = f"cp {rutaDesti}/Bookmarks {rutaDesti}/BookmarksBACKUP_JMG"
	ssh_cmd = f"/bin/sshpass -p {password} ssh -p 22 -l root -o StrictHostKeyChecking=no {host} '{cmd}'"
	print("SSH_CMD\n", ssh_cmd)
	try:
		resultat = subprocess.run( ssh_cmd, shell=True, capture_output=True, text=True, check=True )
	except subprocess.CalledProcessError as e:
		# return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]<br/> [ Command: {e.cmd} ]" }
		return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]" }
	except:
		return { "missatge": "Error intern del servidor" }

	output = resultat.stdout



	#3. substituim el fitxer Bookmarks pel de ../statics/Bookmarks
	rutaOrigen = "../statics/Bookmarks"
	rutaDesti = f'/home/{user}/.config/google-chrome/Default'

	cmd = f"scp {rutaDesti}/Bookmarks {rutaDesti}/BookmarksBACKUP_JMG"
	ssh_cmd = f"/bin/sshpass -p {password} ssh -p 22 -l root -o StrictHostKeyChecking=no {host} '{cmd}'"
	print("SSH_CMD\n", ssh_cmd)
	try:
		resultat = subprocess.run( ssh_cmd, shell=True, capture_output=True, text=True, check=True )
	except subprocess.CalledProcessError as e:
		# return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]<br/> [ Command: {e.cmd} ]" }
		return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]" }
	except:
		return { "missatge": "Error intern del servidor" }

	output = resultat.stdout



	return { "missatge": output }

