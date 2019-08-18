from .smd import Smd

class SmdApp():
    def __init__(self):
        self.smd = Smd()

    def main(self):
        self.smd.render()
        return 0
