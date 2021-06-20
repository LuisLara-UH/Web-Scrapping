import threading

from node.node import NodeReference
from node.utils.message import Message
from create_chord_node import start_chord_node
from node.scrapper import ScrapperNode


def test_message():
    actions = ['get', 'get-chord', 'ret-chord']
    parameters = ['23%89', '1%4%ip', '127.0.0.1%8888']

    for i in range(len(actions)):
        msg = Message(action=actions[i], parameters=parameters[i])
        assert msg.action == actions[i], "Action not set correctly"
        assert msg.parameters == parameters[i], "Parameters not set correctly"

        msg_pack = msg.pack()
        assert msg_pack == actions[i] + '%' + parameters[i], "Message not packed correctly"

        msg.unpack(actions[i] + '%' + parameters[i])
        assert msg.action == actions[i], "Action not unpacked correctly"
        assert msg.parameters == parameters[i], "Parameters not unpacked correctly"


def test_scrapper():
    scrapper = ScrapperNode('8880', NodeReference('localhost', '8881'))
    urls = ['https://www.google.com']

    for url in urls:
        print(scrapper.get_url_info(url=url))


threading.Thread(target=start_chord_node, args=('localhost', '8880')).start()
threading.Thread(target=start_chord_node, args=('localhost', '8881', 'localhost', '8880')).start()