class NGLStorage:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def store_nodes(self, nodes):
        self.nodes.extend(nodes)

    def get_nodes(self):
        return self.nodes
