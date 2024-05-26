import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from gui.lasindex_tab import LasIndexTab
from gui.lasinfo_tab import LasInfoTab
from utils.utilities import load_config, setup_logging

class MainWindow(QMainWindow):
    """
    Main window class for the LiDAR Processing Wizard application.
    Initializes the user interface and sets up the tabs for different
    processing tasks.
    """
    def __init__(self):
        super().__init__()
        self.config = self.load_and_setup_config()
        self.initUI()

    def load_and_setup_config(self) -> dict:
        """
        Load configuration and set up logging.

        Returns:
            dict: Configuration dictionary loaded from the config file.
        """
        config = load_config()
        setup_logging(
            config['Logging']['LogDirectory'],
            config['Logging']['LogFile'],
            config['Logging']['LogLevel']
        )
        return config

    def initUI(self):
        """
        Initialize the user interface, including setting up tabs for
        different processing tasks.
        """
        self.setWindowTitle('LiDAR Processing Wizard')
        self.setGeometry(300, 300, 800, 600)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        default_directory = self.config['Paths']['DefaultDirectory']

        self.add_tabs(default_directory)

    def add_tabs(self, default_directory: str):
        """
        Add tabs for different processing tasks.

        Args:
            default_directory (str): The default directory path for processing.
        """
        lasindex_tab = LasIndexTab(default_directory)
        lasinfo_tab = LasInfoTab(default_directory)

        self.tab_widget.addTab(lasindex_tab, "Index")
        self.tab_widget.addTab(lasinfo_tab, "Info")

def main():
    """
    Main entry point of the application. Sets up the application and
    displays the main window.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
