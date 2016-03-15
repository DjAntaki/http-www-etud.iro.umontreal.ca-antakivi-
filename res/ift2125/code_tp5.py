#usr/bin/env
# *-* coding: utf8 *-*

from itertools import product

# Intro soft :
#   - Définir espaces d'états (i.e. dans notre cas, les sous-problèmes) 
#   - def base
#   - def récurrence
#   Approche bottom-up : calculer tous les cases dans un ordre qui assure qu'on aille tous les éléments de la récurrence déjà calculé avant.
#   Approche top-down : Explorer la récurrence et mémoïser (mettre en cache) les résultats des appels de la récurrence. 

#
# Intro moins soft (pas matière au cours) :
#
# La programation dynamique est une approche d'optimisation pour les prises de décisions séquentielles. Elle vise à régler un problème complexe en traitant des sous-problèmes (d'où le lien avec la récurrence)
#
#
# La prog. dyn. peut se généraliser par une récurrence selon l'équation de Bellman-Ford.
#
# J(x) = min_{u \in u(x)} [c(x,u) + J_{k+1}(f(x,u))] 
# 
# - x : l'état courant (un vecteur de paramètres)
# - u(x) : une fonction qui définit les choix possibles de l'état x
# - c(x,u) : fonction de coût associé à l'état x et la décision u
# - f(x,u) : la fonction de transition associée à l'état x et la décision u
#
# Pour rendre l'équation d'en haut moins lourde je n'ai pas introduit la notion (facultative) d'étapes (k). Celle-ci peut toutefois être très utile pour modéliser certaines situations avec des dépendances temporelles.
#
# Étapes pour modéliser un problème par programmation dynamique :
#   - Définir l'espace d'états
#   - Définir une fonction qui génère les choix possibles 
#   - Définir une fonction de transition 
#   - Définition d'une fonction de coût 
#
# Notion importante :
#
#  - La malédiction de dimensionnalité (e.g. alignement de x chaines de caractères)
#
# Présentation d'aspect avancés de la programmation dynamique :
#
#  - Il est possible de définir des espaces d'états avec une infinité d'éléments. (e.g. Prog. dyn. continue a.k.a "optimal control theory", prog. dyn. sur horizon infini (k -> \infty))
#  - Il est possible d'introduire des variables aléatoires dans l'équation de Bellman-Ford. On parle dans ce cas de prog. dyn. stochastique.
#





## TP5

# *** Veuillez noter que numpy est utilisé pour l'étape (facultative) d'affichage des tableaux pour l'algorithme de retour de monnaie. De brièves modifications devrait vous permettre de vous débarasser de cette dépendance si c'est votre souhait.

# Dans le cas où vous n'avez pas numpy, vous pouvez l'installer avec le gestionnaire de package pip et la commande :
# sudo pip install numpy

#
# Numéro 2
#

#Voici l'algorithme de programmation dynamique pour le retour de monnaie tel que présenté dans B&B.
# Le but de cet algorithme est de calculer le nombre de pièce minimal nécessaire pour remettre un montant N.
# Celui-ci considère un nombre illimité de chaque type de pièces.

monnaie_canadienne = [1,5,10,25,100,200]

def retour_monnaie(d, N, print_result=False):
    """ 
    d : valeur de chacune des pièces.
    N : Montant à rendre 
    """
    
    n = len(d)
    C = [[None for j in range(N+1)] for i in range(n+1)]
    
    #Initialisation
    for i in range(0,n+1):
        C[i][0] = 0
    for j in range(1,N+1):
        C[0][j] = float('inf')
        
    # on itere a travers tout le tableau
    for i,j in product(range(1,n+1),range(1,N+1)):
        v_i = d[i-1] #petit ajustement d'index
        if (j >= v_i) :           
            t = 1 + C[i][j-v_i]
            C[i][j] = min(C[i-1][j],t)            
        else :
            # On ne peut remettre une pièce puisque sa valeur excède le montant à remettre.
            C[i][j] = C[i-1][j]


    print(C)    
    
    if print_result :
        import numpy
        print(numpy.array(C))

    return C[n][N]

#Appliquons l'algorithme sur un exemple :
rem=27
print("Montant à remettre : " +str(rem))
retour_monnaie(monnaie_canadienne, rem, True)


#
# Il est possible de faire une variante de cette algorithme qui considère un nombre fini de pièce.
# Nous ajoutons tout simplement un compteur b_i, pour les pièces de valeur i qui indique combien de pièces peuvent encore être utilisése. Lorsque b_i atteint 0, on utilise la solution optimale qui n'utilise pas les pièces de valeur i.


def retour_monnaie2(d,b,N,print_result=False):
    """ 
    d : valeur de chacune des pièces, une liste d'entiers non-négatifs.
    b: compte des pièces, une liste d'entiers non-négatifs.  
    N : Montant à rendre, un entier.
    """
    n = len(d) # Nombre de type de pièce
    assert n == len(b) 
    C = [[None for j in range(N+1)] for i in range(n+1)]
    B = [[None for j in range(N+1)] for i in range(n+1)]    
    
    
    #Initialisation
    for i in range(1,n+1):
        B[i][0] = b[i-1]
    
    for i in range(0,n+1):
        C[i][0] = 0
    for j in range(1,N+1):
        C[0][j] = float('inf')
    
    #Calculer la récurrence (bottom-up)   
    for i,j in product(range(1,n+1),range(1,N+1)):
        
        v_i = d[i-1] #Ajustement d'indice pour que ça corresponde au pseudo-code donné.
        if (j >= v_i) and B[i][j-v_i] > 0:           
            t = 1 + C[i][j-v_i]
            C[i][j] = min(C[i-1][j],t)
            
            if not C[i][j] == C[i-1][j]:
                B[i][j] = B[i][j-v_i]-1 # On prend une pièce de type i, on prend la valeur du compteur correspondant
            else :
                B[i][j] = b[i-1]
        else :
            # On ne peut remettre une pièce puisque sa valeur excède le montant à remettre.
            C[i][j] = C[i-1][j]
            B[i][j] = b[i-1] #on prends

    if print_result :
        import numpy
        print(numpy.array(C))

    return C[n][N]

compte = [4, 10, 1, 0, 4, 1]
print("Montant à remettre : " +str(rem))
print("Compte des pièces à notre disposition : " +str(compte))
retour_monnaie2(monnaie_canadienne, compte, rem, True)

#La version récurrente est très similaire. Toutefois, il n'est pas nécessaire de calculer toutes les cases pour arriver à une réponse! En partant de la fin et en stockant les résultats de nos calculs, on peut s'éviter dans certains cas de calculer toute la table.

def rec_retour(d,N,print_result=False):
    """récurence + memoisation = best"""

    n = len(d) # Nombre de type de pièce
    C = [[None for j in range(N+1)] for i in range(n+1)]
    
    #Initialisation
    for i in range(1,n+1):
        C[i][0] = 0
    for j in range(N+1):
        C[0][j] = float('inf')

    #Récurrence, qui n'explore pas toutes les cases (top-down)
    def _rec_retour(i,j):
        if not C[i][j] is None :
            return C[i][j]
        else :
            v_i = d[i-1]
            if (j >= v_i) : #and b[i] > 0: #le compteur de pièce ne doit pas être à 0.            
                t = 1 + _rec_retour(i,j-v_i)
                C[i][j] = min(_rec_retour(i-1,j),t)
                return C[i][j]
#                if (C[i,j]==t) : 
#                    b[i] -= 1 # On prend une pièce de type i, donc on descend le compteur
            else :
                C[i][j] = _rec_retour(i-1,j)
                return C[i][j]
    

    sol = _rec_retour(n,N)

    if print_result :
        import numpy
        print(numpy.array(C))

    return sol

#Le même exemple avec la version par récurrence
print("Version avec récurrence")
print("Montant à remettre : " +str(rem))

rec_retour(monnaie_canadienne,rem,True)


#
# Numéro 4 (le numéro 3 est présenté après car il utilise le code du numéro 4)
#

#Voici l'algorithme du sac-à-dos.

def knapsack(objs, W, print_result=False):
    """
    objs : a list of (value,weight) tuples (can be floats) 
    W: an integer reprenting a the maximum weight allowed in the bag 
    """
    n = len(objs)
    V = [[None for i in range(W+1)] for j in range(n+1)]    
    
    for j in range(W+1):
        V[0][j] = 0
    
    for i in range(1,n+1):
        for j in range(W+1):
            v_i, w_i = objs[i-1]
            if j >= w_i :
                V[i][j] = max(V[i-1][j],V[i-1][j-w_i]+v_i)
                #Chaque objet ne peut être mis qu'une seule fois dans le sac à dos. C'est pour ça que chaque choix de la récurrence pointe vers le ligne précédente du tableau.                
    
            else :
                V[i][j] = V[i-1][j] #Ne pas mettre l'objet dans le sac
                
    if print_result :
        import numpy
        print(numpy.array(V))
                       
    return V[n][W]

#
# Numéro 3
#

objs=[(1,1),(6,2),(18,5),(22,6),(28,7)]
print("objets",objs, "taille du sac :",11)
print(knapsack(objs,11,True))
objs.reverse()
print("objets",objs, "taille du sac :",11)
print(objs)
print(knapsack(objs,11,True))

# Prenez note que la dernière ligne reste inchangée car celle-ci prends en compte toutes les pièces.    

#
# Numéro 6
#

# Peut-il y avoir plusieurs solution optimales au problème du sac-à-dos?

# Oui. Lorsque V[i-1,j] = V[i-1,j-w_i] + v_i, il est aussi avantageux de choisir l'objet i que de ne pas le choisir.

# Voici un exemple. Soit un sac à dos de capacité de 3 unités et les objets suivants : [(v_1=3,w_1=3),(v_2=2,w_2=2),(v_3=1,w_3=1)]. Deux solutions optimale existe soit {o_1} ou {o_2,o_3}

# Il est possible d'adapter les algorithmes de programmation dynamique pour pouvoir calculer toutes les solutions optimales. Il suffit de garder en mémoire pour chaque état le(s) état(s) précédent(s) qui lui donne sa valeur optimale. Il est recommandé d'utiliser la version récursive pour faire ce calcul de façon plus élégante. 

# Si on ne souhaite pas utiliser plus de mémoire, il est aussi possible de retrouver la solution en fonction du tableau remplit. Ce sera plus coûteux en temps par contre.

#
# Numéro 7
#

#Lorsqu'on considère un nombre infini d'objets de chaque type, la modification ci-dessous a comme conséquence d'examiner une solution optimale qui pourrait avoir précédemment utilisé un object de type i. 
                
                # - Rajouter V[i,j-w_i]+v_i comme choix dans la récurrence.
                #V[i,j] = max(V[i-1,j],V[i-1,j-w_i]+v_i,V[i,j-w_i]+v_i)




