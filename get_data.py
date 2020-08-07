import tushare as ts
import urllib


class GetRealtimeData:
    def __init__(self, code, callback, ui_callback):
        try:
            rt = ts.get_realtime_quotes(code)
        except urllib.error.URLError as e:
            print(e.reason)
            return

        cur_price = rt.price[0]
        high_price = rt.high[0]
        callback(code, float(cur_price), float(high_price), ui_callback)
