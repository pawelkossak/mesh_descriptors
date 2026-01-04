from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from ui_interface import Ui_MainWindow
from classes import MeshSession
import sys
from time import sleep


class MeshDescriptorsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._descriptors = []
        self._searchText = ""
        self.session = MeshSession("")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.searchButton.clicked.connect(self._handleSearchClicked)
        self.ui.saveButton.clicked.connect(self._handleSaveClicked)
        self.ui.chartButton.clicked.connect(self._handleGenerateChartClicked)

    @property
    def descriptors(self) -> list:
        return self._descriptors

    @descriptors.setter
    def descriptors(self, value: list):
        self._descriptors = value

    @property
    def searchText(self) -> str:
        return self._searchText

    @searchText.setter
    def searchText(self, value: str):
        self._searchText = value

    def _handleSearchClicked(self):
        self.ui.statusbar.showMessage("Searching for descriptors...")
        sleep(0.1)
        self.searchText = self.ui.medicalText.text()
        self.session.text = self.searchText
        self.descriptors = self.session.get_descriptors()
        if len(self.descriptors) == 0:
            self.ui.resultTable.setRowCount(0)
            self.ui.statusbar.showMessage("No descriptors found")
        else:
            self.ui.resultTable.setRowCount(len(self.descriptors))
            row = 0
            for descriptor, count in self.descriptors:
                self.ui.resultTable.setItem(row, 0, QTableWidgetItem(descriptor))
                self.ui.resultTable.setItem(row, 1, QTableWidgetItem(str(count)))
                row += 1
            self.ui.statusbar.showMessage(f"Found {len(self.descriptors)} descriptors")

    def _handleSaveClicked(self):
        self.ui.statusbar.showMessage("Saving descriptors...")
        message = self.session.save_descriptors_to_txt()
        self.ui.statusbar.showMessage(message)

    def _handleGenerateChartClicked(self):
        self.ui.statusbar.showMessage("Generating chart...")
        message = self.session.generate_and_save_chart()
        self.ui.statusbar.showMessage(message)


def guiMain(args):
    app = QApplication(args)
    window = MeshDescriptorsWindow()
    window.resize(800, 600)
    window.show()
    app.exec()


if __name__ == "__main__":
    guiMain(sys.argv)
