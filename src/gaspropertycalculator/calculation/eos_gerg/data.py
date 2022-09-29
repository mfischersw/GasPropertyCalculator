# This file is part of GasPropertyCalculator.

"""
.. module:: calculation.eos_gerg.data
   :synopsis: This module contains the GERG 2008 EOS relevant data.

.. moduleauthor:: Michael Fischer
"""

# Data
dataTabGasComponents = {0: "methane",
                        1: "nitrogen",
                        2: "carbon dioxide",
                        3: "ethane",
                        4: "propane",
                        5: "n-butane",
                        6: "isobutane",
                        7: "n-pentane",
                        8: "isopentane",
                        9: "n-hexane",
                        10: "n-heptane",
                        11: "n-octane",
                        12: "n-nonane",
                        13: "n-decane",
                        14: "hydrogen",
                        15: "oxygen",
                        16: "carbon monoxide",
                        17: "water",
                        18: "hydrogen sulfide",
                        19: "helium",
                        20: "argon",
                        }

nDataTabGasComponents = len(dataTabGasComponents.keys())

normConditions = {"de0": [101325.0, 273.15],
                  "de15": [101325.0, 288.15],
                  "de20": [101325.0, 293.15],
                  }
