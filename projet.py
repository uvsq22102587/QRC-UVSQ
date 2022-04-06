import PIL as pil
from PIL import Image
from PIL import ImageTk 


def saving(matPix, filename):
    #sauvegarde l'image contenue dans matpix dans le fichier filename
	#utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)

def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
					  #l'image en noir et blanc
    toLoad = pil.Image.open(filename)
    mat = [[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat


def creerQRC():
    qRCode = [[1 for i in range(25)] for i in range(25)]
    # création des carrées pleins
    y = - 1
    for i in range(0, 7):
        x = 0
        y += 1
        for j in range(0, 7):
            qRCode[y][x] = 0
            x += 1
    y = -1
    for i in range(0, 7):
        x = 18
        y += 1
        for j in range(0, 7):
            qRCode[y][x] = 0
            x += 1
    y = 17
    for i in range(0, 7):
        x = 0
        y += 1
        for j in range(0, 7):
            qRCode[y][x] = 0
            x += 1
    # création des lignes en poitillés
    for i in range(6, 18, 2):
        qRCode[6][i] = 0
    for i in range(6, 18, 2):
        qRCode[i][6] = 0
    # création des lignes blanche intra-carrées
    for i in range(1, 6):
        # ligne du haut
        qRCode[1][i] = 1
    for i in range(1, 6):
        #ligne de gauche
        qRCode[i][1] = 1
    for i in range(1, 6):
        # ligne de droite
        qRCode[i][5] = 1
    for i in range(1, 6):
        # ligne du bas
        qRCode[5][i] = 1
    # Deuxième carré lignes blanches
    for i in range(19, 24):
        # ligne du haut
        qRCode[1][i] = 1
    for i in range(1, 6):
        # ligne de gauche
        qRCode[i][19] = 1
    for i in range(1, 6):
        # ligne de droite
        qRCode[i][23] = 1
    for i in range(19, 24):
        # ligne du bas
        qRCode[5][i] = 1
    # Troisième carré lignes blanches
    for i in range(1, 6):
        # ligne du haut
        qRCode[19][i] = 1
    for i in range(19, 24):
        # ligne de gauche 
        qRCode[i][1] = 1
    for i in range(19, 24):
        # ligne de droite
        qRCode[i][5] = 1
    for i in range(1, 6):
        # ligne du bas
        qRCode[23][i] = 1
    return qRCode


def rotationQRC(matrice):
    matrice1 = [[1 for i in range(25)] for j in range(25)]
    for i in range(25):
        ligne = []
        for j in range(25):
            ligne.append(matrice[j][i])
        ligne.reverse()
        matrice1[i] = ligne
    return matrice1

def extraireCoin(matrice, taillecoin):
    """Fonction qui prend une matrice de pixel et qui en sort les 4 coins sous forme de liste."""
    coinGaucheHaut = [[matrice[i][j] for i in range(0, taillecoin)] for j in range(0, taillecoin)]
    coinDroitHaut = [[matrice[i][j] for i in range(0, taillecoin)] for j in range(len(matrice) - taillecoin, len(matrice))]
    coinGaucheBas = [[matrice[i][j] for i in range(len(matrice) - taillecoin, len(matrice))] for j in range(0, taillecoin)]
    return (coinGaucheHaut, coinDroitHaut, coinGaucheBas)

def verifQRC(matrice):
    """Fonction qui compare les coins d'une matrice de pixels et qui les compare à un QRCODE.
    Si la matrice est bien un QRcode, elle le tourne pour qu'il puisse être dans le bon sens."""
    averif = extraireCoin(matrice, 7)
    temoin = extraireCoin(creerQRC(), 7)
    while averif != temoin:
        matrice = rotationQRC(matrice)
        averif = extraireCoin(matrice, 7)
    return matrice


def verifLignesQRC(matrice):
    check = True
    for i in range(6, 18):
        if matrice[6][i] != (i % 2):
            check = False
    for i in range(6, 18):
        if matrice[i][6] != (i % 2):
            check = False
    return check

verifLignesQRC(loading("qr_code_ssfiltre_ascii_rotation.png"))


def correctionHamming(bits):
    # calcul bits de controle
    p1 = bits[2] ^ bits[4] ^ bits[6]
    p2 = bits[2] ^ bits[5] ^ bits[6]
    p3 = bits[4] ^ bits[5] ^ bits[6]
    # position erreur
    num = int(p1 != bits[0]) + int(p2 != bits[1])*2 + int(p3 != bits[3]) * 4
    if num in [3, 5, 6, 7]:
        # on remplace bits[num-1] par 0 s'il valait 1 et par 1 si il valait 0
        bits[num-1] = int(not bits[num - 1])
        print("corection d'un pixel corrompu en position " + str(num) + "\n")
        return [bits[2], bits[4], bits[5], bits[6]]
    else:
        return [bits[2], bits[4], bits[5], bits[6]]

def HammingRead(matrice):
    """Fonction qui prend une matrice de pixels et la lit en effectuant la vérification via le code de Hamming."""
    donnees = []
    bloc = []
    etage = 0
    while len(donnees) < 32:
        for i in range(0, 28):
            if i % 2 == 0:
                y = len(matrice) - 1 - etage * 2
            else:
                y = len(matrice) - 2 - etage * 2
            x = (len(matrice) - 1) - (i // 2)
            bit = matrice[y][x]
            bloc.append(bit)
            if len(bloc) == 7:
                bloc = correctionHamming(bloc)
                donnees.extend(bloc)
                bloc = []
        etage += 1
        for i in range(0, 28):
            if i % 2 == 0:
                y = len(matrice) - 1 - etage * 2
            else:
                y = len(matrice) - 2 - etage * 2
            x = 11 + (i // 2)
            bit = matrice[y][x]
            bloc.append(bit)
            if len(bloc) == 7:
                bloc = correctionHamming(bloc)
                donnees.extend(bloc)
                bloc = []
        etage += 1
    return donnees


def to_ascii(data:list):
    """Fonction qui prend une liste de bits et qui les convertit en caractères ascii."""
    ascii = ""
    resultat = ""
    for i in range(0, len(data)):
        ascii += str(data[i])
        if len(ascii) == 8:
            resultat += chr(int(ascii, 2))
            ascii = ""
    resultat += ascii
    return resultat

print(to_ascii(HammingRead(loading("qr_code_damier_ascii.png"))))