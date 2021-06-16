import sys

from node.utils.node_reference import NodeReference
from node.chord import ChordNode


listen_ip, listen_port = sys.argv[1], sys.argv[2]

try:
    conn_node = NodeReference(sys.argv[3], sys.argv[4])
except:
    conn_node = None


chord = ChordNode(listen_ip, listen_port, conn_node)

chord.listen()