from Circuit.Circuit import Circuit
from Circuit.Components import AND, OR, XOR
from Circuit.Node import Node
from CodeGenerator.CircuitGenerator import CircuitGenerator
from CodeGenerator.CodeGenerator import CodeGenerator
from ImageProcessing.identify import extract_circuit

from PySide2.QtWidgets import QApplication
from GUI.mainWindow import MainWindow
import sys


app = QApplication(sys.argv)
m = MainWindow()

def generate(path):
    circuitDict = path
    circuitGenerator = CircuitGenerator(extract_circuit(circuitDict))
    circuit = circuitGenerator.get_circuit()
    codeGenerator = CodeGenerator(circuit)
    codeGenerator.generate_verilog_file()
    m.img_widget.setImagePath("out.PNG")
    f = open("out.v", "r")
    lines = f.readlines()
    f.close()
    content = "".join(lines)
    m.editor.setPlainText(content)


def main():
    m.convert.connect(generate)
    m.show()
    sys.exit(app.exec_())

main()
