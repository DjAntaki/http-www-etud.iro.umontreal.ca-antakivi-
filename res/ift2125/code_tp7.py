#!/usr/bin/python
# -*- coding: utf-8 -*-

# Algorithmes divides and conquer

def mergesort(T):
    if len(T) < 5:
        return sorted(T)
    else :
        U = T[:ceil(len(T)/2)]
        V = T[ceil(len(T)/2):]
        m = merge(U,V)
        return m

def merge_sentinel(U,V):
    """ la version avec sentinelle, donné dans B&B"""
    n = len(U) + len(V)
    i,j = 0,0
    
    #On rajoute les sentinelles
    U.append(float('inf'))
    V.append(float('inf'))
    T = []
    # ou T = [0 for t in range(n)]
    for k in range(n):
        if U[i] < V[j]:
            T.append(U[i])
            i += 1
        else :
            T.append(V[j])
            j += 1
    return T
            #
    
    
def merge(U,V):
    """ U, V : deux listes d'entiers"""
    i,j = 0,0
    m,n = len(U), len(V)
    
    # la liste dans lequel on insérera les valeurs triées 
    T = [0 for x in range(m+n)]
    
    for k in range(m+n):
        if i == m  :
            T[k] = V[j]
            j += 1
        elif j == n :
            T[k] = U[i]    
            i += 1
        else :
            if U[i] < V[j] :
                T[k] = U[i]
                i += 1
            else :
                T[k] = V[j]
                j += 1
        # Remarque : Il est inutile de traiter le cas i == m and j == n car celui-ci est impossible.
    return T
    
#Exemple
a,b = [0,1,5,8],[2,2,4,5]
print(merge(a,b))

#Une première tentative, ne marche pas toujours lorsqu'il y a des doublons
def tri_fusion_special1(T,k):
    i = 0
    j = k
    n = len(T)
    
    while (i < j and j < n):
        if T[i] <= T[j] :
            i += 1
        else :
            #Copying index and value that we need to keep.
            jj = j
            t = T[i]
            while (j < n and T[j] < t) :
                transpose(T,i,j)       
                i += 1
                j += 1
            if (i < jj) :
                j = jj
            else : 
                j -=1
    return T
                
def tri_fusion_special2(T,k):
    i = 0
    j = k
    n = len(T)
    
    while (i < j and j <n):
        if T[i] <= T[j] :
            i += 1
        else :
            #Copying index and value that we need to keep.
            jj, t = j, T[i]
            transpose(T,i,jj)
            while (jj+1 < n and T[jj+1] < t):
                transpose(T,jj,jj+1)
                jj +=1
                
            i +=1
    return T
                

                
def transpose(liste,i,j):
    t = liste[i]
    liste[i] = liste[j]
    liste[j] = t
    return liste
    
#Tests
def test_merge():
    tests = [([0,2,4],[1,1,3]),([0,1],[2,3]),([0,3,4],[1,2])]
    answers = [[0,1,1,2,3,4],[0,1,2,3],list(range(5))]
    for x,y in zip(tests,answers):
        print("Entrée : ",x)
        print("Réponse : ", y)  
        yh = merge(x[0],x[1])
        print("merge", yh == y,yh)
        yh = merge_sentinel(x[0],x[1])
        print("merge_sentinel", yh == y,yh)
    

def test_fusion_special():
    tests = [([0,2,4,1,1,3],3),([0,1],1),([0,3,4,1,2],3)]
    answers = [[0,1,1,2,3,4],[0,1],list(range(5))]
    
    for x,y in zip(tests,answers):
        x,k = x    
        print("Entrée : ",x,k)
        print("Réponse : ", y)        
        yh = tri_fusion_special1(x,k)
        print("fusion_special1", yh == y,yh)
        yh = tri_fusion_special2(x,k)
        print("fusion_special2",yh == y,yh)
                
#Numéro 3    

def select(T,k):
    """ fonction selection and partition. Pas la même que vue en classe."""
    if len(T) == 1 :
        return T[0]
    lo, piv, hi = partition(T)
    n = len(lo)
    if n == k:
        return piv
    elif n < k:
        return select(hi,k-n-2)
    else :
        return select(lo,k)

def partition(T):
    piv, T = T[0], T[1:]
    lo = [x for x in T if x <= piv]
    hi = [x for x in T if x > piv]
    return lo,piv,hi

def selection_under_m(T,m):
    """ Petite adaption de l'algorithme vue car select ne fait pas des modifications in-place"""
    n = len(T)
    x = select(T,m)

    TT = []
    for y in T:
        if y <= x:
            TT.append(y)    
    TT.sort()
    if len(TT) > m : #il y a des doublons de x dans le tableau
        TT = TT[:m]
    return TT

def test_selection1():
    ex = [[0,3,5,6,3,2,4]]    
    for x in ex :
    
        sorted_x = x.copy()
        sorted_x.sort()
        y = []
        for i in range(1,len(x)-1):
            print("     Entrée : "+str(x),", "+str(i))
            y_hat = selection_under_m(x,i)
            y = sorted_x[:i+1]
            print("     Réponse : "+str(y_hat))
            assert y_hat[i-1] == y[i-1]
            for a in range(i):
                if a < i:
                    assert y_hat[a] <= y[i-1]
                elif a > i :
                    assert y_hat[a] >= y[i-1]
                
               
