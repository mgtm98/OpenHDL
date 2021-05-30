from Circuit.Node import Node


class Circuit:
    def __init__(self):
        self.__inputNodes = []
        self.__outputNodes = []

    def add_input_node(self, node: Node):
        self.__inputNodes.append(node)

    def get_input_nodes(self):
        return self.__inputNodes

    def add_output_node(self, node: Node):
        self.__outputNodes.append(node)

    def get_output_nodes(self):
        return self.__outputNodes
