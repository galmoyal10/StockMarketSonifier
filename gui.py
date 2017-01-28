import sys
import datetime
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *


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
        self.historic_ckbox = self._create_checkbox("View historical data", 60, 60,self.on_historic_checkbox_click)

        # Show the window and run the app
        self._w.show()
        app.exec_()

    def _create_sonify_btns(self):
        self._create_btn("Sonify", 20,80,self.on_click)
        self._create_btn("Stop sonification", 100, 80, self.on_click)

    # Create the actions
    @pyqtSlot()
    def on_click(self):
        self._textbox.setText("Button clicked.")

    def _create_datetime_popup(self, text, position_x, position_y, initial_value = datetime.datetime.today()):
        wid = QDateTimeEdit(self._w)
        wid.setCalendarPopup(True)
        wid.move(position_x, position_y)
        wid.setWindowTitle(text)
        wid.setDate(initial_value)
        wid.show()
        return wid

    def on_historic_checkbox_click(self):
        if self.historic_ckbox.isChecked():
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



