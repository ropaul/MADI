# -*- coding: utf-8 -*-

from mdpmadi16v1 import *

#On réfléchit en COÛTS

#actions
actR = 0
actT = 1
actY = 2
actU = 3
actJ = 4
actH = 5
actG = 6
actF = 7

def transitionAction(grille, i, j, action):
    nbL = len(grille)
    nbC = len(grille[0])
    trans = {}
    if action == actR:
        if (i-1) < 0 or (j-2) < 0:
            trans[i,j] = 1
        else:
            trans = transition(g, i-1, j-2)
    if action == actT:
        if (i-2) < 0 or (j-1) < 0:
            trans[i,j] = 1
        else:
            trans = transition(g, i-2, j-1)
    if action == actY:
        if (i-2) < 0 or (j+1) > (nbC-1):
            trans[i,j] = 1
        else:
            trans = transition(g, i-2, j+1)
    if action == actU:
        if (i-1) < 0 or (j+2) > (nbC-1):
            trans[i,j] = 1
        else:
            trans = transition(g, i-1, j+2)
    if action == actJ:
        if (i+1) > (nbL-1) or (j+2) > (nbC-1):
            trans[i,j] = 1
        else:
            trans = transition(g, i+1, j+2)
    if action == actH:
        if (i+2) > (nbL-1) or (j+1) > (nbC-1):
            trans[i,j] = 1
        else:
            trans = transition(g, i+2, j+1)
    if action == actG:
        if (i+2) > (nbL-1) or (j-1) < 0:
            trans[i,j] = 1
        else:
            trans = transition(g, i+2, j-1)
    if action == actF:
        if (i+1) > (nbL-1) or (j-2) < 0:
            trans[i,j] = 1
        else:
            trans = transition(g, i+1, j-2)
    return trans
            

# Définition du PL dual de l'approche égalitariste
# contraintes (1) : sum(Xsa pourtout a) - gamma*sum(sum(T(s',a,s)*Xsa pourtout a) pourtout s') = µ(s) pourtout s
# contraintes (2) : Xsa >= 0 pourtout s, pourtout a
# contraintes (3) : z - sum(sum(Ri(s,a)*Xsa pourtout a) pourtout s) <= 0 pourtout i
#A FAIRE : RAJOUTER LES VARIABLES CONTRAIGNANT LES POLITIQUES PURES
def matriceMinmax(grille, gamma):
    nbL = len(grille)
    nbC = len(grille[0])
    #Contraintes
    A = np.zeros(((nbL*nbC+1)*(8+1)+2, nbL*nbC*8+1+8))
    b = np.zeros((nbL*nbC+1)*(8+1)+2)
    b[0]=1 #µ((0,0)) = 1
    for i in range(nbL):
        for j in range(nbC):
            for k in range(8):
                A[i*nbC+j][(i*nbC+j)*8+k] = 1 #contraintes (1) : sum(Xsa pourtout a)
                A[nbL*nbC+1+((i*nbC+j)*8+k)][(i*nbC+j)*8+k]=1 #contraintes (2)
                if i != nbL-1 or j != nbC-1:
                    #contraintes (1) : -gamma
                    trans = transitionAction(grille, i, j, k)
                    for t in trans:
                        A[t[0]*nbC+t[1]][(i*nbC+j)*8+k]=-gamma*trans[t]
                    if not trans:
                        A[(nbL*nbC+1)*9][(i*nbC+j)*8+k]=0
                        A[(nbL*nbC+1)*9+1][(i*nbC+j)*8+k]=0
                    else:
                        if grille[i][j] == 2: #case bleue
                            A[(nbL*nbC+1)*9][(i*nbC+j)*8+k]=-1
                        if grille[i][j] == 3: #case rouge
                            A[(nbL*nbC+1)*9+1][(i*nbC+j)*8+k]=-1
                else:
                    A[(nbL*nbC+1)*9][(i*nbC+j)*8+k]=-1000
                    A[(nbL*nbC+1)*9+1][(i*nbC+j)*8+k]=-1000
    #contraintes sur l'etat puits
    for i in range(8):
        A[nbL*nbC][nbL*nbC*8+i]=1-gamma #contraintes (1)
        A[nbL*nbC][(nbL*nbC-1)*8+i]=-gamma #contraintes (1)
        A[nbL*nbC+1+nbL*nbC*8+i][nbL*nbC*8+i]=1 #contraintes (2)
    A[(nbL*nbC+1)*9][(nbL*nbC+1)*8]=1
    A[(nbL*nbC+1)*9+1][(nbL*nbC+1)*8]=1
    #Fonction objectif
    obj = np.zeros(nbL*nbC*8+1+8)
    obj[nbL*nbC*8+8]=1
    return (A, b, obj)
    
        
                            

