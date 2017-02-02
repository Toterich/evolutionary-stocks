#!/usr/local/python3

import random
import math
import copy
import uuid

import Values
from PortfolioTree import PortfolioTree
import FitnessFunctions as ff

def weighted_choice(choices, weights):
  """Randomly returns an element from choices, when each element from choices is
  assigned a choosing probability in weights. len(choices) == len(weights)"""

  positiveWeights = [max(0.0001,w) for w in weights]
  total = sum(positiveWeights)
  r = random.uniform(0, total)
  upto = 0
  for c, w in zip(choices, positiveWeights):
    if upto + w >= r:
      return c
    upto += w
  assert False, "Shouldn't get here"

def initPopulation(populationSize, initialDepth, assetList):
  """Generates a population of random Portfoliotrees."""

  #list holding all individuals
  population = []

  for i in range(populationSize):
    population.append(PortfolioTree(initialDepth, assetList))

  return population

def mutateIndividual(individual, strength, assetList,
                     fitnessFunction = None, highIsGood = True):
  """Randomly mutate an individual."""
  totalDepth = individual.getDepth()
  #choose node of mutation

  #choose mutation depth at random(weighted by the mutation strength)
  mutationDepth = min(max(round(random.gauss(totalDepth * (1 - strength), totalDepth/4)), 1),totalDepth - 1)

  if fitnessFunction is None:
    #choose mutation node at depth at random
    mutationIndex = round(random.uniform(0, pow(2, mutationDepth) - 1))

  else:
    #choose mutation node with a chance according to it's fitness value
    mutationCandidates = individual.getNodesAtDepth(mutationDepth)
    if highIsGood:
      selectionWeights = [1/max(0.00001,x) for x in list(map(fitnessFunction, mutationCandidates))]
    else:
      selectionWeights = map(fitnessFunction, mutationCandidates)

    mutationIndex = weighted_choice(range(pow(2,mutationDepth)), selectionWeights)

  newSubTree = PortfolioTree(totalDepth - mutationDepth, assetList)
  #mutatedIndividual = copy.deepcopy(individual)

  #mutatedIndividual.updateSubTree(mutationDepth, mutationIndex, newSubTree)
  individual.updateSubTree(mutationDepth, mutationIndex, newSubTree)
  individual.iD = uuid.uuid4()
  individual.recursiveCalculateRisk()
  return



def mutatePopulation(population, rate, strength, assetList,
                     fitnessFunction = None, highIsGood  = True):
  """Randomly mutate a population."""
  if rate < 0 or rate > 1:
    print('Mutation rate has to lie in [0,1].')
    return

  if strength <= 0 or strength > 1:
    print('Mutation strength has to lie in  (0,1].')
    return

  #mutatedPopulation = []

  for individual in population:
    if random.random() < rate:
      mutateIndividual(individual, strength, assetList, fitnessFunction, highIsGood)
      #mutatedPopulation.append(individual)
      #mutatedPopulation.append(mutateIndividual(individual, strength, assetList))
    #else:
    #  mutatedPopulation.append(individual)

  #return mutatedPopulation
  return

def crossoverIndividuals(father, mother, fitnessFunction, highIsGood):
  """Recombines two trees to a new one which shares some traits with both of
  them."""

  #choose depth of crossover point at random
  crossoverDepth = round(random.uniform(1,father.getDepth()))

  #get all subtrees of father and mother at that layer of deepness
  fatherNodesAtLayer = father.getNodesAtDepth(crossoverDepth)
  motherNodesAtLayer = mother.getNodesAtDepth(crossoverDepth)

  numberOfNodesinLayer = pow(2, crossoverDepth)

  #if no fitnessfunction is supplied, use random crossover
  if fitnessFunction is None:
    indexM = round(random.uniform(0,numberOfNodesinLayer - 1))
    indexF = round(random.uniform(0,numberOfNodesinLayer - 1))

  #if bws (Best-Worst-Subtree) crossover is used, at crossoverDepth
  #find the best subtree from father and the worst from mother
  else:
    fitnessValuesOfFatherNodes = list(map(fitnessFunction, fatherNodesAtLayer))
    fitnessValuesOfMotherNodes = list(map(fitnessFunction, motherNodesAtLayer))

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
  #give child new id
  child.iD = uuid.uuid4()
  child.recursiveCalculateRisk()
  return child

def crossoverPopulation(population, bwsFitnessFunction = None, highIsGood = True):
  populationSize = len(population)
  recombinedPopulation = []
  allIndividualsEqual = False
  #i = 0
  #while len(recombinedPopulation) < populationSize:
  for i in range(populationSize):
    if allIndividualsEqual:
      recombinedPopulation.append(copy.deepcopy(population[i]))
      continue
    #choose 2 individuals at random
    indices = list(range(populationSize))
    fatherIndex = random.choice(indices)
    motherIndex = i
    while population[fatherIndex].iD == population[motherIndex].iD:
      indices.remove(fatherIndex)
      if not indices:
        recombinedPopulation.append(copy.deepcopy(population[motherIndex]))
        allIndividualsEqual = True
        break
      fatherIndex = random.choice(indices)

    if not allIndividualsEqual:
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

    #selectedPopulation.append(copy.deepcopy(winner))
    selectedPopulation.append(winner)

  return selectedPopulation
