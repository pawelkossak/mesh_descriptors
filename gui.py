from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from ui_interface import Ui_MainWindow
from classes import MeshSession
import sys
import datetime
from time import sleep
import json
import os

class MeshDescriptorsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._descriptors = []
        self._config = json.load(open("config.json"))
        self._searchText = ""
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
    def config(self) -> dict:
        return self._config
    
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
        session = MeshSession(self.ui.medicalText.text())
        self.descriptors = session.get_descriptors()
        if len(self.descriptors) == 0:
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
        if self.descriptors:
            file_folder = self.config["text_file_save_path"]
            if not file_folder.endswith('/'):
                file_folder += '/'
            if not os.path.exists(file_folder):
                os.makedirs(file_folder)
            file_name = f"mesh_descriptors{datetime.datetime.now().strftime("%d%m%Y%H%M%S")}.txt"
            file_path = os.path.join(file_folder, file_name)
            with open(file_path, "w") as f:
                f.write(f"Medical Text: {self.searchText}\n\nMost common MeSH Descriptors found:\n")
                for descriptor, count in self.descriptors:
                    f.write(f"{descriptor} - {count}\n")
            self.ui.statusbar.showMessage(f"Descriptors saved successfully as {file_name}")
        else:
            self.ui.statusbar.showMessage("No descriptors to save")

    
    def _handleGenerateChartClicked(self):
        self.ui.statusbar.showMessage("Generating chart...")
        if self.descriptors:
            fig, ax = plt.subplots()
            descriptors, counts = zip(*self.descriptors)
            ax.bar(descriptors, counts)
            ax.set_ylabel("Count")
            ax.set_title("MeSH Descriptors Frequency")
            ax.set_yticks(range(0, max(counts)+1))
            ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            plt.xticks(rotation=45, ha='right')
            chart_folder = self.config["chart_save_path"]
            if not chart_folder.endswith('/'):
                chart_folder += '/'
            if not os.path.exists(chart_folder):
                os.makedirs(chart_folder)
            chart_file_name = f"mesh_descriptors_chart{datetime.datetime.now().strftime('%d%m%Y%H%M%S')}.png"
            chart_path = os.path.join(chart_folder, chart_file_name)
            plt.savefig(chart_path, format='png')
            sleep(0.1)
            self.ui.statusbar.showMessage(f"Chart saved successfully as {chart_file_name}")
            plt.show()



def guiMain(args):
    app = QApplication(args)
    window = MeshDescriptorsWindow()
    window.resize(800, 600)
    window.show()
    app.exec()

if __name__ == "__main__":
    guiMain(sys.argv)
