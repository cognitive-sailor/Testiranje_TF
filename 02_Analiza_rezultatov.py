import re
import os
import numpy as np


def analiza():
    # pridobi seznam vseh razredov in pot, kjer so shranjene testne slike
    pot, razredi = ustvari_razrede()
    oznake = []
    for i in razredi:
        oznake.append(i.lower())  # spremeni vsa imena razredov tako, da so zapisana z malo zacetnico
    ST_RAZREDOV = len(oznake)  # pridobi stevilo razredov
    print(ST_RAZREDOV)
    M = np.zeros((ST_RAZREDOV, ST_RAZREDOV, 3))  # ustvari matriko M, kamor bomo zapisovali rezultate analize

    # za vsak razred odpri datoteko in jo analiziraj
    for k, r in enumerate(razredi):
        test_datoteka = "./rezultati_testiranj/Testiranje_"+r.strip()+".txt"  # ime/pot datoteke, ki bo analizirana
        pot1 = os.path.join(pot, r.strip())  # pot do slik v posameznem razredu
        ST_VZORCEV = 0
        for slika in os.listdir(pot1):
            ST_VZORCEV += 1  # ugotovi koliko je slik v vsakem razredu
        with open(test_datoteka, "r") as f:
            f1=f.readlines()  # odpri datoteko za analizo
        print(f"\nObdelujem rezulrate za razred {r.upper()}")
        # za vsako n vrstico (napoved, ki ima največjo gotovost je vedno na vrhu, tako je narejena datoteka label_image.py) preveri kateri razred je.
        for x in f1[1::(ST_RAZREDOV+1)]:
            M = preveri_razred(k, x, ST_VZORCEV, oznake, M)
        for p, i in enumerate(razredi):
            print(f"{r.upper()}\nPovprecna gotovost napovedi: {M[k,p,2]}\nStevilo napovedi za razred {i}: {int(M[k,p,0])} izmed {ST_VZORCEV} ==> {round((M[k,p,0]/ST_VZORCEV)*100,2)} %\n")


def ustvari_razrede():
    with open("pot_do_mape_za_test.txt","r") as f:
        pot = f.read()
    razredi = []
    for razred in os.listdir(pot):
        razredi.append(razred)
    return pot, razredi


def preveri_razred(k, x, st_vzorcev, oznake, M):
    # v zgornji vrstici preverjamo kateri razred je bil napovedan in rezultate belezimo v matriko M.
    for p, i in enumerate(oznake):
        oznake[p] = oznake[p].replace("_", " ")
        if i in x:
            score = re.findall("\d+\.\d+", x)
            M[k, p, 0] += 1  # stevilo napovedi
            M[k, p, 1] += float(score[0])
            M[k, p, 2] = M[k, p, 1]/M[k, p, 0]  # povprecna gotovost napovedi
    return M



analiza()
