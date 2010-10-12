lstOutConnectedMovingNeurone = []
lstInConnectedNonMovingNeurone = []
for numCluster in clustersChangedIndex:
    for numNeurone in copy_lstInd[couple[0]].lstClusterToNeuron[numCluster]:
        outEdges1 = copy_lstInd[couple[0]].graph.out_edges(numNeurone,data=True)
        nOutConnection = size(outEdges1,0)
        for outConnection in range(nOutConnection):
            if outEdges1[outConnection][2]['weight']!=float(0):
               movingCluster = [ copy_lstInd[couple[0]].lstClusterToNeuron[x] for x in clustersChangedIndex1 ]
               # on enlève les connexions qui vont des clusters qui sont 
               # recombinés vers les clusters qui ne sont pas recombinés
               if !(outEdges1[outConnection][1] in flatten(movingCluster)):
                  copy_lstInd[couple[0]].graph.remove_edges_from(outEdges1[outConnection])
                  lstOutConnected.append(outEdges1[outConnection])

        inEdges1 = copy_lstInd[couple[0]].graph.in_edges(numNeurone,data=True)
        nInConnection = size(inEdges1,0)
        for inConnection in range(nInConnection):
            if inEdges1[inConnection][2]['weight']!=float(0):
               movingCluster = [ copy_lstInd[couple[0]].lstClusterToNeuron[x] for x in clustersChangedIndex1 ]
               # on enlève les connexions qui vont des clusters qui sont 
               # recombinés vers les clusters qui ne sont pas recombinés
               if !(outEdges1[outConnection][1] in flatten(movingCluster)):
                  copy_lstInd[couple[0]].graph.remove_edges_from(outEdges1[outConnection])
                  lstOutConnected.append(outEdges1[outConnection])
                  
                  
                  

    lstClusterConnection1 = [];
    lstClusterConnection2 = [];
    #ici c le chantier. Il faut que l'on arrive à redéfinir l'identité des neurones interface en refaisant un nb de connexions inter par cluster qui est fixe, comme lors de la génération des individus. 
    #pcInter = int(nbNeuronByCluster /  interRatio)   #Nombre de neurones connectes entre deux clusters à retirer entre cluster recombinés et non-recombinés
    nbClustersDispo=nbClusters-len(clustersChangedIndex)
    nbConnecByCluster=round(nbEdges/nbClustersDispo)
    count=0
    for i in range(nbEdges,step=nbConnecByCluster):
        clustersChangedIndex[count]
        count+
        
   
    for numEdges in range(nbEdges) :
        lstClusterConnection1.append( rd.sample( [x for x in clustersChangedIndex ] ,1 ) ) 
        lstClusterConnection2.append( rd.sample( [x for x in range(nbClusters) if not(x in clustersChangedIndex) ],1 ) )     
    lstClusterConnection=[lstClusterConnection1,lstClusterConnection2]       
    return(lstClusterConnection) 
