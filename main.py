from Circuit.Circuit import Circuit
from Circuit.Components import AND, OR, XOR
from Circuit.Node import Node
from CodeGenerator.CircuitGenerator import CircuitGenerator
from CodeGenerator.CodeGenerator import CodeGenerator
from ImageProcessing.identify import extract_circuit

if __name__ == '__main__':
    # and1 = AND()
    # and2 = AND()
    # or1 = OR()
    # in1 = Node()
    # in2 = Node()
    # in3 = Node()
    # in1.connect_to(and1.get_unconnected_input_node())
    # in2.connect_to(and1.get_unconnected_input_node())
    # in2.connect_to(or1.get_unconnected_input_node())
    # in3.connect_to(or1.get_unconnected_input_node())
    # and1.get_output_node().connect_to(and2.get_unconnected_input_node())
    # or1.get_output_node().connect_to(and2.get_unconnected_input_node())
    # circuit = Circuit()
    # circuit.add_input_node(in1)
    # circuit.add_input_node(in2)
    # circuit.add_input_node(in3)
    # # circuit.add_output_node(and2.get_output_node())
    # codeGenerator = CodeGenerator(circuit)
    # codeGenerator.generate_verilog_file()

    # print(extract_circuit("G:\\College\\Second Term\\Image Processing\\Project\\OpenHDL\\ImageProcessing\\images\\test_cir3_x3.PNG"))

    # circuitDict = extract_circuit("C:\\Users\\mgtmP\\Desktop\\4th\\Image\\OpenHDL\\ImageProcessing\\images\\test_cir3_x3.PNG")

    circuitDict = {'AND0': {'inputs': ['N1', 'J0'], 'output': 'N2'},
                   'OR1': {'inputs': ['N5', 'N10'], 'output': 'J0'},
                   'AND3': {'inputs': ['J0', 'J3'], 'output': 'N13'},
                   'AND4': {'inputs': ['N16', 'N18'], 'output': 'J3'},
                   'NOT2': {'inputs': ['N13'], 'output': 'N12'}
                   }
    circuitGenerator = CircuitGenerator(circuitDict)
    circuit = circuitGenerator.get_circuit()
    codeGenerator = CodeGenerator(circuit)
    codeGenerator.generate_verilog_file()
