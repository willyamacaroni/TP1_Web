class Compte:
    def __init__(self, pIdentifiant, pMotDePasse, pNomUtilisateur, pAdmin):
        self.identifiant = pIdentifiant
        self.motDePasse = pMotDePasse
        self.nomUtilisateur = pNomUtilisateur
        self.admin = pAdmin

class Produit:
    def __init__(self, lstAttributs):
        self.id = lstAttributs[0]
        self.nom = lstAttributs[1]
        self.description = lstAttributs[2]
        self.stock = lstAttributs[3]
        self.coutant = lstAttributs[4]
        self.format = lstAttributs[6]
        self.prix = lstAttributs[7]
        self.type = lstAttributs[9]
        self.taxableFed = bool(lstAttributs[10])
        self.taxableProv = bool(lstAttributs[11])