#! /usr/bin/python

__author__="YR"
__date__ ="$17 avr. 2010 17:10:00$"


from pylab import *
import random as rd

def selection(nonSelectedParametersPop, collecCV) :
    parametersPop = nonSelectedParametersPop
    nbInd = size(nonSelectedParametersPop, 0)
    
    for coupleInd in range(nbInd):
         couple = rd.sample(range(size(parametersPop, 0)-1), 2)
         if collecCV[couple[0]] > collecCV[couple[1]]:
            parametersPop[coupleInd] = nonSelectedParametersPop[couple[0]]
         else:
            parametersPop[coupleInd] = nonSelectedParametersPop[couple[1]]
            

    return(parametersPop)
    
def mutePop(newRecombinedPop, tauxMutation, nbPara, nbInd):
    newMutatedPop = newRecombinedPop
    #params[ind]=[pEE, pEI, pII, pIE, inter, pcExc, interRatio]
    for Ind in range(nbInd-1):
        if rd.random()>tauxMutation:
            locus=rd.randint(0, nbPara-1)
            newPara = newRecombinedPop[Ind]
            newPara[locus] = newPara[locus] +  rd.sample([-1 , 1], 1)[0] * (newPara[locus] * 0.33)
            if (locus<=3 or locus ==5):
                newPara[locus] =min([newPara[locus] , 1])
            newMutatedPop[Ind] = newPara          
                  
    return newMutatedPop
        
    
def mixParameters(nonSelectedParametersPop, tauxMutation, collecCV):
    newRecombinedPop = []
    
    parametersPop = selection(nonSelectedParametersPop, collecCV)  

    nbInd = size(parametersPop, 0)
    nbPara = size(parametersPop, 1)
    #La boucle n'est pas terrible car elle oblige a avoir un nombre pair d'individus...
    for coupleInd in range(nbInd/2):
        couple = rd.sample(range(nbInd-1), 2)
        recStart = rd.randint(0, nbPara-2)
        recEnd = rd.randint(recStart+1, nbPara-1)
        ind1 = list(parametersPop[couple[0]])
        ind2 = list(parametersPop[couple[1]])

        newInd1 = ind1[0:recStart] + ind2[recStart:recEnd] + ind1[recEnd:]
        newInd2 = ind2[0:recStart] + ind1[recStart:recEnd] + ind2[recEnd:]
        
        newRecombinedPop.append(newInd1)
        newRecombinedPop.append(newInd2)
    
    newMutatedPop = mutePop(newRecombinedPop, tauxMutation, nbPara,nbInd )
    return newMutatedPop
