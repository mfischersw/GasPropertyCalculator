# This file is part of GasPropertyCalculator.

"""
.. module:: calculation.eos_gerg.basic
   :synopsis: Basic gas properties calculation.

.. moduleauthor:: Michael Fischer
"""


# Python modules
import numpy


# Data
ind_molmass = 0
ind_normdensity = 1
ind_criticalT = 2   # [K]
ind_criticalp = 3   # [Pa]
ind_netcalorific = 4  # [kJ/kg]
ind_grosscalorific = 5  # [kJ/kg]

metaGenProp = {"molmass": ind_molmass,
               "normdensity": ind_normdensity,
               "criticalT": ind_criticalT,
               "criticalp": ind_criticalp,
               "netcalorific": ind_netcalorific,
               "grosscalorific": ind_grosscalorific,
               }

nGenProp = len(metaGenProp)

facsGenProp = {"molmass": 1.0,
               "normdensity": 1.0,
               "criticalT": 1.0,
               "criticalp": 1000.0,
               "netcalorific": 1000.0,
               "grosscalorific": 1000.0,
               }

facsGenProp = [1.0, 1.0, 1.0, 1000.0, 1000.0, 1000.0]

dataGenProp = {
    "methane": [16.043, 0.717, 190.58, 4604.0, 802.32, 890.36],
    "nitrogen": [28.0134, 1.250, 126.3, 3399.0, 0.0, 0.0],
    "carbon dioxide": [44.010, 1.977, 304.3, 7382.0, 0.0, 0.0],
    "ethane": [30.069, 1.355, 305.42, 4880.0, 1427.83, 1559.88],
    "propane": [44.096, 2.011, 369.82, 4250.0, 2044.01, 2220.03],
    "n-butane": [58.123, 2.701, 425.18, 3797.0, 2657.05, 2877.09],
    "isobutane": [58.123, 2.689, 408.14, 3648.0, 2648.68, 2868.72],
    "n-pentane": [72.150, 3.454, 469.7, 3369.0, 3272.10, 3536.15],
    "isopentane": [72.150, 3.427, 460.43, 3381.0, 3264.06, 3528.12],
    "n-hexane": [86.177, 4.204, 507.5, 3012.0, 3886.81, 4194.92],
    "n-heptane": [100.203, 4.888, 540.3, 2736.0, 4501.44, 4853.57],
    "n-octane": [114.230, 5.572, 568.83, 2487.0, 5115.57, 5511.71],
    "n-nonane": [128.257, 6.256, 594.64, 2290.0, 5730.87, 6170.98],
    "n-decane": [142.284, 6.941, 617.7, 2100.0, 6345.54, 6829.71],
    "hydrogen": [2.0158, 0.090, 33.3, 1298.0, 241.827, 285.840],
    "oxygen": [31.9988, 1.429, 154.8, 5081.0, 0.0, 0.0],
    "carbon monoxide": [28.010, 1.250, 133.0, 3499.0, 282.989, 282.989],
    "water": [18.0512, 0.833, 647.4, 22120.0, 0.0, 0.0],
    "hydrogen sulfide": [34.08, 1.536, 373.6, 9005.0, 518.52, 562.54],
    "helium": [4.0026, 0.178, 5.3, 229.0, 0.0, 0.0],
    "argon": [39.948, 1.784, 150.8, 4865.0, 0.0, 0.0],
    }


def getGenProp_from_gasmixture(gasmixture):
    """Extract and scale relevant general properties.

        Parameters
        ----------
        gasmixture : dict
            Gas mixture.

        Returns
        ----------
        psi : numpy.array
            Fractions.
        genProp : numpy.array
            Properties.
    """

    Nmix = len(gasmixture)

    psi = numpy.zeros(Nmix)
    genProp = numpy.zeros((Nmix, nGenProp))

    counter = -1
    for name in gasmixture.keys():
        counter = counter + 1
        psi[counter] = gasmixture[name]
        genProp[counter, :] = (numpy.array(dataGenProp[name]) *
                               numpy.array(facsGenProp))

    psi = psi*1.0/numpy.sum(psi)

    return (psi, genProp)


def mix_genProp(psi, genProp):
    """Mix general properties.

        Parameters
        ----------
        psi : numpy.array
            Fractions.
        genProp : numpy.array
            Properties.

        Returns
        ----------
        out : numpy.array
            Mixed Properties.
    """

    return numpy.sum(psi*numpy.transpose(genProp), axis=1)


def calc_basicPropsFromMixture(gasmixture):
    """Calculate basic properties.

        Parameters
        ----------
        gasmixture : dict
            Gas mixture.

        Returns
        ----------
        genPropMix : numpy.array
            Mixed Properties.
    """

    (psi, genProp) = getGenProp_from_gasmixture(gasmixture)

    genPropMix = mix_genProp(psi, genProp)

    # Correct values
    genPropMix[ind_netcalorific] = (genPropMix[ind_netcalorific] /
                                    genPropMix[ind_molmass])
    genPropMix[ind_grosscalorific] = (genPropMix[ind_grosscalorific] /
                                      genPropMix[ind_molmass])

    return genPropMix
