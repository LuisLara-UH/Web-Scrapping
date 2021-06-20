import sys
import threading

from node.utils.node_reference import NodeReference
from node.chord import ChordNode


listen_ip, listen_port = sys.argv[1], sys.argv[2]

try:
    conn_node = NodeReference(sys.argv[3], sys.argv[4])
except:
    conn_node = None


chord = ChordNode(listen_ip, listen_port, conn_node)

thread = threading.Thread(target=chord.stabilize)
thread.start()

# thread = threading.Thread(target=chord.fix_fingers)
# thread.start()

# thread = threading.Thread(target=chord.check_succcessor)
# thread.start()

chord.listen()
