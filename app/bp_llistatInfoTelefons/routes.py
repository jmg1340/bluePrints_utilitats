from flask import render_template, request, session, url_for
from . import llistatTelefons
from app import socketioApp
from flask_socketio import emit
import ipaddress
import nmap
from bs4 import BeautifulSoup
import requests


@llistatTelefons.route('/llistatTelefons', methods=['GET'])
def fllistatTelefons():
    # ... tu código actual (sin cambios)
    if "username" in session:
        return render_template('llistatTelefons.html', titol="Llistat informació telèfons")
    else:
        return "Accés prohibit."


@socketioApp.on('arranca_proces_info_telefons')
def arranca_proces_info_telefons(strAdreçaXarxa): # <--- 1. Ya no es 'async def'
    print("estic a 'arranca_proces_info_telefonss'")
    
    nm = nmap.PortScanner()
    nm.scan(hosts=strAdreçaXarxa, arguments='-p 80')
    arrTotsElsHosts = nm.all_hosts()

    # Enviamos el total de IPs al cliente para la barra de progreso
    socketioApp.emit('infoTotalIPs', len(arrTotsElsHosts))
    
    
    online_hosts = []
    for host in arrTotsElsHosts:
        host_info={}

        if nm[host].state() == 'up':
            host_info={"ip": host}

            if 'tcp' in nm[host] and 80 in nm[host]['tcp'] and nm[host]['tcp'][80]['state'] == 'open':
                host_info['port_80_open'] = True

                # Si el puerto 80 está abierto, intentamos hacer scraping
                #print(f"[*] Puerto 80 abierto en {host}. Intentando scraping...")
                scraped_info = scrape_device_info(host)
                host_info.update(scraped_info) # Unimos la info del scraping a la del host

            else:
                host_info['port_80_open'] = False


            socketioApp.emit('recepcioDadesTelefons', host_info)



        

def scrape_device_info(ip):
    """
    Extrae información específica de la página web de un dispositivo.
    Maneja redirecciones 'meta refresh'.
    """
    scraped_data = {
        'serial_number': 'N/A',
        'web_mac': 'N/A',
        'host_name': 'N/A',
        'phone_directory': 'N/A',
        'model': 'N/A'
    }

    # La URL inicial
    base_url = f"http://{ip}"

    try:
        # Petición inicial
        response = requests.get(base_url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- INICIO DE LA MODIFICACIÓN: DETECCIÓN DE REDIRECCIÓN ---

        # Buscamos una etiqueta <meta> de tipo refresh
        meta_refresh = soup.find('meta', attrs={'http-equiv': 'REFRESH'})

        if meta_refresh:
            #print(f"  [i] Detectada redirección en {ip}. Siguiendo enlace...")
            # Extraemos el contenido del atributo 'content'
            content = meta_refresh.get('content')
            # La URL está después de 'URL='
            redirect_url_part = content.split('URL=')[1]

            # Construimos la URL completa para la segunda petición
            final_url = f"{base_url}/{redirect_url_part}"

            # Hacemos una segunda petición a la URL final
            response = requests.get(final_url, timeout=5)
            response.raise_for_status()


            # Forzamos la codificación también en la segunda respuesta
            response.encoding = 'utf-8'


            # Actualizamos el objeto soup con el contenido de la página real
            soup = BeautifulSoup(response.text, 'html.parser')

        # --- FIN DE LA MODIFICACIÓN ---

        # El resto del código de scraping funciona sobre el 'soup' correcto
        # Ahora cada clave apunta a una tupla de posibles nombres
        fields_map = {
            "serial_number": ("Número de serie", "N.º de serie", "Número de sèrie"),
            "web_mac": ("Dirección MAC", "Adreça MAC"), # Usamos una tupla con un solo elemento
            "host_name": ("Nombre de host", "Nom de host"),
            "phone_directory": ("N.º directorio telefónico", "N.º de directorio telefónico", "Número de directori telefònic"),
            "model": ("N.º de modelo", "Número de model")
        }

        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 1:
                key_text = cells[0].get_text(strip=True)

                # Iteramos sobre nuestro mapa para encontrar una coincidencia
                for internal_key, possible_names in fields_map.items():
                    if key_text in possible_names:
                        value_text = cells[-1].get_text(strip=True)
                        scraped_data[internal_key] = value_text
                        # Rompemos el bucle interior una vez que encontramos una coincidencia para esta fila
                        break


    except Exception as e:
        print(f"  [!] Ocurrió un error al procesar {ip}: {e}")

    return scraped_data
