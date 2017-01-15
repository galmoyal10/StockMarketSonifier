from data_streamer.stock_streamer import SonifiableStockStreamer
from sonifier.sonifier import Sonifier
from Consts import SoundParams
from manager import SonificationManager

if __name__ == '__main__':
    streamer = SonifiableStockStreamer('GOOG')
    sonifier = Sonifier([0, 115, 43])
    mapping = dict()
    mapping['price'] = SoundParams.pitch
    mapping['last_trade_with_time'] = SoundParams.amplitude
    manager = SonificationManager(streamer, sonifier, mapping, 1)
    manager.run()