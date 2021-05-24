from Circuit.Node import Node


class AND:
    def __init__(self):
        self.__inputs = []
        self.__out = Node()

    def get_unconnected_input_node(self):
        node = Node()
        self.__inputs.append(node)
        return node

    def get_input_nodes(self):
        return self.__inputs

    def get_output_node(self):
        return self.__out


class OR:
    def __init__(self):
        self.__inputs = []
        self.__out = Node()

    def get_unconnected_input_node(self):
        node = Node()
        self.__inputs.append(node)
        return node

    def get_input_nodes(self):
        return self.__inputs

    def get_output_node(self):
        return self.__out


class XOR:
    def __init__(self):
        self.__inputs = []
        self.__out = Node()

    def get_unconnected_input_node(self):
        node = Node()
        self.__inputs.append(node)
        return node

    def get_input_nodes(self):
        return self.__inputs

    def get_output_node(self):
        return self.__out
