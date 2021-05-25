class Node:
    def __init__(self):
        self.__component = None
        self.__connectedFromNode = None
        self.__connectedToNodes = []

    def set_component(self, component):
        self.__component = component

    def get_component(self):
        return self.__component

    def connect_to(self, node):
        assert node.__connectedFromNode is None
        self.__connectedToNodes.append(node)
        node.__connectedFromNode = self

    def get_connected_to_nodes(self):
        return self.__connectedToNodes

    def get_connected_from_node(self):
        return self.__connectedFromNode

    def is_connected(self):
        return len(self.__connectedFromNodes) != 0
