class DataStreamer(object):

    # returns a list of the data properties
    def get_data_properties(self):
        raise NotImplementedError()

    def get_data_current_state(self):
        raise NotImplementedError()

    def get_value(self, property):
        state = self.get_data_current_state()
        return state[property]
