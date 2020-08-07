import time
from threading import Timer
from util import Config
from util import WarnBox
from get_data import GetRealtimeData
from strategy import QuitStrategy
from tkinter import *

c = Config()

# past7 = time.time() - 604800
# past7_str = time.strftime("%Y%m%d", time.localtime(past7))

# # ts.set_token("efa59ba827607d4a4bb71670cc686067906873ebd0ae887f02057be6")

# now_str = time.strftime("%Y%m%d", time.localtime(time.time()))

# pro = ts.pro_api()
# df = pro.daily(ts_code='600000.SH', start_date=past7_str, end_date=now_str)
# print(df)


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

        self.start()

    def on_close(self):
        print("watch closing....")
        for t in self.timers:
            t.cancel()

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
        # mywatch = Button(frame1, text = '走你...', command = mw.start)
        # mywatch.pack(side = LEFT)

        def on_closing():
            mw.on_close()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    main()