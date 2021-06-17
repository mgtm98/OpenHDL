from Circuit.Circuit import Circuit
from Circuit.Components import AND, OR, XOR, NOT
from Circuit.Node import Node


class CircuitGenerator:
    def __init__(self, circuitDict: dict):
        self.__circuitDict: dict = circuitDict
        self.__mapComponentNameToComponent = {}
        self.__mapOutputNodesNamesToOutputNodes = {}
        self.__mapInputNodesNamesToInputNodes = {}

    def set_circuit_dict(self, circuitDict: dict):
        self.__circuitDict = circuitDict
        self.__mapComponentNameToComponent = {}
        self.__mapOutputNodesNamesToOutputNodes = {}
        self.__mapInputNodesNamesToInputNodes = {}

    def get_circuit(self) -> Circuit:
        circuit = Circuit()
        # Map component names to components and Map output nodes names to output nodes
        for componentName in self.__circuitDict.keys():
            outputNodeName = self.__circuitDict[componentName]["output"]
            if "AND" in componentName:
                self.__mapComponentNameToComponent[componentName] = AND()
            elif "XOR" in componentName:
                self.__mapComponentNameToComponent[componentName] = XOR()
            elif "OR" in componentName and "XOR" not in componentName:
                self.__mapComponentNameToComponent[componentName] = OR()
            elif "NOT" in componentName:
                self.__mapComponentNameToComponent[componentName] = NOT()
            self.__mapOutputNodesNamesToOutputNodes[outputNodeName] = self.__mapComponentNameToComponent[
                componentName].get_output_node()
        # Loop over inputs of components and if output name is in the inputs, connect output to input
        for componentName in self.__circuitDict.keys():
            for inputNodeName in self.__circuitDict[componentName]["inputs"]:
                if inputNodeName in self.__mapOutputNodesNamesToOutputNodes.keys():
                    self.__mapOutputNodesNamesToOutputNodes[inputNodeName].connect_to(
                        self.__mapComponentNameToComponent[componentName].get_unconnected_input_node())
                else:
                    if inputNodeName in self.__mapInputNodesNamesToInputNodes.keys():
                        inputNode = self.__mapInputNodesNamesToInputNodes[inputNodeName]
                    else:
                        inputNode = Node()
                        self.__mapInputNodesNamesToInputNodes[inputNodeName] = inputNode
                        circuit.add_input_node(inputNode)
                    inputNode.connect_to(self.__mapComponentNameToComponent[componentName].get_unconnected_input_node())
        return circuit
