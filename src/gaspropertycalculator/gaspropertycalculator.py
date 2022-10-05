# This file is part of GasPropertyCalculator.

"""
.. module:: gaspropertycalculator
   :synopsis: Graphical user interace module.

.. moduleauthor:: Michael Fischer
"""


# Python modules
import numpy
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph

from . import ui
from .calculation import unitConverter
from .calculation.eos_gerg import basic, calc, data
from . import dataGui
from . import generics
from . import parameters
from . import pieChartGui


unitsTarget = {
    "Mm": [unitConverter.Units.kg_kmol,
           unitConverter.Units.lbm_lbmol,
           'kg/kmol', 'lbm/lbmol'],
    "R": [unitConverter.Units.kJ_kgK,
          unitConverter.Units.BTU_lbdegF,
          'kJ/kg K', 'BTU/lb °F'],
    "Tc": [unitConverter.Units.degC,
           unitConverter.Units.degF,
           '°C', '°F'],
    "pc": [unitConverter.Units.bar,
           unitConverter.Units.psi,
           'bar', 'psi'],
    "Hi": [unitConverter.Units.kJ_kg,
           unitConverter.Units.BTU_lb,
           'kJ/kg', 'BTU/lb'],
    "Hs": [unitConverter.Units.kJ_kg,
           unitConverter.Units.BTU_lb,
           'kJ/kg', 'BTU/lb'],
    "rho": [unitConverter.Units.kg_m3,
            unitConverter.Units.lb_ft3,
            'kg/m³', 'lb/ft³'],
    "cp": [unitConverter.Units.kJ_kgK,
           unitConverter.Units.BTU_lbdegF,
           'kJ/kg K', 'BTU/lb °F'],
    "s": [unitConverter.Units.kJ_kgK,
          unitConverter.Units.BTU_lbdegF,
          'kJ/kg K', 'BTU/lb °F'],
    "h": [unitConverter.Units.kJ_kg,
          unitConverter.Units.BTU_lb,
          'kJ/kg', 'BTU/lb'],
    "cv": [unitConverter.Units.kJ_kgK,
           unitConverter.Units.BTU_lbdegF,
           'kJ/kg K', 'BTU/lb °F'],
    "w": [unitConverter.Units.m_s,
          unitConverter.Units.ft_s,
          'm/s', 'ft/s'],
    "mu": [unitConverter.Units.degK_bar,
           unitConverter.Units.degF_psi,
           'K/bar', '°F/bar']
    }


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

        # Setup model-view (gas)
        self.setupTableModelsSpec()  # model
        self.setupTableViewsSpec()  # view

        # Init model-view
        self.initTableModelsSpec()
        self.initGraphicsViewGas()

        # Model-dependent signal-slot connects
        self.createConnectsGas()

        # Clear all components
        self.clearComponents()

        # Metric system as starting point
        self.ui.radioButtonUnitMetric.setChecked(True)

        # De norm condition as starting point
        self.ui.radioButton_T0.setChecked(True)

        # Set units according to unit system
        self.setUnits()

        # Set dummy value for all properties
        self.initPropertiesVals()

        # Init gas apply button
        self.gasComposition = {}
        self.ui.buttonApplyGasComp.setEnabled(False)

        # Initialze diagram
        self.initGrid()
        self.initDiag()
        self.initGrid_hs()
        self.initDiag_hs()

        # Menu page at start
        self.showPageMenu()

    def createConnects(self):
        """Setup signal-slot connections.
        """

        self.ui.buttonComposition.clicked.connect(self.showPageComposition)
        self.ui.buttonProperties.clicked.connect(self.showPageProperties)
        self.ui.buttonDiagrams.clicked.connect(self.showPageDiagrams)
        self.ui.buttonSettings.clicked.connect(self.showPageSettings)
        self.ui.buttonInfo.clicked.connect(self.showPageInfo)
        self.ui.buttonBack.clicked.connect(self.showPageMenu)
        self.ui.buttonBackGasComp.clicked.connect(self.showPageMenu)
        self.ui.buttonApplyGasComp.clicked.connect(self.applyGasComposition)

        self.ui.buttonBasic.clicked.connect(self.showPageBasic)
        self.ui.buttonNorm.clicked.connect(self.showPageNorm)
        self.ui.buttonArbitrary.clicked.connect(self.showPageArbitrary)

        self.ui.buttonCalcArbitrary.clicked.connect(
            self.do_calcArbitraryProperties)

        self.ui.radioButtonUnitMetric.toggled.connect(self.setUnits)

        # ComboBoxes: unit conversion
        self.ui.comboBoxBasicUnit_Mm.currentIndexChanged.connect(
            self.trafoUnit_Mm)
        self.ui.comboBoxBasicUnit_R.currentIndexChanged.connect(
            self.trafoUnit_R)
        self.ui.comboBoxBasicUnit_Tc.currentIndexChanged.connect(
            self.trafoUnit_Tc)
        self.ui.comboBoxBasicUnit_pc.currentIndexChanged.connect(
            self.trafoUnit_pc)
        self.ui.comboBoxBasicUnit_Hi.currentIndexChanged.connect(
            self.trafoUnit_Hi)
        self.ui.comboBoxBasicUnit_Hs.currentIndexChanged.connect(
            self.trafoUnit_Hs)

        self.ui.comboBoxNormUnit_rho.currentIndexChanged.connect(
            self.trafoUnit_rhoN)
        self.ui.comboBoxNormUnit_cp.currentIndexChanged.connect(
            self.trafoUnit_cpN)
        self.ui.comboBoxNormUnit_cv.currentIndexChanged.connect(
            self.trafoUnit_cvN)
        self.ui.comboBoxNormUnit_w.currentIndexChanged.connect(
            self.trafoUnit_wN)
        self.ui.comboBoxNormUnit_mu.currentIndexChanged.connect(
            self.trafoUnit_muN)

        self.ui.comboBoxArbitraryUnit_rho.currentIndexChanged.connect(
            self.trafoUnit_rho)
        self.ui.comboBoxArbitraryUnit_cp.currentIndexChanged.connect(
            self.trafoUnit_cp)
        self.ui.comboBoxArbitraryUnit_cv.currentIndexChanged.connect(
            self.trafoUnit_cv)
        self.ui.comboBoxArbitraryUnit_w.currentIndexChanged.connect(
            self.trafoUnit_w)
        self.ui.comboBoxArbitraryUnit_mu.currentIndexChanged.connect(
            self.trafoUnit_mu)

        # Diagrams
        self.ui.buttonDiagProps.clicked.connect(self.showPageDiagProps)
        self.ui.buttonUpdateDiagram.clicked.connect(self.do_updateDiagram)

        self.ui.buttonDiag_hs.clicked.connect(self.showPageDiag_hs)
        self.ui.buttonUpdateDiagram_hs.clicked.connect(
            self.do_updateDiagram_hs)

        self.ui.comboBoxDiagramsProps.currentIndexChanged.connect(
            self.show_plot_arr)

    def createConnectsGas(self):
        """Gui: Signal-slot connections for gas composition"""

        # Pie chart signal-slot
        self.modelGas.itemChanged.connect(self.updateGas)

        # File operations
        self.ui.buttonNewGas.clicked.connect(self.newGasComponents)
        self.ui.buttonLoadGas.clicked.connect(self.readGasComponents)
        self.ui.buttonSaveGas.clicked.connect(self.saveComponents)

    @QtCore.pyqtSlot()
    def showPageComposition(self):

        ind = self.ui.stackedWidgetMain.indexOf(self.ui.pageComposition)
        indH = self.ui.stackedWidgetHead.indexOf(self.ui.pageHeadComposition)
        indB = self.ui.stackedWidgetBottom.indexOf(self.ui.pageBottomGasComp)
        self.ui.stackedWidgetMain.setCurrentIndex(ind)
        self.ui.stackedWidgetHead.setCurrentIndex(indH)
        self.ui.stackedWidgetBottom.setCurrentIndex(indB)

        if (self.gasobj is None):
            self.clearComponents()

    @QtCore.pyqtSlot()
    def showPageProperties(self):

        ind = self.ui.stackedWidgetMain.indexOf(self.ui.pageProperties)
        self.ui.stackedWidgetMain.setCurrentIndex(ind)

        self.showPageBasic()

    @QtCore.pyqtSlot()
    def showPageDiagrams(self):

        ind = self.ui.stackedWidgetMain.indexOf(self.ui.pageDiagrams)
        self.ui.stackedWidgetMain.setCurrentIndex(ind)

        self.showPageDiagProps()

    @QtCore.pyqtSlot()
    def showPageDiagProps(self):

        ind = self.ui.stackedWidgetDiag.indexOf(self.ui.pageDiagProps)
        indH = self.ui.stackedWidgetHead.indexOf(self.ui.pageHeadDiagProps)
        indB = self.ui.stackedWidgetBottom.indexOf(self.ui.pageBottomBack)
        self.ui.stackedWidgetDiag.setCurrentIndex(ind)
        self.ui.stackedWidgetHead.setCurrentIndex(indH)
        self.ui.stackedWidgetBottom.setCurrentIndex(indB)

        self.uncheckDiagramsButtons()
        self.ui.buttonDiagProps.setChecked(True)

        if (self.gasobj is None):
            self.pw.clear()
            self.emptyDiag()
            self.clearLegend()

    @QtCore.pyqtSlot()
    def showPageDiag_hs(self):

        ind = self.ui.stackedWidgetDiag.indexOf(self.ui.pageDiag_hs)
        indH = self.ui.stackedWidgetHead.indexOf(self.ui.pageHeadDiag_hs)
        indB = self.ui.stackedWidgetBottom.indexOf(self.ui.pageBottomBack)
        self.ui.stackedWidgetDiag.setCurrentIndex(ind)
        self.ui.stackedWidgetHead.setCurrentIndex(indH)
        self.ui.stackedWidgetBottom.setCurrentIndex(indB)

        self.uncheckDiagramsButtons()
        self.ui.buttonDiag_hs.setChecked(True)

        if (self.gasobj is None):
            self.pw_hs.clear()
            self.emptyDiag_hs()
            self.clearLegend_hs()

    def uncheckDiagramsButtons(self):
        """Gui: Uncheck all diagrams buttons"""

        self.ui.buttonDiagProps.setChecked(False)
        self.ui.buttonDiag_hs.setChecked(False)

    @QtCore.pyqtSlot()
    def showPageSettings(self):

        ind = self.ui.stackedWidgetMain.indexOf(self.ui.pageSettings)
        indH = self.ui.stackedWidgetHead.indexOf(self.ui.pageHeadSettings)
        indB = self.ui.stackedWidgetBottom.indexOf(self.ui.pageBottomBack)
        self.ui.stackedWidgetMain.setCurrentIndex(ind)
        self.ui.stackedWidgetHead.setCurrentIndex(indH)
        self.ui.stackedWidgetBottom.setCurrentIndex(indB)

    @QtCore.pyqtSlot()
    def showPageInfo(self):

        ind = self.ui.stackedWidgetMain.indexOf(self.ui.pageInfo)
        indH = self.ui.stackedWidgetHead.indexOf(self.ui.pageHeadInfo)
        indB = self.ui.stackedWidgetBottom.indexOf(self.ui.pageBottomBack)
        self.ui.stackedWidgetMain.setCurrentIndex(ind)
        self.ui.stackedWidgetHead.setCurrentIndex(indH)
        self.ui.stackedWidgetBottom.setCurrentIndex(indB)

    @QtCore.pyqtSlot()
    def showPageMenu(self):

        ind = self.ui.stackedWidgetMain.indexOf(self.ui.pageMenu)
        indH = self.ui.stackedWidgetHead.indexOf(self.ui.pageHeadMenu)
        indB = self.ui.stackedWidgetBottom.indexOf(self.ui.pageBottomMenu)
        self.ui.stackedWidgetMain.setCurrentIndex(ind)
        self.ui.stackedWidgetHead.setCurrentIndex(indH)
        self.ui.stackedWidgetBottom.setCurrentIndex(indB)

    @QtCore.pyqtSlot()
    def showPageBasic(self):

        ind = self.ui.stackedWidgetProperties.indexOf(self.ui.pageBasic)
        indH = self.ui.stackedWidgetHead.indexOf(self.ui.pageHeadBasic)
        indB = self.ui.stackedWidgetBottom.indexOf(self.ui.pageBottomBack)
        self.ui.stackedWidgetProperties.setCurrentIndex(ind)
        self.ui.stackedWidgetHead.setCurrentIndex(indH)
        self.ui.stackedWidgetBottom.setCurrentIndex(indB)

        self.uncheckPropertiesButtons()
        self.ui.buttonBasic.setChecked(True)

        if not (self.gasobj is None):

            genPropMix = basic.calc_basicPropsFromMixture(
                self.gasobj.get_gasmixture())

            self.Mm = self.gasobj.get_Mm()
            self.R = self.gasobj.get_Rspec()
            self.Tc = genPropMix[basic.ind_criticalT]
            self.pc = genPropMix[basic.ind_criticalp]
            self.Hi = genPropMix[basic.ind_netcalorific]
            self.Hs = genPropMix[basic.ind_grosscalorific]

        else:

            self.setBasicTrivial()

        self.trafoUnit_Mm()
        self.trafoUnit_R()
        self.trafoUnit_Tc()
        self.trafoUnit_pc()
        self.trafoUnit_Hi()
        self.trafoUnit_Hs()

    @QtCore.pyqtSlot()
    def showPageNorm(self):

        ind = self.ui.stackedWidgetProperties.indexOf(self.ui.pageNorm)
        indH = self.ui.stackedWidgetHead.indexOf(self.ui.pageHeadNorm)
        indB = self.ui.stackedWidgetBottom.indexOf(self.ui.pageBottomBack)
        self.ui.stackedWidgetProperties.setCurrentIndex(ind)
        self.ui.stackedWidgetHead.setCurrentIndex(indH)
        self.ui.stackedWidgetBottom.setCurrentIndex(indB)

        self.uncheckPropertiesButtons()
        self.ui.buttonNorm.setChecked(True)

        self.set_normCondLabel()

        if not (self.gasobj is None):

            (pN, TN) = self.determine_normCond()

            propDictN = self.gasobj.calc_allPropDict(pN, TN)

            self.rhoN = propDictN["rho"]
            self.ZN = propDictN["Z"]
            self.KN = 1.0
            self.cpN = propDictN["cp"]
            self.cvN = propDictN["cv"]
            self.wN = propDictN["w"]
            self.muN = propDictN["mu"]*1.0e6
            self.kappaN = propDictN["kappa"]

        else:

            self.setNormTrivial()

        self.trafoUnit_rhoN()
        self.ui.labelNormVal_Z.setText(str("{0:.4f}".format(self.ZN)))
        self.ui.labelNormVal_K.setText(str("{0:.4f}".format(self.KN)))
        self.trafoUnit_cpN()
        self.trafoUnit_cvN()
        self.trafoUnit_wN()
        self.trafoUnit_muN()
        self.ui.labelNormVal_k.setText(str("{0:.4f}".format(self.kappaN)))

    @QtCore.pyqtSlot()
    def showPageArbitrary(self):

        ind = self.ui.stackedWidgetProperties.indexOf(self.ui.pageArbitrary)
        indH = self.ui.stackedWidgetHead.indexOf(self.ui.pageHeadArbitrary)
        indB = self.ui.stackedWidgetBottom.indexOf(self.ui.pageBottomBack)
        self.ui.stackedWidgetProperties.setCurrentIndex(ind)
        self.ui.stackedWidgetHead.setCurrentIndex(indH)
        self.ui.stackedWidgetBottom.setCurrentIndex(indB)

        self.uncheckPropertiesButtons()
        self.ui.buttonArbitrary.setChecked(True)

        if (self.gasobj is None):

            self.setArbitraryTrivial()

            self.trafoUnit_rho()
            self.ui.labelArbitraryVal_Z.setText(str("{0:.4f}".format(self.Z)))
            self.ui.labelArbitraryVal_K.setText(str("{0:.4f}".format(self.K)))
            self.trafoUnit_cp()
            self.trafoUnit_cv()
            self.trafoUnit_w()
            self.trafoUnit_mu()
            self.ui.labelArbitraryVal_k.setText(
                str("{0:.4f}".format(self.kappa)))

    def uncheckPropertiesButtons(self):
        """Gui: Uncheck all properties buttons"""

        self.ui.buttonBasic.setChecked(False)
        self.ui.buttonNorm.setChecked(False)
        self.ui.buttonArbitrary.setChecked(False)

    @QtCore.pyqtSlot()
    def do_calcArbitraryProperties(self):

        if not (self.gasobj is None):

            try:
                p_in = float(self.ui.lineEditArbitraryVal_p.text())
                T_in = float(self.ui.lineEditArbitraryVal_T.text())

                (induni, induniStr) = self.determine_induni()

                unit_p = unitsTarget["pc"][induni]
                unit_T = unitsTarget["Tc"][induni]

                p = unitConverter.trafo_unit(p_in, unit_p,
                                             unitConverter.Units.Pa)
                T = unitConverter.trafo_unit(T_in, unit_T,
                                             unitConverter.Units.degK)

                # Critical point
                (rhocrit, Tcrit, pcrit) = self.gasobj.calc_critPoint()

                isGood_p = (p > 0.0)
                isGood_T = (T > Tcrit)

            except Exception as e:
                print(e)
                QtWidgets.QMessageBox.warning(
                    self, "State Input Error",
                    "The values for pressure and temperature \
                    have to be numbers. Please correct your input.")
                return

            if (not isGood_p):
                if (isGood_T):
                    QtWidgets.QMessageBox.warning(
                        self, "State Input Error",
                        "The value for pressure has to be larger than 0. \
                        Please correct your input.")
                    return
                else:
                    QtWidgets.QMessageBox.warning(
                        self, "State Input Error",
                        "The value for pressure has to be larger than 0 and \
                        the value for temperature larger than the critical \
                        temperature. Please correct your input.")
                    return
            else:
                if (not isGood_T):
                    QtWidgets.QMessageBox.warning(
                        self, "State Input Error",
                        "The value for temperature has to be larger than \
                        the critical temperature. Please correct your input.")
                    return

            try:
                (pN, TN) = self.determine_normCond()

                propDictN = self.gasobj.calc_allPropDict(pN, TN)

                propDict = self.gasobj.calc_allPropDict(p, T)

            except Exception as e:
                print(e)
                self.setArbitraryTrivial()
                return

            self.rho = propDict["rho"]
            self.Z = propDict["Z"]
            self.K = self.Z/propDictN["Z"]
            self.cp = propDict["cp"]
            self.cv = propDict["cv"]
            self.w = propDict["w"]
            self.mu = propDict["mu"]*1.0e6
            self.kappa = propDict["kappa"]

        else:

            self.setArbitraryTrivial()

        self.trafoUnit_rho()
        self.ui.labelArbitraryVal_Z.setText(str("{0:.4f}".format(self.Z)))
        self.ui.labelArbitraryVal_K.setText(str("{0:.4f}".format(self.K)))
        self.trafoUnit_cp()
        self.trafoUnit_cv()
        self.trafoUnit_w()
        self.trafoUnit_mu()
        self.ui.labelArbitraryVal_k.setText(str("{0:.4f}".format(self.kappa)))

    @QtCore.pyqtSlot()
    def setUnits(self):

        # Input units
        (induni, induniStr) = self.determine_induni()

        # unit_rho_Str = unitsTarget["rho"][induniStr]
        unit_p_Str = unitsTarget["pc"][induniStr]
        unit_T_Str = unitsTarget["Tc"][induniStr]

        self.ui.labelArbitraryUnit_p.setText(str(unit_p_Str))
        self.ui.labelArbitraryUnit_T.setText(str(unit_T_Str))

        # Norm state definition
        unit_p = unitsTarget["pc"][induni]
        unit_T = unitsTarget["Tc"][induni]

        pNVal_T0 = unitConverter.trafo_unit(
            data.normConditions["de0"][0],
            unitConverter.Units.Pa, unit_p)
        TNVal_T0 = unitConverter.trafo_unit(
            data.normConditions["de0"][1],
            unitConverter.Units.degK, unit_T)
        pNVal_T15 = unitConverter.trafo_unit(
            data.normConditions["de15"][0],
            unitConverter.Units.Pa, unit_p)
        TNVal_T15 = unitConverter.trafo_unit(
            data.normConditions["de15"][1],
            unitConverter.Units.degK, unit_T)
        pNVal_T20 = unitConverter.trafo_unit(
            data.normConditions["de20"][0],
            unitConverter.Units.Pa, unit_p)
        TNVal_T20 = unitConverter.trafo_unit(
            data.normConditions["de20"][1],
            unitConverter.Units.degK, unit_T)

        self.ui.radioButton_T0.setText(
            "T = " + str("{0:.2f}".format(TNVal_T0)) + " " +
            unit_T_Str + ", \t p = " +
            str("{0:.3f}".format(pNVal_T0)) + " " + unit_p_Str)
        self.ui.radioButton_T15.setText(
            "T = " + str("{0:.2f}".format(TNVal_T15)) + " " +
            unit_T_Str + ", \t p = " +
            str("{0:.3f}".format(pNVal_T15)) + " " + unit_p_Str)
        self.ui.radioButton_T20.setText(
            "T = " + str("{0:.2f}".format(TNVal_T20)) + " " +
            unit_T_Str + ", \t p = " +
            str("{0:.3f}".format(pNVal_T20)) + " " + unit_p_Str)

        # Output units
        self.ui.comboBoxBasicUnit_Mm.setCurrentIndex(induni)
        self.ui.comboBoxBasicUnit_R.setCurrentIndex(induni)
        self.ui.comboBoxBasicUnit_Tc.setCurrentIndex(induni)
        self.ui.comboBoxBasicUnit_pc.setCurrentIndex(induni)
        self.ui.comboBoxBasicUnit_Hi.setCurrentIndex(induni)
        self.ui.comboBoxBasicUnit_Hs.setCurrentIndex(induni)

        self.ui.comboBoxNormUnit_rho.setCurrentIndex(induni)
        self.ui.comboBoxNormUnit_cp.setCurrentIndex(induni)
        self.ui.comboBoxNormUnit_cv.setCurrentIndex(induni)
        self.ui.comboBoxNormUnit_w.setCurrentIndex(induni)
        self.ui.comboBoxNormUnit_mu.setCurrentIndex(induni)

        self.ui.comboBoxArbitraryUnit_rho.setCurrentIndex(induni)
        self.ui.comboBoxArbitraryUnit_cp.setCurrentIndex(induni)
        self.ui.comboBoxArbitraryUnit_cv.setCurrentIndex(induni)
        self.ui.comboBoxArbitraryUnit_w.setCurrentIndex(induni)
        self.ui.comboBoxArbitraryUnit_mu.setCurrentIndex(induni)

        # Diagram units
        self.ui.labelDiagramUnit_minp.setText(str(unit_p_Str))
        self.ui.labelDiagramUnit_maxp.setText(str(unit_p_Str))
        self.ui.labelDiagramUnit_minT.setText(str(unit_T_Str))
        self.ui.labelDiagramUnit_maxT.setText(str(unit_T_Str))

        self.ui.labelDiagramUnit_minp_hs.setText(str(unit_p_Str))
        self.ui.labelDiagramUnit_maxp_hs.setText(str(unit_p_Str))
        self.ui.labelDiagramUnit_minT_hs.setText(str(unit_T_Str))
        self.ui.labelDiagramUnit_maxT_hs.setText(str(unit_T_Str))

    @QtCore.pyqtSlot()
    def clearComponents(self):

        self.gasobj = None

    def initPropertiesVals(self):

        self.setBasicTrivial()
        self.setNormTrivial()
        self.setArbitraryTrivial()

    def trafoUnit_Mm(self):
        ind = self.ui.comboBoxBasicUnit_Mm.currentIndex()
        val = unitConverter.trafo_unit(
            self.Mm, unitConverter.Units.kg_kmol,
            unitsTarget["Mm"][ind])
        self.ui.labelBasicVal_Mm.setText(str("{0:.4f}".format(val)))

    def trafoUnit_R(self):
        ind = self.ui.comboBoxBasicUnit_R.currentIndex()
        val = unitConverter.trafo_unit(
            self.R, unitConverter.Units.kJ_kgK,
            unitsTarget["R"][ind])
        self.ui.labelBasicVal_R.setText(str("{0:.4f}".format(val)))

    def trafoUnit_Tc(self):
        ind = self.ui.comboBoxBasicUnit_Tc.currentIndex()
        val = unitConverter.trafo_unit(
            self.Tc, unitConverter.Units.degK,
            unitsTarget["Tc"][ind])
        self.ui.labelBasicVal_Tc.setText(str("{0:.4f}".format(val)))

    def trafoUnit_pc(self):
        ind = self.ui.comboBoxBasicUnit_pc.currentIndex()
        val = unitConverter.trafo_unit(
            self.pc, unitConverter.Units.Pa,
            unitsTarget["pc"][ind])
        self.ui.labelBasicVal_pc.setText(str("{0:.4f}".format(val)))

    def trafoUnit_Hi(self):
        ind = self.ui.comboBoxBasicUnit_Hi.currentIndex()
        val = unitConverter.trafo_unit(
            self.Hi, unitConverter.Units.kJ_kg,
            unitsTarget["Hi"][ind])
        self.ui.labelBasicVal_Hi.setText(str("{0:.4f}".format(val)))

    def trafoUnit_Hs(self):
        ind = self.ui.comboBoxBasicUnit_Hs.currentIndex()
        val = unitConverter.trafo_unit(
            self.Hs, unitConverter.Units.kJ_kg,
            unitsTarget["Hs"][ind])
        self.ui.labelBasicVal_Hs.setText(str("{0:.4f}".format(val)))

    def trafoUnit_rhoN(self):
        ind = self.ui.comboBoxNormUnit_rho.currentIndex()
        val = unitConverter.trafo_unit(
            self.rhoN, unitConverter.Units.kg_m3,
            unitsTarget["rho"][ind])
        self.ui.labelNormVal_rho.setText(str("{0:.4f}".format(val)))

    def trafoUnit_cpN(self):
        ind = self.ui.comboBoxNormUnit_cp.currentIndex()
        val = unitConverter.trafo_unit(
            self.cpN, unitConverter.Units.kJ_kgK,
            unitsTarget["cp"][ind])
        self.ui.labelNormVal_cp.setText(str("{0:.4f}".format(val)))

    def trafoUnit_cvN(self):
        ind = self.ui.comboBoxNormUnit_cv.currentIndex()
        val = unitConverter.trafo_unit(
            self.cvN, unitConverter.Units.kJ_kgK,
            unitsTarget["cv"][ind])
        self.ui.labelNormVal_cv.setText(str("{0:.4f}".format(val)))

    def trafoUnit_wN(self):
        ind = self.ui.comboBoxNormUnit_w.currentIndex()
        val = unitConverter.trafo_unit(
            self.wN, unitConverter.Units.m_s,
            unitsTarget["w"][ind])
        self.ui.labelNormVal_w.setText(str("{0:.4f}".format(val)))

    def trafoUnit_muN(self):
        ind = self.ui.comboBoxNormUnit_mu.currentIndex()
        val = unitConverter.trafo_unit(
            self.muN, unitConverter.Units.degK_bar,
            unitsTarget["mu"][ind])
        self.ui.labelNormVal_mu.setText(str("{0:.4f}".format(val)))

    def trafoUnit_rho(self):
        ind = self.ui.comboBoxArbitraryUnit_rho.currentIndex()
        val = unitConverter.trafo_unit(
            self.rho, unitConverter.Units.kg_m3,
            unitsTarget["rho"][ind])
        self.ui.labelArbitraryVal_rho.setText(str("{0:.4f}".format(val)))

    def trafoUnit_cp(self):
        ind = self.ui.comboBoxArbitraryUnit_cp.currentIndex()
        val = unitConverter.trafo_unit(
            self.cp, unitConverter.Units.kJ_kgK,
            unitsTarget["cp"][ind])
        self.ui.labelArbitraryVal_cp.setText(str("{0:.4f}".format(val)))

    def trafoUnit_cv(self):
        ind = self.ui.comboBoxArbitraryUnit_cv.currentIndex()
        val = unitConverter.trafo_unit(
            self.cv, unitConverter.Units.kJ_kgK,
            unitsTarget["cv"][ind])
        self.ui.labelArbitraryVal_cv.setText(str("{0:.4f}".format(val)))

    def trafoUnit_w(self):
        ind = self.ui.comboBoxArbitraryUnit_w.currentIndex()
        val = unitConverter.trafo_unit(
            self.w, unitConverter.Units.m_s,
            unitsTarget["w"][ind])
        self.ui.labelArbitraryVal_w.setText(str("{0:.4f}".format(val)))

    def trafoUnit_mu(self):
        ind = self.ui.comboBoxArbitraryUnit_mu.currentIndex()
        val = unitConverter.trafo_unit(
            self.mu, unitConverter.Units.degK_bar,
            unitsTarget["mu"][ind])
        self.ui.labelArbitraryVal_mu.setText(str("{0:.4f}".format(val)))

    def setMinMaxValsForAxes(self):

        self.minp = 0.0
        self.maxp = 200.0
        self.minT = -50.0
        self.maxT = 100.0

        self.ui.doubleSpinBox_minp.setValue(self.minp)
        self.ui.doubleSpinBox_maxp.setValue(self.maxp)
        self.ui.doubleSpinBox_minT.setValue(self.minT)
        self.ui.doubleSpinBox_maxT.setValue(self.maxT)

    def setMinMaxValsForAxes_hs(self):

        self.minp_hs = 0.0
        self.maxp_hs = 200.0
        self.minT_hs = -50.0
        self.maxT_hs = 100.0

        self.ui.doubleSpinBox_minp_hs.setValue(self.minp_hs)
        self.ui.doubleSpinBox_maxp_hs.setValue(self.maxp_hs)
        self.ui.doubleSpinBox_minT_hs.setValue(self.minT_hs)
        self.ui.doubleSpinBox_maxT_hs.setValue(self.maxT_hs)

    @QtCore.pyqtSlot()
    def do_updateDiagram(self):

        if (self.gasobj is None):
            self.emptyDiag()
            return

        minp_in = self.ui.doubleSpinBox_minp.value()
        maxp_in = self.ui.doubleSpinBox_maxp.value()
        minT_in = self.ui.doubleSpinBox_minT.value()
        maxT_in = self.ui.doubleSpinBox_maxT.value()

        # Unit trafo of limits
        (induni, induniStr) = self.determine_induni()

        unit_p = unitsTarget["pc"][induni]
        # unit_p_Str = unitsTarget["pc"][induniStr]
        unit_T = unitsTarget["Tc"][induni]
        # unit_T_Str = unitsTarget["Tc"][induniStr]

        minp = unitConverter.trafo_unit(minp_in, unit_p,
                                        unitConverter.Units.Pa)
        maxp = unitConverter.trafo_unit(maxp_in, unit_p,
                                        unitConverter.Units.Pa)
        minT = unitConverter.trafo_unit(minT_in, unit_T,
                                        unitConverter.Units.degK)
        maxT = unitConverter.trafo_unit(maxT_in, unit_T,
                                        unitConverter.Units.degK)

        # Critical point
        (rhocrit, Tcrit, pcrit) = self.gasobj.calc_critPoint()

        isGood_p = (minp >= 0.0) and (maxp > minp)
        isGood_T = (minT > Tcrit) and (maxT > minT)

        # Checking
        if (not isGood_p):
            if (not isGood_T):
                QtWidgets.QMessageBox.warning(
                    self, "Axis Setting Error",
                    "Both intervals have to be ordered and p >= 0, T >= Tc. \
                    Please correct your input.")
                return
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Axis Setting Error",
                    "Pressure interval has to be ordered and p >= 0. \
                    Please correct your input.")
                return
        else:
            if (not isGood_T):
                QtWidgets.QMessageBox.warning(
                    self, "Axis Setting Error",
                    "Temperature interval has to be ordered and T >= Tc. \
                    Please correct your input.")
                return

        # Arrays
        self.T_arr = numpy.linspace(minT, maxT, self.NT)
        p_arrh = numpy.linspace(minp, maxp, self.Ngrid+1)
        self.p_arr = p_arrh[1:]

        # Clear plot
        self.pw.plotItem.clear()

        # Calculation in target units
        for ii in range(self.NT):
            TT = self.T_arr[ii]

            for jj in range(self.Ngrid):

                pp = self.p_arr[jj]

                propDict = self.gasobj.calc_allPropDict(pp, TT)

                self.rho_arr[ii, jj] = propDict["rho"]
                self.Z_arr[ii, jj] = propDict["Z"]
                self.K_arr[ii, jj] = self.Z_arr[ii, jj]/self.gasobj.get_ZN()
                self.cp_arr[ii, jj] = propDict["cp"]
                self.cv_arr[ii, jj] = propDict["cv"]
                self.w_arr[ii, jj] = propDict["w"]
                self.mu_arr[ii, jj] = propDict["mu"]
                self.kappa_arr[ii, jj] = propDict["kappa"]

        # Plot
        self.show_plot_arr()

    @QtCore.pyqtSlot()
    def do_updateDiagram_hs(self):

        if (self.gasobj is None):
            self.emptyDiag_hs()
            return

        minp_in = self.ui.doubleSpinBox_minp_hs.value()
        maxp_in = self.ui.doubleSpinBox_maxp_hs.value()
        minT_in = self.ui.doubleSpinBox_minT_hs.value()
        maxT_in = self.ui.doubleSpinBox_maxT_hs.value()

        # Unit trafo of limits
        (induni, induniStr) = self.determine_induni()

        unit_p = unitsTarget["pc"][induni]
        # unit_p_Str = unitsTarget["pc"][induniStr]
        unit_T = unitsTarget["Tc"][induni]
        # unit_T_Str = unitsTarget["Tc"][induniStr]

        minp = unitConverter.trafo_unit(minp_in, unit_p,
                                        unitConverter.Units.Pa)
        maxp = unitConverter.trafo_unit(maxp_in, unit_p,
                                        unitConverter.Units.Pa)
        minT = unitConverter.trafo_unit(minT_in, unit_T,
                                        unitConverter.Units.degK)
        maxT = unitConverter.trafo_unit(maxT_in, unit_T,
                                        unitConverter.Units.degK)

        # Critical point
        (rhocrit, Tcrit, pcrit) = self.gasobj.calc_critPoint()

        isGood_p = (minp >= 0.0) and (maxp > minp)
        isGood_T = (minT > Tcrit) and (maxT > minT)

        # Checking
        if (not isGood_p):
            if (not isGood_T):
                QtWidgets.QMessageBox.warning(
                    self, "Axis Setting Error",
                    "Both intervals have to be ordered and p >= 0, T >= Tc. \
                    Please correct your input.")
                return
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Axis Setting Error",
                    "Pressure interval has to be ordered and p >= 0. \
                    Please correct your input.")
                return
        else:
            if (not isGood_T):
                QtWidgets.QMessageBox.warning(
                    self, "Axis Setting Error",
                    "Temperature interval has to be ordered and T >= Tc. \
                    Please correct your input.")
                return

        # Arrays
        self.T_arr_hs = numpy.linspace(minT, maxT, self.NT_hs)
        p_arrh = numpy.linspace(minp, maxp, self.Ngrid_hs+1)
        self.p_arr_hs = p_arrh[1:]

        # Clear plot
        self.pw_hs.plotItem.clear()

        # Calculation in target units
        for ii in range(self.NT_hs):
            TT = self.T_arr_hs[ii]

            for jj in range(self.Ngrid_hs):

                pp = self.p_arr_hs[jj]

                propDict = self.gasobj.calc_allPropDict(pp, TT)

                self.s_arr[ii, jj] = propDict["s"]
                self.h_arr[ii, jj] = propDict["h"]

        # Plot
        self.show_plot_arr_hs()

    @QtCore.pyqtSlot()
    def show_plot_arr(self):

        # Clear plot
        self.pw.clear()

        # Reset diagram
        if (self.gasobj is None):
            self.emptyDiag()
            return

        # Units p,T
        (induni, induniStr) = self.determine_induni()

        unit_p = unitsTarget["pc"][induni]
        unit_p_Str = unitsTarget["pc"][induniStr]
        unit_T = unitsTarget["Tc"][induni]
        unit_T_Str = unitsTarget["Tc"][induniStr]

        self.pw.setLabel('bottom', 'Pressure', units=unit_p_Str)

        # Property array
        ind_arr = self.ui.comboBoxDiagramsProps.currentIndex()
        if (ind_arr == 0):  # rho

            self.pw.setLabel('left', 'Density',
                             units=unitsTarget["rho"][induniStr])

            for ii in range(self.NT):
                self.plotList[ii] = self.pw.plot(
                    unitConverter.trafo_unit(
                        self.p_arr, unitConverter.Units.Pa, unit_p),
                    unitConverter.trafo_unit(
                        self.rho_arr[ii, :],
                        unitConverter.Units.kg_m3,
                        unitsTarget["rho"][induni]),
                    pen=(ii, self.NT))

        elif (ind_arr == 1):  # Z

            self.pw.setLabel('left', 'Real Gas Factor', units='')

            for ii in range(self.NT):
                self.plotList[ii] = self.pw.plot(
                    unitConverter.trafo_unit(
                        self.p_arr, unitConverter.Units.Pa, unit_p),
                    self.Z_arr[ii, :],
                    pen=(ii, self.NT))

        elif (ind_arr == 2):  # K

            self.pw.setLabel('left', 'Compressibility', units='')

            for ii in range(self.NT):
                self.plotList[ii] = self.pw.plot(
                    unitConverter.trafo_unit(
                        self.p_arr, unitConverter.Units.Pa, unit_p),
                    self.K_arr[ii, :],
                    pen=(ii, self.NT))

        elif (ind_arr == 3):  # cp

            self.pw.setLabel('left', 'Heat Cap. cp',
                             units=unitsTarget["cp"][induniStr])

            for ii in range(self.NT):
                self.plotList[ii] = self.pw.plot(
                    unitConverter.trafo_unit(
                        self.p_arr, unitConverter.Units.Pa, unit_p),
                    unitConverter.trafo_unit(
                        self.cp_arr[ii, :],
                        unitConverter.Units.kJ_kgK,
                        unitsTarget["cp"][induni]),
                    pen=(ii, self.NT))

        elif (ind_arr == 4):  # cv

            self.pw.setLabel('left', 'Heat Cap. cv',
                             units=unitsTarget["cv"][induniStr])

            for ii in range(self.NT):
                self.plotList[ii] = self.pw.plot(
                    unitConverter.trafo_unit(
                        self.p_arr, unitConverter.Units.Pa, unit_p),
                    unitConverter.trafo_unit(
                        self.cv_arr[ii, :],
                        unitConverter.Units.kJ_kgK,
                        unitsTarget["cv"][induni]),
                    pen=(ii, self.NT))

        elif (ind_arr == 5):  # w

            self.pw.setLabel('left', 'Speed of Sound',
                             units=unitsTarget["w"][induniStr])

            for ii in range(self.NT):
                self.plotList[ii] = self.pw.plot(
                    unitConverter.trafo_unit(
                        self.p_arr, unitConverter.Units.Pa, unit_p),
                    unitConverter.trafo_unit(
                        self.w_arr[ii, :],
                        unitConverter.Units.m_s,
                        unitsTarget["w"][induni]),
                    pen=(ii, self.NT))

        elif (ind_arr == 6):  # mu

            self.pw.setLabel('left', 'JT Coefficient',
                             units=unitsTarget["mu"][induniStr])

            for ii in range(self.NT):
                self.plotList[ii] = self.pw.plot(
                    unitConverter.trafo_unit(
                        self.p_arr, unitConverter.Units.Pa, unit_p),
                    unitConverter.trafo_unit(
                        self.mu_arr[ii, :],
                        unitConverter.Units.degK_bar,
                        unitsTarget["mu"][induni]),
                    pen=(ii, self.NT))

        elif (ind_arr == 7):  # kappa

            self.pw.setLabel('left', 'Isentropic Exponent', units='')

            for ii in range(self.NT):
                self.plotList[ii] = self.pw.plot(
                    unitConverter.trafo_unit(
                        self.p_arr, unitConverter.Units.Pa, unit_p),
                    self.kappa_arr[ii, :],
                    pen=(ii, self.NT))

        # Clear legend
        try:
            self.pw.getPlotItem().legend.scene().removeItem(
                self.pw.getPlotItem().legend)
        except Exception as e:
            print(e)

        self.pw.addLegend()
        leg = self.pw.getPlotItem().legend

        try:
            self.pw.getPlotItem().legend.items = []
        except Exception as e:
            print(e)

        leg.items = []

        # Legend entries
        for ii in range(self.NT):
            leg.addItem(
                self.plotList[ii], str("{0:.1f}".format(
                    unitConverter.trafo_unit(
                        self.T_arr[ii],
                        unitConverter.Units.degK,
                        unit_T)) + " " + unit_T_Str))

    @QtCore.pyqtSlot()
    def show_plot_arr_hs(self):

        # clear plot
        self.pw_hs.clear()

        # reset diagram
        if (self.gasobj is None):
            self.emptyDiag_hs()
            return

        # units p,T ???
        (induni, induniStr) = self.determine_induni()

        # unit_p = unitsTarget["pc"][induni]
        # unit_p_Str = unitsTarget["pc"][induniStr]
        unit_T = unitsTarget["Tc"][induni]
        unit_T_Str = unitsTarget["Tc"][induniStr]

        unit_s = unitsTarget["s"][induni]
        unit_s_Str = unitsTarget["s"][induniStr]
        unit_h = unitsTarget["h"][induni]
        unit_h_Str = unitsTarget["h"][induniStr]

        self.pw_hs.setLabel('bottom', 'Entropy', units=unit_s_Str)
        self.pw_hs.setLabel('left', 'Enthalpy', units=unit_h_Str)

        for ii in range(self.NT_hs):
            self.plotList_hs[ii] = self.pw_hs.plot(
                unitConverter.trafo_unit(
                    self.s_arr[ii, :],
                    unitConverter.Units.kJ_kgK,
                    unit_s),
                unitConverter.trafo_unit(
                    self.h_arr[ii, :],
                    unitConverter.Units.kJ_kg,
                    unit_h),
                pen=(ii, self.NT_hs))

        for ii in range(self.Ngrid_hs):
            self.pw_hs.plot(
                unitConverter.trafo_unit(
                    self.s_arr[:, ii],
                    unitConverter.Units.kJ_kgK,
                    unit_s),
                unitConverter.trafo_unit(
                    self.h_arr[:, ii],
                    unitConverter.Units.kJ_kg,
                    unit_h),
                pen=(ii, self.NT_hs))

        # Clear legend
        try:
            self.pw_hs.getPlotItem().legend.scene().removeItem(
                self.pw_hs.getPlotItem().legend)
        except Exception as e:
            print(e)

        self.pw_hs.addLegend()
        leg = self.pw_hs.getPlotItem().legend

        try:
            self.pw_hs.getPlotItem().legend.items = []
        except Exception as e:
            print(e)

        leg.items = []

        # Legend entries
        for ii in range(self.NT_hs):
            leg.addItem(self.plotList_hs[ii], str("{0:.1f}".format(
                unitConverter.trafo_unit(
                    self.T_arr_hs[ii],
                    unitConverter.Units.degK,
                    unit_T)) + " " + unit_T_Str))

    def emptyDiag(self):

        self.pw.setLabel('bottom', 'Pressure', units='')
        self.pw.setLabel('left', 'Property', units='')
        self.pw.setXRange(0.0, 1.0)
        self.pw.setYRange(0.0, 1.0)
        self.pw.enableAutoRange()

    def emptyDiag_hs(self):

        self.pw_hs.setLabel('bottom', 'Entropy', units='')
        self.pw_hs.setLabel('left', 'Enthalpy', units='')
        self.pw_hs.setXRange(0.0, 1.0)
        self.pw_hs.setYRange(0.0, 1.0)
        self.pw_hs.enableAutoRange()

    def initGrid(self):

        self.NT = 5
        self.Ngrid = 20

        self.rho_arr = numpy.zeros((self.NT, self.Ngrid))
        self.Z_arr = numpy.zeros((self.NT, self.Ngrid))
        self.K_arr = numpy.zeros((self.NT, self.Ngrid))
        self.cp_arr = numpy.zeros((self.NT, self.Ngrid))
        self.cv_arr = numpy.zeros((self.NT, self.Ngrid))
        self.w_arr = numpy.zeros((self.NT, self.Ngrid))
        self.mu_arr = numpy.zeros((self.NT, self.Ngrid))
        self.kappa_arr = numpy.zeros((self.NT, self.Ngrid))

    def initGrid_hs(self):

        self.NT_hs = 5
        self.Ngrid_hs = 20

        self.s_arr = numpy.zeros((self.NT_hs, self.Ngrid_hs))
        self.h_arr = numpy.zeros((self.NT_hs, self.Ngrid_hs))

    def initDiag(self):

        self.pw = self.ui.graphicsView
        self.pw.setMouseEnabled(x=False, y=False)
        self.pw.plot()
        self.pw.enableAutoRange()
        self.pw.hideButtons()
        self.setMinMaxValsForAxes()
        self.emptyDiag()
        self.plotList = [None]*self.NT
        self.pw.addLegend()

    def initDiag_hs(self):

        self.pw_hs = self.ui.graphicsView_hs
        self.pw_hs.setMouseEnabled(x=False, y=False)
        self.pw_hs.plot()
        self.pw_hs.enableAutoRange()
        self.pw_hs.hideButtons()
        self.setMinMaxValsForAxes_hs()
        self.emptyDiag_hs()
        self.plotList_hs = [None]*self.NT_hs
        self.pw.addLegend()

    def clearLegend(self):

        try:
            self.pw.getPlotItem().legend.items = []
        except Exception as e:
            print(e)

    def clearLegend_hs(self):

        try:
            self.pw_hs.getPlotItem().legend.items = []
        except Exception as e:
            print(e)

    def setBasicTrivial(self):

        self.Mm = 0.0
        self.R = 0.0
        self.Tc = 0.0
        self.pc = 0.0
        self.Hi = 0.0
        self.Hs = 0.0

    def setNormTrivial(self):

        self.rhoN = 0.0
        self.ZN = 0.0
        self.KN = 0.0
        self.cpN = 0.0
        self.cvN = 0.0
        self.wN = 0.0
        self.muN = 0.0
        self.kappaN = 0.0

    def setArbitraryTrivial(self):

        self.rho = 0.0
        self.Z = 0.0
        self.K = 0.0
        self.cp = 0.0
        self.cv = 0.0
        self.w = 0.0
        self.mu = 0.0
        self.kappa = 0.0

    def determine_induni(self):

        if (self.ui.radioButtonUnitMetric.isChecked()):
            induni = 0
        else:
            induni = 1

        induniStr = induni + 2

        return (induni, induniStr)

    def determine_normCond(self):

        if (self.ui.radioButton_T0.isChecked()):
            return data.normConditions["de0"]
        elif (self.ui.radioButton_T15.isChecked()):
            return data.normConditions["de15"]
        else:
            return data.normConditions["de20"]

    def set_normCondLabel(self):

        if (self.ui.radioButton_T0.isChecked()):
            condText = self.ui.radioButton_T0.text()
        elif (self.ui.radioButton_T15.isChecked()):
            condText = self.ui.radioButton_T15.text()
        else:
            condText = self.ui.radioButton_T20.text()

        self.ui.labelNormStateDef.setText(
            "Norm state definition: \t " + str(condText))

    def setupTableModelsSpec(self):
        """Setup specific table model (gas, boundaries)"""

        # table model gas
        (self.modelGas,
         self.selectionModelGas) = generics.setupTableModelGen(
            self, "Component", "Fraction [mol%]")

    def setupTableViewsSpec(self):
        """Setup specific table views (gas, boundaries)"""

        # table view gas
        generics.setupTableViewGen(
            self.ui.tableViewGas,
            self.modelGas,
            self.selectionModelGas)

    def initTableModelsSpec(self):
        """Gui: init table models (gas boundaries)"""

        # gas
        self.updateLabelStatusGas(
            parameters.ID_STATUSGAS_FRACTIONSUM_OUTRANGE, {})
        self.initGasComponents()

    def initGasComponents(self):
        """Gui: init table model gas"""

        for ii in range(dataGui.nDataTabGasComponents):

            self.modelGas.insertRows(ii, 1, QtCore.QModelIndex())
            self.modelGas.setData(
                self.modelGas.index(ii, 0, QtCore.QModelIndex()),
                QtGui.QColor(dataGui.dataTabGasComponents[ii][1]),
                QtCore.Qt.DecorationRole)
            self.modelGas.setData(
                self.modelGas.index(ii, 0, QtCore.QModelIndex()),
                dataGui.dataTabGasComponents[ii][0])
            self.modelGas.setData(
                self.modelGas.index(ii, 1, QtCore.QModelIndex()),
                float(0.0))

    def initGraphicsViewGas(self):
        """Gui: init pie chart gas"""

        self.graphicsSceneGas = pieChartGui.GraphicsScenePie()
        self.ui.graphicsViewGas.setScene(self.graphicsSceneGas)
        self.ui.graphicsViewGas.show()
        self.ui.graphicsViewGas.setEnabled(True)

    @QtCore.pyqtSlot()
    def newGasComponents(self):

        dataGui.newGasComponents(self.modelGas)

    @QtCore.pyqtSlot()
    def readGasComponents(self):

        dataGui.readGasComponents(self, self.modelGas)

    @QtCore.pyqtSlot()
    def saveComponents(self):

        dataGui.saveComponents(self, self.modelGas)

    @QtCore.pyqtSlot()
    def updateGas(self):

        # get gas composition
        (gasComposition, idStatus) = dataGui.getGasComponents(self.modelGas)

        # pie chart gas
        self.graphicsSceneGas.updatePieChart(gasComposition)

        # label status gas
        self.updateLabelStatusGas(idStatus, gasComposition)

        # trick: block gas components name change
        dataGui.resetGasComponentsName(self.modelGas)

        # Data model
        if (idStatus == parameters.ID_STATUSGAS_OK):
            self.ui.buttonApplyGasComp.setEnabled(True)
            self.gasComposition = gasComposition
        else:
            self.ui.buttonApplyGasComp.setEnabled(False)
            self.gasComposition = {}

    def updateLabelStatusGas(self, idStatus, gasComposition):

        if (idStatus == parameters.ID_STATUSGAS_OK):
            messg = "Gas composition is complete."
        elif (idStatus == parameters.ID_STATUSGAS_FRACTION_OUTRANGE):
            messg = "Gas composition contains invalid fractions."
        elif (idStatus == parameters.ID_STATUSGAS_FRACTIONSUM_OUTRANGE):
            messg = (
                "Gas composition incomplete: The sum of \n fractions is " +
                str("{0:.2f}".format(sum(gasComposition.values())))
                + " mol%.")

        self.ui.labelStatusGas.setText(str(messg))

    @QtCore.pyqtSlot()
    def applyGasComposition(self):

        self.gasobj = calc.Gas(self.gasComposition, "de0")
