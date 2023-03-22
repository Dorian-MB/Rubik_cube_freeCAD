from constantes import *
from fonctions_logique import *
from fonctions_console import *

jouer = input("entrer le nombre de rotation aleatoire : ")

while not jouer.isdigit():
    jouer = input("saisie invalide, de rotation aleatoire : ")

rubik = generer_rubik(int(jouer))[0]
afficher_rubik(rubik)

while not victoire(rubik):
	next_mouv = saisie_mouvement()
	rubik = appliquer_mouvement(rubik,next_mouv)
	afficher_rubik(rubik)

print("Victoire !")
