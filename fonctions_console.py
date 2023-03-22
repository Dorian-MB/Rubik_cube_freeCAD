from constantes import *
from fonctions_logique import *

#? rubik[x][y][z] = "UFL" : Up/Down ; Front/Back ; Left/Right


########################################################################################

def afficher_rubik(rubik : RUBIK): 
     """ affiche un rubik en console, le rubik est affiché en mode "déplié"
                    
                    exemple :
                                   ~ WWW
                                   ~ WWW
                                   ~ YYY
                                   ~ U

                              ~ OOR GGG ORR   BBB
                              ~ OOR GGG ORR   BBB
                              ~ OOR GGG ORR   BBB
                              ~ L   F   R     B

                                   ~ WWW
                                   ~ YYY
                                   ~ YYY
                                   ~ D

     Args:
         rubik (RUBIK): list[list[list[str]]]
     """

     U = [["N","N","N"],["N","N","N"],["N","N","N"]]
     L = [["N","N","N"],["N","N","N"],["N","N","N"]]
     F = [["N","N","N"],["N","N","N"],["N","N","N"]]
     R = [["N","N","N"],["N","N","N"],["N","N","N"]]
     B = [["N","N","N"],["N","N","N"],["N","N","N"]]
     D = [["N","N","N"],["N","N","N"],["N","N","N"]]
     
     # attention pas de elif ici
     for x in range(len(rubik)) :
          for y in range(len(rubik[x])) :
               for z in range(len(rubik[x][y])) :
                    if z == 0 :
                         D[x][y] = rubik[x][y][z][0]
                    if z == 2 :
                         U[x][y] = rubik[x][y][z][0]
                    if y == 0 :
                         F[x][z] = rubik[x][y][z][1]
                    if y == 2 :
                         B[x][z] = rubik[x][y][z][1]
                    if x == 0 :
                         L[y][z] = rubik[x][y][z][2]
                    if x == 2 :
                         R[y][z] = rubik[x][y][z][2]

     # re-oriente les faces
     # dû au sens de balayage de "rubik" les faces ne sons pas ortienté dans le meme sens 
     # que la realité, ampiriquement on trouve les resultats suivant :
     U = rotation_anti_horaire(U)
     L = T_autres_diag(L)    
     F = rotation_anti_horaire(F)
     R = rotation_anti_horaire(R)
     B = T_autres_diag(B)
     D = T(D)
     
     #affichage du rubik cube deplié
     print("----------------------------")
     for ligne in U :
          print("\t" + "".join(ligne))
     print("\t U")

     for i in range(3) :
          print(" ","".join(L[i]),"".join(F[i]),"".join(R[i]),"".join(B[i]))
     print(" "," L "," F "," R "," B ")

     for ligne in D :
          print("\t" + "".join(ligne))
     print("\t D")

     return 



########################################################################################

def saisie_valide(saisie:str)->bool:
     """ 
     retourne True si la saisie est un mouvement valide
     les mouvements valides sont une chaine de caractères sous la forme (F|L|R|U|D|B['|2])
     """
     return saisie in mouv_valid
	
########################################################################################

def saisie_mouvement()->MOUV:
     """permet la saisie d'un mouvement à effectuer"""
     saisie = input("saisir un mouvement : ")
     while not saisie_valide(saisie):
          saisie = input("mouvement non valide... saisir un mouvement valide : ")
     f = saisie[0]
     sens = False if "'" in saisie or "2" in saisie else True
     double = True if "2" in saisie else False
     return f, sens, double

########################################################################################


def saisie_mouvements():
     """ 
     permet la saisie d'une suite de mouvements à effectuer		
     renvoie toujours une liste de tuples valide (f, sens, double) 
     l'utilisateur est invité à recommencer sa saisie tant que celle-ci est invalide
     """
     n = input(" combien de mouvement voulez vous effectuer ? ")
     while not n.isdigit() :
          n = input(" entrer un nombre entier ... ")
     n = int(n)
     M = []
     for _ in range(n):
          M.append(saisie_mouvement())
     return M

########################################################################################

if __name__ == "__main__":
	rubik = generer_rubik_termine()
	afficher_rubik(rubik)
