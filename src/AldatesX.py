#!/usr/bin/python
'''
Created on 8 Nov 2012

@author: james
'''
from pkg_resources import require
require("avx>=0.92")

from PySide.QtCore import Qt
from PySide.QtGui import QApplication
from org.muscat.avx.Client import Client
from org.muscat.avx.controller.Controller import Controller, VersionMismatchError
from staldates.ui.MainWindow import MainWindow
import argparse
import atexit
import fcntl  # @UnresolvedImport
import logging
import sys
from Pyro4.errors import NamingError, CommunicationError
from staldates.ui.widgets import Dialogs


if __name__ == "__main__":

    pid_file = 'aldatesx.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
    # another instance is running
        print "AldatesX is already running."
        sys.exit(1)

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.INFO)
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fullscreen",
                        help="Run in fullscreen mode and hide the mouse cursor",
                        action="store_true")
    parser.add_argument("-c",
                        help="Specify the controller ID to connect to",
                        metavar="CONTROLLERID",
                        default="")
    args = parser.parse_args()

    try:
        stylesheet = open("AldatesX.qss", "r")
        app.setStyleSheet(stylesheet.read())
    except IOError:
        # never mind
        logging.warn("Cannot find stylesheet, using default system styles.")

    try:
        controller = Controller.fromPyro(args.c)

        remoteVersion = controller.getVersion()

        if remoteVersion != Controller.version:
            raise VersionMismatchError(remoteVersion, Controller.version)

        myapp = MainWindow(controller)

        client = Client(myapp)
        client.setDaemon(True)
        client.start()
        client.started.wait()
        atexit.register(lambda: controller.unregisterClient(client.uri))

        controller.registerClient(client.uri)

        if args.fullscreen:
            QApplication.setOverrideCursor(Qt.BlankCursor)
            myapp.showFullScreen()
        else:
            myapp.show()
        sys.exit(app.exec_())

    except (NamingError, CommunicationError) as e:
        Dialogs.errorBox("Unable to connect to controller. Please check network connections and try again. (Error details: " + str(e) + ")")
    except VersionMismatchError as e:
        Dialogs.errorBox(str(e))
