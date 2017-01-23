from data_streamer.stock_streamer import SonifiableStockStreamer
from data_streamer.historic_stock_streamer import HistoricStockStreamer
from sonifier.sonifier import Sonifier
from Consts import SoundParams
from manager import SonificationManager

if __name__ == '__main__':
#    streamer = SonifiableStockStreamer('GOOG')
    historic_streamer = HistoricStockStreamer('ESLT', '2016-03-01', '2016-05-01', 10)
    mapping = dict()
    mapping['Close'] = (SoundParams.tempo, 114)
    mapping['Volume'] = (SoundParams.pitch, 108)

    manager = SonificationManager(historic_streamer, Sonifier(), mapping)
    manager.run()