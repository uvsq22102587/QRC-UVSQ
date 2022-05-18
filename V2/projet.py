###############################################################################
# Projet IN202 - QRCode
# JACQUIN Valentin, PREHAUD Benjamin
# Groupe LDDBI
###############################################################################
import PIL as pil
from PIL import Image
###############################################################################
# Fonction importée faites en TD


def nbrCol(matrice: list):
    return(len(matrice[0]))


def nbrLig(matrice: list):
    return len(matrice)


def saving(matPix: list, filename: str):
    """
    Sauvegarde l'image contenue dans matpix dans le fichier filename
    utiliser une extension png pour que la fonction fonctionne
    sans perte d'informations.
    """
    toSave = pil.Image.new(mode="1", size=(nbrCol(matPix), nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j, i), matPix[i][j])
    toSave.save(filename)


def loading(filename: str):
    """
    Charge le fichier image filename et renvoie une matrice de 0 et de 1 qui
    représente l'image en noir et blanc.
    """
    toLoad = pil.Image.open(filename)
    mat = [[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j] = 0 if toLoad.getpixel((j, i)) == 0 else 1
    return mat


def conversionEntier(liste: list, b: int):
    """
    Fonction qui convertit une liste de bits en un entier.
    """
    res = 0
    liste.reverse()
    for i in range(0, len(liste)):
        res += (liste[i] * (b**i))
    return res


def conversionBase(nombre: int, b: int):
    """
    Fonction qui convertit un nombre en base b.
    """
    if(nombre == 0):
        return [0]
    res = []
    while nombre / b != 0:
        # On ajoute le reste de la division entière par b au résultat
        res.append(nombre % b)
        # On fait la division entière du nombre par b
        nombre = nombre // b
    # La liste est de la forme b^0 * nombre + b^1 * nombre + ... + b^n * nombre
    # On doit donc inverser la liste pour avoir la bon forme
    res.reverse()
    return res


def baseHexa(liste: list):
    """
    Fonction qui convertit un nombre en base 16
    en affichage hexadecimal.
    """
    dico = ["A", "B", "C", "D", "E", "F"]
    liste.reverse()
    res = ""
    for v in liste:
        # Si le chiffre est supérieur à 9, on l'affiche en lettre
        if(v == 10):
            res += dico[0]
        if(v == 11):
            res += dico[1]
        if(v == 12):
            res += dico[2]
        if(v == 13):
            res += dico[3]
        if(v == 14):
            res += dico[4]
        if(v == 15):
            res += dico[5]
        # Sinon on affiche juste le chiffre.
        if(v < 10):
            res += str(v)
        return res


def correctionHamming(bits: list):
    """
    Fonction qui applique la correction de Hamming à une liste de bits.
    La liste de bits doit être de taille 7.
    Cette fonction a été faite en cours.
    """
    assert len(bits) == 7, "La liste de bits doit être de taille 7."
    # calcul bits de controle
    p1 = bits[0] ^ bits[1] ^ bits[2]
    p2 = bits[0] ^ bits[2] ^ bits[3]
    p3 = bits[1] ^ bits[2] ^ bits[3]
    # position erreur
    num = int(p1 != bits[4]) + int(p2 != bits[5]) * 2 + int(p3 != bits[6]) * 4
    if num == 3:
        # erreur sur le bit 1
        bits[0] = int(not bits[0])
    if num == 5:
        # erreur sur le bit 2
        bits[1] = int(not bits[1])
    if num == 6:
        # erreur sur le bit 3
        bits[2] = int(not bits[2])
    if num == 7:
        # erreur sur le bit 4
        bits[3] = int(not bits[3])
    # (Si le nombre num est différent de 4, 5, 6 ou 7, c'est qu'il y a une
    # erreur sur le bit de contrôle. Donc on ne fait rien.)
    # On retourne la liste de bits sans les bits de controle
    return bits[:4]
###############################################################################


def creerQRC():
    """
    Fonction qui crée un QRCode vierge.
    """
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
        # ligne de gauche
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
    # On pourrait plus simplement créer une matrice de QRCode vide qu'on
    # chargerait à chaque fois.
    return qRCode


def rotationQRC(matrice: list):
    """
    Fonction qui tourne un QRC de 90° dans le sens horaire.
    """
    matrice1 = [[1 for i in range(25)] for j in range(25)]
    for i in range(25):
        ligne = []
        for j in range(25):
            ligne.append(matrice[j][i])
        ligne.reverse()
        matrice1[i] = ligne
    return matrice1


def extraireCoin(matrice: list, taillecoin: int):
    """
    Fonction qui prend une matrice de pixel et qui en sort les 3 coins
    sous forme de liste.
    """
    # Pour le coin gauche haut on prend les premiers éléments de la première
    # ligne puis de la deuxième, jusqu'à arriver à la ligne notée 
    # par la variable taille coin. 
    # Le nombre d'éléments dépendra de la variable taillecoin.
    coinGaucheHaut = [
        [matrice[i][j] for i in range(0, taillecoin)]
        for j in range(0, taillecoin)
        ]
    # Pour le coin droite haut on commence par les premiers élement de la 
    # première ligne.
    coinDroitHaut = [
        [matrice[i][j] for i in range(0, taillecoin)]
        for j in range(len(matrice) - taillecoin, len(matrice))
        ]
    # Pour le coin gauche bas on commence par les élements de la dernière
    # ligne - taille coin jusqu'à la dernière ligne.
    coinGaucheBas = [
        [matrice[i][j] for i in range(len(matrice) - taillecoin, len(matrice))]
        for j in range(0, taillecoin)
        ]
    return (coinGaucheHaut, coinDroitHaut, coinGaucheBas)


def verifQRC(matrice: list):
    """
    Fonction qui compare les coins d'une matrice de pixels et qui les compare
    à un QRCODE.
    Si la matrice est bien un QRcode, elle le tourne pour qu'il puisse
    être dans le bon sens.
    """
    # Averif contient la liste des trois coins de notre image.
    averif = extraireCoin(matrice, 7)
    # Temoin contient la liste de trois coins d'un QRC dans le bon sens.
    # Il va nous servir de témoin par rapport aux trois coins de notre image
    # pour savoir si la matrice est un QRC ou pas.
    temoin = extraireCoin(creerQRC(), 7)
    # Compteur va permettre de compter le nombre de rotation qu'on fait
    # Si il est superieur à 4, c'est que l'image n'est pas un QRCode.
    compteur = 0
    while averif != temoin:
        matrice = rotationQRC(matrice)
        averif = extraireCoin(matrice, 7)
        compteur += 1
        assert compteur < 4, "La matrice n'est pas un QRCode"
    return matrice


def verifLignesQRC(matrice: list):
    """
    Fonction qui vérifie les lignes en pointillés
    caractéristique d'un QRC sur une matrixe de pixels.
    """
    check = True
    for i in range(6, 18): # on parcours la ligne verticale.
        # Si i est pair, la case doit être noire.
        # Si i est impair, la case doit être blanche.
        # Sinon, on change la valeur de check.
        if matrice[6][i] != (i % 2):
            check = False
    # On fait la même chose pour la ligne horizontale.
    for i in range(6, 18):
        if matrice[i][6] != (i % 2):
            check = False
    return check


def gestionHamming(donnees: list):
    """
    Fonction qui applique la correction de Hamming sur chacun
    des bloc de 7 bits de la liste données.
    """
    sousDonnees, donneesFinale = [], []
    # donnees est organisée en bloc de 7 bits.
    # Classés eux même par deux (Deux bloc de 7 bits ensemble).
    # Donc pour chaque sous list de 2 bloc, on applique la correction
    # aux deux bloc qui y sont rangés.
    for j in range(0, len(donnees)):
        for i in range(0, 2):
            # On fait la correction de Hamming sur le bloc correspondant.
            sousDonnees.append(correctionHamming(
                donnees[j][0 + i * 7:7 + i * 7])
                )
        # On ajoute les deux blocs corrigé dans la liste finale.
        donneesFinale.append(sousDonnees)
        sousDonnees = []
    return donneesFinale


def filtre(matrice: list):
    """
    Fonction qui vérifie le type de filtre et qui l'applique
    aux pixels du QRC.
    """
    # Le filtre est stocké dans les pixels 22.8 et 23.8
    filtre = (matrice[22][8] << 1) | (matrice[23][8])
    # On initialise la matrice de Filtre
    matriceFiltre = [[0 for j in range(0, 14)] for i in range(0, 16)]
    if filtre == 0:
        return matrice
    # En fonction du filtre, la matrice filtre va être remplie
    elif filtre == 1:
        # 01 = Damier
        for i in range(0, 16):
            for j in range(0, 14):
                if (i + j) % 2 == 1:
                    matriceFiltre[i][j] = 1
    elif filtre == 2:
        # 10 = Lignes horizontales alternées noires et blanches
        for i in range(0, 16):
            for j in range(0, 14):
                if i % 2 == 1:
                    matriceFiltre[i][j] = 1
    elif filtre == 3:
        # 11 = Lignes verticales alternées noires et blanches
        for i in range(0, 16):
            for j in range(0, 14):
                if j % 2 == 1:
                    matriceFiltre[i][j] = int(not matriceFiltre[i][j])
    for i in range(len(matriceFiltre)):
        # On applique le filtre sur la matrice du QRC
        for j in range(len(matriceFiltre[0])):
            x1, y1 = len(matrice[0]) - 1, len(matrice) - 1
            x2, y2 = len(matriceFiltre[0]) - 1, len(matriceFiltre) - 1
            # On fait un XOR entre les deux matrices
            matrice[y1 - i][x1 - j] = matrice[y1 - i][x1 - j] ^ \
                matriceFiltre[y2 - i][x2 - j]
    return matrice


def rawRead(matrice: list, nbrBloc: int):
    """
    Fonction qui prend une matrice de pixels et la lit sans effectuer
    la vérification via le code de Hamming ni le filtre.
    """
    donnees = []
    etage = 0
    # On lit tous les blocs (maximum 16)
    while len(donnees) <= 16 * 14:
        # On fait le "zigzag" pour lire les données
        for i in range(0, 28):
            # Si on est sur les bits pairs (i % 2 = 0)
            # le y est le plus grand (len(matrice) - 1)
            if i % 2 == 0:
                y = len(matrice) - 1 - etage * 2
            # Sinon on est sur les bits impairs (i % 2 = 1)
            # le y est le plus grand - 1 (len(matrice) - 2)
            else:
                y = len(matrice) - 2 - etage * 2
            # La variable étage va permettre de savoir si on est sur
            # quel étage de bloc on est.
            # Pour chaque étage on enlève 2 à l'indice y
            x = (len(matrice) - 1) - (i // 2)
            # X varie entre 11 et 28 à chaque fois que deux bits sont
            # lus, on enlève 1 à x.
            bit = matrice[y][x]
            donnees.append(bit)
            # On ajoute le bit à la liste stockage de données
        # On a lu un étage de bloc, on passe à l'étage suivant
        etage += 1
        for i in range(0, 28):
            if i % 2 == 0:
                y = len(matrice) - 1 - etage * 2
            else:
                y = len(matrice) - 2 - etage * 2
            # Au lieu d'enlever 1 à x, on lui ajoute +1 en partant
            # de 11 qui est le premier bit à gauche.
            # On lit de gauche à droite.
            x = 11 + (i // 2)
            bit = matrice[y][x]
            donnees.append(bit)
        etage += 1
    # On restreint les données aux nombres de blocs demandés
    donnees = donnees[:nbrBloc * 14]
    # On range les données par bloc de 14 bits
    donneesFinale = []
    sousDonnees = []
    for i in range(0, len(donnees)):
        sousDonnees.append(donnees[i])
        if len(sousDonnees) == 14:
            donneesFinale.append(sousDonnees)
            sousDonnees = []
    if sousDonnees != []:
        donneesFinale.append(sousDonnees)
    return donneesFinale


def to_ascii(data: list):
    """
    Fonction qui prend une liste de bits et qui
    les convertit en caractères ascii.
    """
    assert len(data) == 8, "La liste doit être de taille 8."
    ascii = ""
    resultat = ""
    for i in range(0, len(data)):
        # On mets les bits collés sous forme de string
        # jusqu'à 8 bits
        ascii += str(data[i])
        if len(ascii) == 8:
            # On convertit le string en ascii et on le stocke
            resultat += chr(int(ascii, 2))
            ascii = ""
    # On retourne le résultat
    return resultat


def to_nums(data: list):
    """
    Fonction qui prend une liste de bit en base 2
    et qui les convertit en liste de bits en hexadécimal.
    """
    assert len(data) == 4, "La longueur de la liste doit être de 4"
    # On converti l'entier en entier.
    data = conversionEntier(data, 2)
    # On converti l'entier en base 16.
    data = conversionBase(data, 16)
    # La base 16 doit être filtré pour être afichée.
    data = baseHexa(data)
    # On retourne après que la base 16 ait été filtrée.
    return data


def verifDonnees(matrice: list):
    """
    Fonction qui donne le type de données du QR code.
    """
    # Le pixel en 24,8 donne le type de données,
    # si il est noir c'est que le QRC donne des valeurs
    # numérique, si il est blanc c'est des valeur en ASCII
    if matrice[24][8] == 0:
        return "num"
    elif matrice[24][8] == 1:
        return "ascii"
    else:
        return "erreur"


def verifNbrBloc(matrice: list):
    """
    Fonction qui retourne le nombre de bloc
    codant du QRC.
    """
    nbrBlocbase2 = []
    for i in range(13, 18):
        # On prend les bit de la colonne 1, de la ligne 13 à 18.
        nbrBlocbase2.append(matrice[i][0])
    # On transforme en entier pour avoir le nombre de bloc.
    nbrBloc = conversionEntier(nbrBlocbase2, 2)
    return nbrBloc


def lectureComplete(matrice: list):
    """
    Fonction qui interprète entirement le QRC.
    A l'aide des fonctions écrites précédemment.
    """
    matrice = verifQRC(matrice)
    assert verifLignesQRC(matrice), "QRC invalide, les lignes pointillés \
        sont manquantes"
    nbrBloc = verifNbrBloc(matrice)
    typeDonnees = verifDonnees(matrice)
    matrice = filtre(matrice)
    donnees = rawRead(matrice, nbrBloc)
    donnees = gestionHamming(donnees)
    res = ""
    if typeDonnees == "num":
        for elem in donnees:
            res += (to_nums(elem[0]) + to_nums(elem[1]))
    elif typeDonnees == "ascii":
        for elem in donnees:
            elem = elem[0] + elem[1]
            res += to_ascii(elem)
    return res


print("qr_code_ssfiltre_ascii.png devient:", lectureComplete(
    loading("qr_code_ssfiltre_ascii.png"))
    )
print("qr_code_ssfiltre_ascii_corrupted.png devient:", lectureComplete(
    loading("qr_code_ssfiltre_ascii_corrupted.png"))
    )
print("qr_code_ssfiltre_ascii_rotation.png devient:", lectureComplete(
    loading("qr_code_ssfiltre_ascii_rotation.png"))
    )
print("qr_code_ssfiltre_num.png devient:", lectureComplete(
    loading("qr_code_ssfiltre_num.png"))
    )
print("qr_code_damier_ascii.png devient:", lectureComplete(
    loading("qr_code_damier_ascii.png"))
    )
