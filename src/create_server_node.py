import sys
import threading

from node.utils.node_reference import NodeReference
from node.server import ServerNode


listen_ip, listen_port = sys.argv[1], sys.argv[2]
conn_node_ip, conn_node_port = sys.argv[3], sys.argv[4]

server = ServerNode(listen_ip, listen_port, NodeReference(conn_node_ip, conn_node_port))
print('Server node initialized')
thread = threading.Thread(target=server.listen)
thread.start()

while True:
    print('Enter url:')
    try:
        url_info = server.request_chord_node(input())
        print('Result:')
        print(url_info)
    except Exception as e:
        print('Exception:', e)
