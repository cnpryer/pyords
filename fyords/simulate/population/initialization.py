class InitializationBase:
    def __init__(self):
        pass

class SimpleInitialization(InitializationBase):
    def __init__(self):
        InitializationBase.__init__(self)

    def run(self):
        return []
