from constantes import *

import random
from copy import deepcopy


RUBIK = list
FACE = list
MOUV = tuple

########################################################################################
# NOTE :
# Le But de ce projet etait de realisé les fonctions logique d'un rubik cube SANS utilisé numpy
########################################################################################

def generer_rubik_termine() -> RUBIK:
	"""genere et renvoi un rubik cube fini

	Returns:
		RUBIK: list[list[list[str]]]
	"""
	new_rubik = deepcopy(suqelette_rubik)
	for x in range(len(new_rubik)) :
		for y in range(len(new_rubik[x])) :
			for z in range(len(new_rubik[x][y])) :
				if z == 0 :
						new_rubik[x][y][z] = new_rubik[x][y][z].replace(new_rubik[x][y][z][0],Y)
				if z == 2 :
						new_rubik[x][y][z] = new_rubik[x][y][z].replace(new_rubik[x][y][z][0],W)
				if y == 0 :
						new_rubik[x][y][z] = new_rubik[x][y][z].replace(new_rubik[x][y][z][1],G)
				if y == 2 :
						new_rubik[x][y][z] = new_rubik[x][y][z].replace(new_rubik[x][y][z][1],B)
				if x == 0 :
						new_rubik[x][y][z] = new_rubik[x][y][z].replace(new_rubik[x][y][z][2],O)
				if x == 2 :
						new_rubik[x][y][z] = new_rubik[x][y][z].replace(new_rubik[x][y][z][2],R)
	return new_rubik

########################################################################################

def generer_rubik(nb_mouvs : int) :
	"""genere et renvoi un rubik cube melangé

	Args:
		nb_mouvs (int): nombre de mouvement a effectuer

	Returns:
		tuple[RUBIK,list[MOUV]]: renvoi un rubik's cube melangé et un liste de mouvement
	"""
	rubik = generer_rubik_termine()
	mouvs = []
	i = 0
	while i < nb_mouvs :
		f = random.choice(nom_faces)
		sens = random.choice((True,False))
		double = random.choice((True,False))
		mouv_ = (f,sens,double)
		mouvs.append(mouv_)
		rubik = appliquer_mouvement(rubik,mouv_)
		
		i += 1
	return rubik,mouvs

########################################################################################

def generer_rubik_scramble(scramble : str) -> RUBIK:
	""" 
	genere un rubik mélangé grâce au scramble en paramètre
	scramble : une cdc des mouvements à effectuer (par exemple "B2 F2 F' L2 B")
	"""
	rubik = generer_rubik_termine()
	return m(rubik,scramble)
	
########################################################################################


def melanger(rubik:RUBIK,nb_mouvs:int):
	""" 
	applique au rubik en paramètre nb_mouvs mouvements aléatoires
	retourne le scramble (liste de tuples des mouvements effectués)
	"""
	mouvs = []
	i = 0
	while i <= nb_mouvs :
		f = random.choice(nom_faces)
		sens = random.choice((True,False))
		double = random.choice((True,False))
		mouv_ = (f,sens,double)
		mouvs.append(mouv_)
		rubik = appliquer_mouvement(rubik,mouv_)
		
		i += 1
	return mouvs
		
########################################################################################

def c(cubelet:str,f:str)->str:
	"""
	retourne la couleur du cubelet correspondante à la face demandée
	exemple : ("YGO", "U") renvoie "Y"
	"""
	assert f in nom_faces," entrer une face valide"
	assert type(cubelet) == str and len(cubelet)==3 , "entrer un cubelet valide"
	if f in "UD" : return cubelet[0]
	if f in "FB" : return cubelet[1]
	if f in "LR" : return cubelet[2]
	

########################################################################################

def extraire(rubik : RUBIK, f : str) -> FACE :
	"""extrait une couronne (face) du rubik cube

	Args:
		rubik (RUBIK): list[list[list[str]]]
		f (str): correspond a une face du cube parmis U,D,F,B,L,R 

	Returns:
		FACE: list[list[str]]]
	"""
	face_extraite = deepcopy(squelette_face)
	
	for x in range(3) :
		for y in range(3) :
			for z in range(3) :
					if f == D :
						face_extraite[x][y] = rubik[x][y][0] 
					elif f == U :
						face_extraite[x][y] = rubik[x][y][2] 
					elif f == F :
						face_extraite[x][z] = rubik[x][0][z] 
					elif f == B :
						face_extraite[x][z] = rubik[x][2][z] 
					elif f == L :
						face_extraite[y][z] = rubik[0][y][z]
					elif f == R :
						face_extraite[y][z] = rubik[2][y][z]
	return face_extraite

	
########################################################################################

def T(face : FACE) -> FACE:
     face_T = deepcopy(face)
     for i in range(3):
          for j in range(3) :
               face_T[i][j] = face[j][i]
     return face_T

def rotation_horaire(face:FACE) -> FACE:
	face[0],face[2] = face[2],face[0]
	return T(face)

def rotation_anti_horaire(face:FACE)->FACE:
	face_T = T(face)
	face_T[0],face_T[2] = face_T[2],face_T[0]
	return face_T

def T_autres_diag(face:FACE)->FACE: # pas utilisé dans appliquer_rotation mais utilisé autre part
    T_face = deepcopy(face)
    n = len(face)
    for i in range(n):
        for j in range(n):
            T_face[i][j] = face[n-j-1][n-i-1] # -1 car la liste commence a 0 et fini a 2 = n-1
    return T_face

def appliquer_rotation(face:FACE, sens:bool, double:bool)->FACE:
	""" 
	applique une rotation à la face passée en paramètre
	cette fonction ne modifie PAS l'orientation (couleur) des cubelets
	face : matrice 2D de cubelets
	sens : True pour horaire
	double : True pour 180°
	"""
	if double :
		new_face = rotation_horaire(rotation_horaire(face))
	elif sens :
		new_face = rotation_horaire(face)
	else : 
		new_face = rotation_anti_horaire(face)
	return new_face
	

########################################################################################

def reimplanter(rubik:RUBIK, f:str, face:FACE)->RUBIK:
	"""reimplante (remplace) la face f de rubik avec les cubelets du paramètre face
		note : cette fonction n'applique PAS de rotation ou de réorientation des cubelets
		f : lettre de la face à remplacer, f = caractère (U,L,F,R,B,D)
		face : matrice 2D de cubelets

	Args:
		rubik (RUBIK): list[list[list[str]]]
		f (str): nom face du cube
		face (FACE): list[list[str]]

	Returns:
		RUBIK: list[list[list[str]]]
	"""
	assert f in nom_faces
	for x in range(3) :
		for y in range(3) :
			for z in range(3) :
					if f == D :
						rubik[x][y][0] = face[x][y]
					elif f == U :
						rubik[x][y][2] = face[x][y]
					elif f == F :
						rubik[x][0][z] = face[x][z]
					elif f == B :
						rubik[x][2][z] = face[x][z]
					elif f == L :
						rubik[0][y][z] = face[y][z]
					elif f == R :
						rubik[2][y][z] = face[y][z]
	return rubik

########################################################################################

def inverse_couleur_F_B(cubelet:str)->str:
	return cubelet[::-1] 

def inverse_couleur_U_D(cubelet:str)->str:
	UD,FB,LR = cubelet
	return UD + LR + FB
	
def inverse_couleur_L_R(cubelet:str)->str:
	UD,FB,LR = cubelet
	return FB + UD + LR

def re_oriente_cubelet(face:FACE,f:str) -> FACE:
	for i in range(3):
		for j in range(3):
			cubelet = face[i][j]
			if f in "FB":
				face[i][j] = inverse_couleur_F_B(cubelet)
			elif f in "UD":
				face[i][j] = inverse_couleur_U_D(cubelet)
			elif f in "LR":
				face[i][j] = inverse_couleur_L_R(cubelet)
	return face

def appliquer_mouvement(rubik:RUBIK, mouv:MOUV) -> RUBIK:
	""" 
	effectue un mouvement du rubik
	extrait, applique la rotation, réoriente les couleurs et réimplante la face
	mouv est un tuple (f, sens, double)
	f = caractère (U,L,F,R,B,D)
	sens = booleen (True = horaire)
	double = boolean (True = 180°)
	"""
	f, sens, double = mouv
	face = extraire(rubik,f)

	# pour L B D, la structure de "face" NON ré-oriente change le sens de rotation
	# en effet pour L, B, D on dois effectuer une transposer pour obtenir la face du cube telle quelle 
	# est dans la realite, 
	# cette transposer change les rotations horaire -> en rotations anti-horaire 
	if f in "LBD":
		face = appliquer_rotation(face,not sens,double)
	else : 
		face = appliquer_rotation(face,sens,double)

	if not double :
		face = re_oriente_cubelet(face,f)
	
	return reimplanter(rubik,f,face)


########################################################################################

def face_terminee(face:FACE,f:str)->bool:
	""" 
	renvoie True si la face est terminée
	face : matrice 2D de cubelets
	f : caractère (U,L,F,R,B,D)
	"""
	colors = {1,2} # 1,2 pour que "colors" soit bien detecté comme etant un 'set' et non un 'dict'
	for ligne in face:
		for cubelet in ligne:
			color = c(cubelet,f)
			colors.add(color)
	return len(colors) == 3

########################################################################################

def victoire(rubik:RUBIK)->bool:
	"""renvoie True si le cube est terminé"""
	faces = [extraire(rubik,f) for f in nom_faces]
	face_termine = [face_terminee(face,f) for face,f in zip(faces,nom_faces)]	
	return all(face_termine)

########################################################################################

def mouv(m_ : str) -> MOUV:
	""" 
	renvoie un tuple (face, sens, double) correspondant au mouvement m
	m : chaîne de caractères représentant un mouvement
	exemples: "F" renvoie ('F',True,False), "R'" renvoie ('R',False,False), "L2" renvoie ('L',False,True)
	"""
	assert m_ in mouv_valid , "entrez un mouvement valide"
	f = m_[0]
	sens = False if "'" in m_ or "2" in m_ else True
	double = True if "2" in m_ else False
	return f, sens, double

########################################################################################

def mouvements(ms:str) -> list:
	""" 
	renvoie une liste de tuples correspondants aux mouvements ms
	ms : chaîne de caractères représentant des mouvements (scramble)
	exemple: "F R' L2" renvoie [('F',True,False),('R',False,False),('L',False,True)]
	"""
	assert type(ms) == str # la validité de ms est verifier plus precisement avec la fonction mouv
	mouvs = []
	M = ms.strip(" ").split(" ")
	for m_ in M :
		mouvs.append(mouv(m_))
	return mouvs

########################################################################################

def m(rubik:RUBIK, ms:str) -> RUBIK:
	""" 
	applique les mouvements ms au cube rubik
	ms : chaîne de caractères représentant des mouvements (scramble)
	"""
	mouvs = mouvements(ms)
	for m_ in mouvs :
		rubik = appliquer_mouvement(rubik,m_)
	return rubik

########################################################################################

def scramble(mouvs) -> str:
	""" 
	renvoie une chaîne de caractères correspondant aux mouvements mouvs
	exemple: [('F',True,False),('R',False,False),('L',False,True)] renvoie "F R' L2"
	"""
	mouv_ = ""
	for m in mouvs :
		f,sens,double = m
		double = "2" if double else ""
		sens = "'" if not sens and not double else ""
		mouv_ += f + sens + double + " "
	return mouv_

########################################################################################
