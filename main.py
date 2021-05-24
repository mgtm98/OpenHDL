from Circuit.Circuit import Circuit
from Circuit.Components import AND, OR
from Circuit.Node import Node

if __name__ == '__main__':
    and1 = AND()
    and2 = AND()
    or1 = OR()
    in1 = Node()
    in2 = Node()
    in3 = Node()
    in1.connect_to(and1.get_unconnected_input_node())
    in2.connect_to(and1.get_unconnected_input_node())
    in2.connect_to(or1.get_unconnected_input_node())
    in3.connect_to(or1.get_unconnected_input_node())
    and1.get_output_node().connect_to(and2.get_unconnected_input_node())
    or1.get_output_node().connect_to(and2.get_unconnected_input_node())
    circuit = Circuit()
    circuit.add_input_node(in1)
    circuit.add_input_node(in2)
    circuit.add_input_node(in3)
