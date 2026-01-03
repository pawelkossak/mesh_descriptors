from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from ui_interface import Ui_MainWindow
from classes import MeshSession
import sys
import datetime

class MeshDescriptorsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._descriptors = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.searchButton.clicked.connect(self._handleSearchClicked)
        self.ui.saveButton.clicked.connect(self._handleSaveClicked)

    @property
    def descriptors(self) -> list:
        return self._descriptors
    
    @descriptors.setter
    def descriptors(self, value: list):
        self._descriptors = value

    def _handleSearchClicked(self):
        session = MeshSession(self.ui.medicalText.text())
        self.descriptors = session.get_descriptors()
        if len(self.descriptors) == 0:
            self.ui.resultTable.setRowCount(1)
            self.ui.resultTable.setItem(0, 0, QTableWidgetItem("No descriptors found"))
            self.ui.resultTable.setItem(0, 1, QTableWidgetItem(""))
        else:
            self.ui.resultTable.setRowCount(len(self.descriptors))
            row = 0
            for descriptor, count in self.descriptors:
                self.ui.resultTable.setItem(row, 0, QTableWidgetItem(descriptor))
                self.ui.resultTable.setItem(row, 1, QTableWidgetItem(str(count)))
                row += 1
    
    def _handleSaveClicked(self):
        if self.descriptors:
            file_name = f"mesh_descriptors{datetime.datetime.now().strftime("%d%m%Y%H%M%S")}.txt"
            with open(file_name, "w") as f:
                for descriptor, count in self.descriptors:
                    f.write(f"{descriptor}: {count}\n")
            self.ui.resultTable.setRowCount(1)
            self.ui.resultTable.setItem(0, 0, QTableWidgetItem(f"Descriptors saved successfully as {file_name}"))
        else:
            self.ui.resultTable.setRowCount(1)
            self.ui.resultTable.setItem(0, 0, QTableWidgetItem("No descriptors to save"))


def guiMain(args):
    app = QApplication(args)
    window = MeshDescriptorsWindow()
    window.resize(800, 600)
    window.show()
    app.exec()

if __name__ == "__main__":
    guiMain(sys.argv)
