from Circuit.Node import Node


class AND:
    def __init__(self):
        self.__inputs = []
        self.__out = Node()
        self.__out.set_component(self)

    def get_unconnected_input_node(self):
        node = Node()
        self.__inputs.append(node)
        node.set_component(self)
        return node

    def get_input_nodes(self):
        return self.__inputs

    def get_output_node(self):
        return self.__out


class OR:
    def __init__(self):
        self.__inputs = []
        self.__out = Node()
        self.__out.set_component(self)

    def get_unconnected_input_node(self):
        node = Node()
        self.__inputs.append(node)
        node.set_component(self)
        return node

    def get_input_nodes(self):
        return self.__inputs

    def get_output_node(self):
        return self.__out


class XOR:
    def __init__(self):
        self.__inputs = []
        self.__out = Node()
        self.__out.set_component(self)

    def get_unconnected_input_node(self):
        node = Node()
        self.__inputs.append(node)
        node.set_component(self)
        return node

    def get_input_nodes(self):
        return self.__inputs

    def get_output_node(self):
        return self.__out
