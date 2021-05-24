from Circuit.Node import Node


class AND:
    def __init__(self):
        self.in1 = Node()
        self.in2 = Node()
        self.out = Node()

    def get_unconnected_input_node(self):
        if not self.in1.is_connected():
            return self.in1
        elif not self.in2.is_connected():
            return self.in2
        else:
            raise Exception("Doesn't contain any unconnected nodes")


class OR:
    def __init__(self):
        self.in1 = Node()
        self.in2 = Node()
        self.out = Node()

    def get_unconnected_input_node(self):
        if not self.in1.is_connected():
            return self.in1
        elif not self.in2.is_connected():
            return self.in2
        else:
            raise Exception("Doesn't contain any unconnected nodes")


class XOR:
    def __init__(self):
        self.in1 = Node()
        self.in2 = Node()
        self.out = Node()

    def get_unconnected_input_node(self):
        if not self.in1.is_connected():
            return self.in1
        elif not self.in2.is_connected():
            return self.in2
        else:
            raise Exception("Doesn't contain any unconnected nodes")
