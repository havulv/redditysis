#!/usr/bin/python

'''
    A platform for regression and analysis techniques built in
    Programming for Math & Science as offered by Fordham University
    and taught in the Spring of 2015  by Professors Abe Smith and
    Christine Papadakis.

    Author: John Andersen
    Orig. Date: 3/20/15

    Functions:
        Help()
        F(M,t)
        RSS(M, X, Y)
        MM(X,Y)
        covar(W)
        fit(X,Y)
        pca(W)
        lasso(X,Y,t)
        lasso_step(X,Y,bifurcations=20)
        center(Array)
        lasso_plot(tList, MList, name, tname='_', mname='_')
        OneLasso(X,Y,TT)
        DisplayEq(Model)
        PlotAndExplain(X,Y,TMax,filename)

    TODO:
        logging
        unittest
        PEP 8 compliance
'''


from __future__ import print_function

import re, sys
import matplotlib
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import scipy.optimize as opt

def Help():
    '''
    A nice help message to help the user if they screw up the input
    '''

    name = './linear_analysis.py'
    UsageList = [
            name,
            name + ' mydata.extension pca',
            name + ' mydata.extension fit n',
            name + ' mydata.extension lasso n',
            name + ' mydata.extension lasso n T']

    Descrip = [
            'displays a helpful help message',
            'displays the singular values of the data, from greatest'
            ' to least and shows the vector corresponding to the '
            'absolute greatest singular value',
            'prints the coefficents of the least squares linear fit of'
            ' the data where column \'n\' is the dependent/response'
            ' variable. This also prints the RSS of the model and the'
            ' Fraction-of-Variance-Explained.',
            'Assuming column \'n\' is the dependent/response variable'
            ' and the other columns are the independent/predictor'
            ' variables, this runs lasso minimization for a range of t'
            ' between 0 and the largest absolute value in transpose'
            ' X*Y. This also prints a graph of how the coefficients'
            ' vary with t and a graph of the Fraction of Variance'
            ' Explained, this returns the linear model given by lasso'
            ' at a t= T.'
            ]

    helpmessage = 'This is a program to analyze large sets of data and'
    ' contains different tools to help with this. To efficiently and'
    ' accurately use this tool you must have a data set'
    ' (mydata.extension) and know which column to use as a'
    ' dependent/response variable (i.e. column = n) \n \n'

    print(helpmessage)
    for i in range(4):
        print("{0:<10} {1:>8} \n".format(UsageList[i], Descrip[i]))
    return

def F(M, t):
    '''
        The function which will be minimized over lasso in terms of M and t
        Args:                   Parameters
             M      np.ndarray(matrix of observations)
             t              int(weight constant)
        Returns:
             .5*RSS(M,X,Y)+t*np.linalg.norm(M,1)
    '''
    return .5*RSS(M,X,Y)+t*np.linalg.norm(M,1)


def RSS(M, X, Y):
    '''
        Returns RSS of M by X and Y
        Args:                   Parameters
             M      np.ndarray(matrix of observations)
             X      np.ndarray(first matrix of observs)
             Y      np.ndarray(2nd matrix of observs.)
        Returns:
            <(Y-X*M).T, Y-X*M>
    '''
    M.shape = (X.shape[1],)
    XM = X.dot(M)
    XM.shape = Y.shape
    return ((Y-XM).T).dot(Y-XM)


def MM(X,Y):
    '''
        Least Squares Regression Algorithm
        Args:                   Parameters
             X      np.ndarray(first matrix of observs)
             Y      np.ndarray(2nd matrix of observs.)
        Returns:
            <X.T, X> = a*<X.T, Y> (Solves for vector a)
    '''
    return la.solve(X.T.dot(X), X.T.dot(Y))

def covar(W):
    '''
        Returns covariance matrix; measures data correlation
        Args:                   Parameters
             W      np.ndarray(all observations)
        Returns:
            <W.T, W>/W.rows
    '''
    return (W.T.dot(W))/(len(W[0])-1)


def fit(X,Y):
    '''
        Best fit model for data
        Args:                   Parameters
             X      np.ndarray(first matrix of observs)
             Y      np.ndarray(2nd matrix of observs)
        Returns:
            least squares, residual least squares, variance of data
            MM(X,Y)         <(Y-<X,(MM)>,Y-<X,MM>> (<Y.T,Y>-RLS)/<Y.T,Y>
    '''
    print('Computing RSS...')
    Mx = MM(X,Y)
    RSSM = ((Y-X.dot(Mx)).T).dot(Y-X.dot(Mx))

    print('Computing Fraction of Variance...')
    frac = (Y.T.dot(Y)-RSSM)/(Y.T.dot(Y))
    return Mx,RSSM,frac


def pca(W):
    '''
        Principal Component Analysis on matrix of observations
        Args:                   Parameters
             W      np.ndarray(matrix of observs)
        Returns:
            Eigenvalues, Eigenvectors
    '''
    cov = covar(W)
    print('Computing Eigenvalues and Eigenvectors...')
    Deigs, Deigsv = la.eigh(cov)
    eigs = np.array(list(reversed(Deigs)))
    eigsv = np.array(list(reversed(Deigsv)))
    return eigs, eigsv


def lasso(X,Y,t):
    '''
        Lasso algorithm (essentially weighting PCA by different norms)
        Args:                   Parameters
            X      np.ndarray(first matrix of observs)
            Y      np.ndarray(2nd matrix of observs)
            t                   int(weight)
        Returns:
            Minimum of lasso, Fraction of Variance
    '''
    Min = (opt.minimize(lambda M: .5*RSS(M, X,Y)[0,0]+t*np.linalg.norm(M,1), np.zeros(shape=(X.shape[1])))).x
    RSSLasso = RSS(Min, X,Y)
    LassoFrac = (Y.T.dot(Y)-RSSLasso)/(Y.T.dot(Y))
    return Min, LassoFrac

def lasso_step(X,Y,bifurcations=20):
    '''
        Helper function for iterating on the lasso algorithm guesses
        highest t value instead of random guessing
        Args:                   Parameters
            X      np.ndarray(first matrix of observs)
            Y      np.ndarray(2nd matrix of observs)
            bifurcations        int(20 | number of splits)
        Returns:
            Optimal t-value
    '''
    TLeft = 0.0
    TRight = np.max(np.abs(X.T.dot(Y)))
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
        Centers the array about the mean of the data
        Args:                   Parameters
            Array   np.ndarray(matrix of observs)
    '''
    Mean = Array - np.mean(Array, axis=0)
    return Mean # after subracting the means

def lasso_plot(tList, MList, name, tname='_', mname='_'):
    '''
        Plots and saves a graph based on the given inputs of t and M.
        Args:                   Parameters
             tList  np.ndarray(list of t values)
             MList  np.ndarray(list of M vectors)
             name           str(Graph file name)
             tname          str(X axis name)
             mname          str(Y axis name)
    '''

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
    '''
        lasso minimization at a certain t
        Args:                   Parameters
            X      np.ndarray(first matrix of observs)
            Y      np.ndarray(2nd matrix of observs)
            TT                  int(t value)
    '''
    Model = lasso(X,Y,TT)[0]
    FullModel = DisplayEq(Model)
    print('The linear model given by lasso at t = {0} is: \n f(x)={1}'.format(TT,FullModel))
    return

def DisplayEq(Model):
    '''
        Outputs an equation for the lasso algorithm or PCA
        Args:                   Parameters
             Model      np.ndarray(pca or lasso)
        Returns:
            C_1*x^n + C_2*x^(n-1) + ... + C_n*x^0
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
        Iterates lasso (bifurcations=20), outputs formula and then
        plots the functions
        Args:                   Parameters
            X      np.ndarray(first matrix of observs)
            Y      np.ndarray(2nd matrix of observs)
            TMax            int(Max. t value)
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
        #In the case that the matrices do not align, numpy raises ValueError
        except ValueError:
            print('If t is too large (in this case, t{0}) then'.format(t)
            ' there is a matrix error. This is what just happened. As a'
            ' result, the graph may flatline at the end slightly.')
            pass
        mlist.append(m)
        fracList.append(frac[0])
    lasso_plot(tlist,mlist, 'M'+ NAME, tname='t', mname='M')
    lasso_plot(tlist,fracList, 'Fraction_of_Variance'+NAME, tname='t',
                                            mname='Fraction of Variance')
    return


if __name__ == '__main__':

    #try to open the data file.
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

    # in the case of PCA, there is no need to split the data up
    try:
        dum = int(sys.argv[3])
        xIndex = [True] *columns
        xIndex[dum] = False
        xSelect = np.array(xIndex)
        ySelect = np.array([not i for i in xSelect])

    # Split into X and Y (Dependent and Independent respectively)
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
        print("The linear best fit model is: \n f(x)={0} \n".format(
                                                            FullModel))
        print("The fractional variance is {0}".format(frac[0][0]))
        print("\n The RSS of this model is {0}".format(AllMs))

    # Going through pca -- the singular values then outputting them as
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
        print(
        'The vector associated with this value is: \n {0} \n'.format(
                                                            eigsvec[0]))
        print('\nThe list of Singular Values is:\n{0} \n'.format(svdStr))

    # Go through lasso. if fourth sysarg then lasso once else graph
    elif sys.argv[2] == "lasso" and ValGiven == True:
        try:
            TT = float(sys.argv[4])
            OneLasso(X,Y,TT)
        except IndexError:
            TMax = lasso_step(X,Y)
            PlotAndExplain(X,Y,TMax, sys.argv[1])
    else:
        Help()
