
import os

from PyQt5.QtWidgets import QApplication

import marvinglobal.marvinglobal as mg
import config
import guiLogic


if __name__ == "__main__":

    config.startLogging()

    # connect with shared data
    config.md = mg.MarvinGlobal()
    if not config.md.connect():
        os._exit(1)

    # add own process to shared process list
    config.md.updateProcessDict(config.processName)

    config.log(f"start gui in main thread")

    app = QApplication([])
    window = guiLogic.SkeletonGui()
    app.exec()

