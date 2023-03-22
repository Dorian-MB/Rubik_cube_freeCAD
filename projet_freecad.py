import Draft
from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import (QApplication, QGridLayout,
                                QLineEdit, QListWidget, QPushButton, 
                                QSizePolicy,QWidget,QVBoxLayout,
                                QLabel,QDockWidget)
import json
from pathlib import Path
from random import choice
from functools import partial

from constantes import *
from fonctions_logique import *

####################################################################################################
##* Constantes

doc = FreeCAD.ActiveDocument
if doc == None:	
	doc = FreeCAD.newDocument("Rubik")

BUTTON = {
        "nouveau cube":(0,0,1,6),
        "mélange":(1,0,1,6),
        "U":(2,0,1,1),
        "U'":(3,0,1,1),
        "U2":(4,0,1,1),
        "D":(2,1,1,1),
        "D'":(3,1,1,1),
        "D2":(4,1,1,1),
        "F":(2,2,1,1),
        "F'":(3,2,1,1),
        "F2":(4,2,1,1),
        "B":(2,3,1,1),
        "B'":(3,3,1,1),
        "B2":(4,3,1,1),
        "L":(2,4,1,1),
        "L'":(3,4,1,1),
        "L2":(4,4,1,1),
        "R":(2,5,1,1),
        "R'":(3,5,1,1),
        "R2":(4,5,1,1),
        "animation":(5,0,1,6),
        }

####################################################################################################
##* fct utile

def convertir_couleur_constante(color):
	if color == Y :
		return 1.0,1.0,0.0
	elif color == W :
		return 1.0,1.0,1.0
	elif color == R :
		return 1.0,0.0,0.0
	elif color == B :
		return 0.0,0.0,1.0
	elif color == O :
		return 1.0,0.5,0.0
	elif color == G :
		return 0.0,1.0,0.0
	else :
		return 0.0,0.0,0.0

####################################################################################################
##* sauvegarde

current_dir = Path(__file__).parent # methode cwd ne marche pas
save_file = current_dir / "save.json"

def get_saved_cube():
    try :
        with open(save_file,"r") as f:
            cubes = json.load(f) # plante si json vide
    except :
            return False
    return cubes

def write_saved_cube(cubes):
    with open(save_file,"w") as f:
        json.dump(cubes,f,indent=4)    

def save():
    cubes = get_saved_cube()
    if cubes == False : 
        cubes = {}
    rubik_name = UI.le_save.text()
    cubes[rubik_name] = Rubik.rubik # si nom existe deja, ecrase le rubik precedent
    write_saved_cube(cubes)
    UI.le_save.clear()
    UI.load_lw()

def reload():
    cubes = get_saved_cube()
    items = UI.lw_save.selectedItems()
    if items != []:
        item = choice(items) #si plusieur rubik sont selectionné, prend un au hasard
        Rubik.rubik = cubes[item.text()]
        Rubik.init_nb_mouv()
        Rubik.cube3D()
        UI.buttons["mélange"].setText("mélange")

def delete():
    cubes = get_saved_cube()
    items = UI.lw_save.selectedItems()
    if items != []:
        for item in items :
            UI.lw_save.takeItem(UI.lw_save.row(item))
            del cubes[item.text()]
        write_saved_cube(cubes)
        UI.load_lw()

####################################################################################################
##* Animation: 

# rappel : cube fini est ici : Front = Vert, Left = orange, Up = Blanc
nom_cubelet_D = [] # nom des cubelets FreeCAD PAR FACE DU CUBE == constante
nom_cubelet_U = [] # en revanche les cubelets Freecad qui vont porter ces noms depandent 
nom_cubelet_F = [] # du rubik's cube python, et changeront a chaque rotation du cube
nom_cubelet_B = [] # ie : le cubelet dans le coins en haut a droite devant nous sera toujours
nom_cubelet_L = [] # le "cubelet202" mais il peut etre le "blanc,vert,rouge" (cube fini)
nom_cubelet_R = [] # comme le "blanc,rouge,bleu" (rotation U apres cube fini)

for x in range(3):
    for y in range(3):
        for z in range(3):
            if z == 0 : nom_cubelet_D.append(f"cubelet{x}{y}{z}") # pas de elif
            if z == 2 : nom_cubelet_U.append(f"cubelet{x}{y}{z}")
            if y == 0 : nom_cubelet_F.append(f"cubelet{x}{y}{z}")
            if y == 2 : nom_cubelet_B.append(f"cubelet{x}{y}{z}")
            if x == 0 : nom_cubelet_L.append(f"cubelet{x}{y}{z}")
            if x == 2 : nom_cubelet_R.append(f"cubelet{x}{y}{z}")

def rotate(cubelet,angle,axis):
    # centre de rotation ("center" dans Draf.rotate) = centre du cube (une arrete = 30), 
    # ainsi les axes de oration passent toujours par le centre de rotation
    try :
        Draft.rotate(cubelet,angle,center=FreeCAD.Vector(15.0,15.0,15.0),axis=axis,copy=False)
    except:
        pass

def animation(timer,cubelet,angle,axis):
        if not hasattr(animation,"count"): 
            # vérifie si animation a un attribut "count", sinon on le crée
            animation.count = 0
        animation.count += 1
        rotate(cubelet,angle,axis)
        if animation.count >= 10 : # boucle 10fois, pour un angle = 9° => 90°
            timer.stop()
            animation.count = 0

####################################################################################################
##* Rubik 3D

class RubikCube :
    def __init__(self) :
        self.cubelet = {}
        self.rubik = []
        self.nb_mouv = 0

    # Genere Rubik's cube terminé ou mélangé
    def generer_rubik3D_termine(self): # teminé
        self.rubik = generer_rubik_termine()
        self.init_nb_mouv()
        self.cube3D()
        UI.buttons["mélange"].setText("mélange")

    def generer_rubik3D(self): # mélangé
        self.rubik,scramble_ = generer_rubik(15)
        self.init_nb_mouv()
        self.cube3D()
        UI.buttons["mélange"].setText("mélange: " + scramble(scramble_))

    # Cree Rubik's cube 3D
    def cube3D(self):
        self.clear_doc() # ne pas inverser l'ordre
        self.cubelet.clear()
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    cube = doc.addObject("Part::Box",f"cubelet{x}{y}{z}")
                    self.cubelet[f"cubelet{x}{y}{z}"] = cube
                    cube.Length = 10
                    cube.Width = 10
                    cube.Height = 10
                    U_D_color = convertir_couleur_constante(self.rubik[x][y][z][0])
                    F_B_color = convertir_couleur_constante(self.rubik[x][y][z][1])
                    L_R_color = convertir_couleur_constante(self.rubik[x][y][z][2])
                    cube.Placement = App.Placement(App.Vector(10*x,10*y,10*z),App.Rotation(0,0,0,1))
                    cube.ViewObject.ShapeColor=(0.0,0.0,0.0)
                    cube.ViewObject.DiffuseColor=[L_R_color,L_R_color,F_B_color,F_B_color,U_D_color,U_D_color]

    def clear_doc(self):
        for cube_name in self.cubelet.keys():
            doc.removeObject(cube_name)

    def init_nb_mouv(self):
        self.nb_mouv = 0
        UI.lb_nb_mouv.setText("nb de mouvement: 0")

    # Rotation 3D SANS animation
    def appliquer_rotation_3D_listewidget(self):
        try :
            self.appliquer_rotation_3D(UI.le_mouv.text())
        except AssertionError as error :
            UI.le_mouv.setText(str(error))
        else :
            UI.le_mouv.clear()

    def appliquer_rotation_3D(self,mouv_):
        mouvs = mouvements(mouv_)
        for mouve in mouvs:
            self.rubik = appliquer_mouvement(self.rubik,mouve)
            self.nb_mouv += 1
        UI.lb_nb_mouv.setText("nb de mouvement: "+str(self.nb_mouv))
        self.cube3D()

    # Rotation 3D AVEC animation 
    def appliquer_rotation_3D_animation(self,mouv_):
        self.cube3D()
        self.rubik=appliquer_mouvement(self.rubik,mouv(mouv_))
        self.nb_mouv += 1
        UI.lb_nb_mouv.setText("nb de mouvement: "+str(self.nb_mouv))

        #animation du mouvement
        timer = QtCore.QTimer()
        self.set_cubelet(mouv_) 
        cubelet,angle,axis = self.chose_animation(mouv_)
        animcall = partial(animation,cubelet=cubelet ,timer=timer, angle=angle,axis=axis)
        timer.timeout.connect(animcall)
        timer.start(1)

    def set_cubelet(self,mouv_):
        mouv_ = mouv_.strip("'2") # "R2" ou "R'" -> "R"
        if mouv_ == D :
            self.cubelet_D = [self.cubelet[el] for el in nom_cubelet_D] #self.cubelet est un dictionnaire
        elif mouv_ == U:
            self.cubelet_U = [self.cubelet[el] for el in nom_cubelet_U]
        elif mouv_ == F:
            self.cubelet_F = [self.cubelet[el] for el in nom_cubelet_F]
        elif mouv_ == B:
            self.cubelet_B = [self.cubelet[el] for el in nom_cubelet_B]
        elif mouv_ == L:
            self.cubelet_L = [self.cubelet[el] for el in nom_cubelet_L]
        elif mouv_ == R:
            self.cubelet_R = [self.cubelet[el] for el in nom_cubelet_R]

    def chose_animation(self,mouv_):
        if "'" in mouv_ : signe = -1
        else : signe = 1
        if "2" in mouv_ : double = 2
        else : double = 1

        if U in mouv_: 
            return self.cubelet_U,-signe*double*9,FreeCAD.Vector(0.0,0.0,1.0)
        elif D in mouv_: 
            return self.cubelet_D,signe*double*9,FreeCAD.Vector(0.0,0.0,1.0)
        elif L in mouv_: 
            return self.cubelet_L,signe*double*9,FreeCAD.Vector(1.0,0.0,0.0)
        elif R in mouv_: 
            return self.cubelet_R,-signe*double*9,FreeCAD.Vector(1.0,0.0,0.0)
        elif F in mouv_: 
            return self.cubelet_F,signe*double*9,FreeCAD.Vector(0.0,1.0,0.0)
        elif B in mouv_: 
            return self.cubelet_B,-signe*double*9,FreeCAD.Vector(0.0,1.0,0.0)

####################################################################################################
##* interface utilisateur

class RubikWidget(QDockWidget):
    def __init__(self):
        super().__init__()
        self.widget = QWidget(self)
        self.window = QApplication.activeWindow()
        self.window.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        self.setWindowTitle("IU rubik")		
        self.widget.setGeometry(QtCore.QRect(0, 20, 500,750))

        self.buttons = {}
        self.animation = True
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self.widget)
        self.layout_btn = QGridLayout()
        self.upper_layout = QVBoxLayout()
        self.bottom_layout = QVBoxLayout()
        self.main_layout.addLayout(self.upper_layout)
        self.main_layout.addLayout(self.layout_btn)
        self.main_layout.addLayout(self.bottom_layout)
        
        self.lb_nb_mouv = QLabel("nb de mouvement: 0")
        self.le_mouv = QLineEdit()
        self.upper_layout.addWidget(self.lb_nb_mouv)
        self.upper_layout.addWidget(self.le_mouv)
        
        for btn_name,btn_position in BUTTON.items():
            button = QPushButton(btn_name)
            self.buttons[btn_name] = button
            self.layout_btn.addWidget(button,*btn_position)

        self.lw_save = QListWidget()
        self.le_save = QLineEdit()
        self.btn_save = QPushButton("sauvegarder")
        self.btn_reload = QPushButton("reload")
        self.btn_delete = QPushButton("supprimer")
        self.bottom_layout.addWidget(self.lw_save)
        self.bottom_layout.addWidget(self.le_save)
        self.bottom_layout.addWidget(self.btn_save)
        self.bottom_layout.addWidget(self.btn_reload)
        self.bottom_layout.addWidget(self.btn_delete)
        self.buttons["sauvegarder"] = self.btn_save
        self.buttons["reload"] = self.btn_reload
        self.buttons["supprimer"] = self.btn_delete

        self.init_css()
        self.connection()
        self.load_lw()

    def init_css(self):
        self.lb_nb_mouv.setAlignment(QtCore.Qt.AlignCenter)
        self.lw_save.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setStyleSheet("""
            background-color: #111;
            color: #fff ;
            font-size: 16px;
            font-weight:bold;
            """)
        self.lw_save.setStyleSheet("border : 2px solid #f31d58")
        self.le_mouv.setPlaceholderText("entré une suite de mouvements (non annimé)")
        self.le_mouv.setStyleSheet("""
            border : 2px solid #f31d58;
            padding: 8px;
            font-size: 20px;
            """)
        self.le_save.setPlaceholderText("entré un nom de sauvegarde")
        self.le_save.setStyleSheet("""
            border : 2px solid #f31d58;
            padding: 4px;
            font-size: 16px;
            font-weight: bold;
            """)
        for button in self.buttons.values():
            button.setMinimumSize(30,30)
            button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            button.setStyleSheet("""
                QPushButton{
                    border: none;
                    font-weight:bold;
                    background-color:#111;}
                QPushButton:pressed {background-color:#f31d58;}
                """)
        self.buttons["animation"].setStyleSheet("background-color:#f31d58;")

    def connection(self):
        self.le_mouv.returnPressed.connect(Rubik.appliquer_rotation_3D_listewidget)
        self.buttons["nouveau cube"].clicked.connect(Rubik.generer_rubik3D_termine)
        self.buttons["mélange"].clicked.connect(Rubik.generer_rubik3D)
        for btn_name,btn in self.buttons.items():
            if btn_name not in ("nouveau cube","mélange","animation","sauvegarder","reload","supprimer"):
                btn.clicked.connect(self._sender_for_btnwidget)
        self.buttons["animation"].clicked.connect(self.set_aniamtion)
        self.lw_save.itemDoubleClicked.connect(reload)
        self.le_save.returnPressed.connect(save)
        self.btn_save.clicked.connect(save)
        self.btn_reload.clicked.connect(reload)
        self.btn_delete.clicked.connect(delete)

    def load_lw(self):
        self.lw_save.clear()
        cubes = get_saved_cube()
        if cubes != False :
            for cube_name in cubes.keys() :
                self.lw_save.addItem(cube_name)

    def _sender_for_btnwidget(self):
        if self.animation :
            Rubik.appliquer_rotation_3D_animation(self.sender().text())
        else :
            Rubik.appliquer_rotation_3D(self.sender().text())
        
    def set_aniamtion (self):
        if not self.animation:
            self.animation = True
            self.buttons["animation"].setStyleSheet("background-color:#f31d58;")
        else :
            self.animation = False
            self.buttons["animation"].setStyleSheet("background-color:#111;")

####################################################################################################

Rubik = RubikCube()
UI = RubikWidget()
Rubik.generer_rubik3D_termine()

sel = Gui.Selection.getSelection()
Gui.SendMsgToActiveView("ViewFit")
