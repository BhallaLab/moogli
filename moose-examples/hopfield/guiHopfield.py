import os
import sys
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import QEvent, Qt
import numpy as np
from hopfield_ui import Ui_MainWindow
from hopfield import HopfieldNetwork

class DesignerMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """Customization for Qt Designer created window"""
    def __init__(self, interpreter=None,parent = None):
        # initialization of the superclass
        super(DesignerMainWindow, self).__init__(parent)
        # setup the GUI --> function generated by pyuic4
        self.setupUi(self)
        self.hop = HopfieldNetwork(100)
        self.hop.setClocksHopfield()
        self.defaultButtonState()
        self.mem1 = []
        self.mem2 = []
        self.mem3 = []
        self.mem4 = []
        self.input = []
        self.connectElements()
        self.runCount = 0
        self.runPushButton.setEnabled(False)
        self.statusbar.showMessage('Hopfield Network Demo')
        self.inputChanged = False

    def defaultButtonState(self):
        self.mem1PushButton.setEnabled(False)
        self.mem2PushButton.setEnabled(False)
        self.mem3PushButton.setEnabled(False)
        self.mem4PushButton.setEnabled(False)
        self.inputPushButton.setEnabled(False)

    def connectElements(self):
        self.connect(self.clearDisplayPushButton,QtCore.SIGNAL('clicked()'), self.clearDisplay)
        self.connect(self.memorizePushButton,QtCore.SIGNAL('clicked()'),self.memorizePattern)
        self.connect(self.randomizePushButton,QtCore.SIGNAL('clicked()'),self.randomizePattern)
        self.connect(self.clearMemPushButton,QtCore.SIGNAL('clicked()'),self.clearMemory)
        self.connect(self.runPushButton,QtCore.SIGNAL('clicked()'),self.runStep)
        self.connect(self.mem1PushButton,QtCore.SIGNAL('clicked()'),self.retriveMem1)
        self.connect(self.mem2PushButton,QtCore.SIGNAL('clicked()'),self.retriveMem2)
        self.connect(self.mem3PushButton,QtCore.SIGNAL('clicked()'),self.retriveMem3)
        self.connect(self.mem4PushButton,QtCore.SIGNAL('clicked()'),self.retriveMem4)
        self.connect(self.inputPushButton,QtCore.SIGNAL('clicked()'),self.retriveInput)
        self.connect(self.saveInputPushButton,QtCore.SIGNAL('clicked()'),self.saveInput)
        self.connect(self.aPushButton,QtCore.SIGNAL('clicked()'),self.retriveA)
        self.connect(self.bPushButton,QtCore.SIGNAL('clicked()'),self.retriveB)
        self.connect(self.cPushButton,QtCore.SIGNAL('clicked()'),self.retriveC)
        self.connect(self.dPushButton,QtCore.SIGNAL('clicked()'),self.retriveD)
        self.connect(self.computeSynWeightsPushButton,QtCore.SIGNAL('clicked()'),self.computeAllWeights)

    def saveInput(self):
        print('saving current pattern as input')
        inpList = []
        for i in range(100):
            exec(('inpList.append(int(self.pushButton_%s.isChecked()))' %i))
        self.input = inpList
        self.inputPushButton.setEnabled(True)
        self.inputChanged = True
        self.runCount = 0

    def computeAllWeights(self):
        self.statusbar.showMessage('Computing synaptic weights')
        self.hop.assignAllSynapticWeights() #weights are assigned
        self.runPushButton.setEnabled(True)

    def runStep(self):
        self.statusbar.showMessage('Running')

        if self.inputChanged:
            inputPattern = self.input
            self.hop.updateInputs(inputPattern) #input updating
            self.hop.mooseReinit()
            self.hop.runMooseHopfield(0.0310)

        if self.runCount == 0:
            for i in range(100):
                if np.any((self.hop.allSpikes[i].vector>0.0)&(self.hop.allSpikes[i].vector<0.0310)):
                    exec(('self.pushButton_%s.setChecked(True)' %i))
                else:
                    exec(('self.pushButton_%s.setChecked(False)' %i))

        else:
            self.hop.runMooseHopfield(0.02)
            #print 0.0310+(0.02*(self.runCount-1)),(0.0310+(0.02*self.runCount))
            for i in range(100):
                if np.any((self.hop.allSpikes[i].vector>(0.0301+(0.02*(self.runCount-1))))&(self.hop.allSpikes[i].vector<(0.0301+(0.02*self.runCount)))):
                    exec(('self.pushButton_%s.setChecked(True)' %i))
                else:
                    exec(('self.pushButton_%s.setChecked(False)' %i))

        self.runCount += 1
        self.statusbar.showMessage('Done Running')
        
    def retriveMem1(self):
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(self.mem1[int(%s)])' %(i,i)))
        self.statusbar.showMessage('Showing Mem1')

    def retriveMem2(self):
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(self.mem2[int(%s)])' %(i,i)))
        self.statusbar.showMessage('Showing Mem2')

    def retriveMem3(self):
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(self.mem3[int(%s)])' %(i,i)))
        self.statusbar.showMessage('Showing Mem3')

    def retriveMem4(self):
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(self.mem4[int(%s)])' %(i,i)))
        self.statusbar.showMessage('Showing Mem4')

    def retriveInput(self):
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(self.input[int(%s)])' %(i,i)))
        self.statusbar.showMessage('Showing Input')

    def retriveA(self):
        a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(a[int(%s)])' %(i,i)))
        self.statusbar.showMessage('Showing Sample A')
        
    def retriveB(self):
        b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(b[int(%s)])' %(i,i)))
        self.statusbar.showMessage('Showing Sample B')

    def retriveC(self):
        c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(c[int(%s)])' %(i,i)))
        self.statusbar.showMessage('Showing Sample C')

    def retriveD(self):
        d = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(d[int(%s)])' %(i,i)))
        self.statusbar.showMessage('Showing Sample D')

    def clearMemory(self):
        self.hop.clearAllMemory()
        self.clearDisplay()
        self.defaultButtonState()
        self.mem1 = []
        self.mem2 = []
        self.mem3 = []
        self.input = []
        self.statusbar.showMessage('Cleared all Memory')
        self.runPushButton.setEnabled(False)
        self.inputPushButton.setEnabled(False)
        self.runCount = 0
        
    def randomizePattern(self):
        r = np.random.randint(2,size=100)
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(r[int(%s)])' %(i,i)))

    def memorizePattern(self):
        pattern = []
        for i in range(100):
            exec(('pattern.append(int(self.pushButton_%s.isChecked()))' %i))

        self.hop.updateWeights(pattern)

        for k in range(100): #very weird that I have to do this!
            if pattern[k] == -1:
                pattern[k] = 0

        savedAlready = self.hop.numMemories
        if savedAlready == 1:
            self.mem1 = pattern
            self.mem1PushButton.setEnabled(True)
            #print pattern
        elif savedAlready == 2:
            self.mem2 = pattern
            self.mem2PushButton.setEnabled(True)
            #print pattern
        elif savedAlready == 3:
            self.mem3 = pattern
            self.mem3PushButton.setEnabled(True)
        elif savedAlready == 4:
            self.mem4 = pattern
            self.mem4PushButton.setEnabled(True)

        self.runPushButton.setEnabled(False)

        self.statusbar.showMessage('New Pattern Memorised')

    def clearDisplay(self):
        for i in range(100):
            exec(('self.pushButton_%s.setChecked(False)' %i)) 
        self.statusbar.showMessage('Cleared display')


app = QtGui.QApplication(sys.argv)
# instantiate the main window
dmw = DesignerMainWindow()
# show it
dmw.show()
# start the Qt main loop execution, exiting from this script
#http://code.google.com/p/subplot/source/browse/branches/mzViewer/PyMZViewer/mpl_custom_widget.py
#http://eli.thegreenplace.net/files/prog_code/qt_mpl_bars.py.txt
#http://lionel.textmalaysia.com/a-simple-tutorial-on-gui-programming-using-qt-designer-with-pyqt4.html
#http://www.mail-archive.com/matplotlib-users@lists.sourceforge.net/msg13241.html
# with the same return code of Qt application
sys.exit(app.exec_())

