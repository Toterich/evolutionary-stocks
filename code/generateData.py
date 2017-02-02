
import sys
import pandas as pd
import numpy as np

import Values as val
import GeneticOperators as go
import FitnessFunctions as ff

picklePath = './pickle/'

nrOfRuns = 5

nrOfGens = 1000
populationSize = 30
treeSize = 4
assets = list(val.pastFaceValues.keys())
fitnessFunc = ff.sharpeRatio
try:
  if sys.argv[1] == '--use-fitness':
    print('Using optimized genetic operators.')
    genOpFitnessFunc = fitnessFunc
    bestFitFile = picklePath + 'bestFitOpt.pkl'
    meanFitFile = picklePath + 'meanFitOpt.pkl'
    diversityFile = picklePath + 'diversityOpt.pkl'
    portfolioFile = picklePath + 'portfolioOpt.pkl'
except IndexError:
  genOpFitnessFunc = None
  bestFitFile = picklePath + 'bestFit.pkl'
  meanFitFile = picklePath + 'meanFit.pkl'
  diversityFile = picklePath + 'diversity.pkl'
  portfolioFile = picklePath + 'portfolio.pkl'


defaultHighIsGood = True


bestFitDF = pd.DataFrame(columns=list(range(nrOfRuns)))
meanFitDF = pd.DataFrame(columns=list(range(nrOfRuns)))
diversityDF = pd.DataFrame(columns=list(range(nrOfRuns)))
portfolioDF = pd.DataFrame(columns=assets)


for i in range(nrOfRuns):

  print('Run: ', i)

  selectionContenders = 2
  mutationStrength = 0.9


  population = go.initPopulation(populationSize, treeSize, assets)

  for j in range(nrOfGens):

    popFitnessValues = list(map(fitnessFunc, population))

    if defaultHighIsGood:
      bestFitness = max(popFitnessValues)
    else:
      bestFitness = min(popFitnessValues)

    meanFitness = np.mean(popFitnessValues)

    diversity = np.var(popFitnessValues)

    #append current gen's parameters to dataframe
    bestFitDF.set_value(j, i, bestFitness)
    meanFitDF.set_value(j, i, meanFitness)
    diversityDF.set_value(j, i, diversity)

    population = go.selectTourney(population, fitnessFunc, selectionContenders, defaultHighIsGood)
    population = go.crossoverPopulation(population, genOpFitnessFunc, defaultHighIsGood)
    go.mutatePopulation(population, 0.5, mutationStrength, assets, genOpFitnessFunc, defaultHighIsGood)

    #every 200th generation, increase the selection pressure
    if (j+1) % (nrOfGens//3) == 0:
      selectionContenders += 1
    #every 10th generation, reduce the mutation strength
    if (j+1) % (nrOfGens//10) == 0:
      mutationStrength -= 0.05

  index = popFitnessValues.index(bestFitness)
  bestIndividual = population[index]
  for key, value in bestIndividual.getTotalAssetWeights().items():
    portfolioDF.set_value(i, key, value)

#calculate mean and stdev over runs per generation
bestFitDF['Mean'] = bestFitDF.mean(1)
meanFitDF['Mean'] = meanFitDF.mean(1)
diversityDF['Mean'] = diversityDF.mean(1)

bestFitDF['StdDev'] = bestFitDF.std(1)
meanFitDF['StdDev'] = meanFitDF.std(1)
diversityDF['StdDev'] = diversityDF.std(1)

bestFitDF.to_pickle(bestFitFile)
meanFitDF.to_pickle(meanFitFile)
diversityDF.to_pickle(diversityFile)
portfolioDF.to_pickle(portfolioFile)