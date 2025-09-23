from flask import render_template, request, session, url_for
from . import perfils
from decouple import config

import time
import subprocess
import os


@perfils.route('/perfilsNFS', methods=['GET'])
def fFormulariPerfils():
	if "username" in session:
		return render_template( 'perfils.html', titol="ELIMINACIÓ PERIFL al NFS" )
	else:
		return "Accés prohibit."



@perfils.route('/eliminarPerfil', methods=['POST'])
def feliminarPerfil():
	print( "estic a POST de perfilsNFS")
	dadesFormulari = request.get_json() 
	# print("dadesFormulari", dadesFormulari)
	user = dadesFormulari['user']
	srv = dadesFormulari['srv']
	print("dadesFormulari['user']", dadesFormulari['user'])
	print("dadesFormulari['srv']", dadesFormulari['srv'])
	
	if ( user ):
		return { "missatge": eliminar( user, srv ) }
	else:
		return { "missatge": "Falta informar usuari"}
	


@perfils.route('/llistarPerfils', methods=['POST'])
def fllistarPerfils():
	print( "estic a POST de perfilsNFS")
	dadesFormulari = request.get_json() 
	srv = dadesFormulari['srv']
	
	if ( srv ):
		return { "missatge": llistar( srv ) }
	else:
		return { "missatge": "Falta informar el servidor"}
	






def eliminar( user, srv ):

	#comandamentVerificacioExistenciaCarpeta = f'if [ -d /export/home/{user} ] ; then echo "yes" ; else echo "no" ; fi'
	comandamentVerificacioExistenciaCarpeta = f'/bin/ls /export/home/{user}'

	try:
		# password = os.getenv("PWDCOS")

		# Del fitxer .env llegim el valor de la calu 'entorn'
		password = config('PWDCOS')
	except:
		return "*** NO s'ha establert la variable d'entorn PWDCOS ***"


	ssh_cmd1 = f"/usr/bin/sshpass -p {password} ssh -o StrictHostKeyChecking=no root@{srv} '{comandamentVerificacioExistenciaCarpeta}'"
	#ssh_cmd1 = ssh_cmd1.encode('utf-8').strip()
	#print(ssh_cmd1)
	try:
			#status1, output1 = subprocess.getstatusoutput(ssh_cmd1)
			oProcesCompletat = subprocess.run(ssh_cmd1, shell=True, capture_output=True, text=True, check=True)
			print(f"oPC.returncode:  {oProcesCompletat.returncode}")
	except subprocess.CalledProcessError as e:
		stdout_decodificado = oProcesCompletat.stdout.decode('utf-8', errors='replace')
		stderr_decodificado = oProcesCompletat.stderr.decode('utf-8', errors='replace')
		
		if e.returncode == 2:
			return f"\tNO EXISTEIX la carpeta: /export/home/{user} al servidor {srv} \n\n\t{stdout_decodificado}"
		else:
			# return f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]<br/> [ Command: {e.cmd} ]"
			return f"No s'ha pogut executar el comandament:<br/> [ {stderr_decodificado} ]<br/> [ Return code: {e.returncode} ]"
	
	except Exception as err:
		return f"Error intern del servidor al verificar perfil <br>{ err }"



	comandamentEliminacio = f'/bin/rm -rf /export/home/{user}/'
	ssh_cmd = f"/usr/bin/sshpass -p {password} ssh -p 22 -l root -o StrictHostKeyChecking=no {srv} '{comandamentEliminacio}'"
	
	try:
		oProcesCompletat2 = subprocess.run(ssh_cmd,  shell=True, capture_output=True, text=True, check=True)

		# Si el comando tiene éxito, la salida suele estar vacía.
		# Puedes decodificar y mostrar la salida si es necesario.
		stdout_decodificado = oProcesCompletat2.stdout.decode('utf-8', errors='replace')
		stderr_decodificado = oProcesCompletat2.stderr.decode('utf-8', errors='replace')

		if stdout_decodificado:
			print("Salida estándar:", stdout_decodificado)
		if stderr_decodificado:
			print("Salida de error:", stderr_decodificado)


		if oProcesCompletat2.returncode == 0:
			return f"\tPerfil '{user}' ELIMINAT del servidor {srv}"
		else:
			return f"\tNO S'HA POGUT ELIMINAR EL PERFIL '{user}' del servidor {srv}:<br/><br/>{stdout_decodificado}<br/><br/>{stderr_decodificado}"

	except subprocess.CalledProcessError as e:
		# Si el comando devuelve un código de salida de error, se lanzará esta excepción.
		# Decodificamos la salida de error para poder leerla.
		stdout_decodificado = e.stdout.decode('utf-8', errors='replace')
		stderr_decodificado = e.stderr.decode('utf-8', errors='replace')
		# return f"No s'ha pogut executar el comandament:<br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]<br/> [ Command: {e.cmd} ]" 
		return f"No s'ha pogut executar el comandament:<br/> [ {stderr_decodificado} ]<br/> [ Return code: {e.returncode} ]" 
	except Exception as err:
		return f"Error intern del servidor al eliminar perfil: {err}" 




def llistar( srv ):

	#comandamentVerificacioExistenciaCarpeta = f'if [ -d /export/home/{user} ] ; then echo "yes" ; else echo "no" ; fi'
	comandamentVerificacioExistenciaCarpeta = f'/bin/ls /export/home/'

	try:
		# password = os.getenv("PWDCOS")

		# Del fitxer .env llegim el valor de la calu 'entorn'
		password = config('PWDCOS')
	except:
		return "*** NO s'ha establert la variable d'entorn PWDCOS ***"


	ssh_cmd1 = f"/usr/bin/sshpass -p {password} ssh -o StrictHostKeyChecking=no root@{srv} '{comandamentVerificacioExistenciaCarpeta}'"
	#ssh_cmd1 = ssh_cmd1.encode('utf-8').strip()
	#print(ssh_cmd1)
	try:
			#status1, output1 = subprocess.getstatusoutput(ssh_cmd1)
			oProcesCompletat = subprocess.run(ssh_cmd1, shell=True, capture_output=True, text=True, check=True)
			return (f"Perfils de {srv}:<br/><br/> {oProcesCompletat.stdout}")
			
	except subprocess.CalledProcessError as e:
		return f"No s'ha pogut llistar els perfils de {srv}: <br/> [ {e.stderr} ]<br/> [ Return code: {e.returncode} ]"
	
	except:
		return "Error intern del servidor al llistar perfils"








