from ruler import Ruler

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("nom_fichier", type = str, help = "fichier contenant des chaines à tester")
args = parser.parse_args()
nom = args.nom_fichier

with open('DATASET.csv', "r") as fichier:
    L = []
    for e in fichier:
        L.append(e)
    for i in range(0,len(L)-1, 2):
        a = Ruler(L[i], L[i+1])
        a.compute()
        top, bottom = a.report()
        print(f'''Example # {(i+1)//2 + 1} - distance = {a.distance}
        {top}
        {bottom}''')


# LE CODE MARCHE EN TAPANT python bundle.py DATASET.csv DANS ANACONDA PROMPT