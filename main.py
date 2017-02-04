from data_streamer.stock_streamer import SonifiableStockStreamer
from data_streamer.historic_stock_streamer import HistoricStockStreamer
from data_streamer.stock_streamer import SonifiableStockStreamer
from sonifier.sonifier import Sonifier
from Consts import SoundParams
from manager import SonificationManager
import gui


def GUI():
    gui = gui.GUIUtils()

def manual():
    historic_streamer = HistoricStockStreamer('AAPL', '2016-01-01', '2016-04-01')
    live_streamer = SonifiableStockStreamer('AAPL')
    mapping = dict()
    mapping['Close'] = (SoundParams.tempo, 15)
    mapping['Volume'] = (SoundParams.pitch, 14)

    manager = SonificationManager(historic_streamer, Sonifier(), mapping)
    manager.run()

if __name__ == '__main__':
    manual()
