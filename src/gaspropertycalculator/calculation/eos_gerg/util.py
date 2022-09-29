# This file is part of GasPropertyCalculator.

"""
.. module:: calculation.eos_gerg.util
   :synopsis: Access to external DLL via path variables or folder.

.. moduleauthor:: Michael Fischer
"""


# Python modules
import os

# Constants
DIRNAME_SEARCH = "LibGergCalc"
DLL_NAMES = ["LibGergCalc.dll"]


def isLibInstalled():

    os_env = dict(os.environ)
    path_list = os_env['PATH'].split(";")

    dirInstalled = ""
    for ppath in path_list:
        if (DIRNAME_SEARCH in ppath):
            dirInstalled = ppath

    if (dirInstalled != ""):

        try:
            files = os.listdir(dirInstalled)

            isInstalled = True
            for name in DLL_NAMES:
                if not (name in files):
                    isInstalled = False
        except OSError:
            isInstalled = False

    else:
        isInstalled = False

    return dirInstalled, isInstalled


def isLibInFolder(dirname):

    dirInstalled = dirname

    files = os.listdir(dirInstalled)

    isInstalled = True
    for name in DLL_NAMES:
        if not (name in files):
            isInstalled = False

    return dirInstalled, isInstalled
