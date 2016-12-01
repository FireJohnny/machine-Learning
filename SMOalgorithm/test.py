#coding:utf-8
__author__ = 'FireJohnny'

from numpy import *

def smoSimple(dataMatIn,classLabels,C,toler,maxIter):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    b= 0
    m,n =shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while iter < maxIter:
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b
            Ei  = fXi - float(labelMat[i])
            if (labelMat[i]*Ei<-toler and alphas[i] < C) or labelMat[i]*Ei > 0:
                j = selectJrand(i,m)
                fXj = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphasJold = alphas[j].copy()
                if labelMat[i] != labelMat[j]:
                    L = max(0,alphas[j] - alphas[i])
                    H = min(C,C + alphas[j]  - alphas[i])
                else:
                    L = max(0,alphas[j] + alphas[i]  - C)
                    H = min(C,C + alphas[j] + alphas[i])
                if L == H:
                    print "L==H"
                    continue
                eta  = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - \
                    dataMatrix[i,:] * dataMatrix[i,:].T - \
                    dataMatrix[j,:] * dataMatrix[j,:].T
                if eta >=0:
                    print "eta>=0"
                    continue
                alphas[j] -= labelMat[j] * (Ei - Ej)/eta
                alphas[i] = clipAlpha(alphas[j],H,L)
                if abs(alphas[j] - alphasJold) < 0.00001:
                    print "j not moving enough"
                    continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphasJold - alphas[j])
                b1 = b - Ei - labelMat[i]*(alphas[i] - alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - \
                    labelMat[j]*(alphas[j] - alphasJold) * \
                    dataMatrix[i,:]*dataMatrix[j,:].T

                b2 = b - Ei - labelMat[i]*(alphas[i] - alphaIold)*\
                    dataMatrix[i,:]*dataMatrix[j,:].T -\
                    labelMat[j]*(alphas[j] - alphasJold)*\
                    dataMatrix[j,:]*dataMatrix[j,:].T
                if 0<alphas[i] and C >alphas[i]:
                    b = b1
                elif 0 < alphas[j] and C> alphas[j]:
                    b =b2
                else:
                    b = (b1 + b2)/2.0
                alphaPairsChanged +=1
                print "iter:%d i :%d,pairs changed %d" %(iter,i,alphaPairsChanged)
        if(alphaPairsChanged == 0):
            iter +=1
        else:
            iter = 0
        print "iteration number: %d" % iter
    return b,alphas


