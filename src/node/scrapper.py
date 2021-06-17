from node.utils.chord_messages import req_post_finger
from zmq.sugar.frame import Message
from .node import Node, NodeReference
from .utils import message
import urllib.request

class ScrapperNode(Node):
    def __init__(self, listen_ip, listen_port, conn_node: NodeReference):
        if conn_node is None:
            raise Exception("Scrapper node must receive address of connecting node")
        super().__init__(listen_ip, listen_port, conn_node)

        self.req_set_scrap_node(self.chord_node)

    def get_url_info(self, url: str):
        print('gets here')
        webUrl = urllib.request.urlopen(url)
        return webUrl.read()

    def read_msg(self, msg: message.Message):
        ret_msg = super().read_msg(msg)
        if not ret_msg is None:
            return ret_msg

        if not msg.action == message.GET_SCRAP_URL:
            raise Exception("Invalid action. Scrapper node cannot do: " + msg.action)

        url_info = self.get_url_info(msg.parameters)
        if url_info is None or url_info == '':
            raise Exception("Couldnt read from " + msg.parameters)

        return message.Message(action=message.RET_SCRAP_URL, parameters=url_info)

    def req_set_scrap_node(self, chord_node: NodeReference):
        req_msg = message.Message(action=message.GET_POST_SCRAP_NODE, parameters=NodeReference(ip=self.ip, port=self.port).pack())
        rep_msg = self.sender.request(chord_node, req_msg)
        
        if not rep_msg.action == message.RET_POST_SCRAP_NODE:
            raise Exception("Invalid answer. Scrapper received action: " + rep_msg.action)