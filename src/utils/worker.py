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


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QProgressBar
    from PyQt5.QtCore import QThreadPool

    class ExampleApp(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.layout = QVBoxLayout()
            self.label = QLabel('Progress:')
            self.progress_bar = QProgressBar()
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.progress_bar)
            self.setLayout(self.layout)
            self.threadpool = QThreadPool()

            # Example function to be executed in a worker thread
            def example_function(progress_callback):
                for i in range(1, 6):
                    progress_callback.emit(i * 20)
                    time.sleep(1)
                return "Completed"

            self.start_worker(example_function)

        def start_worker(self, fn: callable):
            worker = Worker(fn, progress_callback=self.progress_bar.setValue)
            worker.signals.result.connect(self.on_result)
            worker.signals.error.connect(self.on_error)
            worker.signals.progress.connect(self.on_progress)
            worker.signals.log.connect(self.on_log)
            self.threadpool.start(worker)

        def on_result(self, result: str):
            self.label.setText(result)

        def on_error(self, error: tuple):
            exctype, value, traceback_str = error
            self.label.setText(f"Error: {value}")

        def on_progress(self, value: int):
            self.progress_bar.setValue(value)

        def on_log(self, message: str):
            print(message)

    app = QApplication(sys.argv)
    ex = ExampleApp()
    ex.show()
    sys.exit(app.exec_())
