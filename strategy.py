from util import Config

class QuitStrategy:
    def __init__(self, code, cur_price, high_price, ui_callback):
        info = Config.get_info_by_code(code)
        # calc
        cost = info['cost']

        if cur_price < cost:
            per = (cost - cur_price) / cost
            msg = self.tip_message(False, info['name'], info['cost'], cur_price, high_price, per, per)

            # if per >= 0.03:
                # WarnBox(msg)

            ui_callback(code, msg)
        else:
            high_per = (high_price - cost) / cost
            cur_per = (cur_price - cost) / cost

            msg = self.tip_message(True, info['name'], info['cost'], cur_price, high_price, cur_per, high_per)
            pairs = [[0.05, 0.03], [0.07, 0.04], [0.10, 0.06], [0.15, 0.1], [0.20, 0.14], [0.30, 0.23], [0.40, 0.31], [0.50, 0.40], [0.60, 0.48]]
            for pair in pairs:
                if high_per >= pair[0] and cur_per <= pair[1]:
                    # WarnBox(msg)
                    break
            ui_callback(code, msg)

    def tip_message(self, is_earn, name, cost, cur_price, high_price, cur_per, high_per):
        format_msg = '盈利ing... name = {}, cost = {}\ncur = {}, high = {}\ncur_per = {:.2f}%, high_per = {:.2f}%'.format(name, cost, cur_price, high_price, cur_per * 100, high_per* 100)
        if not is_earn:
            format_msg = '亏损ing...name = {}, cost = {}\ncur = {}, high = {}\ncur_per = -{:.2f}%'.format(name, cost, cur_price, high_price, cur_per * 100)
        return format_msg
