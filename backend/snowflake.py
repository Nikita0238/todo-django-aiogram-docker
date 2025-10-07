import time
import threading
import os

class Snowflake:
    def __init__(self, node_id=1, epoch=1577836800000):
        self.node_id = node_id & 0x3FF
        self.epoch = epoch
        self.sequence = 0
        self.last_ts = -1
        self.lock = threading.Lock()

    def _timestamp(self):
        return int(time.time() * 1000)

    def generate(self):
        with self.lock:
            ts = self._timestamp()
            if ts == self.last_ts:
                self.sequence = (self.sequence + 1) & 0xFFF
                if self.sequence == 0:
                    while ts <= self.last_ts:
                        ts = self._timestamp()
            else:
                self.sequence = 0
                self.last_ts = ts
            id_ = ((ts - self.epoch) << (10 + 12)) | (self.node_id << 12) | self.sequence
            return id_

NODE_ID = int(os.getenv('SNOWFLAKE_NODE_ID', '1'))
_generator = Snowflake(node_id=NODE_ID)
def get_snowflake_id():
    return _generator.generate()
