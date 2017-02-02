import Values
from statistics import stdev
"""
A selection of fitness functions for the portfolio problem
"""

def simpsonIndex(node):
  """Returns 0 if the asset weights are uniformly spread. Returns 1 if the
  portfolio consists of 1 asset only."""
  weights = node.getTotalAssetWeights().values()
  nrOfAssets = len(weights)
  return (sum([x ** 2 for x in weights]) - 1/nrOfAssets) / ( 1 - 1/nrOfAssets)

def equalFunc(node):
  """Returns the standard deviation of the asset weights."""
  weights = node.getTotalAssetWeights()
  return stdev(list(weights.values()))

def estimatedReturn(node):
  """Returns the estimated return value of a node as the moving average of past
  return values."""

  #if the node is a single asset, estimated return value is
  #calculated as the moving average of the past face values of that asset
  if node.isLeaf():
    assetName = node.asset
    pastReturnValuesOfAsset = Values.pastReturnValues[assetName]
    #calculate the moving average of return values
    return sum(pastReturnValuesOfAsset) / (len(pastReturnValuesOfAsset) - 1)
  #if the node has children, the estimated return is calculated as the
  #weighted sum of the estimated return of its children
  else:
    return node.weight * estimatedReturn(node.lChild) + \
           (1 - node.weight) * estimatedReturn(node.rChild)

def volatality(node):
  """Returns the volatality of a node using the standard deviation."""

  #if the node is a single asset, volatality is given by the volatalities-dict
  if node.isLeaf():
    return Values.volatalities[node.asset]
  #if the node has children, volatality is calculated using the covariance
  #between the cildren
  return node.weight * volatality(node.lChild) + \
         (1 - node.weight) * volatality(node.rChild) + \
         2 * node.weight * (1 - node.weight) * node.covariance

def sharpeRatio(node):
  """Returns the ratio of the expected return value of a node divided by its
volatality."""

  #sharpeRatio = estimatedReturn(node)/node.risk
  sharpeRatio = (estimatedReturn(node)-(Values.risklessReturn/Values.period))/node.risk
  #Sharpe ratio doesnt work for negative values. Thus, return 0 if the ratio is
  #negative
  return sharpeRatio
  #return max(0, sharpeRatio)