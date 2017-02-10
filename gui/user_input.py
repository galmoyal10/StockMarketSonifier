

class StockParamWidgets:
    """
    A class for stock sonifying parameters in GUI
    """

    def __init__(self, label, enable_widget, sonic_param_widget, instrument_widget):
        """
        initializes object
        :param label: label of stock param
        :param enable_widget: enable/disable stock param checkbox object
        :param sonic_param_widget: sonic param drop down object
        :param instrument_widget: instrument drop down object
        """
        self._label = label
        self._enable_widget = enable_widget
        self._sonic_param_widget = sonic_param_widget
        self._instrument_widget = instrument_widget

    def is_activated(self):
        """
        indicates whether stock param is chosen or not
        """
        return self._enable_widget.isChecked()

    @staticmethod
    def _get_drop_down_widget_value(widget):
        """
        returns the current value of a drop down widget
        """
        return widget.itemData(widget.currentIndex()).toPyObject()

    def get_sonic_param(self):
        """
        returns the chosen sonic param from GUI
        """
        return StockParamWidgets._get_drop_down_widget_value(self._sonic_param_widget)

    def get_instrument(self):
        """
        returns the chosen instrument from GUI
        """
        return StockParamWidgets._get_drop_down_widget_value(self._instrument_widget)

    @staticmethod
    def _destroy_widget(widget):
        """
        destroys the widget in GUI
        """
        widget.destroy()
        widget.hide()
        widget.setEnabled(False)

    def destroy(self):
        """
        destroy all stock param related widgets
        """
        StockParamWidgets._destroy_widget(self._label)
        StockParamWidgets._destroy_widget(self._enable_widget)
        StockParamWidgets._destroy_widget(self._sonic_param_widget)
        StockParamWidgets._destroy_widget(self._instrument_widget)
