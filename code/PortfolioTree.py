import uuid
from numpy import cov
import random
from itertools import product
from collections import Counter
#from math import pow

import Values


class PortfolioTree(object):
  """
  Python class implementing a tree structure where every Node has 0 or 2
  children. Additionally, each Node has a weight w with 0 < w < 1 which
  represents the weight of the first (left) child. The weight of the
  second (right) child automatically becomes 1 - w.

  Each Leafnote represents an asset.
  """

  def __init__(self, depth, assetList, parent = None, isLeftChild = None):

    self.iD = uuid.uuid4()
    self.parent = parent
    self.depth = depth
    self.isLeftChild = isLeftChild
    self.risk = 0
    self.weight = 0
    if depth < 1:
      self.lChild = None
      self.rChild = None
      self.asset = random.choice(assetList)
    else:
      self.weight = random.uniform(0.001, 0.999)
      self.lChild = PortfolioTree(depth - 1, assetList, parent = self, isLeftChild = True)
      self.rChild = PortfolioTree(depth - 1, assetList, parent = self, isLeftChild = False)
    self.calculateRisk()

  def recursiveCalculateRisk(self):
    """Calculate the risk for this and all parent nodes."""
    self.calculateRisk()
    #if self.parent is None:
     # return
    try:
      self.parent.recursiveCalculateRisk()
    except AttributeError:
      return

  def calculateRisk(self):
    """Calculates the risk inhabited by the portfolio."""
    #return
    if self.isLeaf():
      self.risk = Values.variances[self.asset]
      return

    self.risk = 0
    assetWeights = self.getTotalAssetWeights()

    for assetA, assetB in product(assetWeights, repeat=2):
      if assetA == assetB:
        self.risk += pow(Values.variances[assetA] * assetWeights[assetA],2)
      else:
        self.risk += cov(Values.pastReturnValues[assetA],
                                 Values.pastReturnValues[assetB])[0][1] * \
                             assetWeights[assetA] * assetWeights[assetB]



  def updateSubTree(self, depth, index, newTree):
    """Updates the subtree at the specified depth and index with newTree."""
    numberOfNodes = pow(2, depth)

    if index not in range(numberOfNodes):
      print('Not a valid node index.')
      print('Depth: ', depth)
      print('Index: ', index)
      return

    if depth == 1:
      if index == 0:
        self.lChild = newTree
        self.lChild.parent = self
        self.lChild.isLeftChild = True
      if index == 1:
        self.rChild = newTree
        self.rChild.parent = self
        self.rChild.isLeftChild = False

    elif index < numberOfNodes/2:
      self.lChild.updateSubTree(depth - 1, index, newTree)
    else:
      self.rChild.updateSubTree(depth - 1, int(index - numberOfNodes/2), newTree)

    self.calculateRisk()

  def getDepth(self):
    """Calculates the number of layers from this node to the leaf layer."""
    if self.isLeaf():
      return 0

    return 1 + self.lChild.getDepth()

  def getNodesAtDepth(self, depth):
    """Returns all nodes at specified depth in a list."""

    if depth < 1:
      return [self]

    return self.lChild.getNodesAtDepth(depth - 1) + self.rChild.getNodesAtDepth(depth - 1)

  def isLeaf(self):
    """Returns True if the calling node is a leaf, i.e. has no children.
    Returns False otherwise."""
    if self.lChild is None and self.rChild is None:
      return True
    return False

  # def getTotalWeight(self, root):
  #   """Calculates the weight this node has from the root node."""
  #   if self.parent is None:
  #     return 1
  #   if self.parent.iD is root.iD:
  #     if self.isLeftChild:
  #       return self.parent.weight
  #     else:
  #       return (1 - self.parent.weight)
  #   if self.isLeftChild:
  #     return self.parent.weight * self.parent.getTotalWeight(root)
  #   elif self.isLeftChild is False:
  #     return (1 - self.parent.weight) * self.parent.getTotalWeight(root)

  # def getTotalAssetWeights(self):
  #   """Returns a dictionary which contains all available assets with their total
  #   weight of the calling node."""

  #   def __recursiveLeafRollout(node):
  #     if node.isLeaf():
  #       assetWeight = [(node.asset , node.getTotalWeight(self))]
  #       return assetWeight

  #     return __recursiveLeafRollout(node.lChild) + \
  #            __recursiveLeafRollout(node.rChild)

  #   #initialize the dict to 0
  #   assetWeights = {}
  #   for assetName in Values.pastFaceValues:
  #     assetWeights[assetName] = 0

  #   weightList = __recursiveLeafRollout(self)

  #   #normalize, so that the weight's sum equals 1
  #   sumOfWeights = sum([pair[1] for pair in weightList])

  #   for element in weightList:
  #     assetWeights[element[0]] += element[1]/sumOfWeights

  #   return assetWeights

  def getTotalAssetWeights(self):

    def __recursiveGetWeights(node):
      if node.isLeaf():
        return {node.asset : 1}

      #if node.lChild.isLeaf():
      #  lWeights = {node.lChild.asset : node.weight}
      #  rWeights = {node.rChild.asset : (1 - node.weight)}

      else:
        lWeights = __recursiveGetWeights(node.lChild)
        rWeights = __recursiveGetWeights(node.rChild)

        lWeights.update((key, value*node.weight) for key, value in lWeights.items())
        rWeights.update((key, value*(1 - node.weight)) for key, value in rWeights.items())

        return dict(Counter(lWeights) + Counter(rWeights))

    assetWeights = {}
    for assetName in Values.pastFaceValues:
      assetWeights[assetName] = 0

    assetWeights.update(__recursiveGetWeights(self))
    return assetWeights


