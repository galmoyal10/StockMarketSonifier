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

    def show_error_as_dialogbox(func):
        """
        refreshs the value before executing the function
        """

        def func_wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self._show_exception_dialog(e)


        return func_wrapper

    @show_error_as_dialogbox
    def __init__(self):
            # create our window
            app = QApplication(sys.argv)
            self._w = QWidget()
            self._w.setWindowTitle('Sonification Menu')
            self._w.setFixedSize(250, 400)

            self._stock_txtbox = self._create_textbox(20, 20, 200, 40)
            self._create_sonify_btns()
            self._historic_ckbox = self._create_checkbox("View historical data", 60, 70, self.on_historic_checkbox_click)

            self._param_cbs = list()
            self._create_param_matching_widgets()

            self._is_playing = False
            # Show the window and run the app
            self._w.show()
            app.exec_()

    def _create_param_matching_widgets(self):

        if self._param_cbs:
            for label, dropdown in self._param_cbs:
                label.destroy()
                label.hide()
                dropdown.destroy()
                dropdown.hide()

        self._param_cbs = list()

        if self._historic_ckbox.isChecked():
            data_params = HistoricStockStreamer.get_data_params()
            start_y_position = 220

        else:
            data_params = SonifiableStockStreamer.get_data_params()
            start_y_position = 150


        for i, param in enumerate(data_params):
            label = QLabel(self._w)
            label.setText(param + ": ")
            label.move(20, start_y_position + i * 30)
            label.show()

            cb = QComboBox(self._w)
            cb.addItems([sparam.name for sparam in Sonifier.get_supported_sonifiable_params()])
            cb.move(100, start_y_position + i * 30)
            cb.show()

            self._param_cbs.append((label, cb))

    @staticmethod
    def _show_exception_dialog(e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setText("An Exception Occurred")
        msg.setInformativeText(e.message)
        msg.setWindowTitle("Sonification Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg.exec_()

    def _create_sonify_btns(self):
        self._create_btn("Sonify", 20, 110, lambda : self.on_sonification_btn_click(True))
        self._create_btn("Stop sonification", 100, 110, lambda:self.on_sonification_btn_click(False))

    # Create the actions
    @pyqtSlot()
    @show_error_as_dialogbox
    def on_sonification_btn_click(self, should_start):
        try:
            if should_start:
                if self._is_playing:
                    raise Exception("A sonification is already playing! stop it in order to play another one.")
                if self._historic_ckbox.isChecked():
                    streamer = HistoricStockStreamer(self._stock_txtbox.text(), self._start_date.date().toPyDate(), self._end_date.date().toPyDate())

                    mapping = dict()
                    mapping['Close'] = (SoundParams.tempo, 114)
                    mapping['Volume'] = (SoundParams.pitch, 108)
                else:
                    streamer = SonifiableStockStreamer(self._stock_txtbox.text())
                    #TODO: @Yarden, Change mapping
                    mapping = None

                manager = SonificationManager(streamer, Sonifier(), mapping)
                manager.run()
                self._is_playing = True
            else:
                #TODO: stop the melody
                self._is_playing = False
                pass

        except Exception as e:
            self._show_exception_dialog(e)

    def _create_datetime_popup(self, text, position_x, position_y, initial_value = datetime.datetime.today()):
        wid = QDateTimeEdit(self._w)
        wid.setCalendarPopup(True)
        wid.move(position_x, position_y)
        wid.setWindowTitle(text)
        wid.setDate(initial_value)
        wid.show()
        return wid

    def on_historic_checkbox_click(self):
        self._create_param_matching_widgets()

        if self._historic_ckbox.isChecked():
            self._start_date = self._create_datetime_popup("Start date", 20, 150)
            self._end_date = self._create_datetime_popup("End date", 20, 180)
        else:
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



