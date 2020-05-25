import typing as t
import multiprocessing as mp
import functools as ft

import PySide2.QtCore as qc


class Combination:
    def __init__(self,
                 data: t.Any,
                 func: t.Callable,
                 args: t.Iterable[t.Any] = None,
                 kwargs: t.Mapping[str, t.Any] = None):
        self.data = data
        self.func = func
        self.args = [] if args is None else args
        self.kwargs = {} if kwargs is None else kwargs


class BasePoolThread(qc.QThread):
    prepared = qc.Signal(list)
    process_started = qc.Signal(object)
    process_finished = qc.Signal(object, object)
    process_error = qc.Signal(object, str)

    def __init__(self, parent: t.Optional[qc.QObject] = None):
        super().__init__(parent)

        self._abort = False

    def prepare(self) -> t.Any:
        raise NotImplementedError()

    def combine(self) -> t.Generator[Combination, None, None]:
        raise NotImplementedError()

    def run(self):
        with mp.Pool() as pool:
            prepared_data = self.prepare()
            self.prepared.emit(prepared_data)

            receivers = {}

            for comb in self.combine():
                # funcs
                process_func = ft.partial(
                    self._process_func_wrapper,
                    comb.func, comb.args, comb.kwargs
                )
                callback = ft.partial(self._on_process_finished, comb.data)
                error_callback = ft.partial(self._on_process_error, comb.data)

                # process
                receiver, sender = mp.Pipe(False)
                pool.apply_async(
                    process_func,
                    [sender], {},
                    callback, error_callback)

                # add
                receivers[receiver] = comb.data

            self._pool_loop(receivers)

            if self._abort:
                pool.terminate()
            else:
                pool.close()
            pool.join()

    @staticmethod
    def _process_func_wrapper(func, args, kwargs, sender) -> object:
        sender.send(object())  # send start signal
        return func(*args, **kwargs)

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
