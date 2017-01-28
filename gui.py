import sys
import datetime
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

from data_streamer.stock_streamer import SonifiableStockStreamer
from data_streamer.historic_stock_streamer import HistoricStockStreamer
from sonifier.sonifier import Sonifier
from Consts import SoundParams
from manager import SonificationManager

class GUIUtils(object):

    def __init__(self):
        # create our window
        app = QApplication(sys.argv)
        self._w = QWidget()
        self._w.setWindowTitle('Sonification Menu')

        # Set window size.
        self._w.resize(250, 150)

        self._textbox = self._create_textbox(20,20, 200, 40)
        self._create_sonify_btns()
        self._historic_ckbox = self._create_checkbox("View historical data", 60, 60, self.on_historic_checkbox_click)

        # Show the window and run the app
        self._w.show()
        app.exec_()

    def _create_sonify_btns(self):
        self._create_btn("Sonify", 20, 80, lambda : self.on_sonification_btn_click(True))
        self._create_btn("Stop sonification", 100, 80, lambda:self.on_sonification_btn_click(False))

    # Create the actions
    @pyqtSlot()
    def on_sonification_btn_click(self, should_start):
        if should_start:

            if self._historic_ckbox.isChecked():
                historic_streamer = HistoricStockStreamer(self._textbox.text(), self._start_date.date().toPyDate(), self._end_date.date().toPyDate(), 10)
                #TODO : handle input validation

                mapping = dict()
                mapping['Close'] = (SoundParams.tempo, 114)
                mapping['Volume'] = (SoundParams.pitch, 108)

                manager = SonificationManager(historic_streamer, Sonifier(), mapping)
                manager._start_caching()
            else:
                #TODO: Do something..
                pass

        else:
            #TODO: stop the melody
            pass


    def _create_datetime_popup(self, text, position_x, position_y, initial_value = datetime.datetime.today()):
        wid = QDateTimeEdit(self._w)
        wid.setCalendarPopup(True)
        wid.move(position_x, position_y)
        wid.setWindowTitle(text)
        wid.setDate(initial_value)
        wid.show()
        return wid

    def on_historic_checkbox_click(self):
        if self._historic_ckbox.isChecked():
            self._w.resize(250, 350)
            self._start_date = self._create_datetime_popup("Start date", 20, 130)
            self._end_date = self._create_datetime_popup("End date", 20, 160)
        else:
            self._w.resize(250, 150)
            self._start_date.hide()
            self._end_date.hide()

    def _create_btn(self, message, position_x, position_y, callback_function):
        # Create a button in the window
        button = QPushButton(message, self._w)
        button.move(position_x, position_y)

        # connect the signals to the slots
        button.clicked.connect(callback_function)

    def _create_textbox(self, position_x, position_y, width, height):
        # Create textbox
        textbox = QLineEdit(self._w)
        textbox.move(position_x, position_y)
        textbox.resize(width, height)
        return textbox

    def _create_checkbox(self, label, position_x, position_y, callback_function, initial_value=False):
        ckbox = QCheckBox(label, self._w)
        ckbox.move(position_x, position_y)
        ckbox.setChecked(initial_value)
        ckbox.stateChanged.connect(callback_function)
        return ckbox



