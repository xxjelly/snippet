import tushare as ts
import urllib
import time
from threading import Timer
from util import Config
from util import WarnBox

from tkinter import *
import time


c = Config()

# past7 = time.time() - 604800
# past7_str = time.strftime("%Y%m%d", time.localtime(past7))

# # ts.set_token("efa59ba827607d4a4bb71670cc686067906873ebd0ae887f02057be6")

# now_str = time.strftime("%Y%m%d", time.localtime(time.time()))

# pro = ts.pro_api()
# df = pro.daily(ts_code='600000.SH', start_date=past7_str, end_date=now_str)
# print(df)


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

class QuitStrategy:
    def __init__(self, code, cur_price, high_price, ui_callback):
        info = Config.get_info_by_code(code)
        # calc
        cost = info['cost']

        if cur_price < cost:
            per = (cost - cur_price) / cost
            msg = '亏损ing...name = {}, cost = {}\ncur = {}, high = {}\ncur_per = -{:.2f}%\n'.format(info['name'], info['cost'], cur_price, high_price, per * 100)
            print(msg)
            if per >= 0.03:
                msg = '亏损ing...name = {}, cost = {}\n\ncur = {}, high = {}\n\ncur_per = -{:.2f}%'.format(info['name'], info['cost'], cur_price, high_price, per * 100)
                WarnBox(msg)

            ui_callback(code, msg)
        else:
            high_per = (high_price - cost) / cost
            cur_per = (cur_price - cost) / cost
            msg = '盈利ing...name = {}, cost = {}\ncur = {}, high = {}\ncur_per = {:.2f}%, high_per = {:.2f}%\n'.format(info['name'], info['cost'], cur_price, high_price, cur_per * 100, high_per* 100)
            print(msg)

            pairs = [[0.05, 0.03], [0.07, 0.04], [0.10, 0.06], [0.15, 0.1], [0.20, 0.14], [0.30, 0.23], [0.40, 0.31], [0.50, 0.40], [0.60, 0.48]]
            for pair in pairs:
                if high_per >= pair[0] and cur_per <= pair[1]:
                    msg = '盈利ing... name = {}, cost = {}\n\ncur = {}, high = {}\n\ncur_per = {:.2f}%, high_per = {:.2f}%'.format(info['name'], info['cost'], cur_price, high_price, cur_per * 100, high_per* 100)
                    WarnBox(msg)
                    break
            ui_callback(code, msg)

class RepeatingTimer(Timer): 
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)

# def do_work():
#     stocks = Config.get_stocks()
#     for item in stocks:
#         t = RepeatingTimer(1, GetRealtimeData, [item['code'], QuitStrategy])
#         t.start()  
# do_work()

class Watch(Frame):
    msec = 1000
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._running = False
        self.timers = []
        self.stock_timer_map = {}
        stocks = Config.get_stocks()
        for item in stocks:
            strvar = StringVar()
            strvar.set('init...')
            self.stock_timer_map[item['code']] = strvar

            msg_label = Label(self, textvariable = strvar)
            msg_label.pack()

        self.flag = True


    def OnClose(self, event):
        print("closing....")

    def _update(self):
        stocks = Config.get_stocks()
        for item in stocks:
            t = RepeatingTimer(1, GetRealtimeData, [item['code'], QuitStrategy, self._settime])
            t.start()
            self.timers.append(t)


    def _settime(self, stock_code, msg):
        strvar = self.stock_timer_map[stock_code]
        strvar.set(msg)

    def start(self):
        self._update()
        self.pack(side = TOP)

if __name__ == '__main__':
    def main():
        root = Tk()
        root.title('***伟伟快看***')
        root.geometry('800x400')
        frame1 = Frame(root)
        frame1.pack(side = BOTTOM)

        mw = Watch(root)
        mywatch = Button(frame1, text = '走你...', command = mw.start)
        mywatch.pack(side = LEFT)
        mw.Bind(wx.EVT_CLOSE, mw.OnClose)

        root.mainloop()
    main()