class Translator:
    name = 'default_translater'
    event = None
    pri = 1000
    bot = None
    cfg = None

    def __init__(self, fnc_dict):
        for key, fnc in fnc_dict:
            setattr(self, key, fnc)

    def load(self, bot, cfg):
        self.bot = bot
        self.cfg = cfg
    
    def match(self, e):
        pass

    def deal(self, e):
        pass
