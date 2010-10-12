#! /usr/bin/python

__author__="YR"
__date__ ="$20 mar. 2010 13:58:00$"

from InitSimulation_Ind import  *
from nest import *
import nest.raster_plot as raster
try:
    import networkx as nx
except:
    raise
    
def  createNestNetwork(individu,nbClusters, connectInter, connectIntra, pcExc, pcInh, nbNeuronByCluster, interRatio, plotMe=False):
        TIME_SIM=400.0

        ResetKernel()

        print 'Initialisation du reseau'
        nbNeurones = nbClusters * nbNeuronByCluster
        
        neurones=Create("iaf_psc_delta",nbNeurones)

        SetDefaults("spike_detector", {"withtime":True,"withgid":True})
        spikedetector=Create("spike_detector")
        correlator=Create("correlation_detector",params={"delta_tau":1.0,"tau_max":100.0})
        
        print "Creation d'un individu"
        #individu=Ind(nbClusters, connectInter, connectIntra, pcExc, pcInh, nbNeuronByCluster, interRatio)
        
        print 'Connexion du reseau de neurones'

        CopyModel("static_synapse","N2N")
        #CopyModel("stdp_pl_synapse_hom","N2N")

    
        for nSource,voisins in individu.graph.adjacency_iter():
            #print nSource, voisins
            for voisin,eattr in voisins.iteritems():
                #print voisin, eattr
                
                poids=eattr[0]['weight']
                poids=poids*20
                Connect([neurones[nSource]],[neurones[voisin]],params={"weight":double(poids)},model="N2N")
                
         
        DRIVE=30
        space= 0.9
        NB_DRIVER = 20
        #aleatime=random.randint(1,100)
        t=0.1
        times=[t+space*x for x in range(DRIVE)]
        #times.extend([DRIVE + t+space*2*x+aleatime for x in range(DRIVE)])
  
        spiker=Create("spike_generator",3,params={"spike_times":times})       
        
        DivergentConnect(spiker,neurones[1:NB_DRIVER])
        ConvergentConnect(neurones,spikedetector)
        Connect([neurones[3]],correlator,params={"receptor_type":0})
        Connect([neurones[3]],correlator,params={"receptor_type":1})
        SetStatus(spikedetector,[{"n_events":0}])        
        SetStatus(correlator,[{"n_events":[0,0]}])
        noisy=Create("noise_generator", params={"mean":0.0, "std":10.0})
        DivergentConnect(noisy, neurones)
        
        print "Simulation en cours..." 
        
        Simulate(TIME_SIM)

        rate=GetStatus(spikedetector,"n_events")[0]
        print "Nombre de PAs : ",rate
        rate=(rate /(TIME_SIM / 1000.0))/(nbNeurones)

        #Fin de la simulation on affiche des choses

        print "Frequence moyenne : ",rate
        
        #print "Nombre total de synapses : ", GetStatus("N2N","num_connections")   
        
        if (plotMe):
            raster.from_device(spikedetector, "Petit raster artificiel",  hist=True)
            plt.figure()
            plt.plot(GetStatus(correlator,"histogram")[0])
            plt.show()
        
        rasterDict=GetStatus(spikedetector,"events")[0]
        
        return(rasterDict)
        #repr(individu)
        #print times
        #plt.vlines(times, 0, max(times)+1, color='k')
        
