from PyQt5.QtWidgets import (
    QCheckBox, QSpinBox, QLineEdit, QHBoxLayout, QLabel, QWidget, QFormLayout, QGroupBox
)
from typing import Dict, Any


class FormBuilder:
    """
    A utility class to build forms dynamically in PyQt5.
    """
    def __init__(self, form_layout: QFormLayout):
        """
        Initialize the FormBuilder with the given form layout.

        Args:
            form_layout (QFormLayout): The form layout to add widgets to.
        """
        self.form_layout = form_layout
        self.current_layout = form_layout

    def set_current_layout(self, layout: QFormLayout):
        """
        Set the current layout to add widgets to.

        Args:
            layout (QFormLayout): The layout to set as current.
        """
        self.current_layout = layout

    def add_checkbox(self, label_text: str, default_value: bool = False) -> QCheckBox:
        """
        Add a checkbox to the current layout.

        Args:
            label_text (str): The label for the checkbox.
            default_value (bool, optional): The default value of the checkbox. Defaults to False.

        Returns:
            QCheckBox: The created checkbox widget.
        """
        checkbox = QCheckBox()
        checkbox.setChecked(default_value)
        self.current_layout.addRow(self.create_checkbox_layout(label_text, checkbox))
        return checkbox

    def add_spinbox(self, label: str, min_val: int, max_val: int, default_val: int = None) -> QSpinBox:
        """
        Add a spinbox to the current layout.

        Args:
            label (str): The label for the spinbox.
            min_val (int): The minimum value for the spinbox.
            max_val (int): The maximum value for the spinbox.
            default_val (int, optional): The default value of the spinbox. Defaults to None.

        Returns:
            QSpinBox: The created spinbox widget.
        """
        layout = QHBoxLayout()
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        if default_val is not None:
            spinbox.setValue(default_val)
        layout.addWidget(QLabel(label))
        layout.addWidget(spinbox)
        widget = QWidget()
        widget.setLayout(layout)
        self.current_layout.addRow(widget)
        return spinbox

    def add_lineedit(self, label_text: str, default_value: str = "") -> QLineEdit:
        """
        Add a line edit to the current layout.

        Args:
            label_text (str): The label for the line edit.
            default_value (str, optional): The default value of the line edit. Defaults to "".

        Returns:
            QLineEdit: The created line edit widget.
        """
        lineedit = QLineEdit(default_value)
        self.current_layout.addRow(label_text, lineedit)
        return lineedit

    def create_checkbox_layout(self, label_text: str, checkbox: QCheckBox) -> QWidget:
        """
        Create a layout for a checkbox with a label.

        Args:
            label_text (str): The label for the checkbox.
            checkbox (QCheckBox): The checkbox widget.

        Returns:
            QWidget: The created layout widget containing the checkbox and label.
        """
        layout = QHBoxLayout()
        layout.addWidget(checkbox)
        layout.addWidget(QLabel(label_text))
        layout.addStretch()
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def add_section(self, title: str):
        """
        Add a new section to the form layout.

        Args:
            title (str): The title of the section.
        """
        group_box = QGroupBox(title)
        group_box.setCheckable(True)
        group_box.setChecked(False)
        group_box_layout = QFormLayout()
        group_box.setLayout(group_box_layout)
        self.form_layout.addWidget(group_box)
        self.set_current_layout(group_box_layout)

    def add_collapsible_section(self, title: str, params: Dict[str, Dict[str, Any]]):
        """
        Add a collapsible section to the form layout.

        Args:
            title (str): The title of the section.
            params (Dict[str, Dict[str, Any]]): The parameters to add in the section.
        """
        group_box = QGroupBox(title)
        group_box.setCheckable(True)
        group_box.setChecked(False)
        group_box_layout = QFormLayout()
        group_box.setLayout(group_box_layout)
        self.form_layout.addWidget(group_box)

        self.set_current_layout(group_box_layout)
        self.add_parameters(params)
        self.set_current_layout(self.form_layout)

    def add_parameters(self, params: Dict[str, Dict[str, Any]]):
        """
        Add parameters to the current layout.

        Args:
            params (Dict[str, Dict[str, Any]]): The parameters to add.
        """
        for param, config in params.items():
            if config['type'] == 'checkbox':
                self.add_checkbox(config['label'], config.get('default', False))
            elif config['type'] == 'spinbox':
                self.add_spinbox(config['label'], config['min'], config['max'], config.get('default'))
            elif config['type'] == 'lineedit':
                self.add_lineedit(config['label'], config.get('default', ''))
