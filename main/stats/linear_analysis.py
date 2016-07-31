#!/usr/bin/python

'''
A platform for regression and analysis techniques built in Programming for Math & Science
as offered by Fordham University and taught in the Spring of 2015  by Professors Abe
Smith and Christine Papadakis.

Author: John Andersen
Orig. Date: 3/20/15
Last Revised: 5/28/16
    -- Documentation update

Currently no source control is used for this program.
Hopefully, the code will be brought up to PEP 8 standards of maintenance
'''


from __future__ import print_function

import re
import matplotlib
#matplotlib.use('Agg')
import numpy as np
import sys
import scipy.linalg as la
import matplotlib.pyplot as plt
import scipy.optimize as opt

def Help():
    '''
    A nice help message to help the user if they screw up the input
    '''

    name = './linear_analysis.py'
    UsageList = [name, name + ' mydata.extension pca', name + ' mydata.extension fit n',
                    name + ' mydata.extension lasso n', name + 'mydata.extension lasso n T']
    Descrip = ['displays a helpful help message',
'displays the singular values of the data, from greatest to least and shows the vector corresponding to the absolute greatest singular value',
'prints the coefficents of the least squares linear fit of the data where column \'n\' is the dependent/response variable. This also prints the RSS of the model and the Fraction-of-Variance-Explained.',
'Assuming column \'n\' is the dependent/response variable and the other columns are the independent/predictor variables, this runs lasso minimization for a range of t between 0 and the largest absolute value in transpose X*Y. This also prints a graph of how the coefficients vary with t and a graph of the Fraction-of-Variance-Explained, this returns the linear model given by lasso at a t= T.']
    helpmessage = 'This is a program to analyze large sets of data and contains different tools to help with this. To efficiently and accurately use this tool you must have a data set (mydata.extension) and know which column to use as a dependent/response variable (i.e. column = n) \n \n'
    print(helpmessage)
    for i in range(4):
        print("{0:<10} {1:>8} \n".format(UsageList[i], Descrip[i]))
    return

def F(M, t):
    ''' The function which will be minimized over lasso in terms of M and t '''
    return .5*RSS(M,X,Y)+t*np.linalg.norm(M,1)


def RSS(M, X, Y):
    '''
    The RSS formula. Essentially, residual transposed times residual. The only careful bit in here
    is that numpy likes to switch column vectors to row vectors (or vice versa) and so it is
    necessary to reset the rows of M to equal the columns of X, and to set the shape of X.dot(M)
    equal to Y so they can be subtracted from one another.
    '''
    M.shape = (X.shape[1],)
    XM = X.dot(M)
    XM.shape = Y.shape
    return ((Y-XM).T).dot(Y-XM)


def MM(X,Y):
    ''' finding M in the quickest way that we know -- linear least squares regression '''
    return la.solve(X.T.dot(X), X.T.dot(Y))

def covar(W):
    '''
    The Covariance of the matrix. This measures how correlated the data is to each other.
    Essentially it shows how much the data is pointing in each direction, normalized by the
    amount of data.
    '''
    return (W.T.dot(W))/(len(W[0])-1)


def fit(X,Y):
    '''
    Computes the model of best fit, the absolutely most accurate model, with the fraction of
    variance. The fraction of variance tells us a percentage of how much this model actually
    varies from the independent variable
    '''

    print('Computing RSS...')
    Mx = MM(X,Y)
    RSSM = ((Y-X.dot(Mx)).T).dot(Y-X.dot(Mx))

    print('Computing Fraction of Variance...')
    frac = (Y.T.dot(Y)-RSSM)/(Y.T.dot(Y))
    return Mx,RSSM,frac


def pca(W):
    '''
    Delivers the eigenvalues and eigenvectors in reversed order (which is greatest to least).
    The eigenvalues deliver the variance of the matrix in scalar form. That is,
    (lambda*I-A)v=0 where lambda is the eigenvalue. Moreover, Av=(lambda)v. Thus, the eigenvalues
    we are given are that which turn the matrix of data into a vector. Although, as we will see
    later on, this only accounts for the largest eigenvalue.
    '''

    cov = covar(W)
    print('Computing Eigenvalues and Eigenvectors...')
    Deigs, Deigsv = la.eigh(cov)
    eigs = np.array(list(reversed(Deigs)))
    eigsv = np.array(list(reversed(Deigsv)))
    return eigs, eigsv


def lasso(X,Y,t):
    '''
    lasso calculates the same thing as fit except that it does so while adjusting for complexity
    of equation. The t constraint allows for the function to weight the individual variables more.
    As t becomes greater, the norm becomes greater, and the largest variables become more
    important than the others. As t approaches 0, the function optimizes towards the RSS function.
    This function also outputs the fraction of variance between the minimzed function and the data
    '''

    Min = (opt.minimize(lambda M: .5*RSS(M, X,Y)[0,0]+t*np.linalg.norm(M,1), np.zeros(shape=(X.shape[1])))).x
    RSSLasso = RSS(Min, X,Y)
    LassoFrac = (Y.T.dot(Y)-RSSLasso)/(Y.T.dot(Y))
    return Min, LassoFrac

def lasso_step(X,Y,bifurcations=20):
    '''
    When iterating it is necessary to have a close guess as to what the highest t is. Otherwise
    there are far too many t's to try that could be far beyond the scope of the problem. This
    function bounces back and forth between one possible tmax and another, each time drawing
    closer to the actual tmax.
    The previous resolution (1/(2^(-10))) was too small so I had to pump it up to
    (1/(2^(-20))). At the previous resolution TMax was off by 88 (~.25%).
    '''

    TLeft = 0.0
    TRight = np.max(np.abs(X.T.dot(Y)))
    Traj = []
    for i in range(bifurcations):
        TMid = (TLeft+TRight)/2.0
        try:
            MMid, LsFrac = lasso(X,Y,TMid)
            #checks if all the elements of MMid are equal to 0 within a tolerance 1e-05
            if np.allclose(MMid, 0.0):
                TRight = TMid
            else:
                TLeft= TMid
        except:
            print("lasso_step failed at t={0}, so it must be too big. Treating as Mt==0.".format(
                                                                                            TMid))
            TRight = TMid
    return TRight

def center(Array):
    '''
    Centers the array about the mean of the data so that there is no need to compute larger
    numbers than necessary.
    '''

    Mean = Array - np.mean(Array, axis=0)
    return Mean # after subracting the means

def lasso_plot(tList, MList, name, tname='_', mname='_'):
    ''' Plots and saves a graph based on the given inputs of t and M.'''

    print('Plotting {0}...'.format(name))
    plt.plot(tList, MList, label='m_{0}'.format(i))
    if not(tname=='_' and mname=='_'):
        plt.xlabel('{0}'.format(tname))
        plt.ylabel('{0}'.format(mname))
    plt.suptitle('{0}'.format(name))
    figgg = plt.gcf()
    plt.show()
    print('Saving as {0}.png...'.format(name))
    figgg.savefig("{0}.png".format(name))
    return

def OneLasso(X,Y,TT):
    ''' in the event that the user only wants the lasso minimization at a certain t '''
    Model = lasso(X,Y,TT)[0]
    FullModel = DisplayEq(Model)
    print('The linear model given by lasso at t = {0} is: \n f(x)={1}'.format(TT,FullModel))
    return

def DisplayEq(Model):
    '''
    This is the function used to nicely display pca or OneLasso results in the form of an
    equation. It takes inputs in a list, addendums a variable and then makes that equal to f(x)
    '''
    if type(Model[0]) == np.ndarray:
        Equation = [str(Model[i][0])+'x_'+str(i) for i in range(len(Model))]
    else:
        Equation = [str(Model[i])+'x_'+str(i) for i in range(len(Model))]
    FullModel = ' '
    for i in range(len(Equation)):
        if i != len(Equation)-1:
            FullModel+= Equation[i]+' + '
        else:
            FullModel+= Equation[i]
    return FullModel


def PlotAndExplain(X,Y,TMax,filename):
    '''
    This function iterates over the lasso minimization from t=0 up to t=tmax in steps
    of 20. As well, it also plots the function nicely at the end.
    '''
    addName = re.split('\W+', filename)
    NAME = '_' + addName[len(addName)-2]
    tlist = []
    mlist = []
    fracList = []
    print("Computing Fraction of variance and M as it approaches TMax...")
    for t in range(0, int(TMax)-1, int(TMax)/20):
        tlist.append(t)
        try:
            m, frac = lasso(X,Y,t)
        #In the case that the matrices do not align, numpy raises a ValueError
        except ValueError:
            print('If t is too large (in this case, t{0}) then there is a matrix error. This is what just happened. As a result, the graph may flatline at the end slightly.'.format(t))
            pass
        mlist.append(m)
        fracList.append(frac[0])
    lasso_plot(tlist,mlist, 'M'+ NAME, tname='t', mname='M')
    lasso_plot(tlist,fracList, 'Fraction_of_Variance'+NAME, tname='t',
                                            mname='Fraction of Variance')
    return


if __name__ == '__main__':

    #try to open the data file. If it can't open then it repeats the help function and tells you why it isn't opening
    try:
        data_file = open(sys.argv[1])
    except IndexError:
        Help()
        raise Exception('Please use a valid filename with a valid extension (i.e. .csv, .txt, etc.')

    #Centers the data and chooses the independent variable
    raw_data = np.loadtxt(data_file)
    W = np.array(center(raw_data))
    ValGiven = True
    row, columns = W.shape

    # The try block is used so that, in the case of PCA, there is no need to split the data
    # up or do anything with it. Else, if not going through pca, the code will execute
    # normally and not go through the exception.
    try:
        dum = int(sys.argv[3])
        xIndex = [True] *columns
        xIndex[dum] = False
        xSelect = np.array(xIndex)
        ySelect = np.array([not i for i in xSelect])

    # Split into X and Y (Dependent and Independent respectively
        Y = np.array(W[:, ySelect])
        X = np.array(W[:, xSelect])
    except IndexError:
        ValGiven = False
        pass

    # Going through fit and displaying the best linear model
    if sys.argv[2] == "fit" and ValGiven == True:
        M,RSS,frac = fit(X,Y)
        FullModel = DisplayEq(M)
        AllMs = ""
        for i in range(len(M)):
            if i != len(M)-1:
                AllMs += str(M[i][0]) +', '
            else:
                AllMs += str(M[i][0])
        print("The linear best fit model is: \n f(x)={0} \n".format(FullModel))
        print("The fractional variance is {0}".format(frac[0][0]))
        print("\n The RSS of this model is {0}".format(AllMs))

    # Going through pca and computing the singular values and then outputting them as
    # strings with the largest singular value associated with its eigenvector
    elif sys.argv[2] == "pca" and ValGiven == False:
        eigs, eigsvec = pca(W)
        svds = [(eigs[i])**(1.0/2.0) for i in range(len(eigs))]
        svdStr = ''
        for i in range(len(svds)):
            if i == len(svds)-1:
                svdStr+= str(svds[i])
            else:
                svdStr+=str(svds[i]) +', '
        print('The largest Singular Value is: {0} \n'.format(svds[0]))
        print('The vector associated with this value is: \n {0} \n'.format(eigsvec[0]))
        print('\nThe list of Singular Values is:\n{0} \n'.format(svdStr))

    # Go through lasso. In the case that there is a fourth system argument then it will run
    # through lasso once. Else it will output the graphs associated with going through lasso
    # to find the minimization.
    elif sys.argv[2] == "lasso" and ValGiven == True:
        try:
            TT = float(sys.argv[4])
            OneLasso(X,Y,TT)
        except IndexError:
            TMax = lasso_step(X,Y)
            PlotAndExplain(X,Y,TMax, sys.argv[1])
    else:
        Help()
