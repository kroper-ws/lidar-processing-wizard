import traceback
import logging
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject

class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:
    - result: object data returned from processing
    - error: tuple (exctype, value, traceback)
    - progress: int indicating % progress
    - log: str log messages
    """
    result = pyqtSignal(object)
    error = pyqtSignal(tuple)
    progress = pyqtSignal(int)
    log = pyqtSignal(str)


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals, and wrap-up.

    :param fn: function to run on this worker thread.
    :param args: Arguments to pass to the function.
    :param kwargs: Keyword arguments to pass to the function.
    """
    def __init__(self, fn: callable, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialize the runner function with passed args, kwargs.
        """
        try:
            logging.info(f"Worker started with function {self.fn.__name__} and arguments {self.args}, {self.kwargs}")
            self.signals.progress.emit(0)
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            traceback_str = traceback.format_exc()
            logging.error(f"Error in worker thread: {traceback_str}")
            self.signals.error.emit((e, traceback_str))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.progress.emit(100)
