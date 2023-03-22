# taille du cube
TAILLE = 3


#nom des faces
U = "U"
D = "D"
L = "L"
R = "R"
F = "F"
B = "B"

# nom des couleurs (on repete certain)
N = "N"
W = "W"
Y = "Y"
O = "O"
R = "R"
G = "G"
B = "B"

# couleurs du cube
couleurs = (N ,B ,W ,Y ,G ,O ,R)

# faces du cube
nom_faces = (U ,D ,L ,R ,F ,B)

#mouvements valide
mouv_valid = ("F","L","R","U","D","B","F2","L2","R2","U2","D2","B2","F'","L'","R'","U'","D'","B'")


# squelette d'une face
squelette_face = [
       ["NNN","NNN","NNN"],
       ["NNN","NNN","NNN"],
       ["NNN","NNN","NNN"]
			]

# squelette d'un cube
# rq : pour la fonction generer_rubik_termine on a besoin de 3 caracteres differents 
# pour utilisé la methode replace.
suqelette_rubik = [
                     [["+-*", "+-*", "+-*"], ["+-*", "+-*", "+-*"], ["+-*", "+-*", "+-*"]],
                     [["+-*", "+-*", "+-*"], ["+-*", "+-*", "+-*"], ["+-*", "+-*", "+-*"]],
                     [["+-*", "+-*", "+-*"], ["+-*", "+-*", "+-*"], ["+-*", "+-*", "+-*"]]
                     ]
                                   
