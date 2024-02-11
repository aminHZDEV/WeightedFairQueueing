from queue import Queue


class Buffer:
    def __init__(self, addr: str = ""):
        self.buffer = Queue()
        self.addr = addr
