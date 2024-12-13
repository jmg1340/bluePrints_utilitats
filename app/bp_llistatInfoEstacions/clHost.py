import re
import os
import subprocess
from decouple import config

class Host:
  def __init__( self, host ):
    self.host = host


  def comprovarPing( self ):
    try:
      return hostUp( self.host )
    except:
      print("FALLA A comprovarPing")






  def getNomHost(self):
    try:
      resultat = obtenirInfo( self.host, "hostname" )
      print( "getNomHost - resultat: ", resultat )
      if True:
        strResultat = resultat
        if "\n" in strResultat: 
          return strResultat.replace( "\n", "" )
        else:
          return strResultat
      else:
        return "status:"+str(resultat)

    except :    
      print("getNomHost: EXCEPCIO")
      return "getNomHost: EXCEPCIO"
      

  def getUsuari( self ):
    try:
      resultat = obtenirInfo( self.host, "w" )

      usuaris = set()
      if True:
        liniesResultat = resultat.split("\n")

        liniesResultat.pop(0)
        liniesResultat.pop(0)

        for linia in liniesResultat:
          usuaris.add( linia[0:9].strip() )

        return ",".join( dada for dada in usuaris )
      else:
        return ("--")
    except:
      print ("FALLA A getUsuari")




  def getIpMac(self):
    try:
      resultat = obtenirInfo( self.host, "ifconfig eth0" )
      if True:

        linia = extraureLinia( resultat, 2 )
        resultatRe = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", linia)
        ip =  resultatRe.group() 

        linia = extraureLinia( resultat, 3 )
        resultatRe = re.search(".{2}:.{2}:.{2}:.{2}:.{2}:.{2}", linia)
        mac = resultatRe.group() 

        linia = extraureLinia( resultat, 5 )
        paquets = linia.strip()

        return ((ip, mac, paquets))
      else:
        return (( "--", "--", "--"))
    except:
      print ("FALLA A getIpMac")


  def getSpeed( self ):
    try:
      resultat = obtenirInfo( self.host, "ethtool eth0" )
      resultatRe = re.search("Speed.*\n", resultat)
      if resultatRe != None: 
        return resultatRe.group().strip().replace("Speed: ", "")
      else:
        return "--"
    except:
      print ("FALLA A getSpeed")


  def getConnectatA( self ):
    try:
      resultat = obtenirInfo( self.host, "lldpctl" )
      liniesResultat = resultat.split("\n")

      sysname = "--"
      sysdescr= "--"
      portdescr= "--"

      for linia in liniesResultat:
        resultatRe = re.search("^SysName", linia.strip() )
        if resultatRe != None:
          sysname = linia.strip().replace("SysName:", "").strip()

        resultatRe = re.search("^SysDescr", linia.strip() )
        if resultatRe != None:
          sysdescr = linia.strip().replace("SysDescr:", "").strip()

        resultatRe = re.search("^PortDescr", linia.strip() )
        if resultatRe != None:
          portdescr = linia.strip().replace("PortDescr:", "").strip()


      return( (sysname, sysdescr, portdescr)  )
    except:
      print ("FALLA A getConnectatA")



  def getInfoPc( self ):
    try:
      resultat = obtenirInfo( self.host, "dmidecode -t system" )
      liniesResultat = resultat.split("\n")

      manufacturer = "--"
      version= "--"
      serialnumber= "--"

      for linia in liniesResultat:
        resultatRe = re.search("^Manufacturer", linia.strip() )
        if resultatRe != None:
          manufacturer = linia.strip().replace("Manufacturer:", "").strip()

        resultatRe = re.search("^Version", linia.strip() )
        if resultatRe != None:
          version = linia.strip().replace("Version:", "").strip()

        resultatRe = re.search("^Serial Number", linia.strip() )
        if resultatRe != None:
          serialnumber = linia.strip().replace("Serial Number:", "").strip()


      return( (manufacturer, version, serialnumber)  )
    except:
      print ("FALLA A getInfoPc")


  def getInfoMonitor( self ):
    try:
      resultat = obtenirInfo( self.host, "hwinfo --monitor" )
      liniesResultat = resultat.split("\n")

      serialID= "--"

      for linia in liniesResultat:
        resultatRe = re.search("^Serial ID", linia.strip() )
        if resultatRe != None:
          serialID = linia.strip().replace("Serial ID:", "").strip()

      return( serialID  )
    except:
      print ("FALLA A getInfoMonitor")











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




# obtenir informacio del sistema
def obtenirInfo ( host, instruccio ):
  password = config('PWDASE')
  ssh_cmd = f"sshpass -p {password} ssh -p 22 -l root -o StrictHostKeyChecking=no " + host + " '" + instruccio + "'"
  # print( ssh_cmd )

  # status, output = subprocess.getstatusoutput(ssh_cmd)
  # return (status, output)
  try:
    output = subprocess.check_output(ssh_cmd, shell=True)
    # print("OBTENIR_INFO - OUTPUT\n", output.decode(), "\n")
    return output.decode() 
  except subprocess.CalledProcessError as e:
      print(f"obtenirInfo: Command failed with return code {e.returncode}")
  except :    
    print(f"obtenirInfo: EXCEPCIO")


# extraure una linia d'un text amb caracters de retorn
def extraureLinia ( text, numLinia ):
  linies = text.split("\n")
  return linies[ numLinia - 1 ]


# comprovar si el host te connectivitat
def hostUp(hostname, waittime=1000):
  '''Function returns True if host IP returns a ping, else False'''
  assert isinstance(hostname, str), \
      "IP/hostname must be provided as a string."
  if os.system("ping -c 3 -W " + str(waittime) + " " + hostname + " > /dev/null 2>&1") == 0:
      HOST_UP = True
  else:
      HOST_UP = False
  return HOST_UP