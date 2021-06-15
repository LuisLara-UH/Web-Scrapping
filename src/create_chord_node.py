import sys

from src.node.utils.node_reference import NodeReference
from src.node.chord import ChordNode


listen_ip, listen_port = sys.argv[1], sys.argv[2]

try:
    conn_node_ip = sys.argv[3]
    conn_node_port = sys.argv[4]
except:
    conn_node_ip = conn_node_port = None


chord = ChordNode(listen_ip, listen_port, NodeReference(conn_node_ip, conn_node_port))

chord.listen()