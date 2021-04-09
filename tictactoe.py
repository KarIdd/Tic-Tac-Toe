# import des librairies et de la police d'écriture
import pygame,sys
pygame.init()
police = pygame.font.Font("Minigame.otf",60)
import random as rd


class Morpion :
    # création du Morpion
    def __init__(self,profondeur):
        self.J1="X"
        self.IA="O"
        self.ecran=pygame.display.set_mode((600,600))       # création de la fenêtre
        self.grille=Grille(self.ecran)              # initialisation de la classe Grille dans la vaiable self.grille
        self.compteur=0
        self.profondeur=profondeur
        
    
    def test_fin_jeu(self,player):
        # teste si un joueur à gagner ou s'il y a égalité
        for i in range(3):
            if self.grille.grille[i][0]==self.grille.grille[i][1]==self.grille.grille[i][2]==player:
                return player
        for j in range(3):
            if self.grille.grille[0][j]==self.grille.grille[1][j]==self.grille.grille[2][j]==player:
                return player
        if self.grille.grille[0][0]==self.grille.grille[1][1]==self.grille.grille[2][2]==player:
            return player
        if self.grille.grille[2][0]==self.grille.grille[1][1]==self.grille.grille[0][2]==player:
            return player
        for i in range(3):
            for j in range(3):
                if self.grille.grille[i][j]==None:
                    return True
        return False
    
    
    def jeu(self):
        # lance la partie et gère les interactions entre le joueur et la machine
        pygame.display.set_caption("MORPION")
        players=[self.IA,self.J1]
        fin=False
        
        clock = pygame.time.Clock()
        
        while not fin:
            time = clock.tick(10)  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                player=players[self.compteur%2]
                
                if player==self.IA :
                    self.intelligence_artificielle(self.profondeur)
                        
                else:
                    if player==self.J1 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                        position = event.pos
                        position_x ,position_y = position[1]//200 ,position[0]//200
                        self.grille.fixer_la_valeur(position_x, position_y, self.J1)
                     
                if self.test_fin_jeu(player)==player or self.test_fin_jeu(player)==False:
                    fin=True
                    
                elif self.grille.compteur_on:
                    self.compteur += 1
                    self.grille.compteur_on = False
                    
            self.ecran.fill((240,240,240))
            self.grille.afficher()
            pygame.display.flip()
            
                    
        if self.test_fin_jeu(player)==player:
            # affiche le vainqueur
            texte = police.render(f"Gagnant : {player}",True,pygame.Color("#000000"))
            rectTexte = texte.get_rect()
            rectScreen = self.ecran.get_rect()
            rectTexte.center = rectScreen.center
            self.ecran.blit(texte,rectTexte)
            pygame.display.flip()
                    
        else:
            # affiche égalité
            texte = police.render("Egalité",True,pygame.Color("#000000"))
            rectTexte = texte.get_rect()
            rectScreen = self.ecran.get_rect()
            rectTexte.center = rectScreen.center
            self.ecran.blit(texte,rectTexte)
            pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
        
        
    def intelligence_artificielle(self,depth):
        # l'IA joue
        max_i,max_j=None,None
        maximum = -10000
        jeu = self.grille.grille            # copie du jeu dans une variable temporaire
        for i in range(3):
            for j in range(3):
                if jeu[i][j] == None:            # pour chaque case vide, l'IA joue
                    jeu[i][j] = self.IA
                    tmp = self.valeur_mini(jeu, depth-1)
                
                    if tmp > maximum or (tmp==maximum and rd.randint(0,2)==1):          # l'IA garde en mémoire le meilleur coup
                        maximum = tmp
                        max_i = i
                        max_j = j
                    jeu[i][j] = None                # l'IA réinitialise ses tentatives
        if self.test_fin_jeu(self.IA)==True:
            self.grille.fixer_la_valeur(max_i, max_j, self.IA)              # l'IA joue le meilleur coup
    
        
    def valeur_maxi(self,jeu, depth):
        # détermine le meilleur coup pour l'IA
        maximum = -10000
        if depth == 0 or self.test_fin_jeu(self.J1)!=True or self.test_fin_jeu(self.IA)!=True:
            return self.evaluer(jeu)
        for i in range(3):
            for j in range(3):
                if jeu[i][j] == None:
                    jeu[i][j] = self.IA
                    tmp = self.valeur_mini(jeu, depth-1);
        
                    if tmp > maximum:
                        maximum = tmp;
                    
                    jeu[i][j] = None
        return maximum
    
    
    def valeur_mini(self,jeu, depth):
        # détermine le milleur coup pour le joueur
        minimum = 10000

        if depth == 0 or self.test_fin_jeu(self.J1)!=True or self.test_fin_jeu(self.IA)!=True:
            return self.evaluer(jeu)
    
        for i in range(3):
            for j in range(3):
                if jeu[i][j] == None:
            
                    jeu[i][j] = self.J1
                    tmp = self.valeur_maxi(jeu, depth-1)
                
                    if tmp < minimum:
                        minimum = tmp
                    jeu[i][j] = None
        return minimum
    
    def nb_series(jeu, series_j1, series_j2, n = 0):
        # compte le nombre de séries de n pions alignés de chacun des joueurs
        series_j1, series_j2 = 0, 0
        compteur1, compteur2 = 0, 0
        largeur=len(jeu[0])
        
        # diagonale descendante
        for i in range(largeur):
            if jeu[i][i] == 1:
        
                compteur1+=1
                compteur2 = 0

                if compteur1 == n:
                    series_j1+=1
        
            elif jeu[i][i] ==2:
                compteur2+=1
                compteur1 = 0
     
                if compteur2 == n:
                     series_j2+=1

        compteur1, compteur2 = 0,0

        # diagonale montante
        for i in range(largeur):
            if jeu[i][largeur-i] == 1:
                compteur1+=1
                compteur2 = 0

                if compteur1 == n:
                    series_j1+=1
            elif jeu[i][largeur-i] == 2:
                compteur2+=1
                compteur1 = 0
     
                if compteur2 == n:
                     series_j2+=1

        # en ligne
        for i in range(largeur):
            compteur1, compteur2 = 0, 0
       
            # horizontalement
            for j in range(largeur):
                if jeu[i][j] == 1:
                    compteur1+=1
                    compteur2 = 0

                    if compteur1 == n:
                        series_j1+=1
            
                elif jeu[i][j] == 2:
                    compteur2+=1
                    compteur1 = 0

                    if compteur2 == n:
                        series_j2+=1

            compteur1,compteur2  = 0, 0

            # verticalement
            for j in range(largeur):
                if jeu[j][i] == 1:
                    compteur1+=1
                    compteur2 = 0

                    if compteur1 == n:
                        series_j1+=1
            
                elif jeu[j][i] == 2:
                    compteur2+=1
                    compteur1 = 0

                    if compteur2 == n:
                        series_j2+=1

    def evaluer(self,jeu): 
        # évalue la grille de jeu
        gagnant=None
        nb_de_pions = 0
    
        # compte le nombre de pions présents sur la grille
        for i in range(3):
            for j in range(3):
                if jeu[i][j] != None:
                    nb_de_pions+=1

        if self.test_fin_jeu(self.J1)!=True or self.test_fin_jeu(self.IA)!=True:
            gagnant = self.test_fin_jeu(self.J1)
        
        if gagnant == self.IA:
            return 1000 - nb_de_pions;
        
        elif gagnant == self.J1:
            return -1000 + nb_de_pions
        else:
            return 0

        # compte le nombre de séries de 2 pions alignés de chacun des joueurs
        series_j1 = 0
        series_j2 = 0
    
        nb_series(jeu, series_j1, series_j2, 2)

        return series_j1 - series_j2 
             
 

class Grille():
    # création de la grille
    def __init__(self,ecran):
        self.ecran=ecran
        self.lignes=[((200,0),(200,600)), ((400,0),(400,600)), ((0,200),(600,200)), ((0,400),(600,400))]
        self.grille=[[None,None,None],
                      [None,None,None],
                      [None,None,None]
                      ]
        self.compteur_on=False
      
        
        
    def afficher(self):
        # affiche la grille et des croix et des ronds en fonction de l'état du plateau
        for ligne in self.lignes :
            pygame.draw.line(self.ecran,(0,0,0),ligne[0],ligne[1],2)
        for y in range(0,len(self.grille)):
            for x in range(0,len(self.grille)):
                if self.grille[y][x] == 'X' :
                    pygame.draw.line(self.ecran, (255, 0, 0), (x * 200, y * 200), (200 + (x * 200), 200 + (y * 200)), 7) 
                    pygame.draw.line(self.ecran, (255, 0, 0), ((x * 200), 200 + (y * 200)), (200 + (x * 200), (y * 200)),7)

                elif self.grille[y][x] == 'O' :
                    pygame.draw.circle(self.ecran, (0, 0, 255), (100 + (x * 200), 100 + (y * 200)), 100, 7)
    
    def fixer_la_valeur(self,x,y,valeur):
        # met à jour la grille avec la nouvelle valeur
        if self.grille[x][y]==None:
            self.grille[x][y]=valeur
            self.compteur_on=True
           
    
    
# détermination de la difficulté de l'IA
info_niveau=0
info_niveau=int(input("Niveau : 1(facile) à 9(difficile)\nVotre choix : "))
while info_niveau<1 or info_niveau>9:
    print("Saisie invalide")
    info_niveau=int(input("Niveau : 1(facile) à 9(difficile)\nVotre choix : "))

game=Morpion(info_niveau)
game.jeu()



