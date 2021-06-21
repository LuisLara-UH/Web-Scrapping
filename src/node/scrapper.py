from node.utils.codifiers import code_url_info
import threading

from .node import Node, NodeReference
from .utils import message
from .utils.web_node import WebNode


class ScrapperNode(Node):
    def __init__(self, listen_ip, listen_port, conn_node: NodeReference):
        if conn_node is None:
            raise Exception("Scrapper node must receive address of connecting node")
        super().__init__(listen_ip, listen_port, conn_node)

        self.req_set_scrap_node(self.chord_node)

    def get_url_info(self, url: str):
        print('Scrapping url', url, 'with depth 3...')
        web_node = WebNode(url=url)

        thread = threading.Thread(target=self.send_urls_info, args=[web_node])
        thread.start()

        print('Se escrapeo:', web_node.html)
        return web_node.html

    def send_urls_info(self, web_node: WebNode):
        assert self.chord_node, 'Chord node not found'

        for index in range(len(web_node.level_one_links)):
            url = web_node.level_one_links[index]
            url_info = web_node.level_one_html[index]
            self.req_set_url_info(url=url, url_info=url_info)

        for index in range(len(web_node.level_two_links)):
            url = web_node.level_two_links[index]
            url_info = web_node.level_two_html[index]
            self.req_set_url_info(url=url, url_info=url_info)

    def read_msg(self, msg: message.Message):
        ret_msg = super().read_msg(msg)
        if ret_msg is not None:
            return ret_msg

        if not msg.action == message.GET_SCRAP_URL:
            raise Exception("Invalid action. Scrapper node cannot do: " + msg.action)

        url_info = self.get_url_info(msg.parameters)
        if url_info is None or url_info == '':
            url_info = ''
            print("Couldn't read from " + msg.parameters)

        return message.Message(action=message.RET_SCRAP_URL, parameters=url_info)

    def req_set_scrap_node(self, chord_node: NodeReference):
        req_msg = message.Message(action=message.GET_POST_SCRAP_NODE,
                                  parameters=NodeReference(ip=self.ip, port=self.port).pack())
        rep_msg = self.sender.request(chord_node, req_msg)

        if not rep_msg.action == message.RET_POST_SCRAP_NODE:
            raise Exception("Invalid answer. Scrapper received action: " + rep_msg.action)

    def req_set_url_info(self, url: str, url_info: str):
        url_pack = code_url_info(url=str(url), url_info=str(url_info))
        req_msg = message.Message(action=message.GET_SET_URL, parameters=url_pack)
        rep_msg = self.sender.request(self.chord_node, req_msg)

        assert rep_msg.action == message.RET_SET_URL, 'Invalid answer. Scrapper received action: ' + rep_msg.action
