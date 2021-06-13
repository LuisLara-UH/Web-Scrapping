from zmq.sugar.frame import Message
from .node import Node
from .utils import message
import urllib.request

class ScrapperNode(Node):
    def get_url_info(self, url: str):
        webUrl = urllib.request.urlopen(url)
        return webUrl.read()

    def read_msg(self, msg: message.Message):
        if not msg.action == message.GET_SCRAP_URL:
            raise Exception("Invalid action. Scrapper node cannot do: " + msg.action)

        url_info = self.get_url_info(msg.parameters)
        if url_info is None or url_info == '':
            raise Exception("Couldnt read from " + msg.parameters)

        return message.Message(action=message.RET_SCRAP_URL, parameters=url_info)