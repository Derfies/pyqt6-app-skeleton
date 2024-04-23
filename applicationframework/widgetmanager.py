import logging

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QSplitter, QWidget

# noinspection PyUnresolvedReferences
from __feature__ import snake_case


logger = logging.getLogger(__name__)


class WidgetManager:

    def __init__(self, company_name: str, app_name: str):
        self._settings = QSettings(company_name, app_name)
        self._widgets = {}

        logger.debug(f'Loading widget settings file: {self._settings.file_name()}')

    def register_widget(self, name: str, widget: QWidget):
        self._widgets[name] = widget

    def load_settings(self):
        for key in self._settings.all_keys():
            value = self._settings.value(key)
            name, param = key.split('/')
            logger.debug(f'Loading widget settings: {name} setting: {value}')
            if param == 'rect':
                self._widgets[name].set_geometry(value)
            elif param == 'splitter_settings':
                self._widgets[name].restore_state(value)

    def save_settings(self):
        for name, widget in self._widgets.items():
            self._settings.begin_group(name)
            self._settings.set_value('rect', widget.geometry())
            if isinstance(widget, QSplitter):
                self._settings.set_value('splitter_settings', widget.save_state())
            self._settings.end_group()
