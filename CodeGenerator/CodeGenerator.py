import os

from Circuit.Circuit import Circuit


class CodeGenerator:
    def __init__(self, circuit: Circuit):
        self.__circuit = circuit
        self.__outputNodes = []
        self.__verilogCode = ""

    def set_circuit(self, circuit: Circuit) -> None:
        self.__circuit = circuit

    def __generate_verilog_code(self) -> None:
        verilogCode = ""
        self.__verilogCode = verilogCode

    def get_verilog_code(self) -> str:
        return self.__verilogCode

    def generate_verilog_file(self, path="", outFileName="out.txt") -> None:
        f = open(os.path.join(path, outFileName), "w")
        f.write(self.get_verilog_code())
        f.close()
