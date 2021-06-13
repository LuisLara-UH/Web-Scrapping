from .node import Node
from .utils import message

class ServerNode(Node):
    def request_chord_node(self, url: str):
        req_msg = message.Message(action=message.GET_CHORD_URL, parameters=url)

        rep_msg = self.request(self.chord_node, req_msg)
        if not rep_msg.action == message.RET_CHORD_URL:
            raise Exception("Invalid answer. Server received action: " + rep_msg.action)
        
        if rep_msg.parameters == '':
            raise Exception("Invalid answer. Received empty information at server node")

        return rep_msg.parameters

    def read_msg(self, msg: message.Message):
        if not msg.action == message.GET_URL_INFO:
            raise Exception("Invalid action. Server node cannot do: " + msg.action)

        url_info = self.request_chord_node(msg.parameters)

        return message.Message(action=message.RET_URL_INFO, parameters=url_info)
