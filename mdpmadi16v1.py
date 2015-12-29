# script pion.py hjyf
from Tkinter import *
import numpy
import numpy as np
import time
import matplotlib.pyplot as plt

def initialize():
    global PosX,PosY,cost, globalcost
# position initiale du robot
    PosX = 20+10*zoom
    PosY = 20+10*zoom
    for k in range(5):
        cost[k]=0
# cout et affichage
    Canevas.coords(Pion,PosX -9*zoom, PosY -9*zoom, PosX +9*zoom, PosY +9*zoom)
    w.config(text='Cost = '+ str(globalcost))

def colordraw(g,nblignes,nbcolonnes):
    pmur=0.15 #0.15
    pblanc=0.55 #0.55
    pverte=0.1
    pbleue=0.1
    prouge=0.1
    pnoire=0.1
    for i in range(nblignes):
        for j in range(nbcolonnes):
            z=np.random.uniform(0,1)
            if z < pmur:
                c=-1
            else:
                if z < pmur+ pblanc:
                    c=0
                else:    
                    if z < pmur+ pblanc + pverte:
                        c=1
                    else:
                        if z < pmur+ pblanc +pverte + pbleue:
                            c=2
                        else:
                            if z< pmur + pblanc + pverte + pbleue +prouge:
                                c=3
                            else:
                                c=4   
            g[i,j]=c
    g[0,0]=0
    g[0,1]=0
    g[2,0]=0    
    g[nblignes-1,nbcolonnes-1]=0
    g[nblignes-2,nbcolonnes-1]=0
    g[nblignes-1,nbcolonnes-2]=0
    for i in range(nblignes):
        for j in range(nbcolonnes):          
            y =zoom*20*i+20
            x =zoom*20*j+20
            if i == 0 and j == 0 :
                Canevas.create_text(x+zoom*10,y+zoom*10,text="DEPART",fill=myblack,font = "Verdana "+str(int(10*zoom/3))+" bold")
            if i == nblignes -1 and j == nbcolonnes -1 :
                Canevas.create_text(x+zoom*10,y+zoom*10,text="BUT",fill=myblack,font = "Verdana "+str(int(10*zoom/3))+" bold")
               
            if g[i,j]>0:            
                Canevas.create_oval(x+zoom*(10-3),y+zoom*(10-3),x+zoom*(10+3),y+zoom*(10+3),width=1,outline=color[g[i,j]],fill=color[g[i,j]])
            else:
                if g[i,j]<0:
                    Canevas.create_rectangle(x, y, x+zoom*20, y+zoom*20, fill=myblack)
                    Canevas.create_rectangle(x, y, x+zoom*20, y+zoom*20, fill=myblack)
  
def Clavier(event):
    global PosX,PosY,cost,g, globalcost
    touche = event.keysym
    cj=(PosX-30)/(20*zoom)
    li=(PosY-30)/(20*zoom)
    changed=0
    # deplacement aleatoire en appuyant sur space
    if touche == 'space':
#        t=np.random.randint(6)
#        lettre = ['f','g','h','j','y','u',]
#        touche=lettre[t]
        touche = marcheAutoMixte(li,cj)
        print "i=" +str(li) + ",j=" +str(cj)
        print touche
    # deplacement (-2,1)
    if touche == 'y' and li>1 and cj < nbcolonnes-1 and g[li-2,cj+1]>-1:
        PosY -= zoom*20*2
        PosX += zoom*20 
        cost[g[li-2,cj+1]]+=1 
        changed=1
    # deplacement (-2,-1)
    if touche == 't' and li>1 and cj > 0 and g[li-2,cj-1]>-1:
        PosY -= zoom*20*2       
        PosX -= zoom*20                 
        cost[g[li-2,cj-1]]+=1
        changed=1
   # deplacement (-1,2)
    if touche == 'u' and li>0 and cj < nbcolonnes-2 and g[li-1,cj+2]>-1:
        PosY -= zoom*20        
        PosX += zoom*20*2       
        cost[g[li-1,cj+2]]+=1
        changed=1
    # deplacement (-1,-2)
    if touche == 'r' and li>0 and cj >1 and g[li-1,cj-2]>-1:
        PosY -= zoom*20
        PosX -= zoom*20*2           
        cost[g[li-1,cj-2]]+=1
        changed=1
     # deplacement (2,1)  
    if touche == 'h' and li<nblignes-2 and cj < nbcolonnes-1 and g[li+2,cj+1]>-1:
        PosY += zoom*20*2
        PosX += zoom*20 
        cost[g[li+2,cj+1]]+=1
        changed=1
    # deplacement (2,-1)
    if touche == 'g' and li<nblignes-2 and cj > 0 and g[li+2,cj-1]>-1:
        PosY += zoom*20*2       
        PosX -= zoom*20                 
        cost[g[li+2,cj-1]]+=1
        changed=1
   # deplacement (1,2)
    if touche == 'j' and li<nblignes-1 and cj < nbcolonnes-2 and g[li+1,cj+2]>-1:
        PosY += zoom*20        
        PosX += zoom*20*2       
        cost[g[li+1,cj+2]]+=1
        changed=1
    # deplacement (1,-2)
    if touche == 'f' and li<nblignes-1 and cj >1 and g[li+1,cj-2]>-1:
        PosY += zoom*20
        PosX -= zoom*20*2           
        cost[g[li+1,cj-2]]+=1 
        changed=1


# La variable alea =1 si on veut des effets aleatoires sinon les transitions sont deterministes
    #On ajoute un effet aleatoire dans les transitions
    if alea==1 and changed==1:
        t=np.random.uniform(0,1)    
        if t>0.5:
            d=np.random.randint(8)
            dli=0
            if d== 0 or d==1 or d==2:
                dli=-1
            if d== 4 or d==5 or d==6:
                dli==1
            dcj=0
            if d==0 or d==7 or d==6:
                dcj=-1
            if d==2 or d==3 or d==4:
                dcj=1    
        # l'effet aleatoire est applique s'il cree un deplacement sur une case admissible     
            NewPosY = PosY+zoom*20*dli
            NewPosX = PosX+zoom*20*dcj        
            newcj=(NewPosX-30)/(20*zoom)
            newli=(NewPosY-30)/(20*zoom)
            print('d',dli,dcj)
            if newli>=0 and newcj>=0 and newli<=nblignes-1 and newcj<=nbcolonnes-1 and g[newli,newcj]>-1:
                PosY=NewPosY
                PosX=NewPosX            
            
# on dessine le pion a sa nouvelle position
    Canevas.coords(Pion,PosX -9*zoom, PosY -9*zoom, PosX +9*zoom, PosY +9*zoom)       
    globalcost=0    
    for k in range(5):
        globalcost+=cost[k]*weight[k]
    w.config(text='Cost = '+ str(globalcost))  


def marcheAutoMixte(i,j):
    global sol
    return sol[i][j]



################################################################################
#
#                            PARTIE 1.B  
#
################################################################################




##dit si l est autorise d'aller sur cette case ou pas
def autorize (g, i,j,nblignes, nbcolonnes):
    if ( i < 0 or j < 0):
        return False
    if (i >= nblignes or j >= nbcolonnes):
        return False
    if g[j][i]== -1 :
        return False #si c'est un mur
#    if (i == nblignes -1 and j == nbcolonnes -1):
#        return False #si c'est la case de fin , on va nul part
    return True


def iterationValeurDeterministe(g,  gamma ):
    global nblignes, nbcolonnes,directions, directionsValue
    vbut = 1000
    oldV0 = np.zeros((nblignes,nbcolonnes))
    V0 = np.zeros((nblignes,nbcolonnes))
    V0[nbcolonnes-1][nblignes-1]=vbut
    QR =np.zeros((nbcolonnes,nblignes))
    QT =np.zeros((nbcolonnes,nblignes))
    QF =np.zeros((nbcolonnes,nblignes))
    QG =np.zeros((nbcolonnes,nblignes))
    QY =np.zeros((nbcolonnes,nblignes))
    QU =np.zeros((nbcolonnes,nblignes))
    QJ =np.zeros((nbcolonnes,nblignes))
    QH =np.zeros((nbcolonnes,nblignes))
    Q = [QR,QT,QY,QU,QF,QG,QJ,QH]
    epsilon = 1
    t =0
    maxdiff = -10000
    while ( abs ( maxdiff) > epsilon or t ==0 ) :
        
        maxdiff = 0
        t+= 1;
        oldV0 =np.copy( V0)
        for j in range (nbcolonnes):
            for i in range (nblignes):  
                for direction in directions:
                    sumTV = 0
                  #  trans = transition (g, direction, i , j , probaTransition)
                    #print trans
                    kprime = i + directionsValue[direction][1]
                    lprime = j +directionsValue[direction][0]
#                    if( kprime == nblignes -1 and lprime == nblignes -1):
#                        print str(i) +"  " + str(j) + "  "+str (autorize (g, kprime,lprime,nblignes, nbcolonnes))
                    if ( autorize (g, kprime,lprime,nblignes, nbcolonnes)):
                        sumTV += 1  * oldV0[lprime][kprime] 
                    else :
                        sumTV += -10000
                    Q[direction][j][i]= -1  +  gamma * sumTV
                V0[j][i] = max (Q[0][j][i],Q[1][j][i],Q[2][j][i],Q[3][j][i],Q[4][j][i],Q[5][j][i],Q[6][j][i],Q[7][j][i])
                if (i == nblignes -1 and  j == nbcolonnes -1 ) :
                    V0[j][i] =  vbut   
                    
                maxdiff = max (maxdiff , abs( V0[j][i] - oldV0[j][i]))
        
                
    sol = np.zeros((nblignes,nbcolonnes),dtype=numpy.str)
    for i in range (nblignes):
        for j in range (nbcolonnes):  
            if ( V0[j][i] == Q[0][j][i]):
                sol [j][i] = strDirections[0]
            if ( V0[j][i] == Q[1][j][i]):
                sol [j][i] = strDirections[1]
            if ( V0[j][i] == Q[2][j][i]):
                sol [j][i] = strDirections[2]
            if ( V0[j][i] == Q[3][j][i]):
                sol [j][i] = strDirections[3]
            if ( V0[j][i] == Q[4][j][i]):
                sol [j][i] = strDirections[4]
            if ( V0[j][i] == Q[5][j][i]):
                sol [j][i] = strDirections[5]
            if ( V0[j][i] == Q[6][j][i]):
                sol [j][i] = strDirections[6]
            if ( V0[j][i] == Q[7][j][i]):
                sol [j][i] = strDirections[7]
     
    return sol





################################################################################
#
#                            PARTIE 1.C
#
################################################################################


#Calcule la loi de probabilite de transition pour  une position (i, j) donnees.
#Retourne trans, la loi de probabilite sous la forme d'un dictionnaire
#Note : si une position n'appartient pas au dictionnaire, alors la probabilite d'aller dans cette position est nulle.
def transition(g, i, j):
    nbl=g.shape[0]
    nbc=g.shape[1]
    trans = {}
    cpt = 0
    if g[i,j]==-1 :
        return trans
    for iprime in range (-1,2):
        for jprime in range (-1,2):
            if (i +iprime>= 0 and i +iprime < nbl and j + jprime >= 0 and j + jprime < nbc):
                if g[i +iprime, j +jprime] != -1:
                    cpt +=1
    cpt+= -1 # on retire la valeur (i,j)
    
    for iprime in range (-1,2):
        for jprime in range (-1,2):
            if (i +iprime>= 0 and i +iprime < nbl and j + jprime >= 0 and j + jprime < nbc):
                if g[i +iprime][ j +jprime] != -1:
                    trans[i +iprime, j +jprime] = float (1/16.0)
    trans[i,j] = float ( 1 - (cpt/16.0))
    return trans



def iterationValeurNonDeterministe(g,  gamma ):
    global nblignes, nbcolonnes,directions, directionsValue
    vbut = 1000
    oldV0 = np.zeros((nblignes,nbcolonnes))
    V0 = np.zeros((nblignes,nbcolonnes))
    V0[nbcolonnes-1][nblignes-1]=vbut
    QR =np.zeros((nbcolonnes,nblignes))
    QT =np.zeros((nbcolonnes,nblignes))
    QF =np.zeros((nbcolonnes,nblignes))
    QG =np.zeros((nbcolonnes,nblignes))
    QY =np.zeros((nbcolonnes,nblignes))
    QU =np.zeros((nbcolonnes,nblignes))
    QJ =np.zeros((nbcolonnes,nblignes))
    QH =np.zeros((nbcolonnes,nblignes))
    Q = [QR,QT,QY,QU,QF,QG,QJ,QH]
    epsilon = 0.1
  
    maxdiff = -10000
    while ( abs ( maxdiff) > epsilon or t ==0 ) :
        
        maxdiff = 0
      
        oldV0 =np.copy( V0)
        for j in range (nbcolonnes):
            for i in range (nblignes):  
                for direction in directions:
                    sumTV = 0
                  #  trans = transition (g, direction, i , j , probaTransition)
                    #print trans
                    kprime = i + directionsValue[direction][1]
                    lprime = j +directionsValue[direction][0]
#                    if( kprime == nblignes -1 and lprime == nblignes -1):
#                        print str(i) +"  " + str(j) + "  "+str (autorize (g, kprime,lprime,nblignes, nbcolonnes))
                    if ( autorize (g, kprime,lprime,nblignes, nbcolonnes)):
                        trans = transition(g, kprime,lprime)
                        for t in trans :
                            sumTV += trans[t]  * oldV0[t[0]][t[1]] 
                    else :
                        sumTV += -10000
                    Q[direction][j][i]= -1  +  gamma * sumTV
                V0[j][i] = max (Q[0][j][i],Q[1][j][i],Q[2][j][i],Q[3][j][i],Q[4][j][i],Q[5][j][i],Q[6][j][i],Q[7][j][i])
                if (i == nblignes -1 and  j == nbcolonnes -1 ) :
                    V0[j][i] =  vbut   
                    
                maxdiff = max (maxdiff , abs( V0[j][i] - oldV0[j][i]))
        
                
    sol = np.zeros((nblignes,nbcolonnes),dtype=numpy.str)
    for i in range (nblignes):
        for j in range (nbcolonnes):  
            if ( V0[j][i] == Q[0][j][i]):
                sol [j][i] = strDirections[0]
            if ( V0[j][i] == Q[1][j][i]):
                sol [j][i] = strDirections[1]
            if ( V0[j][i] == Q[2][j][i]):
                sol [j][i] = strDirections[2]
            if ( V0[j][i] == Q[3][j][i]):
                sol [j][i] = strDirections[3]
            if ( V0[j][i] == Q[4][j][i]):
                sol [j][i] = strDirections[4]
            if ( V0[j][i] == Q[5][j][i]):
                sol [j][i] = strDirections[5]
            if ( V0[j][i] == Q[6][j][i]):
                sol [j][i] = strDirections[6]
            if ( V0[j][i] == Q[7][j][i]):
                sol [j][i] = strDirections[7]
     
    return sol


################################################################################
#
#                            FONCTION TEST
#
################################################################################


def testDeterministe(tailleDebut,tailleFin,nbiteration) :
    global nbcolonnes, nblignes, g
    tabResultMoy = np.zeros(tailleFin - tailleDebut)
    tabResultVar = np.zeros(tailleFin - tailleDebut)
    tabIteration = np.zeros (nbiteration)
    xResult = range (tailleDebut,tailleFin)
    for taille in xResult:
        nblignes=taille
        nbcolonnes=taille
        for i in range (nbiteration):
            
            g= np.zeros((taille,taille), dtype=numpy.int)
            timer = float (time.time() )
            iterationValeurDeterministe(g, 0.9)
            tabIteration[i] = time.time() - timer
        tabResultMoy[taille - tailleDebut] = np.average(tabIteration)
        tabResultVar[taille - tailleDebut] = np.var(tabIteration)
        print str( 1.00 *(taille -tailleDebut) /(tailleFin -tailleDebut) *100) + " %" 
    return xResult,tabResultMoy,tabResultVar
    
def testNonDeterministe(tailleDebut,tailleFin,nbiteration) :
    global nbcolonnes, nblignes, g
    tabResultMoy = np.zeros(tailleFin - tailleDebut)
    tabResultVar = np.zeros(tailleFin - tailleDebut)
    tabIteration = np.zeros (nbiteration)
    xResult = range (tailleDebut,tailleFin)
    for taille in xResult:
        nblignes=taille
        nbcolonnes=taille
        for i in range (nbiteration):
            
            g= np.zeros((taille,taille), dtype=numpy.int)
            timer = float (time.time() )
            iterationValeurDeterministe(g, 0.9)
            tabIteration[i] = time.time() - timer
        tabResultMoy[taille - tailleDebut] = np.average(tabIteration)
        tabResultVar[taille - tailleDebut] = np.var(tabIteration)
        print str( 1.00 *(taille -tailleDebut) /(tailleFin -tailleDebut) *100) + " %" 
    return xResult,tabResultMoy,tabResultVar
    
def testNonDeterministeGamma(gammaDebut,gammaFin,nbiteration) :
    global nbcolonnes, nblignes, g
    tabResultMoy = np.zeros(gammaFin - gammaDebut)
    tabResultVar = np.zeros(gammaFin - gammaDebut)
    tabIteration = np.zeros (nbiteration)
    xResult = range (gammaDebut,gammaFin)
    nblignes=10
    nbcolonnes=10
    for gamma in xResult:
        for i in range (nbiteration):    
            g= np.zeros((taille,taille), dtype=numpy.int)
            timer = float (time.time() )
            iterationValeurDeterministe(g, gamma   )
            tabIteration[i] = time.time() - timer
        tabResultMoy[gamma - gammaDebut] = np.average(tabIteration)
        tabResultVar[gamma - gammaDebut] = np.var(tabIteration)
        print str( 1.00 *(gamma -gammaDebut) /(gammaFin -gammaDebut) *100) + " %" 
    return xResult,tabResultMoy,tabResultVar

def ploter(x , ymoy , yvar):
    taille = len(x)
    varSup = np.zeros(taille)
    varInf = np.zeros(taille)
    for i in range (taille):
        varSup[i] =ymoy[i] + yvar[i]
        varInf[i] =ymoy[i] - yvar[i]
    plt.plot(x, ymoy, 'bs', x, varSup, 'r--', x, varInf, 'r--')
    plt.show()
#    plt.plot(x, ymoy, 'bs', x, yvar, 'r--')
#    plt.show()
    plt.plot( x, yvar, 'r--')
    plt.show()


################################################################################
#
#                            VARIABLES
#
################################################################################


Mafenetre = Tk()
Mafenetre.title('MDP')

zoom=2

alea = 0 #transitions aleatoires si alea =1 sinon mettre alea=0

#taille de la grille
nblignes=6
nbcolonnes=6
 
globalcost=0

# Creation d'un widget Canvas (pour la grille)
Largeur = zoom*20*nbcolonnes+40
Hauteur = zoom*20*nblignes+40
 
# valeurs de la grille
g= np.zeros((nblignes,nbcolonnes), dtype=numpy.int)
cost= np.zeros(5, dtype=numpy.int)
weight= np.zeros(5, dtype=numpy.int)
weight[0] = 1
weight[1] = 10
weight[2] = 20
weight[3] = 30
weight[4] = 40

# def des couleurs
myred="#D20B18"
mygreen="#25A531"
myblue="#0B79F7"
mygrey="#E8E8EB"
myyellow="#F9FB70"
myblack="#2D2B2B"
mywalls="#5E5E64"
mywhite="#FFFFFF"
color=[mywhite,mygreen,myblue,myred,myblack]

#directions
R=0
T=1
Y=2
U=3
F=4
G=5
J=6
H=7

directions= [R,T,Y,U,F,G,J,H]
strDirections= ["r","t","y","u","f","g","j","h"]

dirR=[-1,-2]
dirT=[-2,-1]
dirY=[-2,+1]
dirU=[-1,+2]
dirF=[+1,-2]
dirG=[+2,-1]
dirJ=[+1,+2]
dirH=[+2,+1]

directionsValue = [dirR,dirT,dirY,dirU,dirF,dirG,dirJ,dirH]



################################################################################
#
#                            RESULTATS TESTS
#
################################################################################


tailleDebut=10
tailleFin =30
nbiteration = 10

x, ymoy,yvar = testDeterministe(tailleDebut,tailleFin,nbiteration)
print ymoy
print yvar
ploter (x,ymoy,yvar)


################################################################################
#
#                            GRAPHIQUES
#
################################################################################



## ecriture du quadrillage et coloration
#Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg =mywhite)
#for i in range(nblignes+1):
#    ni=zoom*20*i+20
#    Canevas.create_line(20, ni, Largeur-20,ni)
#for j in range(nbcolonnes+1):
#    nj=zoom*20*j+20
#    Canevas.create_line(nj, 20, nj, Hauteur-20)
#colordraw(g,nblignes,nbcolonnes)
#
# 
#Canevas.focus_set()
#Canevas.bind('<Key>',Clavier)
#Canevas.pack(padx =5, pady =5)
#
#PosX = 20+10*zoom
#PosY = 20+10*zoom
#
## Creation d'un widget Button (bouton Quitter)
#Button(Mafenetre, text ='Restart', command = initialize).pack(side=LEFT,padx=5,pady=5)
#Button(Mafenetre, text ='Quit', command = Mafenetre.destroy).pack(side=LEFT,padx=5,pady=5)
#
#w = Label(Mafenetre, text='Cost = '+str(globalcost),fg=myblack,font = "Verdana 14 bold")
#w.pack() 
#
#Pion = Canevas.create_oval(PosX-10,PosY-10,PosX+10,PosY+10,width=2,outline='black',fill=myyellow)
#
#initialize()
#
#####################################
##
##         test
##
######################################
#
#sol = iterationValeurNonDeterministe(g, 0.9 )
#
#print sol
#
#
#
#
#Mafenetre.mainloop()

