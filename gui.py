from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from ui_interface import Ui_MainWindow
from classes import MeshSession
import sys

class MeshDescriptorsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.searchButton.clicked.connect(self._handleSearchClicked)

    def _handleSearchClicked(self):
        session = MeshSession(self.ui.medicalText.text())
        descriptors = session.get_descriptors()
        if len(descriptors) == 0:
            self.ui.resultTable.setRowCount(1)
            self.ui.resultTable.setItem(0, 0, QTableWidgetItem("No descriptors found"))
            self.ui.resultTable.setItem(0, 1, QTableWidgetItem(""))
        else:
            self.ui.resultTable.setRowCount(len(descriptors))
            row = 0
            for descriptor, count in descriptors:
                self.ui.resultTable.setItem(row, 0, QTableWidgetItem(descriptor))
                self.ui.resultTable.setItem(row, 1, QTableWidgetItem(str(count)))
                row += 1

def guiMain(args):
    app = QApplication(args)
    window = MeshDescriptorsWindow()
    window.setWindowTitle("Mesh Descriptors")
    window.resize(800, 600)
    window.show()
    app.exec()

if __name__ == "__main__":
    guiMain(sys.argv)
