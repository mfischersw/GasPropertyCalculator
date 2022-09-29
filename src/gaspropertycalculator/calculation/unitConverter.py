# This file is part of GasPropertyCalculator.

"""
.. module:: calculation.unitConverter
   :synopsis: Unit conversion.

.. moduleauthor:: Michael Fischer
"""


# Python modules
from enum import IntEnum


class Observables(IntEnum):

    rho = 1
    T = 2
    p = 3
    h = 4
    u = 5
    s = 6
    cp = 7
    cv = 8
    R = 9
    w = 10
    mu = 11
    Mm = 12


class Units(IntEnum):

    kg_m3 = 1
    lb_ft3 = 2
    degC = 3
    degK = 4
    degF = 5
    bar = 6
    Pa = 7
    MPa = 8
    psi = 9
    kJ_kg = 10
    BTU_lb = 11
    kJ_kgK = 12
    BTU_lbdegF = 13
    m_s = 14
    km_h = 15
    mph = 16
    ft_s = 17
    degK_bar = 18
    degK_MPa = 19
    degF_psi = 20
    kg_kmol = 21
    lbm_lbmol = 22


def trafo_unit(value, iunitfrom, iunitto):

    if (iunitfrom == iunitto):
        return value

    elif (iunitfrom == Units.kg_m3):
        if (iunitto == Units.lb_ft3):
            return value*0.06243023738482223

    elif (iunitfrom == Units.lb_ft3):
        if (iunitto == Units.kg_m3):
            return value/0.06243023738482223

    elif (iunitfrom == Units.degC):
        if (iunitto == Units.degK):
            return value + 273.15
        elif (iunitto == Units.degF):
            return value*1.8 + 32.0

    elif (iunitfrom == Units.degK):
        if (iunitto == Units.degC):
            return value - 273.15
        elif (iunitto == Units.degF):
            return value*1.8-459.67

    elif (iunitfrom == Units.degF):
        if (iunitto == Units.degC):
            return (value - 32.0)/1.8
        elif (iunitto == Units.degK):
            return value/1.8 + 255.3722222222222

    elif (iunitfrom == Units.bar):
        if (iunitto == Units.Pa):
            return value*1.0e5
        elif (iunitto == Units.MPa):
            return value/10.0
        elif (iunitto == Units.psi):
            return value/0.06895

    elif (iunitfrom == Units.Pa):
        if (iunitto == Units.bar):
            return value/1.0e5
        elif (iunitto == Units.MPa):
            return value/1.0e6
        elif (iunitto == Units.psi):
            return value/6895.0

    elif (iunitfrom == Units.MPa):
        if (iunitto == Units.bar):
            return value*10.0
        elif (iunitto == Units.Pa):
            return value*1.0e6
        elif (iunitto == Units.psi):
            return value/0.006895

    elif (iunitfrom == Units.psi):
        if (iunitto == Units.bar):
            return value*0.06895
        elif (iunitto == Units.MPa):
            return value*0.006895
        elif (iunitto == Units.Pa):
            return value*6895.0

    elif (iunitfrom == Units.kJ_kg):
        if (iunitto == Units.BTU_lb):
            return value*0.42992261819021416

    elif (iunitfrom == Units.BTU_lb):
        if (iunitto == Units.kJ_kg):
            return value*2.3259999769483213

    elif (iunitfrom == Units.kJ_kgK):
        if (iunitto == Units.BTU_lbdegF):
            return value*0.2388458989945634

    elif (iunitfrom == Units.BTU_lbdegF):
        if (iunitto == Units.kJ_kgK):
            return value*4.186799958506978

    elif (iunitfrom == Units.m_s):
        if (iunitto == Units.km_h):
            return value*3.6
        elif (iunitto == Units.mph):
            return value/0.44704
        elif (iunitto == Units.ft_s):
            return value*3.2808

    elif (iunitfrom == Units.km_h):
        if (iunitto == Units.m_s):
            return value/3.6
        elif (iunitto == Units.mph):
            return value/1.609344
        elif (iunitto == Units.ft_s):
            return value*0.9113333333333333

    elif (iunitfrom == Units.mph):
        if (iunitto == Units.km_h):
            return value*1.60938
        elif (iunitto == Units.m_s):
            return value*0.44704
        elif (iunitto == Units.ft_s):
            return value*1.466648832

    elif (iunitfrom == Units.ft_s):
        if (iunitto == Units.km_h):
            return value*1.097293343087052
        elif (iunitto == Units.mph):
            return value/1.466648832
        elif (iunitto == Units.m_s):
            return value/3.2808

    elif (iunitfrom == Units.degK_bar):
        if (iunitto == Units.degK_MPa):
            return value*10.0
        elif (iunitto == Units.degF_psi):
            return value*0.12411

    elif (iunitfrom == Units.degK_MPa):
        if (iunitto == Units.degK_bar):
            return value/10.0
        elif (iunitto == Units.degF_psi):
            return value*0.012411

    elif (iunitfrom == Units.degF_psi):
        if (iunitto == Units.degK_bar):
            return value*8.057368463459834
        elif (iunitto == Units.degK_MPa):
            return value*80.57368463459834

    elif (iunitfrom == Units.kg_kmol):
        if (iunitto == Units.lbm_lbmol):
            return value

    elif (iunitfrom == Units.lbm_lbmol):
        if (iunitto == Units.kg_kmol):
            return value
