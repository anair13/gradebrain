from internal import *
import scipy
import numpy
from sklearn import linear_model

def covariance(samples):
    """ Gets the covariance of grades """
    xs, ys = list(map(lambda a: a[0], samples)), list(map(lambda a: a[1], samples))
    avgx = sum(xs) / len(xs)
    avgy = sum(ys) / len(ys)
    return sum([(xs[i] - avgx) * (ys[i] - avgy) for i in range(len(samples))]) / len(samples)

def variance(samples):
    """ Gets the variance of y of x """
    xs, ys = list(map(lambda a: a[0], samples)), list(map(lambda a: a[1], samples))
    b, a = simple_lr(samples)
    sum([(ys[i] - (xs[i] * b + a)) ** 2 for i in range(len(samples))]) / len(samples)

def simple_lr(samples):
    """ Returns linear regression coefficients (b, a) where f = bx + a
    samples :: [(Float, Float)]

    Throws a NotEnoughDataException if not enough data exists.
    """
    xs, ys = list(map(lambda a: a[0], samples)), list(map(lambda a: a[1], samples))
    if len(xs) == 0:
        raise NotEnoughDataException("Not enough data! Regression model has a coefficient of 0 or infinity")
    avgx = sum(xs) / len(xs)
    avgy = sum(ys) / len(ys)
    bnum = sum([(xs[i] - avgx) * (ys[i] - avgy) for i in range(len(samples))])
    bdenom = sum([(xs[i] - avgx) ** 2 for i in range(len(samples))])
    if bnum == 0 or bdenom == 0:
        raise NotEnoughDataException("Not enough data! Regression model has a coefficient of 0 or infinity")
    b = bnum / bdenom
    a = avgy - b * avgx
    return (b, a)

def multivariate_lr(x, y):
    """Returns linear regression coefficients (a0, a1, a2, x3 ... an)
        where y = a0 + a1*x1 + a2*x2 + a3*x3 ... an * xn
        x :: [[x1, x2, x3 ... xn], ... xk]
        y :: [y0, y1 ... yk]

        Note, len(x) == len(y), otherwise exception raised
    """
    clf = linear_model.LinearRegression()
    clf.fit(x,y)
    coeff = []
    coeff.append(clf.intercept_)
    coeff += list(clf.coef_)
    return coeff



