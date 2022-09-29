# This file is part of GasPropertyCalculator.

"""
.. module:: calculation.util
   :synopsis: Utility functions.

.. moduleauthor:: Michael Fischer
"""


# Python modules
import numpy


def sumFractions_from_gasmixture(gasmixture):

    Nmix = len(gasmixture)

    psi = numpy.zeros(Nmix)

    counter = -1
    for name in gasmixture.keys():
        counter = counter + 1
        psi[counter] = gasmixture[name]

    return numpy.sum(psi)


def isSumFractionsOK(gasmixture):

    eps = 0.1
    sumPsi = sumFractions_from_gasmixture(gasmixture)
    return (abs(sumPsi-100.0) < eps)


def isPsiOK(gasmixture):

    Nmix = len(gasmixture)

    psi = numpy.zeros(Nmix)

    counter = -1
    for name in gasmixture.keys():
        counter = counter + 1
        psi[counter] = gasmixture[name]

        if (psi[counter] < 0.0 or psi[counter] > 100.0):
            return False

    return True
