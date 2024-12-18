from flask import render_template, request, session, url_for
from . import llistatEstacions
from app import socketioApp
from flask_socketio import emit
from .clHost import Host
import ipaddress
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, as_completed, FIRST_EXCEPTION
import subprocess
import time



@llistatEstacions.route('/llistatEstacions', methods=['GET'])
def fllistatEstacions():
	if "username" in session:
		return render_template( 'llistat.html', titol="Llistat informació estacions plataforma" )
	else:
		return "Accés prohibit."



@socketioApp.on('arranca_processos')
def ejecutarProcessos( strAdreçaXarxa ):
    print( "\n*** ARRANCA PROCESSOS ***\n" )
    try:
        # strAdreçaXarxa = "192.168.8.0/23"
        rangIPs = ipaddress.ip_network( strAdreçaXarxa )
        hostsXarxa = rangIPs.hosts()    # hostsXarxa es un objecte "generator"
        llistaHostsXarxa = [i for i in hostsXarxa] # conversio de objecte "generator" a objecte "llista"
        # llistaHostsXarxa = llistaHostsXarxa[100:120]

        # totalIPs = rangIPs.num_addresses
        totalIPs = len( llistaHostsXarxa )
        socketioApp.emit('infoTotalIPs', totalIPs)
        # print("Total IPs:", totalIPs)


        # with ProcessPoolExecutor(max_workers=30) as executor:
        with ThreadPoolExecutor(max_workers=30) as executor:
            tasks = []
            for objIp in llistaHostsXarxa:
                strIP = str( objIp )
                task = executor.submit( imprimirHost, strIP )
                tasks.append( task )
                # tasks.append( {"ip":strIP, "tasca": task} )
                # time.sleep(0.5)

            print( "Esperant que les tasques s'acabin" )
            
            # for ip_task in as_completed(task["tasca"] for task in tasks):
            #     try:
            #         data = ip_tasca["tasca"].result()
            #     except Exception as exc:
            #         print( f'{ip_tasca["ip"]} generated an exception: {exec}' )
            #     else:
            #         print( f'{ip_tasca["ip"]} tasca completada amb resultat: {data}' )



            fetesNoFetes = wait( tasks , return_when=FIRST_EXCEPTION)
            print( f"taskes acabades: {len(fetesNoFetes[0])}",  f"taskes NO acabades: {len(fetesNoFetes[1])}")
            
            # for task in as_completed(tasks):
            #     print("TASCA COMPLETADA:", task.result()) # result is None in this case



    except Exception as e:
        print( f"EXCEPCIO ejecutarProcessos: {e}" )

    print( "**** Totes les tasques fetes ****" )



def imprimirHost( ip ):
    try:
        objH = Host(ip)
        # print( "COMPROVAR PING: ", objH.comprovarPing() )
        if objH.comprovarPing() == True:
            #   if objH.getNomHost().startswith("status") == False:
            #   tempsIniciDadesHost = time.time()

            if objH.getNomHost() != "invalid host":
                # print("\n================================")
                nom = objH.getNomHost()
                # print ("NOM", nom)
                ipmacpaq = objH.getIpMac()
                # print( "ipmacpaq", ipmacpaq)
                servidorNFS = objH.getServidorNFS()
                # print( "servidorNFS", servidorNFS )
                speed = objH.getSpeed()
                # print( "speed", speed )
                connectatA = objH.getConnectatA()
                # print( "connectatA", connectatA)
                infoPc = objH.getInfoPc()
                # print( "infoPc", infoPc)
                infoMonitor = objH.getInfoMonitor()
                # print( "infoMonitor", infoMonitor)
                user = objH.getUsuari()
                # print( "user", user)
                # print("================================\n")

                arr = [
                    ip, 
                    nom, 
                    user or "", 
                    infoPc[0] + " - " + infoPc[1] or "", 
                    infoPc[2] or "", 
                    infoMonitor or "", 
                    servidorNFS, 
                    ipmacpaq[1], 
                    speed, 
                    ipmacpaq[2], 
                    connectatA[0] or "", 
                    connectatA[2]
                ]
                # print("arr", arr)
                socketioApp.emit('recepcioDades', arr)
            
            else:
                ''' fa pinta de que sigui algo diferent a una estacio de treball '''
                socketioApp.emit('recepcioDades', "")
                
        else:
            # print( "{}: no respon a pings".format( ip ) )
            socketioApp.emit('recepcioDades', "")

    except Excetpion as e:
        print ( f"s'ha produit el error\n{e}" )
