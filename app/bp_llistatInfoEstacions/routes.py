from flask import render_template, request, session, url_for
from . import llistatEstacions
from app import socketioApp
from flask_socketio import emit
from .clHost import Host
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
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
        hostsXarxa = rangIPs.hosts()
        totalIPs = rangIPs.num_addresses

        socketioApp.emit('infoTotalIPs', totalIPs)

        # print("Total IPs:", totalIPs)

        executor = ThreadPoolExecutor( max_workers = 10 )
        futures = []
        for objIp in hostsXarxa:
            strIP = str( objIp )
            # if strIP > "192.168.8.50" : 
            # print ( f"string IP: {strIP}" )
            futures.append( executor.submit( imprimirHost, strIP ))
            time.sleep(0.0)

        print( "Esperant que les tasques s'acabin" )
        wait( futures )
    except Exception as e:
        print( f"Error amb el map:\n{e}" )

    print( "**** Totes les tasques fetes ****" )



def imprimirHost( ip ):
    try:
        objH = Host(ip)
        if objH.comprovarPing() == True:
            #   if objH.getNomHost().startswith("status") == False:
            #   tempsIniciDadesHost = time.time()

            if objH.getNomHost() != "getNomHost: EXCEPCIO":
                # print("\n================================")
                nom = objH.getNomHost()
                # print ("NOM", nom)
                ipmacpaq = objH.getIpMac()
                # print( "ipmacpaq", ipmacpaq)
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
                    user, 
                    infoPc[0] + " - " + infoPc[1], 
                    infoPc[2], 
                    infoMonitor, 
                    ipmacpaq[0], 
                    ipmacpaq[1], 
                    speed, 
                    ipmacpaq[2], 
                    connectatA[0], 
                    connectatA[2]
                ]

                socketioApp.emit('recepcioDades', arr)
            
            else:
                ''' fa pinta de que sigui algo diferent a una estacio de treball '''
                socketioApp.emit('recepcioDades', "")
                
        else:
            # print( "{}: no respon a pings".format( ip ) )
            socketioApp.emit('recepcioDades', "")

    except Excetpion as e:
        print ( f"s'ha produit el error\n{e}" )
