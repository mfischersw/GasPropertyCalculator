# This file is part of GasPropertyCalculator.

"""
.. module:: generics
   :synopsis: Generic routines.

.. moduleauthor:: Michael Fischer
"""


# Python modules
import numpy
from PyQt5 import QtCore, QtGui, QtWidgets


def setupTableModelGen(parent, name1, name2):

    model = QtGui.QStandardItemModel(0, 2, parent)

    model.setHeaderData(0, QtCore.Qt.Horizontal, name1)
    model.setHeaderData(1, QtCore.Qt.Horizontal, name2)
    selectionModel = QtCore.QItemSelectionModel(model)

    return (model, selectionModel)


def setupTableViewGen(view, model, selectionModel):

    view.setModel(model)
    view.setSelectionModel(selectionModel)
    view.horizontalHeader().setResizeMode(QtWidgets.QHeaderView.Stretch)


def addTableRowGen(model, irow, x1, x2):

    model.insertRows(irow, 1, QtCore.QModelIndex())
    model.setData(model.index(irow, 0, QtCore.QModelIndex()), float(x1))
    model.setData(model.index(irow, 1, QtCore.QModelIndex()), float(x2))


def removeTableRowGen(model):

    nRows = model.rowCount(QtCore.QModelIndex())

    if (nRows > 1):
        model.removeRows(nRows-1, 1, QtCore.QModelIndex())
        x1 = model.data(model.index(nRows-2, 0, QtCore.QModelIndex()),
                        float(0.0))
        x2 = model.data(model.index(nRows-2, 1, QtCore.QModelIndex()),
                        float(0.0))
        model.removeRows(nRows-2, 1, QtCore.QModelIndex())
        addTableRowGen(model, nRows-2, x1, x2)


def clearTableRowsGen(model):

    nRows = model.rowCount(QtCore.QModelIndex())
    model.removeRows(0, nRows, QtCore.QModelIndex())
    addTableRowGen(model, 0, float(0.0), float(0.0))


def importBoundaryTxtGen(parent, model):

    fileName = QtWidgets.QFileDialog.getOpenFileName(parent, filter='*.txt')

    if fileName:

        try:
            data = numpy.loadtxt(fileName[0])
            (nrow, ncol) = data.shape

            clearTableRowsGen(model)

            for ii in range(nrow):
                addTableRowGen(model, ii,
                               float(data[ii, 0]), float(data[ii, 1]))

            removeTableRowGen(model)

        except OSError as e:
            print("OS ERROR: ", e.errno)


def getBoundaryGen(model):

    nRows = model.rowCount(QtCore.QModelIndex())
    boundData = numpy.zeros((nRows, 2))

    status = True

    xvalt = -1.0
    for ii in range(nRows):

        xval = model.data(model.index(ii, 0, QtCore.QModelIndex()), float(0.0))
        yval = model.data(model.index(ii, 1, QtCore.QModelIndex()), float(0.0))

        if (xval <= xvalt):  # x has to be strictly monotonic
            status = False

        boundData[ii, 0] = xval
        boundData[ii, 1] = yval
        xvalt = xval

    return (boundData, status)


def initDiag(graphicsView, xlabel, xunit):

    graphicsView.setMouseEnabled(x=False, y=False)
    graphicsView.plot()
    graphicsView.enableAutoRange()
    graphicsView.hideButtons()
    emptyDiag(graphicsView, xlabel, xunit)


def emptyDiag(graphicsView, xlabel, xunit):

    graphicsView.setLabel('bottom', xlabel, units=xunit)
    graphicsView.setXRange(0.0, 1.0)
    graphicsView.setYRange(0.0, 1.0)
    graphicsView.enableAutoRange()


def setupListModelGen(parent):

    model = QtGui.QStandardItemModel(parent)
    selectionModel = QtCore.QItemSelectionModel(model)

    return (model, selectionModel)


def setupListViewGen(view, model, selectionModel):

    view.setModel(model)
    view.setSelectionModel(selectionModel)


def addListModelItem(model, name, qcolor, withCheckable):

    item = QtGui.QStandardItem()
    item.setData(str(name), QtCore.Qt.DisplayRole)
    item.setData(qcolor, QtCore.Qt.DecorationRole)
    if (withCheckable):
        item.setCheckable(True)

    model.appendRow(item)


def findCheckedListModelItems(model):

    lChecked = []

    for row in range(model.rowCount()):
        item = model.item(row)
        if item.checkState() == QtCore.Qt.Checked:
            lChecked.append(row)

    return lChecked
