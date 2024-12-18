from flask import render_template, request, session, url_for
from . import llistatEstacions
from app import socketioApp
from flask_socketio import emit
from .clHost import Host
import ipaddress
import concurrent.futures 
import subprocess
import time
import asyncio
import paramiko
from decouple import config



@llistatEstacions.route('/llistatEstacions', methods=['GET'])
def fllistatEstacions():
	if "username" in session:
		return render_template( 'llistat.html', titol="Llistat informació estacions plataforma" )
	else:
		return "Accés prohibit."



@socketioApp.on('arranca_processos')
def ejecutarProcessos( strAdreçaXarxa ):

    rangIPs = ipaddress.ip_network( strAdreçaXarxa )
    hostsXarxa = rangIPs.hosts()    # hostsXarxa es un objecte "generator"
    llistaHostsXarxa = [i for i in hostsXarxa] # conversio de objecte "generator" a objecte "llista"
    llistaHostsXarxa = llistaHostsXarxa[100:103]

    # totalIPs = rangIPs.num_addresses
    totalIPs = len( llistaHostsXarxa )
    socketioApp.emit('infoTotalIPs', totalIPs)

    asyncio.run(executaProcessosAssincrònics(llistaHostsXarxa))

async def executaProcessosAssincrònics( hostsXarxa ):
    print( "\n*** ARRANCA PROCESSOS ***\n" )
    print( "Nº de HOSTS: ", len(hostsXarxa) )
    
    try:

        # executor = ThreadPoolExecutor( max_workers = 10 )
        with concurrent.futures.ThreadPoolExecutor() as executor:
            password = config('PWDASE')
            print ("PASSWORD:", password )

            ssh_clients = []
            for ip in hostsXarxa:
                ssh_client = paramiko.SSHClient()
                # print( "ssh_client" )
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                # print( "ssh_client.set_missing_host_key_policy" )
                ssh_client.load_system_host_keys()
                # print( "ssh_client.load_system_host_keys" )
                print( "ip", ip )
                try:
                    ssh_client.connect(hostname=str(ip), port=22, username='admin', password=password)
                except paramiko.ssh_exception.NoValidConnectionsError as e:
                    print("username not exists", e)
                except paramiko.ssh_exception.AuthenticationException as e:
                    print("passwd not correct", e)
                except Exception as e:
                    print("*** Caught exception: %s: %s" % (e.__class__, e))
                    # traceback.print_exc() 

                print( "ssh_client.connect" )
                ssh_clients.append(ssh_client)

            print( "Llista SSH_CLIENTS feta")

            async with concurrent.futures.ThreadPoolExecutor() as executor:
                tasks = []
                for ip, ssh_client in zip(hostsXarxa, ssh_clients):
                    tasks.append(executor.submit(imprimirHost, ip, ssh_client))

                for task in concurrent.futures.as_completed(tasks):
                    ip, output = task.result()
                    print(f"Output from {ip}: {output}")

            for ssh_client in ssh_clients:
                ssh_client.close()
            
            
            
            # tasks = []
            # for objIp in hostsXarxa:
            #     strIP = str( objIp )
            #     tasks.append( executor.submit( imprimirHost, strIP ))
            #     time.sleep(0.0)

            # print( "Esperant que les tasques s'acabin" )
            # for task in concurrent.futures.as_completed(tasks):
            #     ip, output = await task.result()
            #     print(f"Tasca acabada, {ip}: {output}")

    except Exception as e:
        print( f"Error amb el map:\n{e}" )

    print( "**** Totes les tasques fetes ****" )



def imprimirHost( ip, ssh_client ):
    try:
        objH = Host(ip, ssh_client)
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
