#! /usr/bin/python

__author__="YR"
__date__ ="$17 avr. 2010 16:03:00$"

from nestInterface import *
from pylab import *
#from evolutionCV import *
from evolutionClusters import *
import progressbar as pb

def testNetwork(individu, nbNetwork,  nbClusters, connectInter, connectIntra, pcExc, pcInh, nbNeuronByCluster, interRatio):
    #pEE,pEI,pII,pIE
    cv=[]
    for indNetwork in range(nbNetwork):
        rasterDict=createNestNetwork(individu,nbClusters, connectInter, connectIntra, pcExc, pcInh, nbNeuronByCluster, interRatio, False)
        cv.append(computeCVs(rasterDict))
        
    return (cv)

def computeCVs(raster):
    nbNeurones=max(raster['senders'])
    for idNeurone in range(nbNeurones+1):
        posPA=find(raster['senders']==idNeurone)
        timesPA=raster['times'][posPA]
        ISI=diff(timesPA)
        CV=std(ISI)/mean(ISI)
        if (isnan(CV)):
            CV=0
    return(CV)
    

def CreateParam(taillePop):
    params=zeros([taillePop, 7])
    for ind in range (taillePop):
        pEE=rd.random()
        pEI=rd.random()
        pII=rd.random()
        pIE=rd.random()
        inter=rd.random()
        pcExc=rd.random()
        interRatio=rd.randint(1, 30)
        params[ind]=[pEE, pEI, pII, pIE, inter, pcExc, interRatio]
    
    return (params)
 
###
#Script de test
###
maxCV=-1 
collecCV=[]
lstInd=[]
i=0
taillePop=15
pbar=pb.ProgressBar(maxval=taillePop).start()
for i in range(taillePop):
    individu=Ind( 15,0.6,[0.4,0.7, 0.3, 0.6],0.8, 1-0.8,10, 10)
    lstInd.append(individu)
    pbar.update(i+1)

pbar.finish()

i=0
for x in range(10):
    
    i+=1
    print "*************************************"
    print 'Iteration numero : ', i
    print "*************************************"
    cvGeneration=[]
    for ind in range(taillePop):
        print "**************", ind, "******************"
        cv=testNetwork(lstInd[ind],1,15,0.6,[0.4,0.7, 0.3, 0.6],0.8, 1-0.8,10, 10)
        cvGeneration.append(cv[0])
        print ">>> CV de l'individu : ",cv[0]
    collecCV.append(cvGeneration)
    if x<4:
        lstInd=mixClusters(lstInd,cvGeneration)
        
    newMaxCV=max(cvGeneration)
    if newMaxCV > maxCV:
        maxCV=newMaxCV
#    params=mixParameters(params, 0.05, cvGeneration)
    print "CVmax across generations>>> ", maxCV , " <<<"
    print "CVmax last generations>>> ", newMaxCV , " <<<"

