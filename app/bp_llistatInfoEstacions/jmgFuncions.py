import subprocess
import os



## temps transcorregut entre dos times.time()
def getTempsTranscorregut( tempsInici, tempsFi ):
  tempsTranscorregut_segons = tempsFi - tempsInici
  minuts = int(tempsTranscorregut_segons / 60)
  segons = int(tempsTranscorregut_segons % 60)
  return str(minuts) + " min  " + str(segons) + " seg\n"




# verifica que la IP siguin 4 numeros separats per un .
# retorna true o false
def verificacioIP( ip ):

  llOctets = []
  llista = ip.split(".")

  if len(llista) == 4:
    for octet in llista:
      try:
        entrada = int(octet)
        llOctets.append( entrada )
      except:
        return (False, None)
  else:
    return (False, None)

  return (True, llOctets)


# comprovar si el host te connectivitat
def hostUp(ip):
    '''Devuelve True si la IP responde a ping, si no, False.'''
    
    # Construimos el comando de forma segura
    # -c 1: Enviar solo 1 paquete
    # -W 1: Esperar máximo 1 segundo de respuesta
    comando = f"ping -c 1 -W 1 {ip}"

    proceso = subprocess.run(
        comando,
        stdout= subprocess.DEVNULL,
        stderr= subprocess.DEVNULL 
    )
    
    # Esperamos a que el proceso termine
    proceso.communicate()
    
    # Devolvemos True si el código de salida es 0
    return proceso.returncode == 0


# obtenir informacio del sistema
def obtenirInfo ( ip, instruccio ):
  ssh_cmd = "sshpass -p asepeyoasepeyo ssh -p 22 -l root -o StrictHostKeyChecking=no " + ip + " '" + instruccio + "'"

  try:
    process = subprocess.Popen(
          ssh_cmd,
          shell= True,
          stdout= subprocess.PIPE,
          stderr= subprocess.PIPE
      )
      
    # Esperamos a que el proceso termine
    stdout, stderr = process.communicate()

    # Comprueba si el comando se ejecutó correctamente
    if process.returncode == 0:
      info = stdout.decode().strip()
      # print(f"✅ Éxito en {ip}:\n{info}")
      return info
    else:
      # Si hay un error, lo captura y lo muestra
      error_msg = stderr.decode().strip()
      print(f"❌ Error en {ip}: {error_msg}")
      return f"Error: {error_msg}"

  except FileNotFoundError:
    # Maneja el caso en que sshpass no esté instalado
    print("Error: El comando 'sshpass' no fue encontrado. ¿Está instalado?", file=sys.stderr)
    # Salimos del programa ya que no puede continuar
    sys.exit(1)
  except Exception as e:
    # Captura cualquier otra excepción
    print(f"❌ Error inesperado en {ip}: {e}")
    return f"Error inesperado: {e}"



# extraure una linia d'un text amb caracters de retorn
def extraureLinia ( text, numLinia ):
  linies = text.split("\n")
  return linies[ numLinia - 1 ]
