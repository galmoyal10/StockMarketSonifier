import sys
import datetime
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from user_input import StockParamWidgets
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

            self._param_widgets = list()
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

    def create_label_widget(self, text, x_pos, y_pos):
        label = QLabel(self._w)
        label.setText(text + ": ")
        label.move(x_pos, y_pos)
        label.show()
        return label

    def create_sonic_param_widget(self, sonic_params, x_pos, y_pos):
        sonic_param_widget = QComboBox(self._w)
        for sonic_param in sonic_params:
            sonic_param_widget.addItem(sonic_param.name, QVariant(sonic_param))
        sonic_param_widget.move(x_pos, y_pos)
        sonic_param_widget.hide()
        return sonic_param_widget

    def create_instrument_widget(self, x_pos, y_pos):
        insturment_widget = QComboBox(self._w)
        for instrument_id, instrument_name in enumerate(MidiWrapper.get_instruments()):
            insturment_widget.addItem(instrument_name, QVariant(instrument_id))
        insturment_widget.move(x_pos, y_pos)
        insturment_widget.hide()
        return insturment_widget

    def _create_param_matching_widgets(self):
        if self._param_widgets:
            for widget in self._param_widgets:
                widget[1].destroy()

        self._param_widgets = list()

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
            label = self.create_label_widget(param[0], GUIUtils.COLUMNS['Stock Parameter'], y_position)
            sonic_param_drop_down_widget = self.create_sonic_param_widget(param[1], GUIUtils.COLUMNS['Sonic Parameter'], y_position)
            instrument_drop_down_widget = self.create_instrument_widget(GUIUtils.COLUMNS['Instrument'], y_position)

            param_enable_widget = self._create_checkbox("", 10, y_position)
            param_enable_widget.stateChanged.connect(partial(GUIUtils._on_enable_check_box_clicked,
                                                  [instrument_drop_down_widget, sonic_param_drop_down_widget],
                                                  param_enable_widget))
            param_enable_widget.show()

            self._param_widgets.append((param[0], StockParamWidgets(label,
                                                                    param_enable_widget,
                                                                    sonic_param_drop_down_widget,
                                                                    instrument_drop_down_widget)))

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
        for param_name, param_widgets in self._param_widgets.items():
            if param_widgets.isActivated():
                mapping[param_name] = (param_widgets.getSonicParam(), param_widgets.getInstrumentParam())
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



