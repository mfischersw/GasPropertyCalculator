# This file is part of GasPropertyCalculator.

"""
.. module:: dataGui
   :synopsis: Graphical user interace data.

.. moduleauthor:: Michael Fischer
"""


# Python modules
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, parse
from xml.dom import minidom

from PyQt5 import QtCore, QtWidgets

from . import parameters


# Tab data: gas components
dataTabGasComponents = {0: ["methane", "#c91414"],
                        1: ["nitrogen", "#5311d9"],
                        2: ["carbon dioxide", "#2fe70b"],
                        3: ["ethane", "#d0d717"],
                        4: ["propane", "#ec0fc5"],
                        5: ["n-butane", "#036a5f"],
                        6: ["isobutane", "#8c87fb"],
                        7: ["n-pentane", "#d187fb"],
                        8: ["isopentane", "#8347b5"],
                        9: ["n-hexane", "#7b4f4f"],
                        10: ["n-heptane", "#616332"],
                        11: ["n-octane", "#6ab15c"],
                        12: ["n-nonane", "#8164bc"],
                        13: ["n-decane", "#c83b15"],
                        14: ["hydrogen", "#38e1cf"],
                        15: ["oxygen", "#f6ea87"],
                        16: ["carbon monoxide", "#0c04ac"],
                        17: ["water", "#534c4e"],
                        18: ["hydrogen sulfide", "#9f5091"],
                        19: ["helium", "#332f3a"],
                        20: ["argon", "#000"],
                        }

nDataTabGasComponents = len(dataTabGasComponents.keys())


def resetGasComponentsName(modelGas):

    for ii in range(nDataTabGasComponents):
        modelGas.setData(modelGas.index(ii, 0, QtCore.QModelIndex()),
                         dataTabGasComponents[ii][0])


def getGasComponents(modelGas):

    gasComposition = {}

    status = True
    idStatus = parameters.ID_STATUSGAS_OK

    for ii in range(nDataTabGasComponents):

        val = modelGas.data(
            modelGas.index(ii, 1, QtCore.QModelIndex()),
            float(0.0))

        gasComposition[ii] = val

        if (val < 0.0 or val > 100.0):
            status = False
            idStatus = parameters.ID_STATUSGAS_FRACTION_OUTRANGE

    if (status):
        if (abs(sum(gasComposition.values())-100.0) > parameters.EPSSUM_GAS):
            idStatus = parameters.ID_STATUSGAS_FRACTIONSUM_OUTRANGE

    return (gasComposition, idStatus)


def newGasComponents(modelGas):

    for ii in range(nDataTabGasComponents):
        modelGas.setData(
            modelGas.index(ii, 1, QtCore.QModelIndex()),
            float(0.0))


def readGasComponents(parent, modelGas):

    fileName = QtWidgets.QFileDialog.getOpenFileName(parent,
                                                     filter='*.xml')
    if fileName:
        try:
            tree = parse(fileName[0])
            root = tree.getroot()
            for child in root:
                ii = child.find('index').text
                molfrac = child.find('molfrac').text
                modelGas.setData(
                    modelGas.index(int(ii), 1, QtCore.QModelIndex()),
                    float(molfrac))
        except OSError as e:
            print("OS ERROR: ", e.errno)


def saveComponents(parent, modelGas):

    (gasComposition, idStatus) = getGasComponents(modelGas)

    if (idStatus == parameters.ID_STATUSGAS_OK):

        # Generate xml structure
        top = Element('gasmixture')
        comment = Comment('Generated from GasPipeFlow')
        top.append(comment)
        for ii in range(nDataTabGasComponents):
            gascomp = dataTabGasComponents[ii][0]
            child = SubElement(top, 'gascomp')
            subchild_i = SubElement(child, 'index')
            subchild_i.text = str(ii)
            subchild_gascomp = SubElement(child, 'name')
            subchild_gascomp.text = gascomp
            subchild_molfrac = SubElement(child, 'molfrac')
            subchild_molfrac.text = str(gasComposition[ii])

        rough_string = tostring(top, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        xmldump = reparsed.toprettyxml(indent="\t")

        fileName = QtWidgets.QFileDialog.getSaveFileName(parent,
                                                         filter='*.xml')
        if fileName:
            try:
                f = open(fileName[0], mode='w')
                f.writelines(xmldump)
                f.close()
            except OSError as e:
                print("OS ERROR: ", e.errno)
