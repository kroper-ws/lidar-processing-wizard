import logging
from PyQt5.QtWidgets import QCheckBox, QSpinBox, QLineEdit, QVBoxLayout, QFileDialog
from gui.base_tab import BaseTab
from utils.form_builder import FormBuilder
from processing.run_lasinfo import run_lasinfo
from processing.params_config import get_param_group, load_params

class LasInfoTab(BaseTab):
    """
    Tab for viewing LAS file information. Inherits from BaseTab.
    """
    def __init__(self, default_directory: str, emitter: logging.Logger):
        """
        Initialize the LAS Info tab.

        Args:
            default_directory (str): The default directory path.
            emitter (logging.Logger): The log emitter for logging messages.
        """
        self.default_directory = default_directory
        params = load_params()
        self.LASINFO_PARAMS = get_param_group(params, "LASINFO_PARAMS")
        super().__init__('View LAS Info', self.run_process, emitter)

    def initUI(self):
        """
        Initialize the user interface components for the LAS Info tab.
        """
        super().initUI()
        self.dir_input.setText(self.default_directory)

        self.form_layout = QVBoxLayout()
        form_builder = FormBuilder(self.form_layout)
        self.params_widgets = {}

        self.init_parameters(form_builder)

        self.advanced_options_layout.addLayout(self.form_layout)

    def init_parameters(self, form_builder: FormBuilder):
        """
        Initialize parameters for different sections using the form builder.

        Args:
            form_builder (FormBuilder): The form builder instance.
        """
        for param, config in self.LASINFO_PARAMS.items():
            if config['type'] == 'checkbox':
                self.params_widgets[param] = form_builder.add_checkbox(config['label'], config.get('default', False))
            elif config['type'] == 'spinbox':
                self.params_widgets[param] = form_builder.add_spinbox(config['label'], config['min'], config['max'], config.get('default'))
            elif config['type'] == 'lineedit']:
                self.params_widgets[param] = form_builder.add_lineedit(config['label'], config.get('default', ''))

    def collect_params(self) -> dict:
        """
        Collect parameters from the user inputs.

        Returns:
            dict: The collected parameters.
        """
        params = {}
        for param, widget in self.params_widgets.items():
            if isinstance(widget, QCheckBox):
                params[param] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                if widget.value() != widget.minimum() or widget.minimum() != 1:
                    params[param] = widget.value()
            elif isinstance(widget, QLineEdit):
                text = widget.text()
                if text:
                    params[param] = text
        return params

    def run_process(self, input_path: str, **params):
        """
        Run the LAS info process.

        Args:
            input_path (str): The input directory path.
            params (dict): Additional parameters for the process.
        """
        try:
            logging.info("Starting LAS info process...")
            result = run_lasinfo(input_path, **params)
            logging.info("LAS info process completed.")
            self.output_text.append(result)  # Append the result to the console
            return result
        except Exception as e:
            logging.error(f"An error occurred during LAS info processing: {str(e)}")
            self.output_text.append(f"An error occurred: {str(e)}")  # Append error to the console
            raise

    def browse_directory(self):
        """
        Open a file dialog for the user to select an LAS file.
        """
        file_path = QFileDialog.getOpenFileName(self, "Select LAS File", "", "LAS Files (*.las *.laz)")[0]
        if file_path:
            self.dir_input.setText(file_path)
