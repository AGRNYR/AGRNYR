#! /usr/bin/python

__author__="YR"
__date__ ="$04 mar. 2010 20:48:00$"

import random as rd
from numpy import *

try:
    import networkx as nx
except:
    raise
    
import matplotlib.pyplot as plt

#connectIntra = (pEE,pEI,pII,pIE)

def CreateConnectionMatrix(pcExc,pcInh,nbNeuronByCluster,connectIntra):
    """
    Creation de la matrice de connexion intracluster pour un seul cluster
    La matrice contient les poids synaptiques (negatifs pour inhibition)
    L'element (ligne i, colonne j) = poids synaptique de Neurone i -> Neurone j
    Les neurones excitateurs sont les pcExc * nbNeuronByCluster premiers 
    """

   #Initialisation de la matrice
    matrix=zeros(nbNeuronByCluster**2).reshape(nbNeuronByCluster,nbNeuronByCluster)

    #Nombre de neurones de chaque type
    nbExc = int(pcExc * nbNeuronByCluster)
    nbInh = int(nbNeuronByCluster - nbExc)

    #Calcul des poids synaptiques excitateurs
    for neuronId in range(nbExc):
        nbSynapsesEE = int(connectIntra[0] * pcExc * nbNeuronByCluster)
        nbSynapsesEI = int(connectIntra[1] * pcInh * nbNeuronByCluster)
       
        connectedEEindex = rd.sample(range(nbExc), nbSynapsesEE)
        connectedEIindex = list( add( [nbExc] * nbSynapsesEI , rd.sample(range(nbInh), nbSynapsesEI) ))
        
        matrix[neuronId,connectedEEindex]= [rd.random() for x in range(nbSynapsesEE)]
        matrix[neuronId,connectedEIindex]= [rd.random() for x in range(nbSynapsesEI)]

    #Calcul des poids synaptiques inhibiteurs
    for neuronId in range(nbExc,nbNeuronByCluster):

        nbSynapsesII = int(connectIntra[2] * pcInh * nbNeuronByCluster)
        nbSynapsesIE = int(connectIntra[3] * pcExc * nbNeuronByCluster)

        connectedIEindex = rd.sample(range(nbExc), nbSynapsesIE)
        connectedIIindex = list( add([nbExc] * nbSynapsesII , rd.sample(range(nbInh), nbSynapsesII) ))
        
        matrix[neuronId,connectedIEindex]= [- rd.random() for x in range(nbSynapsesIE)]
        matrix[neuronId,connectedIIindex]= [- rd.random() for x in range(nbSynapsesII)]

    return(matrix)





def drawNetwork(network):

    pos=nx.spring_layout(network) # positions for all nodes shell, spring, circular, random, spectral

    inhib = [(u,v) for (u,v,d) in network.edges(data=True) if d < 0 ]
    excit = [(u,v) for (u,v,d) in network.edges(data=True) if d > 0 ]

    # nodes
    nx.draw_networkx_nodes(network, pos, edgelist=inhib ,node_size=100,node_color='b')
    nx.draw_networkx_nodes(network, pos, edgelist=excit ,node_size=100,node_color='r')

    # edges
    we=[d for (u,v,d) in network.edges(data=True) if d>0]
    if (we != []):
        we=asarray(we)
        we=we-min(we)
        we=we/max(we)
        we=2*we
        we=list(we)

    wi=[d for (u,v,d) in network.edges(data=True) if d<0]
    if (wi != []):
        wi=asarray(wi)
        wi=abs(wi)
        wi=wi-min(wi)
        wi=wi/max(wi)
        wi=2*wi
        wi=list(wi)

    nx.draw_networkx_edges(network,pos,edgelist=inhib,edge_color='b',width=wi,arrows=False)
    nx.draw_networkx_edges(network,pos,edgelist=excit,edge_color='r',width=we,arrows=False)
    nx.draw_networkx_labels(network,pos,font_size=8,alpha=0.8)
    
def CreateClusterConnection(connectInter,nbClusters) :
    lstClusterConnection = [];  
    for numCluster in range(nbClusters):
        lstClusterConnection.append( rd.sample( [x for x in range(nbClusters) if x!=numCluster] , min( int(connectInter*nbClusters), nbClusters-1) ))
        
    return(lstClusterConnection)
    
def CreateInterConnectionMatrix(numCluster,nbNeuronByCluster,lstClusterToNeuron,lstClusterConnection,pcInter,lstNeuronsType):
    preNeurones = []
    postNeurones = []
    weights = []
    for postCluster in lstClusterConnection[numCluster]:
        preNeurones.extend( rd.sample( lstClusterToNeuron[numCluster], pcInter ) )
        postNeurones.extend( rd.sample( lstClusterToNeuron[postCluster],pcInter ) )
    for n in preNeurones:    
        weights.append( rd.random()*lstNeuronsType[n] )
        
    return(preNeurones,postNeurones,weights)

def CreateInd(nbClusters, connectInter, connectIntra, pcExc, pcInh, nbNeuronByCluster, interRatio):
    """
    connectInter est la probabilite de connecter deux clusters entre eux
    connectIntra est une liste de probabilite de connection de neurones suivant leur type (pEE,pEI,pII,pIE)
    pcExc et pcInh sont le pourcentage de chaque type de neurones
    interRatio est le ratio de neurones-interface entre deux clusters (>1)
    """

    nbNeuronsInd = nbClusters * nbNeuronByCluster
    
    numNeuron = 0
    nbExc = int(pcExc * nbNeuronByCluster)
    lstNeuronsType = ([1] * nbExc  + [-1]*(nbNeuronByCluster - nbExc)) * nbClusters 
    lstNeuronToCluster = [y for y in range(nbClusters) for x in range(nbNeuronByCluster)]
    lstClusterToNeuron = [range(y*nbNeuronByCluster,(y+1)*nbNeuronByCluster) for y in range(nbClusters) ]
    lstInterfaceNeuron = [[],[],[],[]]  #Liste des neurones de chaque cluster connectes aux neurones d'autres clusters

    gphInd =  nx.MultiDiGraph()

    #Creation des clusters
    for numCluster in range(nbClusters):
        gphCluster = nx.MultiDiGraph()
        matrix = CreateConnectionMatrix(pcExc,pcInh,nbNeuronByCluster,connectIntra)
        #Parcourt de la matrice de connexion du cluster
        for ligne in range(nbNeuronByCluster):
            for col in range(nbNeuronByCluster):
                gphCluster.add_edge(ligne+numNeuron , col+numNeuron,data=matrix[ligne,col])

        #Permet la numerotation continue entre les clusters
        numNeuron+=nbNeuronByCluster
        #Rajoute le graphe du cluster (gphCluster) au graphe total (gphInd)
        gphInd=nx.disjoint_union(gphInd,gphCluster)
        gphCluster=nx.create_empty_copy(gphCluster)

    #Creation des connexions inter-cluster
    lstClusterConnection = CreateClusterConnection(connectInter,nbClusters)
    for numCluster in range(nbClusters):
        pcInter = int(nbNeuronByCluster /  interRatio)   #Nombre de neurones connectes entre deux clusters
        (preNeurones,postNeurones,weights) = CreateInterConnectionMatrix(numCluster,nbNeuronByCluster,lstClusterToNeuron,lstClusterConnection,pcInter,lstNeuronsType)
        for n in range(len(preNeurones)):
            gphInd.add_edge(preNeurones[n] , postNeurones[n] ,data=weights[n])
            
     #Liste caracterisant les connexions inter-cluster
     #ligne 0 : numero de cluster des neurones pre-synaptiques
     #ligne 1 : numero des neurones pre-synaptiques
     #ligne 2 : numero de cluster des neurones post-synaptiques
     #ligne 3 : numero des neurones post-synaptiques
           
        lstInterfaceNeuron[0].extend([numCluster] * len(preNeurones))
        lstInterfaceNeuron[1].extend(preNeurones)       
        lstInterfaceNeuron[2].extend( [lstNeuronToCluster[x] for x in postNeurones] )   
        lstInterfaceNeuron[3].extend(postNeurones)
        
        
        
    drawNetwork(gphInd)
    plt.show()
    return(gphInd,lstNeuronsType,lstNeuronToCluster,lstClusterToNeuron)

