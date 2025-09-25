from . import jmgFuncions as fn
import re
import subprocess

class Host:
  def __init__( self, host ):
    self.host = host


  def comprovarPing( self ):
    """
    Lanza un único ping a una IP.
    Devuelve True si la IP responde, si no, False.
    """
    # Comando para Linux. -c 1 = 1 paquete, -W 1 = 1 segundo de timeout.
    comando = ["/bin/ping", "-c", "1", "-W", "1", self.host ]
    
    proceso = subprocess.Popen(
        comando,
        # Descartamos la salida para ser más eficientes
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Esperamos a que el proceso termine
    proceso.communicate()
    
    # El resultado es True si el comando tuvo éxito (código de salida 0)
    return proceso.returncode == 0





  # METODES PER RECUPERAR LA INFORMACIÓ DELS HOSTS

  def getNomHost(self):
    resultat = fn.obtenirInfo( self.host, "hostname" )
    return resultat
    # if resultat[0] == 0:
    #   strResultat = resultat[1]
    #   if "\n" in strResultat: 
    #     return strResultat.split("\n")[1]
    #   else:
    #     return strResultat
    # else:
    #   return "status:"+str(resultat[0])


  def getUsuari( self ):
    resultat = fn.obtenirInfo( self.host, "w" )

    arr = resultat.split("\n")
    if len( arr ) > 2:
      return arr[2][0:9].strip()
    else:
      return "--"

    # usuaris = set()
    # if resultat[0] == 0:
    #   liniesResultat = resultat[1].split("\n")

    #   liniesResultat.pop(0)
    #   liniesResultat.pop(0)

    #   for linia in liniesResultat:
    #     usuaris.add( linia[0:9].strip() )

    #   return ",".join( dada for dada in usuaris )
    # else:
    #   return ("--")


  def getIpMac(self):
    resultat = fn.obtenirInfo( self.host, "ifconfig eth0" )
    
    #   linia = fn.extraureLinia( resultat[1], 2 )
    #   resultatRe = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", linia)
    #   ip =  resultatRe.group() 

    linia = fn.extraureLinia( resultat, 3 )
    resultatRe = re.search(".{2}:.{2}:.{2}:.{2}:.{2}:.{2}", linia)
    mac = resultatRe.group() 


    linia = fn.extraureLinia( resultat, 5 )
    paquets = linia.strip()

    return (mac, paquets)
    


  def getServidorNFS( self ):
    resultat = fn.obtenirInfo( self.host, "/bin/cat /proc/mounts | /bin/grep nfs | /usr/bin/head -n 1 | /usr/bin/cut -d ':' -f 1")
    if resultat != None: 
      return resultat
    else:
      return "--"



  def getSpeed( self ):
    resultat = fn.obtenirInfo( self.host, "ethtool eth0" )
    resultatRe = re.search("Speed.*\n", resultat)
    if resultatRe != None: 
      return resultatRe.group().strip().replace("Speed: ", "")
    else:
      return "--"


  def getConnectatA( self ):
    resultat = fn.obtenirInfo( self.host, "lldpctl" )
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


  def getInfoPc( self ):
    resultat = fn.obtenirInfo( self.host, "dmidecode -t system" )
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


  def getInfoMonitor( self ):
    resultat = fn.obtenirInfo( self.host, "hwinfo --monitor" )
    liniesResultat = resultat.split("\n")

    serialID= "--"

    for linia in liniesResultat:
      resultatRe = re.search("^Serial ID", linia.strip() )
      if resultatRe != None:
        serialID = linia.strip().replace("Serial ID:", "").strip()

    return( serialID  )










  def getArrayInfoHost( self ):
    print( "\n" + 50*"*" )
    print( "Recopilacio dades per a IP: {}".format( self.host ) )

    nom = objH.getNomHost()
    print ( "{} - NOM: {}".format( ip, nom ) )
    ipmacpaq = objH.getIpMac()
    print ( "{} - IPMACPAQ: {}".format( ip, ipmacpaq ) )
    speed = objH.getSpeed()
    print ( "{} - SPEED: {}".format( ip, speed ) )
    connectatA = objH.getConnectatA()
    print ( "{} - CONNECTAT_A: {}".format( ip, connectatA ) )
    infoPc = objH.getInfoPc()
    print ( "{} - INFO_PC: {}".format( ip, infoPc ) )
    infoMonitor = objH.getInfoMonitor()
    print ( "{} - INFO_MONITOR: {}".format( ip, infoMonitor ) )
    user = objH.getUsuari()
    print ( "{} - USER: {}".format( ip, user ) )

    return [nom, ipmacpaq, speed, connectatA, infoPc, infoMonitor, user]



  def __str__( self ):
    return f"objecte Host ({self.host}) creat."