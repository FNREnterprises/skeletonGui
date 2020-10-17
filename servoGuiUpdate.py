
import time

from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot

import config
import marvinglobal.marvinglobal as mg

# work on update messages of servos
# these functions can be used to emit a GUI update
# the functions called by the emit are defined in the init section of the of the SkeletonGui class
class GuiUpdateSignals(QObject):
    updateServo = pyqtSignal(str)       # calls updateGuiServo
    updateArduino = pyqtSignal(int)
    updateProcess = pyqtSignal(str)


#class GuiUpdateThread(QtCore.QThread):
class GuiUpdateThread(QRunnable):
    """
    This checks for new data in the guiUpdateQueue
    the queue can have different types of data based on the type attribute
    """
    # signal for gui update
    # raises guiLogic.updateGui
    #updateGui = QtCore.pyqtSignal(int, int)

    def __init__(self):
        #QtCore.QThread.__init__(self)
        #super(GuiUpdateThread, self).__init__()
        super().__init__()
        self.signals = GuiUpdateSignals()


    @pyqtSlot()
    def run(self):

        time.sleep(2)       # wait for gui to startup

        while True:

            #time.sleep(0.01)
            #if guiUpdateQueue.empty():
            #    continue
            try:
                guiUpdateData = config.md.guiUpdateQueue.get()
            except:
                # shared queue access broken
                # retry connection with shared dict
                config.md = mg.MarvinGlobal()
                if not config.md.connect():
                    time.sleep(1)
                    continue

            if guiUpdateData is not None:

                #config.log(f"updateData from queue: {updateData}")
                # check for unexpected data
                try:
                    type = guiUpdateData['type']
                except Exception as e:
                    config.log(f"msg from queue without a type {guiUpdateData}")
                    continue

                #if guiUpdateData['type'] == config.SERVO_UPDATE:
                if type == 'servoUpdate':

                    servoName = guiUpdateData['servoName']

                    # as the servo current values are in the shared dict we only need to
                    # specify which servo to update in the gui
                    #Data = {'type', 'assigned', 'moving', 'detached', 'position', 'degree'}
                    #servoStatic: config.ServoStatic = config.md.servoStaticDict.get(servoName)
                    #servoDerived = config.servoDerivedDict[servoName]

                    #if servoStatic is None:
                    #    config.log(f"could not eval servoDefinitions for {servoName}")
                    #    return

                    #del guiUpdateData['type']  # remove added type
                    #del guiUpdateData['servoName']  # remove added servo name

                    # update the local servo store
                    #config.updateServoCurrent(servoName, guiUpdateData)

                    # inform the gui about the changed servo information using the unique servoId
                    #self.signals.update.emit(config.SERVO_UPDATE, servoDerived.servoUniqueId)
                    config.log(f"signal servoUpdate for {servoName}")
                    self.signals.updateServo.emit(servoName)


                #elif guiUpdateData['type'] == config.ARDUINO_UPDATE:
                elif type == "arduinoUpdate":
                    config.log(f"emit arduino update {guiUpdateData}")
                    arduino = guiUpdateData['arduino']
                    self.signals.updateArduino.emit(arduino)

                elif type == "processUpdate":
                    self.signals.updateProcess.emit(guiUpdateData['process'])
