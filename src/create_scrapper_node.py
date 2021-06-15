import sys

from src.node.utils.node_reference import NodeReference
from src.node.scrapper import ScrapperNode


listen_ip, listen_port = sys.argv[1], sys.argv[2]
conn_node_ip, conn_node_port = sys.argv[3], sys.argv[4]

scrapper = ScrapperNode(listen_port, listen_ip, NodeReference(conn_node_ip, conn_node_port))

scrapper.listen()
