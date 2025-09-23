from flask import render_template, request, session, url_for
from . import marcadors
from decouple import config
import subprocess
import os


@marcadors.route('/marcadors', methods=['GET'])
def fmarcadors():
	if "username" in session:
		return render_template( 'marcadors.html', titol="Marcadors Google Chrome" )
	else:
		return "Accés prohibit."



@marcadors.route('/carregarBookmarksDefecte/')
def carregarBookmarksDefecte():
  rutaApp = os.path.dirname(__file__)
  print( 'rutaApp', rutaApp )
  
  try:
    with open( rutaApp+'/static/Bookmarks', newline='' ) as f:
      textFitxer = f.read()
    #   for row in reader:
    #     llistaHosts.append(row)

    return textFitxer
  except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    return err







@marcadors.route('/getInfoMarcadors', methods=['POST'])
def fgetInfoMarcadors():
	print( "estic a POST de getInfoMarcadors")
	dades = request.get_json() 
	# print("dadesFormulari", dadesFormulari)
	# host = dades['host']
	host="nfs0885-h.asepeyo.site"
	user = dades['user']
	print("dades['user']", user)
	print("dades['host']", host)
	
	try:
		# password = os.getenv("PWDASE")
		# Del fitxer .env llegim el valor de la calu 'entorn'
		password = config('PWDCOS')

	except:
		return { "missatge": "NO s'ha establert PWDASE" }

	cmd = f"cat /export/home/{user}/.config/google-chrome/Default/Bookmarks"
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

	user = dades['user']
	contingut = dades['contingut']

	print("**** CONTINGUT ****\n", contingut, "\n**************")


	rutaDesti = f'/export/home/{user}/.config/google-chrome/Default'
	print( "RUTA DESTI", rutaDesti )
	try:
		host="nfs0885-h.asepeyo.site"
		password = config('PWDCOS')
		cmd = f"echo '{contingut}' > {rutaDesti}/Bookmarks"
		ssh_cmd = f"/bin/sshpass -p {password} ssh -p 22 -l root -o StrictHostKeyChecking=no {host} \"{cmd}\""
		print("SSH_CMD\n", ssh_cmd)

		resultat = subprocess.run( ssh_cmd, shell=True, capture_output=True, text=True, check=True )
		return resultat.stdout
	except subprocess.CalledProcessError as e:
		# return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]<br/> [ Command: {e.cmd} ]" }
		return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]" }
	except Exception as err:
		return { "missatge": f"Error intern del servidor <br>{err}" }
	





@marcadors.route('/postCreateMarcadors', methods=['POST'])
def fPostCreateMarcadors():
	dades = request.get_json() 

	host="nfs0885-h.asepeyo.site"
	user = dades['user']

	rutaApp = os.path.dirname(__file__)
	print( 'rutaApp', rutaApp )

	# llegim el fitxer /static/Bookmarks
	try:
		with open( rutaApp+'/static/Bookmarks', newline='' ) as f:
			textFitxer = f.read()

	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		return err



	rutaDesti = f'/export/home/{user}/.config/google-chrome/Default'
	try:
		password = config('PWDCOS')
		cmd = f"echo '{textFitxer}' > {rutaDesti}/Bookmarks"
		ssh_cmd = f"/bin/sshpass -p {password} ssh -p 22 -l root -o StrictHostKeyChecking=no {host} \"{cmd}\""
		print("SSH_CMD\n", ssh_cmd)

		resultat = subprocess.run( ssh_cmd, shell=True, capture_output=True, text=True, check=True )
		return resultat.stdout
	except subprocess.CalledProcessError as e:
		# return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]<br/> [ Command: {e.cmd} ]" }
		return {"missatge": f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]" }
	except:
		return { "missatge": "Error intern del servidor" }


