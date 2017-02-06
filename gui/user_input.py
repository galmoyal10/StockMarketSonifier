class StockParamWidgets:
    def __init__(self, label, enable_widget, sonic_param_widget, instrument_widget):
        self._label = label
        self._enable_widget = enable_widget
        self._sonic_param_widget = sonic_param_widget
        self._instrument_widget = instrument_widget

    def is_activated(self):
        return self._enable_widget.isChecked()

    @staticmethod
    def _get_drop_down_widget_value(widget):
        return widget.itemData(widget.currentIndex()).toPyObject()

    def get_sonic_param(self):
        return StockParamWidgets._get_drop_down_widget_value(self._sonic_param_widget)

    def get_instrument(self):
        return StockParamWidgets._get_drop_down_widget_value(self._instrument_widget)

    @staticmethod
    def _destroy_widget(widget):
        widget.destroy()
        widget.hide()

    def destroy(self):
        StockParamWidgets._destroy_widget(self._label)
        StockParamWidgets._destroy_widget(self._enable_widget)
        StockParamWidgets._destroy_widget(self._sonic_param_widget)
        StockParamWidgets._destroy_widget(self._instrument_widget)
