# This file is part of GasPropertyCalculator.

"""
.. module:: calculation.eos_gerg.calc
   :synopsis: This module contains the thermodynamic GERG 2008 EOS
              gas properties calculation (accessing external DLL).

.. moduleauthor:: Michael Fischer
"""


# Python modules
import ctypes
import numpy
import os
import sys

from . import data
from . import util

# Constants
DLL_NAME = 'LibGergCalc.dll'

# Access to installation of LibGergCalc via environment variable
(dirInstalled, isInstalled) = util.isLibInstalled()

# Alternative access to package folder
if (isInstalled is False):

    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    elif __file__:
        dirname = os.path.dirname(__file__)

    (dirInstalled, isInstalled) = util.isLibInFolder(dirname)

# Dll import
if (isInstalled):   # Dlls accessible

    print("Dlls accessible from: ", dirInstalled)

    # Dll path
    dll_path = os.path.join(dirInstalled, DLL_NAME)

    # Dll
    CalcDll = ctypes.cdll.LoadLibrary(dll_path)

    # Lib functions
    getm_Mm = CalcDll.__gerglib_MOD_get_mm
    getm_Rspez = CalcDll.__gerglib_MOD_get_rspez
    prepare_gerg = CalcDll.__gerglib_MOD_prepare_gerg
    calc_allpropdict = CalcDll.__gerglib_MOD_calc_allproparr
    calc_critpoint = CalcDll.__gerglib_MOD_calc_critpoint
    calcm_allPropArrGrid = CalcDll.__gerglib_MOD_calc_allproparrgrid

    # Data type interfaces
    getm_Mm.restype = ctypes.c_double
    getm_Mm.argtypes = []

    getm_Rspez.restype = ctypes.c_double
    getm_Rspez.argtypes = []

    prepare_gerg.restype = ctypes.c_void_p
    prepare_gerg.argtypes = [ctypes.c_void_p]

    calc_allpropdict.restype = ctypes.c_void_p
    calc_allpropdict.argtypes = [ctypes.c_double, ctypes.c_double,
                                 ctypes.c_void_p]

    calc_critpoint.restype = ctypes.c_void_p
    calc_critpoint.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                               ctypes.c_void_p]

    calcm_allPropArrGrid.restype = ctypes.c_void_p
    calcm_allPropArrGrid.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                     ctypes.c_int, ctypes.c_int,
                                     ctypes.c_void_p,  ctypes.c_void_p,
                                     ctypes.c_void_p,  ctypes.c_void_p,
                                     ctypes.c_void_p, ctypes.c_void_p,
                                     ctypes.c_void_p,  ctypes.c_void_p,
                                     ctypes.c_void_p,  ctypes.c_void_p]

# else:   # Dlls missing
#     raise ImportError('Dlls missing')


class Gas(object):
    """Gas class

       This class contains several methods for the calculation of gas
       properties.
       It takes a gas mixture given as dictionary as input.
    """

    def __init__(self, gascomp, normType):
        """Initialize gas object.

        Parameters
        ----------
        gascomp : dict
            Gas composition.
        normType : str
            Norm condition type.
        """

        # Input
        self.gascomp = gascomp
        self.normType = normType

        # Fill molar fractions vector
        self.fill_xvec(self.gascomp)
        self.set_gasmixture()

        # Norm state
        [PNORM, TNORM] = data.normConditions[self.normType]

        # Prepare GERG calculation
        if (isInstalled):
            prepare_gerg(self.xvec.ctypes.data_as(ctypes.c_void_p))

        # Calculate fundamental properties
        if (isInstalled):
            self.Mm = getm_Mm()
            self.Rspez = getm_Rspez()
        else:
            self.Mm = 0.0
            self.Rspez = 0.0

        # Calculate norm properties
        self.propDictout_N = self.calc_allPropDict(PNORM, TNORM)

        self.ZN = self.propDictout_N["Z"]
        self.rhoN = self.propDictout_N["rho"]
        self.sN = self.propDictout_N["s"]
        self.uN = self.propDictout_N["u"]
        self.cvN = self.propDictout_N["cv"]
        self.hN = self.propDictout_N["h"]
        self.cpN = self.propDictout_N["cp"]
        self.kappaN = self.propDictout_N["kappa"]
        self.wN = self.propDictout_N["w"]
        self.muN = self.propDictout_N["mu"]

    def fill_xvec(self, gascomp):
        """Fill molar fractions vector.

        Parameters
        ----------
        gascomp : dict
            Gas composition { ii : mol% ...}.
        """

        self.xvec = numpy.zeros(data.nDataTabGasComponents)

        for ind in gascomp.keys():
            self.xvec[ind] = gascomp[ind]/100.0

    def calc_critPoint(self):
        """Calculate critical point.

        Returns
        -------
        rhoc : float
            Critical density.
        Tc : float
            Critical temperature.
        pc : float
            Critical pressure.
        """

        if (isInstalled):
            rhoc = ctypes.c_double()
            Tc = ctypes.c_double()
            pc = ctypes.c_double()
            calc_critpoint(ctypes.byref(rhoc), ctypes.byref(Tc),
                           ctypes.byref(pc))

            return (rhoc.value, Tc.value, pc.value)
        else:
            return (0.0, 0.0, 0.0)

    def calc_allPropDict(self, p, T):
        """Calculate all state-dependent properties as dictionary.

        Parameters
        ----------
        p : float
            Pressure [Pa].
        T : float
            Temperature [K].

        Returns
        -------
        out : dict
            Gas properties.
        """

        y = numpy.zeros(10)

        if (isInstalled):
            calc_allpropdict(p, T, y.ctypes.data_as(ctypes.c_void_p))

        propDictout = {"Z": y[0],
                       "rho": y[1],
                       "s": y[2],
                       "u": y[3],
                       "cv": y[4],
                       "h": y[5],
                       "cp": y[6],
                       "kappa": y[7],
                       "w": y[8],
                       "mu": y[9],
                       }

        return propDictout

    def calc_allPropArrGrid(self, arr_p, arr_T):
        """Calculate all state-dependent properties as arrays.

        Parameters
        ----------
        p : numpy.array
            Pressure array [Pa].
        T : numpy.array
            Temperature array [K].

        Returns
        -------
        arr_Z : numpy.array
            Real gas factor.
        arr_rho : numpy.array
            Density.
        arr_s : numpy.array
            Entropy.
        arr_u : numpy.array
            Energy.
        arr_cv : numpy.array
            Isochoric heat capacity.
        arr_h : numpy.array
            Enthalpy.
        arr_cp : numpy.array
            Isobaric heat capacity.
        arr_kappa : numpy.array
            Isentropix exponent.
        arr_w : numpy.array
            Speed of sound.
        arr_mu : numpy.array
            Joule-Thomson-coefficient.
        """

        nT = len(arr_T)
        np = len(arr_p)

        arr_Z = numpy.zeros((nT, np))
        arr_rho = numpy.zeros((nT, np))
        arr_s = numpy.zeros((nT, np))
        arr_u = numpy.zeros((nT, np))
        arr_cv = numpy.zeros((nT, np))
        arr_h = numpy.zeros((nT, np))
        arr_cp = numpy.zeros((nT, np))
        arr_kappa = numpy.zeros((nT, np))
        arr_w = numpy.zeros((nT, np))
        arr_mu = numpy.zeros((nT, np))

        if (isInstalled):
            calcm_allPropArrGrid(arr_p.ctypes.data_as(ctypes.c_void_p),
                                 arr_T.ctypes.data_as(ctypes.c_void_p),
                                 np,
                                 nT,
                                 arr_Z.ctypes.data_as(ctypes.c_void_p),
                                 arr_rho.ctypes.data_as(ctypes.c_void_p),
                                 arr_s.ctypes.data_as(ctypes.c_void_p),
                                 arr_u.ctypes.data_as(ctypes.c_void_p),
                                 arr_cv.ctypes.data_as(ctypes.c_void_p),
                                 arr_h.ctypes.data_as(ctypes.c_void_p),
                                 arr_cp.ctypes.data_as(ctypes.c_void_p),
                                 arr_kappa.ctypes.data_as(ctypes.c_void_p),
                                 arr_w.ctypes.data_as(ctypes.c_void_p),
                                 arr_mu.ctypes.data_as(ctypes.c_void_p))

        return (arr_Z, arr_rho, arr_s, arr_u, arr_cv, arr_h, arr_cp,
                arr_kappa, arr_w, arr_mu)

    def set_gasmixture(self):
        """Set gas mixture."""

        self.gasmixture = {}

        for ii in self.gascomp.keys():
            name = data.dataTabGasComponents[ii]
            self.gasmixture[name] = self.gascomp[ii]

    def get_gascomp(self):

        return self.gascomp

    def get_gasmixture(self):

        return self.gasmixture

    def get_xvec(self):

        return self.xvec

    def get_Mm(self):

        return self.Mm

    def get_Rspec(self):

        return self.Rspez/1000.0

    def get_ZN(self):

        return self.ZN

    def get_rhoN(self):

        return self.rhoN
