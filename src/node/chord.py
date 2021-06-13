from .node import Node

class ChordNode(Node):
    def get_chord_node(self):
        return self

    def read_msg(self, msg: message.Message):
        return super().read_msg(msg)