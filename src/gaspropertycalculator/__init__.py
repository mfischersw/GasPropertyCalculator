# This file is part of GasPropertyCalculator.

from . import calculation
from . import ui

from . import dataGui
from . import gaspropertycalculator
from . import generics
from . import parameters
from . import pieChartGui

__all__ = ['calculation',
           'ui',
           'dataGui',
           'gaspropertycalculator',
           'generics',
           'parameters',
           'pieChartGui',
           ]


def main():
    """Entry point for the application script"""
    print("Starting GasPropertyCalculator from command line")
    gaspropertycalculator.run()
