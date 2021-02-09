#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 20:21:59 2020

@author: benjamintenmann
"""


import numpy as np
from itertools import product
from math import exp
from scipy.stats import uniform
import matplotlib.pyplot as plt

def f(z):
    y = 1/(1+exp(-z))
    return y

def fprime(z):
    der = f(z) * (1-f(z))
    return der

def loss(t,y):
    err = 0.5 * (t-y)**2
    return err

def gradient_descent(t, w, x):
    z = x.dot(w)
    delta_w = (t-f(z)) * fprime(z) * x
    return delta_w

epochs = 500
epsilon = 0.01
inputs = list(product([-1,1], repeat=10))

w = uniform.rvs(size=11)


# training
ep_err = []

n_data_points = len(inputs)
train = int(n_data_points * 0.8)
validate = (n_data_points - train) // 2
test = n_data_points - train - validate

# train the model over the specified number of epochs
for i in range(epochs):
    
    err = 0
    
    for n in range(train): # iterate over the training set
        
        z = np.array(inputs[n])
        t = int(np.sum(z) >= 0) # evaluates to 1 if True and 0 if False
        
        x = np.append(z, -1) # add bias unit to input vector
        
        
        w += epsilon * gradient_descent(t, w, x) # update weights
        err += loss(t, f(x.dot(w))) # record error
        
        
    ep_err.append(err/train) # average training error per-epoch
    
    for n in range(train, train+validate): # validate
        
        z = np.array(inputs[n])
        t = int(np.sum(z) >= 0) # evaluates to 1 if True and 0 if False
        
        x = np.append(z, -1)
        
        # note: no weights update
        err += loss(t, f(x.dot(w)))
        
        
    ep_err.append(err/validate) # average validation error per-epoch

    
# testing
err = 0
for n in range(n_data_points-test, n_data_points):
    
    z = np.array(inputs[n])
    t = int(np.sum(z) >= 0)
    
    x = np.append(z, -1)
    
    err += loss(t, f(x.dot(w)))

test_err = err/test
    



# data visualisation --- plotting the error curve
import seaborn as sns
import pandas as pd

df = pd.DataFrame({'error':ep_err+[test_err]*epochs, 
                   'epoch':np.append(np.repeat(list(range(1,epochs+1)), 2), list(range(1,epochs+1))), 
                   'data-set':['train', 'validate']*epochs + ['test']*epochs})

sns.set_theme()
g, ax = plt.subplots(figsize=(9,6))

sns.lineplot(data=df, x='epoch', y='error', hue='data-set', ax=ax, err_style=None)
fig = ax.get_figure()
fig.savefig('/Users/benjamintenmann/Desktop/outofthebox/TDS/perc_error.png', dpi=400)