from data_streamer.stock_streamer import SonifiableStockStreamer
from data_streamer.historic_stock_streamer import HistoricStockStreamer
from sonifier.sonifier import Sonifier
from Consts import SoundParams
from manager import SonificationManager

if __name__ == '__main__':
#    streamer = SonifiableStockStreamer('GOOG')
    historic_streamer = HistoricStockStreamer('AAPL', '2016-01-01', '2016-04-01', 10)
    mapping = dict()
    mapping['Close'] = (SoundParams.amplitude, 15)
    mapping['Volume'] = (SoundParams.pitch, 14)

    manager = SonificationManager(historic_streamer, Sonifier(), mapping)
    manager.run()