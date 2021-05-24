class Node:
    def __init__(self):
        self.__component = None
        self.__connectedFromNodes = []
        self.__connectedToNodes = []

    def set_component(self, component):
        self.__component = component

    def get_component(self):
        return self.__component

    def connect_to(self, node):
        self.__connectedToNodes.append(node)
        node.__connectedFromNodes.append(self)
        assert len(node.__connectedFromNodes) <= 1

    def get_connected_nodes(self):
        return self.__connectedToNodes

    def is_connected(self):
        return len(self.__connectedFromNodes) != 0
