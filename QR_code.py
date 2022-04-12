

def codage_hamming(bits):
    liste_7bits = [0]*7
    # bits de message
    i = 0
    for j in [2, 4, 5, 6]:
        liste_7bits[j] = bits[1]
        i += 1
    # on ajoute les bits de controlle
    liste_7bits[0] = bits[0] ^ bits[1] ^ bits[3]
    liste_7bits[1] = bits[0] ^ bits[2] ^ bits[3]
    liste_7bits[3] = bits[1] ^ bits[2] ^ bits[3]
    return(liste_7bits)


def decodage_hamming(bits):
    # calcul bits de controle
    p1 = bits[2] ^ bits[4] ^ bits[6]
    p2 = bits[2] ^ bits[5] ^ bits[6]
    p3 = bits[4] ^ bits[5] ^ bits[6]
    # position erreur
    num = int(p1 != bits[0]) + int(p2 != bits[1]) * 2 + int(p3 != bits[3]) * 4
    if num in [3, 5, 6, 7]:
        # on remplace bits[num-1] par 0 s'il valait 1 et par 1 si il valait 0
        bits[num-1] = int(not bits[num - 1])
        print("corection d'un pixel corrompu en position " + str(num) + "\n")
    return [bits[2], bits[4], bits[5], bits[6]]


def decodage_hammingQRCODE(bits):
    # calcul bits de controle
    p1 = bits[0] ^ bits[1] ^ bits[2]
    p2 = bits[0] ^ bits[2] ^ bits[3]
    p3 = bits[1] ^ bits[2] ^ bits[3]
    # position erreur
    num = int(p1 != bits[4]) + int(p2 != bits[5]) * 2 + int(p3 != bits[6]) * 4
    if (num == 3):
        bits[0] = int(not bits[0])
    if num == 5:
        bits[1] = int(not bits[1])
    if num == 6:
        bits[2] = int(not bits[2])
    if num == 7:
        bits[3] = int(not bits[3])
    return bits[:4]


print(decodage_hammingQRCODE([1, 1, 0, 0, 0, 0, 0]))
