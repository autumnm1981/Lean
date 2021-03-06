﻿# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *

# Libraries included with basic python install
from bisect import bisect
import cmath
import collections
import copy
import functools
import heapq
import itertools
import math
import operator
import pytz
import Queue
import re
import time
import zlib

# Third party libraries added with pip
from sklearn.ensemble import RandomForestClassifier
import blaze   # includes sqlalchemy, odo 
import numpy
import scipy
import cvxopt
import cvxpy
from pykalman import KalmanFilter
import statsmodels.api as sm
import talib

class PythonPackageTestAlgorithm(QCAlgorithm):
    '''Basic template algorithm simply initializes the date range and cash'''


    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        
        self.SetStartDate(2013, 10, 7)   #Set Start Date
        self.SetStartDate(2013, 10, 11)  #Set End Date
        self.AddEquity("SPY", Resolution.Daily)

        # numpy test
        print "numpy test >>> print numpy.pi: " , numpy.pi
        
        # scipy test: 
        print "scipy test >>> print mean of 1 2 3 4 5:", scipy.mean(numpy.array([1, 2, 3, 4, 5]))

        #sklearn test
        print "sklearn test >>> default RandomForestClassifier:", RandomForestClassifier()
        
        # cvxopt matrix test
        print "cvxopt >>>", cvxopt.matrix([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], (2,3))

        # blaze test
        blaze_test()
        
        # cvxpy test
        cvxpy_test()

        # statsmodels test
        statsmodels_test()

        # pykalman test
        pykalman_test()

        # talib test
        print "talib test >>>", talib.SMA(numpy.random.random(100))

    def OnData(self, data): pass

def blaze_test():
    accounts = blaze.symbol('accounts', 'var * {id: int, name: string, amount: int}')
    deadbeats = accounts[accounts.amount < 0].name
    L = [[1, 'Alice',   100],
         [2, 'Bob',    -200],
         [3, 'Charlie', 300],
         [4, 'Denis',   400],
         [5, 'Edith',  -500]]
    print "blaze test >>>", list(blaze.compute(deadbeats, L))

def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    i = bisect(breakpoints, score)
    return grades[i]

def cvxpy_test():
    numpy.random.seed(1)
    n = 10
    mu = numpy.abs(numpy.random.randn(n, 1))
    Sigma = numpy.random.randn(n, n)
    Sigma = Sigma.T.dot(Sigma)

    w = cvxpy.Variable(n)
    gamma = cvxpy.Parameter(sign='positive')
    ret = mu.T*w 
    risk = cvxpy.quad_form(w, Sigma)
    print "csvpy test >>> ", cvxpy.Problem(cvxpy.Maximize(ret - gamma*risk), 
               [cvxpy.sum_entries(w) == 1, 
                w >= 0])

def statsmodels_test():
    nsample = 100
    x = numpy.linspace(0, 10, 100)
    X = numpy.column_stack((x, x**2))
    beta = numpy.array([1, 0.1, 10])
    e = numpy.random.normal(size=nsample)

    X = sm.add_constant(X)
    y = numpy.dot(X, beta) + e

    model = sm.OLS(y, X)
    results = model.fit()
    print "statsmodels tests >>>", results.summary()

def pykalman_test():
    kf = KalmanFilter(transition_matrices = [[1, 1], [0, 1]], observation_matrices = [[0.1, 0.5], [-0.3, 0.0]])
    measurements = numpy.asarray([[1,0], [0,0], [0,1]])  # 3 observations
    kf = kf.em(measurements, n_iter=5)
    print "pykalman test >>>", kf.filter(measurements)