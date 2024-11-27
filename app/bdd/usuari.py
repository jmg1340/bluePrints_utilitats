class Usuari:
    def __init__( self, numero, nom, rols ):
        self.numero = numero
        self.nom = nom
        self.rols = rols

    def dadesAGuardar( self ):
        return {
            numero: self.numero,
            nom: self.nom,
            rols: self.rols
        }