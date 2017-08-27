import sys
import time
import logging
import threading
import socket
import subprocess
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui, Qt

server_IP = '192.168.0.21'  # This is the IP of the ESB Pi. It is a static IP.
port = 5002 #Port Number, one port number is picked for each device that is connected to server.
BUFF = 1024

#Sets up logging
logname = time.strftime("log/LC_ClientLog(%H_%M_%S).log", time.localtime())
logger = logging.getLogger("")
logging.basicConfig(filename=logname, level=logging.DEBUG)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Things to note, in the Ping App around line 400, there is something you need to change based on
# whether you are using Linux or Windows

class LaunchControl(QtWidgets.QWidget):
    def __init__(self):

        # initializes the Geometry, the overall window, and the connection settings

        super().__init__()

        self.server_address = (server_IP,port)
        self.connection_status = False

        self.init_ui()

    def init_ui(self):

        # initializes the GUI with the pictures found in the pictures folder.

        self.palettered = QtGui.QPalette()
        self.palettered.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)

        self.paletteblack = QtGui.QPalette()
        self.paletteblack.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)

        self.paletteblue = QtGui.QPalette()
        self.paletteblue.setColor(QtGui.QPalette.Foreground, QtCore.Qt.blue)

        # initial values
        self.kdata = "Open"
        self.mdata = "Open"
        self.ldata = "Open"
        self.bdata = "Intact"

        # time_thread = threading.Thread(target = self.get_time)
        # time_thread.start()

        self.server_address = (server_IP, port)
        self.connection_status = False  # initialzing to a false connection state
        self.arm_status = False

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        #grid.addWidget(self.serial_feed, tl_vertical_grid_pos, tl_hor_grid_pos, vertical_grid_length_min, hor_grid_width_min

        def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf, scolor):
            # makes code smaller, all the labels in the program

            slabel = QtWidgets.QLabel(self)
            slabel.setText(stext)
            slabel.move(smovex, smovey)
            slabel.resize(sresizex, sresizey)
            slabel.setFont(QtGui.QFont('Times', sfontsize, QtGui.QFont.Bold, storf))
            slabel.setPalette(scolor)

        def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):
            # makes code smaller, all the pictures in the program
            # you have to save pictures to the pictures/ path in order to show

            pix = QtWidgets.QLabel(self)
            pix.setPixmap(QtGui.QPixmap('pictures/' + spicture))
            pix.move(smovex, smovey)
            pix.resize(sresizex, sresizey)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Pictures

        #Sets up all of the pictures that can change after the program is run

        whitebackground = createPicture(self, 'white2.png', 0, 0, 805, 505)
        redstripetoolbar = createPicture(self, 'red.png', 0, 0, 805, 40)

        self.redcircle = QtWidgets.QLabel(self)
        self.redcircle.setPixmap(QtGui.QPixmap('pictures/redcircle.png'))
        self.redcircle.move(-80, -100)
        self.redcircle.resize(150, 150)

        self.sdsulogo = QtWidgets.QLabel(self)
        self.sdsulogo.setPixmap(QtGui.QPixmap('pictures/sdsu2.png'))
        self.sdsulogo.move(2, 4)
        self.sdsulogo.resize(30, 24)

        self.statusbreakred = QtWidgets.QLabel(self)
        self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusbreakred.move(110, 90)
        self.statusbreakred.resize(380, 40)

        self.statusmainred = QtWidgets.QLabel(self)
        self.statusmainred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusmainred.move(110, 135)
        self.statusmainred.resize(380, 40)

        self.statusloxred = QtWidgets.QLabel(self)
        self.statusloxred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusloxred.move(110, 180)
        self.statusloxred.resize(380, 40)

        self.statuskerored = QtWidgets.QLabel(self)
        self.statuskerored.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statuskerored.move(110, 225)
        self.statuskerored.resize(380, 40)

        self.statusignitorred = QtWidgets.QLabel(self)
        self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusignitorred.move(110, 270)
        self.statusignitorred.resize(380, 40)

        self.statussafteyred = QtWidgets.QLabel(self)
        self.statussafteyred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statussafteyred.move(110, 315)
        self.statussafteyred.resize(380, 40)

        self.statushgpscolor = QtWidgets.QLabel(self)
        self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statushgpscolor.move(110, 360)
        self.statushgpscolor.resize(380, 40)

        # def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):

        statusboxbreak = createPicture(self, 'statusborder.png', -80, 90, 375, 40)
        statusboxmain = createPicture(self, 'statusborder.png', -80, 135, 375, 40)
        statusboxlox = createPicture(self, 'statusborder.png', -80, 180, 375, 40)
        statusboxkero = createPicture(self, 'statusborder.png', -80, 225, 375, 40)
        statusboxignitor = createPicture(self, 'statusborder.png', -80, 270, 375, 40)
        statusboxsaftey = createPicture(self, 'statusborder.png', -80, 315, 375, 40)
        statusboxhgps = createPicture(self, 'statusborder.png', -80, 360, 375, 40)
        statusbreak = createPicture(self, 'break.png', 100, 40, 100, 10)
        pressurebreak = createPicture(self, 'break.png', 600, 40, 100, 10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Labels

        # def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf, scolor):

        self.rocketlabel = createLabel(self, 'SDSU ROCKET PROJECT', 46, -7, 500, 50, 19, True, self.paletteblack)
        self.breakwirelabel = createLabel(self, 'Breakwire Status', 5, 85, 500, 50, 12, False, self.paletteblue)
        self.mainValvelabel = createLabel(self, 'Main Propellant Valve', 2, 130, 500, 50, 10, False, self.paletteblue)
        self.loxValvelabel = createLabel(self, 'Lox Vent Valve', 5, 175, 500, 50, 12, False, self.paletteblue)
        self.keroValvelabel = createLabel(self, 'Kero Vent Valve', 5, 220, 500, 50, 12, False, self.paletteblue)
        self.ignitorstatuslabel = createLabel(self, 'Ignitor Status', 5, 265, 500, 50, 12, False, self.paletteblue)
        self.safteystatus = createLabel(self, 'Saftey Status', 5, 310, 500, 50, 12, False, self.paletteblue)
        self.hgpsstatuslabel = createLabel(self, 'HGPS', 5, 355, 500, 50, 12, False, self.paletteblue)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Sets up all of the labels that can change after the program is run.

        self.breakwirechange = QtWidgets.QLabel(self)
        self.breakwirechange.setText('Intact')
        self.breakwirechange.move(180, 85)
        self.breakwirechange.resize(500, 50)
        self.breakwirechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.breakwirechange.setPalette(self.paletteblack)

        self.mainValvechange = QtWidgets.QLabel(self)
        self.mainValvechange.setText('Open')
        self.mainValvechange.move(180, 130)
        self.mainValvechange.resize(500, 50)
        self.mainValvechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.mainValvechange.setPalette(self.paletteblack)

        self.loxValvechange = QtWidgets.QLabel(self)
        self.loxValvechange.setText('Open')
        self.loxValvechange.move(180, 175)
        self.loxValvechange.resize(500, 50)
        self.loxValvechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.loxValvechange.setPalette(self.paletteblack)

        self.keroValvechange = QtWidgets.QLabel(self)
        self.keroValvechange.setText('Open')
        self.keroValvechange.move(180, 220)
        self.keroValvechange.resize(500, 50)
        self.keroValvechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.keroValvechange.setPalette(self.paletteblack)

        self.ignitorstatuschange = QtWidgets.QLabel(self)
        self.ignitorstatuschange.setText('Not Lit')
        self.ignitorstatuschange.move(175, 265)
        self.ignitorstatuschange.resize(500, 50)
        self.ignitorstatuschange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.ignitorstatuschange.setPalette(self.paletteblack)

        self.safteystatuschange = QtWidgets.QLabel(self)
        self.safteystatuschange.setText('Disarmed')
        self.safteystatuschange.move(157, 310)
        self.safteystatuschange.resize(500, 50)
        self.safteystatuschange.setFont(QtGui.QFont('Times', 16, QtGui.QFont.Bold, False))
        self.safteystatuschange.setPalette(self.paletteblack)

        self.hgpsstatuschange = QtWidgets.QLabel(self)
        self.hgpsstatuschange.setText('Off')
        self.hgpsstatuschange.move(190, 355)
        self.hgpsstatuschange.resize(500, 50)
        self.hgpsstatuschange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.hgpsstatuschange.setPalette(self.paletteblack)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # sets up the logging text box (or "Action Log") in the console

        self.logTextBox = QtWidgets.QTextBrowser(self)
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.logTextBox.setFont(self.font)
        self.logTextBox.setReadOnly(True)
        self.logTextBox.resize(200, 375)
        self.logTextBox.move(300, 40)
        self.logTextBox.append("   ==Action Log==")

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.setLayout(grid)
        self.homeButtons()
        self.show()

    # self.Time()


    def homeButtons(self):  # Sets up buttons found in the program
        # Font sizes, such that font2 = 18 point size
        self.font2 = QtGui.QFont()
        self.font2.setPointSize(18)
        self.font3 = QtGui.QFont()
        self.font3.setPointSize(12)
        self.font4 = QtGui.QFont()
        self.font4.setPointSize(10)
        self.font5 = QtGui.QFont()
        self.font5.setPointSize(24)

        def createBtn(self, slabel, smovex, smovey, sresizex, sresizey, sfontsize, sfunction):
            # makes code smaller, all the buttons in the program

            Btn = QtWidgets.QPushButton(slabel, self)
            Btn.move(smovex, smovey)
            Btn.resize(sresizex, sresizey)
            Btn.setFont(sfontsize)
            Btn.clicked.connect(sfunction)

        #               createBtn(self, slabel, smovex, smovey, sresizex, sresizey, sfontsize, sfunction):

        self.closeBtn = createBtn(self, "Close", 680, 0, 120, 40, self.font3, self.close_app)
        self.pingBtn = createBtn(self, "Ping Server", 560, 0, 120, 40, self.font3, self.ping_app)
        self.ping_serverBtn = createBtn(self, "Connect", 440, 0, 120, 40, self.font3, self.connect_app)
        self.open_ventsBtn = createBtn(self, "Open Vents", 0, 415, 160, 60, self.font3, self.openvents_app)
        self.close_ventsBtn = createBtn(self, "Close Vents", 160, 415, 160, 60, self.font3, self.closevents_app)
        self.close_mainBtn = createBtn(self, "Close Main", 320, 415, 160, 60, self.font3, self.closemain_app)
        self.hgpsonBtn = createBtn(self, "HGPS On", 480, 415, 160, 60, self.font3, self.hgpson_app)
        self.hgpsoffBtn = createBtn(self, "HGPS Off", 640, 415, 160, 60, self.font3, self.hgpsoff_app)
        self.statusBtn = createBtn(self, "Read Statuses", 0, 50, 300, 35, self.font3, self.read_app)
        self.pressureBtn = createBtn(self, "Read Pressures", 500, 50, 300, 35, self.font3, self.read_app)


    def paintEvent(self, e):

        # sets up the "paint brush" in order to use the drawLines function

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.drawLines2(qp)
        qp.end()

    def drawLines(self, qp):

        # draws the red lines found in the program
        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(800, 0, 800, 480)
        qp.drawLine(0, 480, 800, 480)

    def drawLines2(self, qp):  # (not being used currently)

        # draws the black lines found in the program
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)

    def timer1(self):

        # Creates the timer in the log box, might only be used in the computer client
        self.logTextBox.append("  >  Timer Started!{}".format(time.strftime("   -\t(%H:%M:%S)", time.localtime())))
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer0)
        self.timer.start(1000)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # This is where the functions are for the buttons

    def read_app(self):
        # Application that reads the status's for the valve states (Used when Read Status's Button is pressed)
        if self.connection_status == True:
            self.logTextBox.append("  >  Reading{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Reading at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

            self.infotimer = QtCore.QTimer()
            self.infotimer.timeout.connect(self.get_info)
            self.infotimer.setInterval(200)
            self.infotimer.start()
            self.logTextBox.append(" > Starting Get Info Timer{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Started Get Info Timer at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')


    def connect_app(self):
        # Application that connects the client to the server (Used when Connect Button is pressed)
        self.logTextBox.append("  >  Connecting...{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))

        try:
            self.s = socket.create_connection(self.server_address,timeout = 1.5)
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'Socket Successfully Bound.\nClick "Read Statuses " to start')
            self.connection_status = True
            self.sdsulogo.setPixmap(QtGui.QPixmap('pictures/sdsu2green.png'))
            self.redcircle.setPixmap(QtGui.QPixmap('pictures/greencircle.png'))
            self.logTextBox.append("  >  Connected{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Connection Successful at {}".format(time.asctime()))

        except socket.error as e:
            logger.debug("Connection Unsuccessful at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            reply = QtWidgets.QMessageBox.critical(self, "Connection Results", "Couldn't connect to {} at {}. Error is: \n{}.\nMake sure server is listening.".format(self.server_address[0],self.server_address[1],e),
                                                    QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Retry)
            if reply == QtWidgets.QMessageBox.Cancel:
                self.logTextBox.append("  >  Connection Canceled{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
            elif reply == QtWidgets.QMessageBox.Retry:
                self.connect_app()


    def openvents_app(self):
        # Application that opens vents (Used when the Open Vents Button is pushed)
        if self.connection_status == True:
            self.logTextBox.append("  >  Vents Opened{}".format(time.strftime("    -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Vents Opened at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('VO')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def closevents_app(self):
        # Application that closes vents (Used when the Close Vents Button is pushed)
        if self.connection_status == True:
            self.logTextBox.append("  >  Vents Closed{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Vents Closed at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('VC')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def closemain_app(self):
        # Application that closes main (Used when the Abort Button is pushed)
        if self.connection_status == True:
            self.logTextBox.append("  >  Main Propellant Valve Closed{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Main Closed at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('MC')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def hgpson_app(self):
        # Application that turns on hgps (Used when the Hgps On Button is pushed)
        if self.connection_status == True:
            self.logTextBox.append("  >  HGPS turned ON{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("HGPS ON at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('HGPS_On')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def hgpsoff_app(self):
        # Application that turns off hgps (Used when the Hgps Off Button is pushed)
        if self.connection_status == True:
            self.logTextBox.append("  >  HGPS turned OFF{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("HGPS OFF at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('HGPS_Off')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def ping_app(self):
        # Application that pings the server (Used when the Ping Server Button is pushed)
        QtWidgets.QMessageBox.information(self, '', 'Pinging...')
        #response = subprocess.call(["ping", server_IP,"-c1", "-W1","-q"]) #This is Linux syntax.
        response = subprocess.call("ping {} -n 1 -w 1".format(server_IP)) #This is Windows syntax.
        logger.debug("Pinging Server at {}".format(time.asctime()))
        self.logTextBox.append("  >  Pinging Server{}".format(time.strftime("    -\t(%H:%M:%S)", time.localtime())))

        if response == 0:
            QtWidgets.QMessageBox.information(self, 'Ping Results', 'Ping to {} sucessful!\nGo ahead and connect.'.format(server_IP))
            logger.debug("Ping_Sucessful at {}".format(time.asctime()))
            self.logTextBox.append("  >  Pinging Successful{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
        else:
            QtWidgets.QMessageBox.information(self, 'Ping Results', "Ping to {} unsucessful!\nCheck the IP you're connecting to, or if server is online.".format(server_IP))
            logger.debug("Ping_Unsucessful at {}".format(time.asctime()))
            self.logTextBox.append("  >  Pinging Unsucessful{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))

    def send_info(self,command):
        #Function that sends commands to server and listens for some responses
        if command == 'MO':
            message = b'main_open'
            logger.debug("main_open at {}".format(time.asctime()))
        elif command == 'MC':
            message = b'main_close'
            logger.debug("main_close at {}".format(time.asctime()))
        elif command == 'VO':
            message = b'vents_open'
            logger.debug("vents_open at {}".format(time.asctime()))
        elif command == 'VC':
            message = b'vents_close'
            logger.debug("vents_close at {}".format(time.asctime()))
        elif command == 'L':
            message = b'launch'
            logger.debug("launch at {}".format(time.asctime()))
        elif command == 'A':
            message = b'abort'
            logger.debug("abort at {}".format(time.asctime()))
        elif command == "Ig":
            message = b"ign1_on"
            logger.debug("ign1_on at {}".format(time.asctime()))
        elif command == "IO":
            message = b"ign1_off"
            logger.debug("ign1_off at {}".format(time.asctime()))
        elif command =='HGPS_On':
            message = b"ign2_on"
            logger.debug("HGPS_On at {}".format(time.asctime()))
        elif command == 'HGPS_Off':
            message = b'ign2_off'
            logger.debug("HGPS_Off at {}".format(time.asctime()))
        elif command == "BL":
            message = b'boosters_lit'
            logger.debug("Boosters On at {}".format(time.asctime()))
        elif command == "BO":
            message = b'boosters_off'
            logger.debug("Boosters Off at {}".format(time.asctime()))

        self.s.send(message)
        data = self.s.recv(BUFF)
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        if data.decode("utf-8") == 'Ignitor 1 Lit': #Changes status of ignitor to lit af
            time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
            self.ignitorstatuschange.setText('Lit af')
            logging.info("Ignitor 1 lit: {}".format(time_now))
            logger.debug("Ignitor_1_lit at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Ignitor 1 Off': #Changes status of ignitor to Not Lit
            self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
            self.ignitorstatuschange.setText('Not Lit')
            logger.debug("Ignitor_1_Off at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Ignitor 2 Lit': #Changes status of Hgps to On
            self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
            self.hgpsstatuschange.setText('On')
            logger.debug("HGPS On at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Ignitor 2 Off': #Changes status of Hgps to Off
            self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statred.png'))
            self.hgpsstatuschange.setText('Off')
            logger.debug("HGPS Off at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Boosters Lit': #Changes status of Boosters to On
            #self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
            #self.hgpsstatuschange.setText('On')
            logger.debug("Boosters Lit at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Boosters Off': #Changes status of Boosters to Off
            #self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statred.png'))
            #self.hgpsstatuschange.setText('Off')
            logger.debug("Boosters Off at {}".format(time.asctime()))

    def switch_label(self,label):

        #These statements change the status of the labels
        if label == 'bwire':
            if self.breakwirechange.text() == 'Intact':
                self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.breakwirechange.setText('Broken')
                logger.debug("bwire_Broken at {}".format(time.asctime()))
            elif self.breakwirechange.text() == 'Broken':
                self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.breakwirechange.setText('Intact')
                logger.debug("bwire_Intact at {}".format(time.asctime()))

        if label == 'main':
            if self.mainValvechange.text() == 'Open':
                self.statusmainred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.mainValvechange.setText('Closed')
                logger.debug("main_Closed at {}".format(time.asctime()))
            elif self.mainValvechange.text() == 'Closed':
                self.statusmainred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.mainValvechange.setText('Open')
                logger.debug("main_Open at {}".format(time.asctime()))

        if label == 'kero':
            if self.keroValvechange.text() == 'Open':
                self.statuskerored.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.keroValvechange.setText('Closed')
                logger.debug("kero_Closed at {}".format(time.asctime()))
            elif self.keroValvechange.text() == 'Closed':
                self.statuskerored.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.keroValvechange.setText('Open')
                logger.debug("kero_Open at {}".format(time.asctime()))

        if label == 'lox':
            if self.loxValvechange.text() == 'Open':
                self.statusloxred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.loxValvechange.setText('Closed')
                logger.debug("lox_Closed at {}".format(time.asctime()))
            elif self.loxValvechange.text() == 'Closed':
                self.statusloxred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.loxValvechange.setText('Open')
                logger.debug("lox_Open at {}".format(time.asctime()))

    def get_info(self):
        # Receives information from the server and switches the label based on what the client is given
        try:
            self.s.send(b'bwire_status')
            self.bdata = self.s.recv(BUFF)

            self.s.send(b'main_status')
            self.mdata = self.s.recv(BUFF)

            self.s.send(b'kero_status')
            self.kdata = self.s.recv(BUFF)

            self.s.send(b'LOX_status')
            self.ldata = self.s.recv(BUFF)

        except (socket.error,AttributeError) as err:
            time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            logging.error("{},{}".format(time_now,err))
            logger.debug("{},{}".format(time_now,err))

        #The following if statements call the label to be changed only if the server sends a message that contradicts the current status of the label 
        if self.bdata.decode("utf-8") != self.breakwirechange.text():
            self.switch_label("bwire")
            print("Break Wire Changed:")
            print(self.bdata)
            logger.debug("bwire_status of {} at {}".format(str(self.bdata),time.asctime()))

        if self.mdata.decode("utf-8") != self.mainValvechange.text():
            self.switch_label('main')
            print("Main Changed")
            print(self.mdata)
            logger.debug("main_status of {} at {}".format(str(self.mdata),time.asctime()))

        if self.kdata.decode("utf-8") != self.keroValvechange.text():
            self.switch_label('kero')
            print("Kero Changed")
            print(self.kdata)
            logger.debug("kero_status of {} at {}".format(str(self.kdata),time.asctime()))

        if self.ldata.decode("utf-8") != self.loxValvechange.text():
            self.switch_label('lox')
            print("Lox Changed")
            print(self.ldata)
            logger.debug("lox_status of {} at {}".format(str(self.ldata),time.asctime()))


    def close_app(self):
        # exits GUI
        self.logTextBox.append(">  Exiting...{}".format(time.strftime("\t-           (%H:%M:%S)", time.localtime())))
        choice = QtWidgets.QMessageBox.question(self, "Confirmation.", "Are you sure you want to exit?", 
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            print("System Closed")
            logger.debug("Application Exited at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            sys.exit()
        else:
            self.logTextBox.append("> Exit Stopped{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))


