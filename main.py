from data_streamer.live_stock_streamer import SonifiableLiveStockStreamer
from data_streamer.historic_stock_streamer import SonifiableHistoricStockStreamer
from data_streamer.live_stock_streamer import SonifiableLiveStockStreamer
from sonifier.sonifier import Sonifier
from Consts import SoundParams
from manager import SonificationManager
import gui


def GUI():
    g = gui.GUIUtils()

def manual():
    historic_streamer = SonifiableHistoricStockStreamer('AAPL', '2016-01-01', '2016-04-01')
    live_streamer = SonifiableLiveStockStreamer('AAPL')
    mapping = dict()
    mapping['Close'] = (SoundParams.tempo, 15)
    mapping['Volume'] = (SoundParams.pitch, 14)

    manager = SonificationManager(historic_streamer, Sonifier(), mapping)
    manager.run()

if __name__ == '__main__':
    GUI()
