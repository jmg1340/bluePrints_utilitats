from flask import render_template, request, session, url_for
from . import perfils

import time
import subprocess
import os


@perfils.route('/perfilsNFS', methods=['GET'])
def fFormulariPerfils():
	if "username" in session:
		return render_template( 'perfils.html', titol="ELIMINACIÓ PERIFL als NFS" )
	else:
		return "Accés prohibit."



@perfils.route('/eliminarPerfil', methods=['POST'])
def feliminarPerfil():
	print( "estic a POST de perfilsNFS")
	dadesFormulari = request.get_json() 
	# print("dadesFormulari", dadesFormulari)
	print("dadesFormulari['user']", dadesFormulari['user'])
	print("dadesFormulari['srv']", dadesFormulari['srv'])
	
	return { "missatge": eliminar( dadesFormulari['user'], dadesFormulari['srv'] ) }






def eliminar( user, srv ):

	#comandamentVerificacioExistenciaCarpeta = f'if [ -d /export/home/{user} ] ; then echo "yes" ; else echo "no" ; fi'
	comandamentVerificacioExistenciaCarpeta = f'ls /export/home/{user}'

	try:
		password = os.getenv("PWDCOS")
	except:
		return "*** NO s'ha establert la variable d'entorn PWDCOS ***"


	ssh_cmd1 = f"sshpass -p C0STAISA ssh -o StrictHostKeyChecking=no root@{srv} '{comandamentVerificacioExistenciaCarpeta}'"
	#ssh_cmd1 = ssh_cmd1.encode('utf-8').strip()
	#print(ssh_cmd1)
	try:
			#status1, output1 = subprocess.getstatusoutput(ssh_cmd1)
			oProcesCompletat = subprocess.run(ssh_cmd1, shell=True, stdout=None)
			print(f"oPC.returncode:  {oProcesCompletat.returncode}")
	except Exception as err:
			return f"Hi ha hagut un ERROR al VERIFICAR LA EXISTENCIA DE LA CARPETA:\n\n{err} \n\nINSTRUCCIÓ: {ssh_cmd1}"
	#print( 'status1', status1 )
	#print( 'output1', output1 )

	#output1 = "yes" if "yes" in output1 else "no"
	#if output1 == "yes":
	if oProcesCompletat.returncode == 0:

			comandamentEliminacio = f'rm -rf /export/home/{user}'

			ssh_cmd = f"sshpass -p C0STAISA ssh -p 22 -l root -o StrictHostKeyChecking=no {srv} '{comandamentEliminacio}'"
			try:
					status, output = subprocess.getstatusoutput(ssh_cmd)
			except Exception as e2:
					return f"Hi ha hagut un ERROR a l'executar la INSTRUCCIÓ DE BORRAT DE PERFIL:\n\n{e2}"

			#print( 'status', status )
			#print( 'output', output )


			if status == 0:
					return f"\tPERFIL ELIMINAT del servidor {srv}"
			else:
					return f"\tNO S'HA POGUT ELIMINAR EL PERFIL del servidor {srv}:\n\n\t{output}"

	else:
			return f"\tNO EXISTEIX la carpeta: /export/home/{user} al servidor {srv} \n\n\t{oProcesCompletat.stdout}"


