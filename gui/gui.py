import sys
import datetime
from time import sleep
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import yahoo_finance

from user_input import StockParamWidgets
from data_streamer.live_stock_streamer import SonifiableLiveStockStreamer
from data_streamer.historic_stock_streamer import SonifiableHistoricStockStreamer
from sonifier.sonifier import Sonifier
from manager import SonificationManager
from sonifier.midi_wrapper import MidiWrapper
from functools import partial
import sys


class OutputWidget(QWidget):
    """
    implementation of stdout piping to GUI widget
    """
    class EmittingStream(QtCore.QObject):
        textWritten = QtCore.pyqtSignal(str)

        def write(self, text):
            self.textWritten.emit(text)

    def __init__(self, parent = None):
        super(OutputWidget, self).__init__(parent)
        sys.stdout = OutputWidget.EmittingStream(textWritten=self.normal_output_written)
        self._textEdit = QTextEdit(self)
        self._textEdit.resize(350, 250)
        self._textEdit.move(0,0)
        self._textEdit.setReadOnly(True)

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def clear(self):
        self._textEdit.clear()

    def normal_output_written(self, text):
        """Append text to the QTextEdit."""
        cursor = self._textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self._textEdit.setTextCursor(cursor)
        self._textEdit.ensureCursorVisible()


class GUIUtils(object):
    """
    implementation of applications GUI
    """

    COLUMNS = {"Sonify?" : 10, "Stock Parameter" : 70, "Sonic Parameter" : 180, "Instrument" : 290}

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

    def _create_header_and_footer(self):
        """
        displays application's header and footer
        """
        self._create_label("Enter stock symbol name:", 20, 5)
        self._create_label("Yarden Moskovich & Gal Moyal", 350, 385)
        self._create_label("Sonifier Output:", 580, 20)

    def _create_label(self, text, x_pos, y_pos):
        """
        creates a single label in GUI
        :param text: label's text
        :return:
        """
        label = QLabel(self._w)
        label.setText(text)
        label.move(x_pos, y_pos)
        label.show()
        return label

    @show_error_as_dialogbox
    def __init__(self):
        """
        initializes application's GUI
        """
        # create our window
        app = QApplication(sys.argv)
        self._w = QWidget()
        self._w.setWindowTitle('Sonification Menu')
        self._w.setFixedSize(850, 400)
        self._stock_txtbox = self._create_textbox(20, 20, 300, 40)
        self._create_sonify_btns()
        self._live_ckbox = self._create_checkbox("Switch to live data mode", 60, 70, self.on_live_checkbox_click)
        self._live_label = self._create_label("*Live data might not be accurate after trade hours", 60, 90)
        self._create_header_and_footer()
        self._param_widgets = list()
        self._column_titles = list()
        self._create_param_matching_widgets()

        self._output_widget = OutputWidget(self._w)
        a = self._output_widget.maximumWidth()
        self._output_widget.resize(400,250)
        self._output_widget.move(450, 50)
        self._output_widget.show()
        self._is_playing = False
        # Show the window and run the app
        self._w.show()
        self._manager = None
        self._sonifier = Sonifier()
        app.exec_()

    def _display_column_titles(self, y_position):
        """
        displays stock parameter columns
        """
        for label in self._column_titles:
            label.destroy()
            label.hide()

        for column in GUIUtils.COLUMNS.items():
            label = QLabel(self._w)
            label.setText(column[0])
            myFont = QFont()
            myFont.setBold(True)
            label.setFont(myFont)
            label.move(column[1], y_position)
            label.show()
            self._column_titles.append(label)

    def create_label_widget(self, text, x_pos, y_pos):
        """
        creates and displays a single label
        :param text: label's text
        """
        label = QLabel(self._w)
        label.setText(text + ": ")
        label.move(x_pos, y_pos)
        label.show()
        return label

    def create_sonic_param_widget(self, sonic_params, x_pos, y_pos):
        """
        creates a single sonic params drop down widget
        :param sonic_params: available sonic params
        """
        sonic_param_widget = QComboBox(self._w)
        for sonic_param in sonic_params:
            sonic_param_widget.addItem(sonic_param.name, QVariant(sonic_param))
        sonic_param_widget.move(x_pos, y_pos)
        sonic_param_widget.hide()
        return sonic_param_widget

    def create_instrument_widget(self, x_pos, y_pos):
        """
        creates a singel instrument drop down widget
        """
        insturment_widget = QComboBox(self._w)
        for instrument_id, instrument_name in enumerate(MidiWrapper.get_instruments()):
            insturment_widget.addItem(instrument_name, QVariant(instrument_id))
        insturment_widget.move(x_pos, y_pos)
        insturment_widget.hide()
        return insturment_widget

    def _create_param_matching_widgets(self):
        """
        creates stock parameter widgets
        """
        if self._param_widgets:
            for widget in self._param_widgets.values():
                widget.destroy()

        self._param_widgets = dict()
        start_y_position = 0
        if self._live_ckbox.isChecked():
            streamer_type = SonifiableLiveStockStreamer
            start_y_position = 150

        else:
            self._start_date_label, self._start_date = self._create_datetime_popup("Start date", 20, 150,
                                                                                   datetime.date.today() - datetime.timedelta(3* (365/12)))
            self._end_date_label, self._end_date = self._create_datetime_popup("End date", 20, 180,
                                                                               datetime.date.today() - datetime.timedelta(1))
            streamer_type = SonifiableHistoricStockStreamer
            start_y_position = 210
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

            self._param_widgets[param[0]] = StockParamWidgets(label,
                                                              param_enable_widget,
                                                              sonic_param_drop_down_widget,
                                                              instrument_drop_down_widget)

    @staticmethod
    def _on_enable_check_box_clicked(related_cbs, checkbox):
        """
        callback for clicking stock parameter enable check box
        :param related_cbs: stock parameter related widgets
        :param checkbox: clicked checkbox
        :return:
        """
        if checkbox.isChecked():
            for cb in related_cbs:
                cb.show()
        else:
            for cb in related_cbs:
                cb.hide()

    @staticmethod
    def _show_exception_dialog(e):
        """
        decorator for displaying exceptions as message boxes
        :param e: thrown exception
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An Exception Occurred, Please try again.")

        if isinstance(e, yahoo_finance.YQLResponseMalformedError):
            msg.setInformativeText("Yahoo Finance does not contain the data you requested")
        else:
            msg.setInformativeText(e.message)
        msg.setWindowTitle("Sonification Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg.exec_()

    def _create_sonify_btns(self):
        self._should_start = True
        self._sonify_button = self._create_btn("Sonify", 70, 110, lambda x: self.on_sonification_btn_click())
        self._sonify_button.resize(100,20)

    @staticmethod
    def _get_cb_value(cb):
        return cb.itemData(cb.currentIndex()).toPyObject()

    def _get_mapping_input(self):
        """
        reads stock parameters inputs from GUI
        """
        mapping = dict()
        active = False
        for param_name, param_widgets in self._param_widgets.items():
            if param_widgets.is_activated():
                mapping[param_name] = (param_widgets.get_sonic_param(), param_widgets.get_instrument())
                active = True
        if not active:
            raise Exception("Please choose stock parameters")
        return mapping

    # Create the actions
    @pyqtSlot()
    @show_error_as_dialogbox
    def on_sonification_btn_click(self):
        """
        starts/stop sonification
        """
        if self._should_start:
            if len(self._stock_txtbox.text()) == 0:
                raise Exception("Please enter stock symbol name")
            mapping = self._get_mapping_input()
            if self._live_ckbox.isChecked():
                streamer = SonifiableLiveStockStreamer(self._stock_txtbox.text())
            else:
                streamer = SonifiableHistoricStockStreamer(self._stock_txtbox.text(),
                                                           self._start_date.date().toPyDate(),
                                                           self._end_date.date().toPyDate())

            self._manager = SonificationManager(streamer, self._sonifier, mapping)
            self._output_widget.clear()
            self._manager.run()
            self._live_ckbox.hide()
            self._live_label.hide()
            self._is_playing = True
            self._should_start = False
            self._sonify_button.setText("Stop Sonification")
            for _, sonic_param_widget in self._param_widgets.items():
                sonic_param_widget.disable()
        else:
            if self._is_playing:
                self._live_ckbox.show()
                self._live_label.show()
                self._manager.stop()
                self._is_playing = False
                self._should_start = True
                for _, sonic_param_widget in self._param_widgets.items():
                    sonic_param_widget.enable()
                self._sonify_button.setText("Sonify")

    def _create_datetime_popup(self, text, position_x, position_y, initial_value = datetime.date.today()):
        """
        displays a single date input popup
        """
        label = self.create_label_widget(text,position_x,position_y)
        wid = QDateEdit(self._w)
        wid.setCalendarPopup(True)
        wid.move(position_x + 80, position_y-5)
        wid.setDate(initial_value)
        wid.show()
        return label, wid

    def on_live_checkbox_click(self):
        """
        callback for handling application mode switching (live/historic)
        """
        if self._is_playing:
            self._live_ckbox.setCheckState(0 if self._live_ckbox.isChecked() else 2)
            return
        self._create_param_matching_widgets()

        if self._live_ckbox.isChecked():
            self._start_date_label.hide()
            self._end_date_label.hide()
            self._start_date.hide()
            self._start_date.destroy()
            self._end_date.hide()
            self._end_date.destroy()

    def _create_btn(self, text, position_x, position_y, callback_function):
        """
        creates a single button
        :param text: button's text
        :param callback_function: callback for clicking the button
        """
        # Create a button in the window
        button = QPushButton(text, self._w)
        button.move(position_x, position_y)

        # connect the signals to the slots
        button.clicked.connect(callback_function)
        return button

    def _create_textbox(self, position_x, position_y, width, height):
        """
        creates a textbox for user input
        """
        # Create textbox
        textbox = QLineEdit(self._w)
        textbox.move(position_x, position_y)
        textbox.resize(width, height)
        return textbox

    def _create_checkbox(self, text, position_x, position_y, callback_function = None, initial_value=False):
        """
        creates a checkbox
        """
        ckbox = QCheckBox(text, self._w)
        ckbox.move(position_x, position_y)
        ckbox.setChecked(initial_value)
        if callback_function is not None:
            ckbox.stateChanged.connect(callback_function)
        return ckbox



