import sys
import datetime
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from data_streamer.live_stock_streamer import SonifiableLiveStockStreamer
from data_streamer.historic_stock_streamer import SonifiableHistoricStockStreamer
from sonifier.sonifier import Sonifier
from manager import SonificationManager
from sonifier.midi_wrapper import MidiWrapper
from functools import partial

class GUIUtils(object):

    COLUMNS = {"Sonify" : 10, "Stock Parameter" : 50, "Sonic Parameter" : 150, "Instrument" : 240}

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
            self._w.setFixedSize(370, 400)

            self._stock_txtbox = self._create_textbox(20, 20, 300, 40)
            self._create_sonify_btns()
            self._historic_ckbox = self._create_checkbox("Sonify historical data", 60, 70, self.on_historic_checkbox_click)

            self._param_cbs = list()
            self._column_titles = list()
            self._create_param_matching_widgets()

            self._is_playing = False
            # Show the window and run the app
            self._w.show()
            self._manager = None
            self._sonifier = Sonifier()
            app.exec_()

    def _display_column_titles(self, y_position):
        for label in self._column_titles:
            label.destroy()
            label.hide()

        for column in GUIUtils.COLUMNS.items():
            label = QLabel(self._w)
            label.setText(column[0])
            label.move(column[1], y_position)
            label.show()
            self._column_titles.append(label)

    def _create_param_matching_widgets(self):
        if self._param_cbs:
            for _, label, param_dropdown, instrument_dropdown, enable_check_box in self._param_cbs:
                label.destroy()
                label.hide()
                param_dropdown.destroy()
                param_dropdown.hide()
                instrument_dropdown.destroy()
                instrument_dropdown.hide()
                enable_check_box.destroy()
                enable_check_box.hide()

        self._param_cbs = list()

        if self._historic_ckbox.isChecked():
            streamer_type = SonifiableHistoricStockStreamer
            start_y_position = 210

        else:
            streamer_type = SonifiableLiveStockStreamer
            start_y_position = 150
        self._display_column_titles(start_y_position)
        start_y_position += 20
        data_params = dict()

        for param in streamer_type.get_data_params():
            data_params[param] = [supported_sonic_param for supported_sonic_param in streamer_type.get_supported_sonic_params_for_param(param) if supported_sonic_param in Sonifier.get_supported_sonifiable_params()]

        for i, param in enumerate(data_params.items()):
            y_position = start_y_position + i * 30
            label = QLabel(self._w)
            label.setText(param[0] + ": ")
            label.move(50, y_position)
            label.show()

            sonic_param_cb = QComboBox(self._w)
            for sonic_param in param[1]:
                sonic_param_cb.addItem(sonic_param.name, QVariant(sonic_param))
            sonic_param_cb.move(150, y_position)
            sonic_param_cb.hide()
            insturment_cb = QComboBox(self._w)
            for instrument_id, instrument_name in enumerate(MidiWrapper.get_instruments()):
                insturment_cb.addItem(instrument_name, QVariant(instrument_id))
            insturment_cb.move(240, y_position)
            insturment_cb.hide()
            param_enable_checkbox = self._create_checkbox("", 10, y_position)
            param_enable_checkbox.stateChanged.connect(partial(GUIUtils._on_enable_check_box_clicked,
                                                  [insturment_cb, sonic_param_cb],
                                                  param_enable_checkbox))
            param_enable_checkbox.show()
            self._param_cbs.append((param[0], label, sonic_param_cb, insturment_cb, param_enable_checkbox))

    @staticmethod
    def _on_enable_check_box_clicked(related_cbs, checkbox):
        if checkbox.isChecked():
            for cb in related_cbs:
                cb.show()
        else:
            for cb in related_cbs:
                cb.hide()

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
        self._create_btn("Sonify", 50, 110, lambda : self.on_sonification_btn_click(True))
        self._create_btn("Stop sonification", 150, 110, lambda:self.on_sonification_btn_click(False))

    @staticmethod
    def _get_cb_value(cb):
        return cb.itemData(cb.currentIndex()).toPyObject()

    def _get_mapping_input(self):
        mapping = dict()
        for param_cb in self._param_cbs:
            if param_cb[4].isChecked():
                mapping[param_cb[0]] = ((GUIUtils._get_cb_value(param_cb[2])), GUIUtils._get_cb_value((param_cb[3])))
        return mapping
    # Create the actions
    @pyqtSlot()
    @show_error_as_dialogbox
    def on_sonification_btn_click(self, should_start):
        try:
            mapping = self._get_mapping_input()
            if should_start:
                if self._is_playing:
                    raise Exception("A sonification is already playing! stop it in order to play another one.")
                if self._historic_ckbox.isChecked():
                    streamer = SonifiableHistoricStockStreamer(self._stock_txtbox.text(), self._start_date.date().toPyDate(), self._end_date.date().toPyDate())

                else:
                    streamer = SonifiableLiveStockStreamer(self._stock_txtbox.text())

                self._manager = SonificationManager(streamer, self._sonifier, mapping)
                self._manager.run()
                self._is_playing = True
            else:
                self._is_playing = False
                self._manager.stop()

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

    def _create_checkbox(self, label, position_x, position_y, callback_function = None, initial_value=False):
        ckbox = QCheckBox(label, self._w)
        ckbox.move(position_x, position_y)
        ckbox.setChecked(initial_value)
        if callback_function is not None:
            ckbox.stateChanged.connect(callback_function)
        return ckbox



