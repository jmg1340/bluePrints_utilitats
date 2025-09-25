#
# en tu archivo de servidor (.py)
#
from flask import render_template, request, session, url_for
from . import llistatEstacions
from app import socketioApp
from flask_socketio import emit
from .clHost import Host
import ipaddress
# Ya no necesitamos asyncio ni subprocess aquí directamente si clHost lo maneja

@llistatEstacions.route('/llistatEstacions', methods=['GET'])
def fllistatEstacions():
    # ... tu código actual (sin cambios)
    if "username" in session:
        return render_template('llistat.html', titol="Llistat informació estacions plataforma")
    else:
        return "Accés prohibit."


@socketioApp.on('arranca_proces_info_estacions')
def arranca_proces(strAdreçaXarxa): # <--- 1. Ya no es 'async def'
    print("estic a 'ejecutarProcessos'")
    
    rangIPs = ipaddress.ip_network(strAdreçaXarxa)
    hostsXarxa = rangIPs.hosts()
    ips_a_comprobar = [str(i) for i in hostsXarxa]

    print(f"Comprovant {len(ips_a_comprobar)} IPs...")

    # Enviamos el total de IPs al cliente para la barra de progreso
    socketioApp.emit('infoTotalIPs', len(ips_a_comprobar))
    
    # 2. Lanzamos cada comprobación como una tarea de fondo compatible con eventlet
    for ip in ips_a_comprobar:
        socketioApp.start_background_task(recullInformacio, ip)

# Esta función será ejecutada en un hilo "verde" de eventlet
def recullInformacio(ip): # <--- 3. Ya no es 'async def'
    # La lógica interna es la misma, pero sin 'await'
    objHost = Host(ip)
    faPing = objHost.comprovarPing() # <--- 4. Asumimos que clHost.py usa llamadas bloqueantes (p.ej. subprocess.run)
    
    if faPing:
        nomHost = objHost.getNomHost()
        
        if nomHost.startswith("Error"):
            print(f"ip {ip:<13} [🟢 UP]", f"Nom: {nomHost}")
            socketioApp.emit('recepcioDades', "")
            # Puedes decidir si emitir algo en caso de error
        else:
            servidorNFS = objHost.getServidorNFS()
            usuari = objHost.getUsuari()
            mac_paquets = objHost.getIpMac()
            speed = objHost.getSpeed()
            connectatA = objHost.getConnectatA()
            getInfoPc = objHost.getInfoPc()
            ns_monitor = objHost.getInfoMonitor()

            arr = [
                str(ip),
                servidorNFS,
                nomHost,
                usuari or "",
                getInfoPc[1] or "",  # model
                ns_monitor or "",
                mac_paquets[0],      # mac
                speed,
                mac_paquets[1],      # paquets
                connectatA[0] or "", # switch
                connectatA[2]       # port
            ]
            socketioApp.emit('recepcioDades', arr)
            print(f"ip {str(ip):<13} [🟢 UP]", f"HOST: {nomHost}")
    else:
        print(f"ip {str(ip):<13} [🔴 DOWN]")
        # Opcional: emitir un evento para las IPs caídas y que el cliente actualice el progreso
        socketioApp.emit('recepcioDades', "") # Tu código original tenía esto