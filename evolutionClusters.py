# -*- coding: utf-8 -*-
#! /usr/bin/python

__author__="YR"
__date__ ="$17 avr. 2010 17:10:00$"


from pylab import *
import random as rd
from InitSimulation_Ind import  *
import copy

def selection(lstInd, collecCV):

    """
    Tirage deux par deux des individus et on garde celui qui a le CV le plus haut
    On fait ça jusqu'à retrouver une population de taille identique à celle d'origine
    """
    newPop = lstInd
    nbInd = size(lstInd, 0)
    
    for coupleInd in range(nbInd):
         couple = rd.sample(range(size(newPop, 0)), 2)
         if collecCV[couple[0]] > collecCV[couple[1]]:
            newPop[coupleInd] = lstInd[couple[0]]
         else:
            newPop[coupleInd] = lstInd[couple[1]]          
    return(newPop)
    
def CreateClusterConnection(clustersOutInter,clustersInInter,clustersChangedIndex,nbClusters) :
    #On récupère les index des clusters non impliqués dans la recombinaison
    clustersNonChangedIndex=[]
    clustersNonChangedIndex.append([x for x in range(nbClusters) if not(x in clustersChangedIndex[0])])
    clustersNonChangedIndex.append([x for x in range(nbClusters) if not(x in clustersChangedIndex[1])])
    
    #On mélange les clusters recombinants pour réattribuer les connexions inter au hasard par la suite
    shuffleClustersChanged=copy.deepcopy(clustersChangedIndex)
    shuffle(shuffleClustersChanged[0])
    shuffle(shuffleClustersChanged[1])
    
    #De même pour les clusters non recombinants
    #shuffle(clustersNonChangedIndex[1])

    lstClustersOut=[]
    lstClustersIn=[]
    
    for ind in range(2):
    
        arrayClustersOut=copy.deepcopy(array(clustersOutInter[ind]))
        arrayClustersIn=copy.deepcopy(array(clustersInInter[ind]))
        
        clustersOut=copy.deepcopy(arrayClustersOut)
        clustersIn=copy.deepcopy(arrayClustersIn)
        compteur=0
        for numCluster in clustersChangedIndex[ind]:
            clustersOut[arrayClustersOut==numCluster]=shuffleClustersChanged[ind][compteur]
            clustersIn[arrayClustersIn==numCluster]=shuffleClustersChanged[ind][compteur]
            compteur=compteur+1
            
        #On convertit nos arrays en list de list
        lstOut=[list(x) for x in clustersOut]
        lstIn=[list(x) for x in clustersIn]

        lstClustersOut.append(lstOut)
        lstClustersIn.append(lstIn)  
        
    return(lstClustersOut,lstClustersIn)       

        
        
def CreateInterConnectionMatrix(lstClusterConnection,lstClusterToNeuron,lstNeuronsType):
    preNeurones = []
    postNeurones = []
    weights = []
    for numConnexion in range(len(lstClusterConnection)):
        #print numConnexion
        #print lstClusterConnection
        #print [x for x in lstClusterToNeuron[lstClusterConnection[numConnexion][0]] if not(x in preNeurones)]
        #print preNeurones
        #print postNeurones
        neuronCouple = [ (preNeurones[x],postNeurones[x]) for x in range(len(preNeurones)) ]
        preN =  rd.sample( [x for x in lstClusterToNeuron[lstClusterConnection[numConnexion][0]] ],1 ) 
        postN =  rd.sample( [x for x in lstClusterToNeuron[lstClusterConnection[numConnexion][1]] ],1 ) 
        while (preN,postN) in neuronCouple:
            print "*********************************************************"
            print ">>>>>>>>>>>>>>>>>>>>>>> je retire <<<<<<<<<<<<<<<<<<<<<<<"
            print "*********************************************************"
            preN = rd.sample( [x for x in lstClusterToNeuron[lstClusterConnection[numConnexion][0]] ],1 )  
            postN = rd.sample( [x for x in lstClusterToNeuron[lstClusterConnection[numConnexion][1]] ],1 ) 
        preNeurones.extend( preN ) 
        postNeurones.extend( postN )
    for n in preNeurones:    
        weights.append( rd.random()*lstNeuronsType[n] ) 
    interEdges=[ tuple((preNeurones[x], postNeurones[x], {'weight': weights[x]})) for x in range(len(weights)) ]
    return(interEdges)
    
def actualize_lstNeuronInterface(interEdges,Ind):
    for edge in interEdges:
        Ind.lstInterfaceNeuron[0].append(Ind.lstNeuronToCluster[edge[0]])
        Ind.lstInterfaceNeuron[1].append(edge[0])
        Ind.lstInterfaceNeuron[2].append(Ind.lstNeuronToCluster[edge[1]])
        Ind.lstInterfaceNeuron[3].append(edge[1])                        
    return(Ind)

                
    
def mixClusters(lstInd,collecCV):
    """
    On choisit deux individus au hasard
    Pour chaque on tire un groupe de clusters au hasard à échanger entre les deux
    On garde les connexions intra-clusters
    On supprime les connexions inter-clusters qui n'appartiennent pas au groupe choisit
    On retire toutes ces connexions inter au hasard
    On échange les deux groupes de clusters en renumérotant les neurones et les clusters
    On obtient ainsi deux nouveaux individus après recombinaison
    """

    #La deep copy est nécessaire sinon on travaille sur une référence 
    copyLstInd = copy.deepcopy(lstInd)
    #Proba utilisée pour calculer le nombre de clusters à échanger
    PROBA_CLUSTER_CHANGE = 0.56312

    newRecombinedPop = []
    #On effectue la sélection selon les CV -> On récupère une nouvelle population
    #copyLstInd = selection(copyLstInd, collecCV)  
    
    #Nombre d'individus dans la population
    nbInd = size(copyLstInd, 0)
    #Nombre total de clusters 
    nbClusters=size(copyLstInd[0].lstClusterToNeuron ,0)
    #Nombre de clusters à recombiner
    nbClustersRecombined=int(PROBA_CLUSTER_CHANGE * nbClusters)        
    
    #La boucle n'est pas terrible car elle oblige a avoir un nombre pair d'individus...
    for coupleInd in range(nbInd/2): # nb de fois où l'on recombine
        #On tire deux individus
        couple = rd.sample(range(nbInd), 2)

        #On tire les index des clusters à échanger
        clustersChangedIndex1=rd.sample(range(nbClusters),nbClustersRecombined)
        clustersChangedIndex2=rd.sample(range(nbClusters),nbClustersRecombined)
        clustersChangedIndex=[clustersChangedIndex1,clustersChangedIndex2]

        numInd=0
        numOutEdges={}
        numInEdges={}
        recombinantNeuronsCorrespondance=[]
        recombinantEdges=[]
        recombinantEdges2beInjected=[]
        
        #Liste des couples de clusters impliqués dans une connexion inter, entrante ou sortante. (In et out)
        clustersOutInter=[]
        clustersInInter=[]
        
        for eachInd in couple:
        #Traitement des connexions inter
            #On fait la liste des index des neurones pré impliqués dans une connexion inter avec un cluster qui n'est pas recombiné
            #On fait des deepcopy pour pouvoir actualiser copyLstInd[eachInd].lstInterfaceNeuron sans toucher lstPreCluster et lstPostCluster
            lstPreCluster = copy.deepcopy( copyLstInd[eachInd].lstInterfaceNeuron[0] )
            lstPostCluster = copy.deepcopy( copyLstInd[eachInd].lstInterfaceNeuron[2] )
            indexOut=[x for x in range(len(lstPreCluster)) if ( (lstPreCluster[x] in clustersChangedIndex[numInd]) and not(lstPostCluster[x] in clustersChangedIndex[numInd]) ) ]
#            print [lstPreCluster[x] for x in indexOut]
            #On stocke le nombre de connexions supprimées pour reconstruction ultérieure
            numOutEdges.update({eachInd:len(indexOut)})
            #On construit la liste des edges à supprimer (pre - post avec post dans un cluster non recombinant)
            edgesKill=transpose([ [copyLstInd[eachInd].lstInterfaceNeuron[1][x] for x in indexOut] , [copyLstInd[eachInd].lstInterfaceNeuron[3][x] for x in indexOut] ])
            edgesKill=[tuple(x) for x in edgesKill]
            
            #On récupère le numéro des clusters dans lesquels sont ces neurones
            clustersOut=transpose([ [copyLstInd[eachInd].lstInterfaceNeuron[0][x] for x in indexOut] , [copyLstInd[eachInd].lstInterfaceNeuron[2][x] for x in indexOut] ])
            
            clustersOut=[tuple(x) for x in clustersOut]
            clustersOutInter.append(clustersOut)
            
            
            #On supprime ces connexions sortantes
            copyLstInd[eachInd].graph.remove_edges_from(edgesKill)
            

            ###On fait la même chose pour les connexions entrantes
            #On fait la liste des index des neurones post impliqués dans une connexion inter avec un cluster qui n'est pas recombiné
            indexIn=[x for x in range(len(lstPreCluster)) if ( not(lstPreCluster[x] in clustersChangedIndex[numInd]) and (lstPostCluster[x] in clustersChangedIndex[numInd]) ) ]
            #On stocke le nombre de connexions supprimées pour reconstruction ultérieure
            numInEdges.update({eachInd:len(indexIn)})
            #On construit la liste des edges à supprimer (pre - post avec post dans un cluster non recombinant)
            edgesKill=transpose([ [copyLstInd[eachInd].lstInterfaceNeuron[1][x] for x in indexIn] , [copyLstInd[eachInd].lstInterfaceNeuron[3][x] for x in indexIn] ])
            edgesKill=[tuple(x) for x in edgesKill]
        
            #On récupère le numéro des clusters dans lesquels sont ces neurones
            clustersIn=transpose([ [copyLstInd[eachInd].lstInterfaceNeuron[0][x] for x in indexOut] , [copyLstInd[eachInd].lstInterfaceNeuron[2][x] for x in indexOut] ])
            clustersIn=[tuple(x) for x in clustersIn]
            clustersInInter.append(clustersIn)
        
            #On supprime ces connexions
            copyLstInd[eachInd].graph.remove_edges_from(edgesKill)
            
    #Traitement des connexions intra
            #On fait la liste des neurones que l'on va recombiner
            recombinantNeurons=list(flatten([copyLstInd[eachInd].lstClusterToNeuron[x] for x in clustersChangedIndex[numInd]]))
            recombinantNeuronsCorrespondance.append(recombinantNeurons)
            #On en déduit la liste des connexions entre les neurones à recombiner
            intraEdges=copy.deepcopy(copyLstInd[eachInd].graph.edges(recombinantNeurons,data=True))
            intraEdgesToKill=copy.deepcopy(copyLstInd[eachInd].graph.edges(recombinantNeurons,data=False))
            #print "intraEdges : ",len(intraEdges)
            recombinantEdges.append( intraEdges )
            #On supprime ces connexions avant de faire la recombinaison
            copyLstInd[eachInd].graph.remove_edges_from(intraEdgesToKill)

            #On passe au second individu du couple
            numInd=numInd+1

            #on actualise la lstInterfaceNeuron de chaque individu
            indexToKill=list(flatten([indexIn,indexOut]))
            indexToKill.sort()
            indexToKill.reverse()
            for numList in range(4):
                [ copyLstInd[eachInd].lstInterfaceNeuron[numList].pop(x) for x in indexToKill ]
                
        #print clustersOutInter      
    #Traitement des connexions intra et inter en simultané en les combinant dans edgesRecomb
        #On en fait un array pour pouvoir faire les remplacements
        recombinantEdges1=array(recombinantEdges[0])
        recombinantEdges2=array(recombinantEdges[1])
        #print recombinantEdges
        edgesRecomb1 = copy.deepcopy(recombinantEdges1)
        edgesRecomb2 = copy.deepcopy(recombinantEdges2)

        #On fait la renumérotation des neurones
        for x in range(len(recombinantNeuronsCorrespondance[0])):
            edgesRecomb1[recombinantEdges1==recombinantNeuronsCorrespondance[0][x]]=recombinantNeuronsCorrespondance[1][x]
            edgesRecomb2[recombinantEdges2==recombinantNeuronsCorrespondance[1][x]]=recombinantNeuronsCorrespondance[0][x]
        #On convertit nos arrays en list de tuples ce qui se fait en deux étapes (list de list puis list de tuples)
        temp1=[list(x) for x in edgesRecomb1]
        temp2=[list(x) for x in edgesRecomb2]
        edgesRecomb1 = [tuple(x) for x in temp1]
        edgesRecomb2 = [tuple(x) for x in temp2]
        
        #On remet ces connexions dans les graphes
        copyLstInd[couple[0]].graph.add_edges_from(edgesRecomb2)
        copyLstInd[couple[1]].graph.add_edges_from(edgesRecomb1)        
        
        #on actualise la lstNeuronsType avec les weights des neurones échangés 
        for edge in edgesRecomb1 :
            copyLstInd[couple[0]].lstNeuronsType[edge[0]] = sign( edge[2]['weight'] )
        for edge in edgesRecomb2 :
            copyLstInd[couple[1]].lstNeuronsType[edge[0]] = sign( edge[2]['weight'] )     

        #On tire au hasard les nouvelles connexions inter   
        
        #Creation des connexions inter-cluster
        #Individu 1 : couple[0] et clustersChangedIndex1 et lstNeuronsType1
        #On mélange les connections inter en mélangeant les numéros des clusters recombinants partenaires de ces connexions
        (lstClustersOut,lstClustersIn) = CreateClusterConnection(clustersOutInter,clustersInInter,clustersChangedIndex,nbClusters )

        for ind in range(2):
            #OutEdges
            #On tire des numéros de neurones au sein de chacun des clusters pour établir la nouvelle connectique inter
            interEdges = CreateInterConnectionMatrix(lstClustersOut[ind],copyLstInd[couple[ind]].lstClusterToNeuron,copyLstInd[couple[ind]].lstNeuronsType)
            #On réinjecte ces connexions dans le graph de l'individu
            copyLstInd[couple[ind]].graph.add_edges_from(interEdges)
            #On actualise l'individu
            Ind = actualize_lstNeuronInterface(interEdges,copyLstInd[couple[ind]])
            copyLstInd[couple[ind]]=Ind
            
            #InEdges
            #On tire des numéros de neurones au sein de chacun des clusters pour établir la nouvelle connectique inter
            interEdges = CreateInterConnectionMatrix(lstClustersIn[ind],copyLstInd[couple[ind]].lstClusterToNeuron,copyLstInd[couple[ind]].lstNeuronsType)
            #On réinjecte ces connexions dans le graph de l'individu
            copyLstInd[couple[ind]].graph.add_edges_from(interEdges)
            #On actualise l'individu
            Ind = actualize_lstNeuronInterface(interEdges,copyLstInd[couple[ind]])
            copyLstInd[couple[ind]]=Ind
              
         
              
    return (copyLstInd)
    
    
