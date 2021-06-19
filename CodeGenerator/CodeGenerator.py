import os

from Circuit.Circuit import Circuit
from Circuit.Components import AND, OR, XOR, NOT


class CodeGenerator:
    MODULE_NAME = "rtl_code"

    __id = 0

    @staticmethod
    def __get_id():
        result = CodeGenerator.__id
        CodeGenerator.__id += 1
        return result

    @staticmethod
    def __get_node_name():
        return "a{}".format(CodeGenerator.__get_id())

    def __init__(self, circuit: Circuit):
        self.__circuit: Circuit = circuit
        self.__inputNodes = circuit.get_input_nodes()
        self.__circuitNodes = []
        self.__outputNodes = []
        self.__verilogCode = ""
        self.__mapNodesToNames = {}
        self.__name_nodes()
        self.__generate_verilog_code()

    def set_circuit(self, circuit: Circuit) -> None:
        self.__circuit = circuit
        self.__inputNodes = circuit.get_input_nodes()
        self.__circuitNodes = []
        self.__outputNodes = []
        self.__verilogCode = ""
        self.__mapNodesToNames = {}
        self.__name_nodes()
        self.__generate_verilog_code()

    def __name_nodes(self):
        CodeGenerator.__id = 0
        nodes = []
        for inputNode in self.__inputNodes:
            nodes.append(inputNode)
        while len(nodes) != 0:
            node = nodes.pop(0)
            if node in self.__mapNodesToNames.keys():
                continue
            self.__mapNodesToNames[node] = CodeGenerator.__get_node_name()
            if node not in self.__inputNodes:
                self.__circuitNodes.append(node)
            if len(node.get_connected_to_nodes()) == 0:
                self.__outputNodes.append(node)
            for connectedNode in node.get_connected_to_nodes():
                nodes.append(connectedNode.get_component().get_output_node())

    def __generate_verilog_code(self) -> None:
        verilogCode = ""
        # Add the start of the module
        verilogCode += "module {} (".format(CodeGenerator.MODULE_NAME)
        for inputNode in self.__inputNodes:
            verilogCode += "{}, ".format(self.__mapNodesToNames[inputNode])
        for outputNode in self.__outputNodes:
            verilogCode += "{}, ".format(self.__mapNodesToNames[outputNode])
        verilogCode = verilogCode[:-2]
        verilogCode += ");\n"
        verilogCode += "\n"
        # Add the direction of the ports of the module
        for inputNode in self.__inputNodes:
            verilogCode += "\tinput {};\n".format(self.__mapNodesToNames[inputNode])
        for outputNode in self.__outputNodes:
            verilogCode += "\toutput {};\n".format(self.__mapNodesToNames[outputNode])
        verilogCode += "\n"
        # Add the declaration of the internal signals
        for circuitNode in self.__circuitNodes:
            component = circuitNode.get_component()
            if isinstance(component, AND) or isinstance(component, OR) or isinstance(component, XOR):
                verilogCode += "\twire {};\n".format(self.__mapNodesToNames[circuitNode])
        verilogCode += "\n"
        # Add the rtl code of the components of the circuit
        for circuitNode in self.__circuitNodes:
            component = circuitNode.get_component()
            if isinstance(component, AND):
                verilogCode += "\tassign {} = ".format(self.__mapNodesToNames[component.get_output_node()])
                for inputNode in component.get_input_nodes():
                    previousOutputNode = inputNode.get_connected_from_node()
                    verilogCode += "{} & ".format(self.__mapNodesToNames[previousOutputNode])
                verilogCode = verilogCode[:-3] + ";\n"
            elif isinstance(component, OR):
                verilogCode += "\tassign {} = ".format(self.__mapNodesToNames[component.get_output_node()])
                for inputNode in component.get_input_nodes():
                    previousOutputNode = inputNode.get_connected_from_node()
                    verilogCode += "{} | ".format(self.__mapNodesToNames[previousOutputNode])
                verilogCode = verilogCode[:-3] + ";\n"
            elif isinstance(component, XOR):
                verilogCode += "\tassign {} = ".format(self.__mapNodesToNames[component.get_output_node()])
                for inputNode in component.get_input_nodes():
                    previousOutputNode = inputNode.get_connected_from_node()
                    verilogCode += "{} ^ ".format(self.__mapNodesToNames[previousOutputNode])
                verilogCode = verilogCode[:-3] + ";\n"
            elif isinstance(component, NOT):
                inputNode = component.get_input_node()
                previousOutputNode = inputNode.get_connected_from_node()
                verilogCode += "\tassign {} = ~{};".format(self.__mapNodesToNames[component.get_output_node()],
                                                          self.__mapNodesToNames[previousOutputNode])
        verilogCode += "\n"
        verilogCode += "endmodule"
        self.__verilogCode = verilogCode

    def get_verilog_code(self) -> str:
        return self.__verilogCode

    def generate_verilog_file(self, path=os.getcwd(), outFileName="out.v") -> None:
        f = open(os.path.join(path, outFileName), "w")
        f.write(self.get_verilog_code())
        f.close()
