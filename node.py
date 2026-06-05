#3
class Node:
    def __init__(self, name):
        self.name=name
        self.connections=[] # 2 вузли 
    def connect(self, node):
        self.connections.append(node)
        node.connections.append(self)
class Router(Node):
    pass
