#!/usr/local/python3

import random
import math
import copy

import Values
from PortfolioTree import PortfolioTree
import FitnessFunctions as ff


def initPopulation(populationSize, initialDepth, assetList):
  """Generates a population of random Portfoliotrees."""

  #list holding all individuals
  population = []

  for i in range(populationSize):
    population.append(PortfolioTree(initialDepth, assetList))

  return population

def mutateIndividual(individual, strength, assetList):
  """Randomly mutate an individual."""
  random.seed()
  totalDepth = individual.getDepth()
  #choose node of mutation
  mutationDepth = min(max(round(random.gauss(totalDepth * (1 - strength), totalDepth/4)), 1),totalDepth)
  #mutationDepth = 1
  #mutationDepth = round((random.uniform(0, totalDepth)*(1 - strength) + totalDepth)/totalDepth)
  mutationIndex = round(random.uniform(0, pow(2, mutationDepth) - 1))

  newSubTree = PortfolioTree(totalDepth - mutationDepth, assetList)
  mutatedIndividual = copy.deepcopy(individual)

  mutatedIndividual.updateSubTree(mutationDepth, mutationIndex, newSubTree)

  return mutatedIndividual



def mutatePopulation(population, rate, strength, assetList):
  """Randomly mutate a population."""
  if rate < 0 or rate > 1:
    print('Mutation rate has to lie in [0,1].')
    return

  if strength <= 0 or strength > 1:
    print('Mutation strength has to lie in  (0,1].')
    return

  mutatedPopulation = []

  for individual in population:
    if random.random() < rate:
      mutatedPopulation.append(mutateIndividual(individual, strength, assetList))
    else:
      mutatedPopulation.append(individual)

  return mutatedPopulation

def crossoverIndividuals(father, mother, bwsFitnessFunction, highIsGood):
  """Recombines two trees to a new one which shares some traits with both of
  them."""

  #choose depth of crossover point at random
  crossoverDepth = round(random.uniform(1,father.getDepth()))

  #get all subtrees of father and mother at that layer of deepness
  fatherNodesAtLayer = father.getNodesAtDepth(crossoverDepth)
  motherNodesAtLayer = mother.getNodesAtDepth(crossoverDepth)

  numberOfNodesinLayer = pow(2, crossoverDepth)

  #if no fitnessfunction is supplied, use random crossover
  if bwsFitnessFunction is None:
    indexM = round(random.uniform(0,numberOfNodesinLayer - 1))
    indexF = round(random.uniform(0,numberOfNodesinLayer - 1))

  #if bws (Best-Worst-Subtree) crossover is used, at crossoverDepth
  #find the best subtree from father and the worst from mother
  else:
    fitnessValuesOfFatherNodes = list(map(bwsFitnessFunction, fatherNodesAtLayer))
    fitnessValuesOfMotherNodes = list(map(bwsFitnessFunction, motherNodesAtLayer))

    if highIsGood:
      indexF = fitnessValuesOfFatherNodes.index(max(fitnessValuesOfFatherNodes))
      indexM = fitnessValuesOfMotherNodes.index(min(fitnessValuesOfMotherNodes))
    else:
      indexF = fitnessValuesOfFatherNodes.index(min(fitnessValuesOfFatherNodes))
      indexM = fitnessValuesOfMotherNodes.index(max(fitnessValuesOfMotherNodes))

  fatherCrossOverNode = copy.deepcopy(fatherNodesAtLayer[indexF])

  #exchange identified crossover nodes
  child = copy.deepcopy(mother)
  child.updateSubTree(crossoverDepth, indexM, fatherCrossOverNode)

  return child

def crossoverPopulation(population, bwsFitnessFunction = None, highIsGood = True):
  populationSize = len(population)
  recombinedPopulation = []

  #i = 0
  #while len(recombinedPopulation) < populationSize:
  for i in range(populationSize):
    #choose 2 individuals at random
    fatherIndex = round(random.uniform(0,populationSize-1))
    motherIndex = i
    while fatherIndex == motherIndex:
      fatherIndex = round(random.uniform(0,populationSize-1))

    recombinedPopulation.append(crossoverIndividuals(population[fatherIndex],
                                                     population[motherIndex],
                                                     bwsFitnessFunction,
                                                     highIsGood))
  return recombinedPopulation

def selectTourney(population, fitnessFunction, nrOfContenders = 2, highIsGood = True):
  """Selects individuals out of a population with the best fitness function
  values. Uses a tourney algorithm."""
  populationSize = len(population)
  selectedPopulation = []

  #select until original populationSize is reached
  while len(selectedPopulation) < populationSize:

    if highIsGood:
      bestFitness = -math.inf
    else:
      bestFitness = math.inf

    pastContenders = []

    for i in range(nrOfContenders):
      #choose a contender randomly. Make sure that contenders are not equal
      while True:
        contenderNr = round(random.uniform(0, populationSize - 1))
        if contenderNr in pastContenders:
          continue
        pastContenders.append(contenderNr)
        break

      contender = population[contenderNr]
      fitnessOfContender = fitnessFunction(contender)

      if (highIsGood and fitnessOfContender > bestFitness) or \
         (not highIsGood and fitnessOfContender < bestFitness):
          winner = contender
          bestFitness = fitnessOfContender

    selectedPopulation.append(copy.deepcopy(winner))

  return selectedPopulation
