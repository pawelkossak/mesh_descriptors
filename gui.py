from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from ui_interface import Ui_MainWindow
from classes import MeshSession
import sys
from time import sleep


class MeshDescriptorsWindow(QMainWindow):
    """
    Main Window class for the MeSH Descriptors application. 
    Handles UI interactions, coordinates text analysis via MeshSession, 
    and displays results in a table.

    :param parent: The parent widget of this window, defaults to None.
    :type parent: QWidget, optional
    """
    def __init__(self, parent=None):
        """
        Initializes the window, sets up the UI components, and connects signals to slots.
        """
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
        """
        Gets the list of currently stored MeSH descriptors.

        :return: A list of tuples containing (descriptor, count).
        :rtype: list
        """
        return self._descriptors

    @descriptors.setter
    def descriptors(self, value: list):
        """
        Sets the list of MeSH descriptors.

        :param value: A list of descriptor tuples.
        :type value: list
        """
        self._descriptors = value

    @property
    def searchText(self) -> str:
        """
        Gets the current search text extracted from the UI.

        :return: The medical text string used for analysis.
        :rtype: str
        """
        return self._searchText

    @searchText.setter
    def searchText(self, value: str):
        """
        Sets the search text.

        :param value: The medical text string.
        :type value: str
        """
        self._searchText = value

    def _handleSearchClicked(self):
        """
        Slot handled when the search button is clicked. 
        Triggers the text processing pipeline, fetches descriptors from the session, 
        and updates the results table and status bar.
        """
        self.ui.statusbar.showMessage("Searching for descriptors...")
        sleep(0.1)
        self.searchText = self.ui.medicalText.text()
        self.session.text = self.searchText
        self.descriptors = self.session.get_descriptors()
        if len(self.descriptors) == 0:
            self.ui.resultTable.setRowCount(0)
            self.ui.statusbar.showMessage("No descriptors found")
        elif self.descriptors[0][0] == "error":
            self.ui.resultTable.setRowCount(0)
            self.ui.statusbar.showMessage("Error occured while connecting to MeSH API, check your internet connection.")
        else:
            self.ui.resultTable.setRowCount(len(self.descriptors))
            row = 0
            for descriptor, count in self.descriptors:
                self.ui.resultTable.setItem(row, 0, QTableWidgetItem(descriptor))
                self.ui.resultTable.setItem(row, 1, QTableWidgetItem(str(count)))
                row += 1
            self.ui.statusbar.showMessage(f"Found {len(self.descriptors)} descriptors")

    def _handleSaveClicked(self):
        """
        Slot handled when the save button is clicked.
        Commands the session to save the current descriptors to a text file 
        and displays the result message in the status bar.
        """
        self.ui.statusbar.showMessage("Saving descriptors...")
        message = self.session.save_descriptors_to_txt()
        self.ui.statusbar.showMessage(message)

    def _handleGenerateChartClicked(self):
        """
        Slot handled when the chart button is clicked.
        Commands the session to generate and save a frequency chart 
        and displays the result message in the status bar.
        """
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
