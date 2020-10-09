
import datetime
import logging
import queue

import marvinglobal.marvinglobal as mg


md = None   # shared data

servoNameByArduinoAndPin = {}   # a list to access servos by Arduino and Id

simulateServoMoves = False

guiUpdateQueue = queue.Queue(200)  # deque(maxlen=None) dequeue is not thread safe

def startLogging():
    logging.basicConfig(
        filename=f"log/skeletonControl.log",
        level=logging.INFO,
        format='%(message)s',
        filemode="w")


def log(msg, publish=True):

    logtime = str(datetime.datetime.now())[11:23]
    logging.info(f"{logtime} - {msg}")
    print(f"{logtime} - {msg}")


def evalDegFromPos(servoName: str, inPos: int):
    # inPos has to be in the 0..180 range (servo.write() limits this)
    # minPos has to be smaller than maxPos. Inversion is handled in the arduino
    # minDegrees always has to be smaller than maxDegrees
    servoDerived = mg.servoDerivedDict.get(servoName)
    servoStatic = mg.servoStaticDict.get(servoName)

    degPerPos = servoDerived.degRange / servoDerived.posRange
    deltaPos = inPos - servoStatic.zeroDegPos

    degrees = deltaPos * degPerPos
    # print(f"degrees: {degrees}")
    return round(degrees)


def evalPosFromDeg(servoName, inDeg):
    """
    a servo has min/max pos and deg defined. The 0 degree pos can be off center.
    :param servoStatic:
    :param inDeg:
    :return:
    """
    servoDerived = mg.servoDerivedDict.get(servoName)
    servoStatic = mg.servoStaticDict.get(servoName)

    posPerDeg = servoDerived.posRange / servoDerived.degRange
    pos = (inDeg * posPerDeg) + servoStatic.zeroDegPos
    return round(pos)
