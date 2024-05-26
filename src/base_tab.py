import logging
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton,
    QSpinBox, QTextEdit, QProgressBar, QFileDialog, QCheckBox, QScrollArea, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QThreadPool
from worker import Worker


class BaseTab(QWidget):
    """
    Base tab for running processes with advanced options and progress tracking.
    """
    def __init__(self, title: str, run_process: callable, emitter: logging.Logger):
        """
        Initialize the base tab.

        Args:
            title (str): The title of the tab.
            run_process (callable): The function to run when the process is started.
            emitter (logging.Logger): The log emitter for logging messages.
        """
        super().__init__()
        self.title = title
        self.run_process = run_process
        self.emitter = emitter
        self.init_logging()
        self.initUI()

    def init_logging(self):
        """
        Initialize logging by connecting the emitter's log signal to the log message handler.
        """
        self.emitter.log_message.connect(self.append_log_message)

    def append_log_message(self, message: str):
        """
        Append log messages to the output text area.

        Args:
            message (str): The log message to append.
        """
        self.output_text.append(message)

    def initUI(self):
        """
        Initialize the user interface components.
        """
        self.layout = QVBoxLayout()

        # Directory Input and Browse Button
        self.init_directory_input()

        # Advanced Options
        self.init_advanced_options()

        # Start Button
        self.start_btn = QPushButton(f'Start {self.title}', self)
        self.start_btn.clicked.connect(self.on_start)
        self.layout.addWidget(self.start_btn)

        # Output Text Box and Progress Bar
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

    def init_directory_input(self):
        """
        Initialize the directory input and browse button.
        """
        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit(self)
        self.browse_dir_button = QPushButton('Browse Directory...', self)
        self.browse_dir_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(QLabel("Input Directory:"))
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.browse_dir_button)
        container = QWidget()
        container.setLayout(dir_layout)
        self.layout.addWidget(container)

    def init_advanced_options(self):
        """
        Initialize the advanced options section with a toggle button.
        """
        self.advanced_options_button = QPushButton('Advanced Options', self)
        self.advanced_options_button.setCheckable(True)
        self.advanced_options_button.setChecked(False)
        self.advanced_options_button.toggled.connect(self.toggle_advanced_options)

        self.advanced_options_area = QScrollArea(self)
        self.advanced_options_area.setWidgetResizable(True)
        self.advanced_options_content = QWidget()
        self.advanced_options_layout = QFormLayout(self.advanced_options_content)

        self.advanced_options_content.setLayout(self.advanced_options_layout)
        self.advanced_options_area.setWidget(self.advanced_options_content)

        self.advanced_options_area.setVisible(False)
        self.layout.addWidget(self.advanced_options_button)
        self.layout.addWidget(self.advanced_options_area)

    def toggle_advanced_options(self, checked: bool):
        """
        Toggle the visibility of the advanced options section.

        Args:
            checked (bool): Whether the advanced options are checked (visible).
        """
        self.advanced_options_area.setVisible(checked)

    def on_start(self):
        """
        Start the process when the start button is clicked.
        """
        input_path = self.dir_input.text()
        if not input_path:
            QMessageBox.warning(self, "Error", "Please select a directory first.")
            return

        params = self.collect_params()
        self.execute_process(input_path, **params)

    def collect_params(self) -> dict:
        """
        Collect parameters for the process.

        Returns:
            dict: The collected parameters.
        """
        return {}

    def execute_process(self, input_path: str, **params):
        """
        Execute the process using a worker thread.

        Args:
            input_path (str): The input directory path.
            params (dict): Additional parameters for the process.
        """
        self.progress_bar.setValue(0)
        self.output_text.clear()

        worker = Worker(self.run_process, input_path, **params)
        worker.signals.result.connect(self.on_process_complete)
        worker.signals.error.connect(self.on_process_error)
        worker.signals.progress.connect(self.update_progress)
        QThreadPool.globalInstance().start(worker)

    def on_process_complete(self, result: str):
        """
        Handle the process completion signal.

        Args:
            result (str): The result message from the process.
        """
        self.output_text.append(result)
        self.progress_bar.setValue(100)
        QMessageBox.information(self, "Success", f"{self.title} completed successfully.")

    def on_process_error(self, error: tuple):
        """
        Handle the process error signal.

        Args:
            error (tuple): The error information.
        """
        self.output_text.append(f"Error: {error}")
        self.progress_bar.setValue(0)
        QMessageBox.critical(self, "Error", f"An error occurred during {self.title}: {error}")

    def update_progress(self, value: int):
        """
        Update the progress bar value.

        Args:
            value (int): The progress value to set.
        """
        self.progress_bar.setValue(value)

    def browse_directory(self):
        """
        Open a directory dialog for the user to select an input directory.
        """
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.dir_input.setText(directory)
