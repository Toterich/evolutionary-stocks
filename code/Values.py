from statistics import stdev

"""
This file contains past some values concerning the financial market. These are
used to determine the fitness of a portfolio.
"""

#face values of several assets at the end of every month from April 15 to April 16
pastFaceValues = {
  "adidas" : [73.14, 71.5, 68.94, 74.58, 66.53, 71.71, 81.46, 91.40, 89.99,
              97.78, 98.47, 102.9, 113.49],
  "bayer": [129.73, 130.23, 126.19, 132.58, 121.3, 114.06, 121.3, 126.3, 127.43,
            130.28, 135.37, 130.28, 132.46],
  "commerzbank" : [12.1, 12.13, 11.52, 11.81, 10.02, 9.41, 10.06, 10.39, 9.60,
                   7.52, 7.5, 7.68, 8.15],
  "post" : [29.48, 27.55, 26.3, 27.56, 24.59, 24.63, 27.01, 27.73, 26, 22.32,
            21.19, 24.58, 25.64],
  "infineon" : [10.58, 11.98, 11.2, 10.3, 9.7, 9.98, 11.19, 12.08, 13.54, 12.28,
                11.23, 12.42, 12.47],
  "lufthansa" : [12.1, 12.49, 11.28, 12.05, 10.59, 12.12, 13.1, 13.23, 14.21,
                 13.14, 13.45, 13.86, 13.56],
  "thyssenkrupp" : [23.86, 24.12, 25.34, 24.09, 24.33, 22.68, 20.35, 20.15,
                    18.34, 20.24, 22.62, 23.26, 22.31],
  "pro7" : [43.84, 44.36, 44.65, 47.23, 45.02, 44.44, 50, 49.3, 47.2, 45.2,
            46.94, 45.3, 47.65],
  "vonovia" : [28.81, 28.05, 25.60, 28.55, 30.2, 34.7, 30.72, 32.39, 28.67,
               32.04, 30.2, 34.7, 36.51],
  "merck" : [28.3, 29.05, 29.5, 28.55, 29.87, 30.7, 30.72, 30.39, 31.67,
             29.04, 30.4, 31.7, 32.51],
  "rwe" : [22.86, 23.42, 24.34, 24.09, 24.33, 23.88, 24.35, 25.85,
           25.94, 24.84, 24.9, 25.1, 24.81],
  "siemens" : [83.14, 81.5, 78.94, 84.58, 76.53, 81.71, 71.46, 101.40, 99.99,
               107.78, 108.47, 112.9, 113.49],
  "continental" : [12.1, 12.13, 09.52, 11.81, 13.02, 17.41, 20.06, 18.39, 15.60,
                   19.22, 20.8, 18.68, 23.2],
  "daimler" : [18.81, 18.05, 15.60, 18.55, 19.2, 18.7, 20.72, 20.39, 18.67,
               17.04, 18.2, 21.7, 22.51],
  "eon" : [25.81, 24.05, 25.60, 25.55, 26.2, 25.7, 26.72, 27.39, 27.67,
               27.04, 27.2, 27.7, 28.21],
  "deutschebank" : [12.1, 14.79, 20.38, 12.05, 18.59, 14.12, 16.1, 20.23, 22.21,
                 18.14, 20.45, 26.86, 25.96],
  "bmw" : [70.48, 77.55, 66.3, 64.56, 69.59, 73.63, 79.01, 84.73, 80, 78.32,
            76.19, 80.58, 82.64]
  }

#return values over all 1-month periods from April 15 to April 16
pastReturnValues = {}
for name in pastFaceValues:
  pastReturnValues[name] = [(pastFaceValues[name][i + 1] /
                             pastFaceValues[name][i] - 1) * 100
                             for i in range(len(pastFaceValues[name]) - 1)]

#volatalities over all 1-month periods from April 15 to April 16
variances = {}
for name in pastReturnValues:
  variances[name] = stdev(pastReturnValues[name])


#Estimated yearly return of a safe investment, e.g. a state bond.
#Last Checked:24.05.16
risklessReturn = 1

period = 12