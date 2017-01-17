from data_streamer.stock_streamer import SonifiableStockStreamer
from data_streamer.historic_stock_streamer import HistoricStockStreamer
from sonifier.sonifier import Sonifier
from Consts import SoundParams
from manager import SonificationManager

if __name__ == '__main__':
#    streamer = SonifiableStockStreamer('GOOG')
    historic_streamer = HistoricStockStreamer('AAPL', '2016-09-14', '2016-09-18', 10)
    sonifier = Sonifier([0, 115, 43])
    mapping = dict()
    mapping['High'] = SoundParams.pitch
    mapping['Low'] = SoundParams.pitch
    mapping['Volume'] = SoundParams.pitch
    manager = SonificationManager(historic_streamer, sonifier, mapping, 0.5)
    manager.run()