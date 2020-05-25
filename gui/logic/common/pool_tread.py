import typing as t
import multiprocessing as mp
import functools as ft

import PySide2.QtCore as qc


class BasePoolThread(qc.QThread):
    prepared = qc.Signal(list)
    process_started = qc.Signal(object)
    process_finished = qc.Signal(object, object)
    process_error = qc.Signal(object, str)

    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._abort = False

    def run(self):
        with mp.Pool() as pool:
            combinations = self.combine()
            self.prepared.emit(combinations)

            receivers = {}

            for data in combinations:
                # funcs
                process_func = ft.partial(
                    self._process_func_wrapper,
                    self.process,
                    self.prepare_args(data)
                )
                callback = ft.partial(self._on_process_finished, data)
                error_callback = ft.partial(self._on_process_error, data)

                # process
                receiver, sender = mp.Pipe(False)
                pool.apply_async(
                    process_func,
                    [sender], {},
                    callback, error_callback)

                # add
                receivers[receiver] = data

            self._pool_loop(receivers)

            if self._abort:
                pool.terminate()
            else:
                pool.close()
            pool.join()

    def combine(self) -> list:
        raise NotImplementedError()

    def prepare_args(self, data):
        raise NotImplementedError()

    @staticmethod
    def process(args: object) -> object:
        raise NotImplementedError()

    @staticmethod
    def _process_func_wrapper(
            process_func: t.Callable[[object], object],
            args,
            sender: mp.connection.PipeConnection) -> object:
        sender.send(object())  # send start signal
        return process_func(args)

    def abort(self):
        self._abort = True

    def _pool_loop(self, receivers: dict):
        while receivers and not self._abort:
            for_delete = []
            # handle
            for rec, data in receivers.items():
                if rec.closed:
                    for_delete.append(rec)
                    continue
                try:
                    rec.recv()
                except EOFError:
                    continue

                for_delete.append(rec)
                self._on_process_started(data)
            # clean
            for rec in for_delete:
                del receivers[rec]

    def _on_process_started(self, data):
        if self._abort:
            return
        self.process_started.emit(data)

    def _on_process_finished(self, data, result):
        if self._abort:
            return
        self.process_finished.emit(data, result)

    def _on_process_error(self, data, exception: BaseException):
        self.process_error.emit(data, exception.args[0])
