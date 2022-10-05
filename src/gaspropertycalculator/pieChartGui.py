# This file is part of GasPropertyCalculator.

"""
.. module:: pieChartGui
   :synopsis: Gas composition pie chart.

.. moduleauthor:: Michael Fischer
"""


# Python modules
from PyQt5 import QtGui, QtWidgets

from . import dataGui
from . import parameters


class GraphicsScenePie(QtWidgets.QGraphicsScene):

    def __init__(self, *args):

        QtWidgets.QGraphicsScene.__init__(self, *args)

        self.rectsize = 250
        self.anglefac = 16

        self.initPieChart()

    def addPieToChart(self, angle, delAngle, color):

        ellipse = QtWidgets.QGraphicsEllipseItem(
            0, 0, self.rectsize, self.rectsize)
        ellipse.setPos(0, 0)
        ellipse.setStartAngle(min(angle, 361)*self.anglefac)
        ellipse.setSpanAngle(min(delAngle, 361)*self.anglefac)
        ellipse.setBrush(QtGui.QColor(color))
        self.addItem(ellipse)

    def initPieChart(self):

        self.addPieToChart(0, 360, "white")

    def updatePieChart(self, gasComposition):

        self.clear()

        if (abs(sum(gasComposition.values())) <=
           parameters.EPSSUM_GAS):

            self.initPieChart()
            return

        angle = 0

        for ii in range(dataGui.nDataTabGasComponents):

            delAngle = round(360*gasComposition[ii]/100.0)
            self.addPieToChart(
                angle, delAngle, dataGui.dataTabGasComponents[ii][1])
            angle = angle + delAngle

        if (angle < 360):

            self.addPieToChart(angle, 360-angle, "white")
