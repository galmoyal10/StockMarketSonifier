from data_streamer.stock_streamer import SonifiableStockStreamer
from data_streamer.historic_stock_streamer import HistoricStockStreamer
from sonifier.sonifier import Sonifier
from Consts import SoundParams
from manager import SonificationManager

if __name__ == '__main__':
#    streamer = SonifiableStockStreamer('GOOG')
    historic_streamer = HistoricStockStreamer('AAPL', '2016-09-01', '2016-09-25', 10)
    sonifier = Sonifier([0,41])
    mapping = dict()
    mapping['Close'] = SoundParams.tempo
    mapping['High'] = SoundParams.pitch
    manager = SonificationManager(historic_streamer, sonifier, mapping)
    manager.run()