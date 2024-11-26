from flask import render_template, request, session, url_for
from . import portes
from decouple import config



@portes.route('/getPortes', methods=['GET'])
def fFormulariEstacio():
	if "username" in session:
		return render_template( 'portes.html', titol="Accessos a portes" )
	else:
		return "Accés prohibit."

	
'''
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
	output = output.replace('\n', '<br/>')
	output = output.replace(' ', '&nbsp;')
 
	return { "missatge": output }

'''



