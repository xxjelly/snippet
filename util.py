import os
import yaml

import tkinter
import tkinter.messagebox as mbox


class WarnBox():
    def __init__(self, msg):
        root=tkinter.Tk()
        root.title('***伟伟快看***')
        root.geometry('300x150')
        root.resizable(False, False)
        tkinter.Label(root, text=msg, width=300, height=150).pack()
        root.mainloop()

class Config():
    configs = {}
    code_name_map = {}

    def __init__(self):
        _dir, _filename = os.path.split(__file__)
        config_path = os.path.join(_dir, "config.yml")
        with open(config_path, encoding = "utf-8") as content:
            Config.configs = yaml.load(content, Loader = yaml.FullLoader)

        for item in Config.configs['stocks']:
            Config.code_name_map[item['code']] = {'name': item['name'], 'cost': item['cost']}

    @staticmethod
    def get_stocks():
        return Config.configs['stocks']

    @staticmethod
    def get_info_by_code(code):
        return Config.code_name_map[code]
