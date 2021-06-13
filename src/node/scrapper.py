from .node import Node
import urllib.request

class ScrapperNode(Node):
    def get_url_info(self, url: str):
        webUrl = urllib.request.urlopen(url)
        return webUrl.read()