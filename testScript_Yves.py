#! /usr/bin/python

__author__="YR"
__date__ ="$17 avr. 2010 16:03:00$"

from nestInterface import *
from pylab import *
from evolutionCV import *


def testNetwork(nbNetwork,  nbClusters, connectInter, connectIntra, pcExc, pcInh, nbNeuronByCluster, interRatio):
    #pEE,pEI,pII,pIE
    cv=[]
    for indNetwork in range(nbNetwork):
        rasterDict=createNestNetwork(nbClusters, connectInter, connectIntra, pcExc, pcInh, nbNeuronByCluster, interRatio, False)
        cv.append(computeCVs(rasterDict))
        
    return cv

def computeCVs(raster):
    nbNeurones=max(raster['senders'])
    for idNeurone in range(nbNeurones+1):
        posPA=find(raster['senders']==idNeurone)
        timesPA=raster['times'][posPA]
        ISI=diff(timesPA)
        CV=std(ISI)/mean(ISI)
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
 
 
 
collecCV=[]
collecParam=[]
i=0
taillePop=50
params=CreateParam(taillePop)
#print params
for x in range(30):
    
    i+=1
    print "*************************************"
    print 'Iteration numero : ', i
    print "*************************************"
    cvGeneration=[]
    for ind in range(taillePop):
        print "**************", ind, "******************"
        cv=testNetwork(1, 20,params[ind][4] ,[params[ind][0],params[ind][1], params[ind][2], params[ind][3] ],params[ind][5] , 1-params[ind][5], 25, params[ind][6])
        cvGeneration.append(cv[0])
    collecCV.append(cvGeneration)
    collecParam.append(params)
    
    params=mixParameters(params, 0.05, collecCV)
    print "CVmax >>> ", max(collecCV) , " <<<"
