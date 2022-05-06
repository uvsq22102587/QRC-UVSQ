import PIL as pil


def nbrCol(matrice):
    return(len(matrice[0]))


def nbrLig(matrice):
    return len(matrice)


def saving(matPix, filename):
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


def loading(filename):
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
    """
    Fonction qui prend une matrice de pixel et qui en sort les 3 coins
    sous forme de liste.
    """
    coinGaucheHaut = [
        [matrice[i][j] for i in range(0, taillecoin)]
        for j in range(0, taillecoin)
        ]
    coinDroitHaut = [
        [matrice[i][j] for i in range(0, taillecoin)]
        for j in range(len(matrice) - taillecoin, len(matrice))
        ]
    coinGaucheBas = [
        [matrice[i][j] for i in range(len(matrice) - taillecoin, len(matrice))]
        for j in range(0, taillecoin)
        ]
    return (coinGaucheHaut, coinDroitHaut, coinGaucheBas)


def verifQRC(matrice):
    """
    Fonction qui compare les coins d'une matrice de pixels et qui les compare
    à un QRCODE.
    Si la matrice est bien un QRcode, elle le tourne pour qu'il puisse
    être dans le bon sens.
    """
    averif = extraireCoin(matrice, 7)
    temoin = extraireCoin(creerQRC(), 7)
    while averif != temoin:
        matrice = rotationQRC(matrice)
        averif = extraireCoin(matrice, 7)
    return matrice


def verifLignesQRC(matrice):
    """
    Fonction qui vérifie les lignes en pointillés
    caractéristique d'un QRC sur une matrixe de pixels.
    """
    check = True
    for i in range(6, 18):
        if matrice[6][i] != (i % 2):
            check = False
    for i in range(6, 18):
        if matrice[i][6] != (i % 2):
            check = False
    return check


def gestionHamming(donnees):
    """
    Fonction qui applique la correction de Hamming sur chacun
    des bloc de 7 bits de la liste données.
    """
    sousDonnees, donneesFinale = [], []
    for j in range(0, len(donnees)):
        for i in range(0, 2):
            sousDonnees.append(correctionHamming(
                donnees[j][0 + i * 7:7 + i * 7])
                )
        donneesFinale.append(sousDonnees)
        sousDonnees = []
    return donneesFinale


def correctionHamming(bits):
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
        bits[0] = int(not bits[0])
    if num == 5:
        bits[1] = int(not bits[1])
    if num == 6:
        bits[2] = int(not bits[2])
    if num == 7:
        bits[3] = int(not bits[3])
    return bits[:4]


def filtre(matrice):
    """
    Fonction qui vérifie le filtre et son type et qui applique
    ce filtre au pixel du QRC.
    """
    filtre = (matrice[22][8] << 1) | (matrice[23][8])
    matriceFiltre = [[0 for j in range(0, 14)] for i in range(0, 16)]
    if filtre == 0:
        return matrice
    elif filtre == 1:
        for i in range(0, 16):
            for j in range(0, 14):
                if (i + j) % 2 == 1:
                    matriceFiltre[i][j] = 1
    elif filtre == 2:
        for i in range(0, 16):
            for j in range(0, 14):
                if i % 2 == 1:
                    matriceFiltre[i][j] = 1
    elif filtre == 3:
        for i in range(0, 16):
            for j in range(0, 14):
                if j % 2 == 1:
                    matriceFiltre[i][j] = int(not matriceFiltre[i][j])
    for i in range(len(matriceFiltre)):
        for j in range(len(matriceFiltre[0])):
            x1, y1 = len(matrice[0]) - 1, len(matrice) - 1
            x2, y2 = len(matriceFiltre[0]) - 1, len(matriceFiltre) - 1
            matrice[y1 - i][x1 - j] = matrice[y1 - i][x1 - j] ^ \
                matriceFiltre[y2 - i][x2 - j]
    return matrice


def rawRead(matrice, nbrBloc):
    """
    Fonction qui prend une matrice de pixels et la lit sans effectuer
    la vérification via le code de Hamming ni le filtre.
    """
    donnees = []
    etage = 0
    # On lit tous les blocs (maximum 16)
    while len(donnees) <= 16 * 14:
        for i in range(0, 28):
            if i % 2 == 0:
                y = len(matrice) - 1 - etage * 2
            else:
                y = len(matrice) - 2 - etage * 2
            x = (len(matrice) - 1) - (i // 2)
            bit = matrice[y][x]
            donnees.append(bit)
        etage += 1
        for i in range(0, 28):
            if i % 2 == 0:
                y = len(matrice) - 1 - etage * 2
            else:
                y = len(matrice) - 2 - etage * 2
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
    ascii = ""
    resultat = ""
    for i in range(0, len(data)):
        ascii += str(data[i])
        if len(ascii) == 8:
            resultat += chr(int(ascii, 2))
            ascii = ""
    return resultat


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
        res.append(nombre % b)
        nombre = nombre // b
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
        if(v < 10):
            res += str(v)
        return res


def to_nums(data: list):
    """
    Fonction qui prend une liste de bit en base 2
    et qui les convertit en liste de bits en hexadécimal.
    """
    assert len(data) == 4, "La longueur de la liste doit être de 4"
    data = conversionEntier(data, 2)
    data = conversionBase(data, 16)
    data = baseHexa(data)
    return data


def verifDonnees(matrice):
    """
    Fonction qui vérifie le type de données.
    """
    if matrice[24][8] == 0:
        return "num"
    elif matrice[24][8] == 1:
        return "ascii"
    else:
        return "erreur"


def verifNbrBloc(matrice):
    """
    Fonction qui retourne le nombre de bloc du QRC.
    """
    nbrBlocbase2 = []
    for i in range(13, 18):
        nbrBlocbase2.append(matrice[i][0])
    nbrBloc = conversionEntier(nbrBlocbase2, 2)
    return nbrBloc


def lectureComplete(matrice):
    """
    Fonction qui interprète entirement le QRC.
    A l'aide des fonctions écrites précédemment.
    """
    matrice = verifQRC(matrice)
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
