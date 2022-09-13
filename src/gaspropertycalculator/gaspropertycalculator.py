# This file is part of GasPropertyCalculator.

"""
.. module:: gaspropertycalculator
   :synopsis: Graphical user interace module.

.. moduleauthor:: Michael Fischer
"""


# Python modules
import numpy
import sys

import PyQt5
from PyQt5 import QtCore, QtWidgets
import pyqtgraph

from . import ui


def run():
    """GUI main loop.
    """

    # Plot background change
    pyqtgraph.setConfigOption('background', 'w')
    pyqtgraph.setConfigOption('foreground', 'k')

    # App
    app = QtWidgets.QApplication(sys.argv)

    mainwindow = GPCMainWindow()
    mainwindow.showMaximized()

    sys.exit(app.exec_())


class GPCMainWindow(QtWidgets.QMainWindow):
    """GUI: Main window.
    """

    def __init__(self, *args):

        QtWidgets.QMainWindow.__init__(self, *args)

        self.ui = ui.ui_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        # Activate stylesheet use for centralwidget
        self.ui.centralwidget.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.setWindowTitle("GasPropertyCalculator")

        # Signal-slot connects
        self.createConnects()


    def createConnects(self):
        """Setup signal-slot connections.
        """
        pass
